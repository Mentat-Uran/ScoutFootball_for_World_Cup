"""FastAPI read-only service layer for ScoutFootball."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from scoutfootball.action_value.evidence import (
    get_action_value_evidence as _get_action_value_evidence,
)
from scoutfootball.action_value.evidence import (
    get_action_value_evidence_index as _get_action_value_evidence_index,
)
from scoutfootball.app.data_loader import (
    _MISSING,
    _TTLCache,
    data_source_label,
    load_league_metrics,
    load_model_meta,
    load_oof_predictions,
    load_player_match,
    load_player_ratings,
    load_player_value_metrics,
    load_score_prediction,
    load_score_prediction_dc,
    load_team_match,
)
from scoutfootball.evaluation.scouting_queue import build_scouting_queues
from scoutfootball.head_to_head import get_head_to_head as _compute_head_to_head
from scoutfootball.worldcup.data import (
    BIG5_LEAGUES,
    GROUPS,
    HOSTS,
    compute_group_predictions,
    compute_team_strength_details,
    enrich_squads_with_ratings,
    generate_group_stage_matches,
    get_squad,
    get_team_group,
)

_STATSBOMB_ATTRIBUTION = (
    "StatsBomb Open Data must be attributed in any public display. "
    "License: CC-BY-SA 4.0. See https://github.com/statsbomb/open-data"
)


def _read_parquet(path: Path):
    """Read a Parquet file via DuckDB (avoids pyarrow dependency)."""
    import duckdb

    con = duckdb.connect()
    try:
        return con.execute("SELECT * FROM read_parquet(?)", [str(path)]).fetchdf()
    finally:
        con.close()


# ── World Cup data cache ──────────────────────────────────────────
_wc_cache = _TTLCache()
_WC_ENRICHED_KEY = "wc_enriched"
_WC_SCOUTING_KEY = "wc_scouting_queues"


def _get_wc_enriched_squads(force_refresh: bool = False):
    """Return enriched WC squads, computing once and caching with TTL.

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cached = _wc_cache.get(_WC_ENRICHED_KEY)
    if cached is _MISSING or force_refresh:
        ratings_df = load_player_ratings(force_refresh=force_refresh)
        enriched_squads = enrich_squads_with_ratings(ratings_df)
        strength_details = compute_team_strength_details(
            enriched_squads=enriched_squads
        )
        strengths = {
            team: values["strength"]
            for team, values in strength_details.items()
        }
        cached = {
            "enriched_squads": enriched_squads,
            "strengths": strengths,
            "strength_details": strength_details,
        }
        _wc_cache.set(_WC_ENRICHED_KEY, cached)
    return cached["enriched_squads"], cached["strengths"]


def _get_wc_strength_details(force_refresh: bool = False) -> dict:
    """Return WC team strength details (cached alongside enriched squads)."""
    _get_wc_enriched_squads(force_refresh=force_refresh)
    cached = _wc_cache.get(_WC_ENRICHED_KEY)
    if cached is _MISSING:
        return {}
    return cached.get("strength_details", {})


@dataclass(frozen=True)
class HealthResponse:
    status: str
    data_source: str
    version: str


@dataclass(frozen=True)
class PlayerListResponse:
    player_count: int
    players: list[str]


def _settings():
    from scoutfootball.config import PlatformSettings

    return PlatformSettings.from_root()


def _clean_json_value(value: Any) -> Any:
    import numpy as np

    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        value = float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    # Handle pandas NA/NaT
    try:
        import pandas as pd
        if value is pd.NA or value is pd.NaT:
            return None
    except (ImportError, AttributeError):
        pass
    if isinstance(value, dict):
        return {key: _clean_json_value(val) for key, val in value.items()}
    if isinstance(value, list):
        return [_clean_json_value(item) for item in value]
    return value


def _read_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def _artifact_file_info(
    path: Path,
    label: str,
    *,
    rows: int | None = None,
    display_root: Path | None = None,
) -> dict[str, Any]:
    display_path = path
    if display_root is not None:
        try:
            display_path = path.resolve().relative_to(display_root.resolve())
        except ValueError:
            display_path = path
    return {
        "label": label,
        "path": str(display_path).replace("\\", "/"),
        "exists": path.exists(),
        "rows": rows,
        "updated_at": path.stat().st_mtime if path.exists() else None,
    }


def _latest_run_id() -> str:
    runs = get_model_runs()
    run_list = runs.get("runs", [])
    if run_list:
        return str(run_list[0].get("run_id", "latest-local"))
    return "latest-local"


def _queue_payload(frame, *, limit: int) -> dict[str, Any]:
    limited = frame.head(limit).copy()
    records = _clean_json_value(limited.to_dict(orient="records"))
    return {"count": len(frame), "players": records}


def health_check() -> HealthResponse:
    from scoutfootball import __version__

    return HealthResponse(
        status="ok",
        data_source=data_source_label(),
        version=__version__,
    )


def list_players() -> PlayerListResponse:
    """Return all unique player names from the ratings dataset."""
    df = load_player_ratings()
    col = (
        "player" if "player" in df.columns
        else ("player_name" if "player_name" in df.columns else None)
    )
    if col is None:
        return PlayerListResponse(player_count=0, players=[])
    names = sorted(df[col].dropna().unique().tolist())
    return PlayerListResponse(player_count=len(names), players=names)


def list_teams() -> list[str]:
    """Return teams supported by the active match-prediction artifacts.

    Player-rating rows can contain comma-joined club histories for transferred
    players. Those values are useful in the rating dataset, but they are not
    valid team identifiers for the prediction model. Prefer the exact team ids
    saved with Dixon-Coles/Poisson and only fall back to ratings data when no
    prediction artifact is available.
    """
    artifact_dir = _settings().model_root / "artifacts"
    for filename in ("dc_team_strengths.parquet", "team_strengths.parquet"):
        path = artifact_dir / filename
        if not path.exists():
            continue
        try:
            frame = _read_parquet(path)
        except Exception:
            continue
        if "team_id" not in frame.columns:
            continue
        teams = {
            str(team).strip()
            for team in frame["team_id"].dropna().tolist()
            if str(team).strip()
        }
        if teams:
            return sorted(teams)

    df = load_player_ratings()
    if "team" in df.columns:
        teams = {
            str(team).strip()
            for team in df["team"].dropna().tolist()
            if str(team).strip() and "," not in str(team)
        }
        return sorted(teams)
    # Fallback to team_match
    tm = load_team_match()
    if "team_name" in tm.columns:
        return sorted(tm["team_name"].dropna().unique().tolist())[:200]
    return []


def search_players_and_teams(
    q: str,
    search_type: str = "all",
    limit: int = 10,
) -> dict[str, Any]:
    """Return matching player and team name suggestions for autocomplete.

    Matches are ranked prefix-first (alphabetical), then substring matches
    (alphabetical). Returns ``{"players": [...], "teams": [...]}``.

    Player entries include ``player_name``, ``team``, ``position``, ``rating``
    (optimized_score) and ``league``. Team entries include ``team_name`` and
    ``league``. Comma-joined club histories (transferred players) are excluded
    from team suggestions.
    """
    empty_result: dict[str, Any] = {"players": [], "teams": []}

    # Input validation — require at least 2 characters
    if not q or len(q.strip()) < 2:
        return empty_result
    q = q.strip()

    # Limit clamping (1..25, default 10)
    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 10
    limit = max(1, min(limit, 25))

    # Type validation — invalid values default to "all"
    if search_type not in ("players", "teams", "all"):
        search_type = "all"

    # Load ratings via TTL cache (no forced refresh)
    df = load_player_ratings(force_refresh=False)
    if df is None or df.empty:
        return _clean_json_value(empty_result)

    # Resolve column names (normalize_ratings_frame ensures aliases exist)
    name_col = (
        "player" if "player" in df.columns
        else ("player_name" if "player_name" in df.columns else None)
    )
    team_col = (
        "team" if "team" in df.columns
        else ("team_name" if "team_name" in df.columns else None)
    )
    league_col = "league" if "league" in df.columns else None
    pos_col = (
        "position_group" if "position_group" in df.columns
        else ("sub_position" if "sub_position" in df.columns else None)
    )
    score_col = (
        "optimized_score" if "optimized_score" in df.columns
        else ("rating" if "rating" in df.columns else None)
    )

    players_out: list[dict[str, Any]] = []
    teams_out: list[dict[str, Any]] = []

    # ── Player search ──────────────────────────────────────────────
    if search_type in ("players", "all") and name_col is not None:
        q_lower = q.lower()

        # Deduplicate by player name, keeping the best row (highest score)
        if score_col is not None and score_col in df.columns:
            dedup = df.sort_values(score_col, ascending=False).drop_duplicates(
                subset=[name_col], keep="first",
            )
        else:
            dedup = df.drop_duplicates(subset=[name_col], keep="first")
        dedup = dedup[dedup[name_col].notna()]
        dedup = dedup[dedup[name_col].astype(str).str.strip() != ""]

        dedup_names = dedup[name_col].astype(str).str.lower()
        prefix_mask = dedup_names.str.startswith(q_lower, na=False)
        substring_mask = (
            ~prefix_mask
            & dedup_names.str.contains(q_lower, na=False, regex=False)
        )

        prefix_df = dedup[prefix_mask].sort_values(name_col)
        substring_df = dedup[substring_mask].sort_values(name_col)
        combined = pd.concat([prefix_df, substring_df]).head(limit)

        for _, row in combined.iterrows():
            score_val = row.get(score_col) if score_col else None
            rating = (
                round(float(score_val), 1)
                if score_col and pd.notna(score_val)
                else None
            )
            players_out.append({
                "player_name": str(row.get(name_col, "")),
                "team": str(row.get(team_col, "")) if team_col else "",
                "position": str(row.get(pos_col, "")) if pos_col else "",
                "rating": rating,
                "league": str(row.get(league_col, "")) if league_col else "",
            })

    # ── Team search ────────────────────────────────────────────────
    if search_type in ("teams", "all") and team_col is not None:
        q_lower = q.lower()
        team_df = df[df[team_col].notna()].copy()
        # Exclude comma-joined club histories (transferred players)
        team_df = team_df[~team_df[team_col].astype(str).str.contains(",", na=False)]
        team_df = team_df[team_df[team_col].astype(str).str.strip() != ""]

        if not team_df.empty:
            # Unique teams with league info (first occurrence)
            teams_unique = team_df.drop_duplicates(subset=[team_col], keep="first")
            team_names_lower = teams_unique[team_col].astype(str).str.lower()

            prefix_mask = team_names_lower.str.startswith(q_lower, na=False)
            substring_mask = (
                ~prefix_mask
                & team_names_lower.str.contains(q_lower, na=False, regex=False)
            )

            prefix_teams = teams_unique[prefix_mask].sort_values(team_col)
            substring_teams = teams_unique[substring_mask].sort_values(team_col)
            combined_teams = pd.concat([prefix_teams, substring_teams]).head(limit)

            for _, row in combined_teams.iterrows():
                teams_out.append({
                    "team_name": str(row.get(team_col, "")),
                    "league": str(row.get(league_col, "")) if league_col else "",
                })

    return _clean_json_value({"players": players_out, "teams": teams_out})


def _score_matrix_to_list(prediction) -> list[list[float]]:
    """Convert a score_matrix DataFrame to a 2-D list (0-5 goals)."""
    sm = prediction.score_matrix
    max_goals = 5
    rows = min(max_goals + 1, sm.shape[0])
    cols = min(max_goals + 1, sm.shape[1])
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            val = float(sm.iloc[i, j]) if i < sm.shape[0] and j < sm.shape[1] else 0.0
            row.append(round(val, 4))
        # Pad if score_matrix is smaller than 6x6
        while len(row) < max_goals + 1:
            row.append(0.0)
        matrix.append(row)
    while len(matrix) < max_goals + 1:
        matrix.append([0.0] * (max_goals + 1))
    return matrix


def _prediction_calibration() -> dict[str, Any]:
    """Load Brier/RPS from prediction artifacts."""
    settings = _settings()
    artifact_dir = settings.data_root / "models" / "artifacts"
    calibration: dict[str, Any] = {}

    # Poisson calibration
    poisson_path = artifact_dir / "poisson_baseline_results.parquet"
    if poisson_path.exists():
        try:
            pf = _read_parquet(poisson_path)
            if not pf.empty:
                row = pf.iloc[0].to_dict()
                calibration["brier"] = _clean_json_value(row.get("brier_1x2"))
                calibration["rps"] = _clean_json_value(row.get("rps_1x2"))
                calibration["log_loss"] = _clean_json_value(row.get("log_loss_exact"))
        except Exception:
            pass

    # DC calibration (overrides if available)
    dc_path = artifact_dir / "dixon_coles_results.parquet"
    if dc_path.exists():
        try:
            dc_df = _read_parquet(dc_path)
            if not dc_df.empty:
                dc_row = dc_df.iloc[0].to_dict()
                calibration["brier"] = _clean_json_value(
                    dc_row.get("brier_1x2", calibration.get("brier"))
                )
                calibration["rps"] = _clean_json_value(
                    dc_row.get("rps_1x2", calibration.get("rps"))
                )
        except Exception:
            pass

    # Full calibration detail is produced by the training backtest. Prefer
    # those evaluated metrics when available; the model-summary parquet only
    # stores fitted parameters and therefore cannot populate Brier/RPS.
    try:
        detail = get_prediction_calibration()
        detail_metrics = detail.get("dixon_coles", {})
        if detail_metrics.get("status") != "ok":
            detail_metrics = detail.get("poisson", {})
        if detail_metrics.get("status") == "ok":
            calibration["brier"] = detail_metrics.get("brier_1x2")
            calibration["rps"] = detail_metrics.get("rps_1x2")
            calibration["log_loss"] = detail_metrics.get("log_loss_exact")
    except Exception:
        pass

    return calibration


def _world_cup_score_matrix(
    home_lambda: float, away_lambda: float, *, max_goals: int = 5
) -> list[list[float]]:
    from scipy.stats import poisson

    goals = np.arange(max_goals + 1)
    home_probs = poisson.pmf(goals, home_lambda)
    away_probs = poisson.pmf(goals, away_lambda)
    matrix = np.outer(home_probs, away_probs)
    matrix = matrix / matrix.sum()
    return [
        [round(float(matrix[i, j]), 4) for j in range(max_goals + 1)]
        for i in range(max_goals + 1)
    ]


def _world_cup_market_summary(score_matrix: list[list[float]]) -> dict[str, float]:
    home_win = 0.0
    draw = 0.0
    away_win = 0.0
    over_2_5 = 0.0
    btts_yes = 0.0
    for home_goals, row in enumerate(score_matrix):
        for away_goals, prob in enumerate(row):
            if home_goals > away_goals:
                home_win += prob
            elif home_goals == away_goals:
                draw += prob
            else:
                away_win += prob
            if home_goals + away_goals >= 3:
                over_2_5 += prob
            if home_goals > 0 and away_goals > 0:
                btts_yes += prob
    return {
        "home_win": round(home_win, 4),
        "draw": round(draw, 4),
        "away_win": round(away_win, 4),
        "over_2_5": round(over_2_5, 4),
        "under_2_5": round(1 - over_2_5, 4),
        "btts_yes": round(btts_yes, 4),
        "btts_no": round(1 - btts_yes, 4),
    }


def get_world_cup_match_prediction(home_team: str, away_team: str) -> dict[str, Any]:
    enriched_squads, strengths = _get_wc_enriched_squads()
    valid_teams = set(enriched_squads)
    if home_team not in valid_teams:
        return {"error": f"World Cup home team '{home_team}' not found"}
    if away_team not in valid_teams:
        return {"error": f"World Cup away team '{away_team}' not found"}
    if home_team == away_team:
        return {"error": "Home and away World Cup teams must be different"}

    home_strength = float(strengths.get(home_team, 0.2))
    away_strength = float(strengths.get(away_team, 0.2))

    strength_gap = math.log((home_strength + 0.05) / (away_strength + 0.05))
    host_bonus = 0.12 if home_team in HOSTS else 0.0
    if away_team in HOSTS:
        host_bonus -= 0.12

    total_goals = 2.35 + 0.55 * ((home_strength + away_strength) - 1.0)
    total_goals = min(max(total_goals, 2.05), 3.35)

    home_share = 1 / (1 + math.exp(-(0.62 * strength_gap + host_bonus)))
    home_share = min(max(home_share, 0.22), 0.78)

    home_lambda = min(max(total_goals * home_share, 0.25), 3.2)
    away_lambda = min(max(total_goals - home_lambda, 0.2), 3.0)

    score_matrix = _world_cup_score_matrix(home_lambda, away_lambda)
    summary = _world_cup_market_summary(score_matrix)

    result = {
        "home_team": home_team,
        "away_team": away_team,
        "model_type": "world_cup_strength_poisson",
        "model_version": "wc-1.0",
        "home_lambda": round(home_lambda, 4),
        "away_lambda": round(away_lambda, 4),
        "home_strength": round(home_strength, 4),
        "away_strength": round(away_strength, 4),
        "host_bonus": round(host_bonus, 4),
        "strength_gap": round(strength_gap, 4),
        "score_matrix": score_matrix,
        **summary,
    }
    return _clean_json_value(result)


def get_match_prediction(home_team: str, away_team: str) -> dict:
    try:
        prediction = load_score_prediction(home_team, away_team)
    except Exception as exc:
        return {"error": str(exc)}
    if isinstance(prediction, dict):
        return prediction
    result = {
        "home_team": home_team,
        "away_team": away_team,
        "model_type": "poisson",
        "model_version": "1.0",
        "home_lambda": prediction.home_lambda,
        "away_lambda": prediction.away_lambda,
        "home_win": prediction.summary.home_win,
        "draw": prediction.summary.draw,
        "away_win": prediction.summary.away_win,
        "over_2_5": prediction.summary.over_2_5,
        "btts_yes": prediction.summary.btts_yes,
        "score_matrix": _score_matrix_to_list(prediction),
        "calibration": _prediction_calibration(),
    }
    return _clean_json_value(result)


def get_match_prediction_dc(home_team: str, away_team: str) -> dict:
    """Predict a match using the Dixon-Coles model.

    Returns the same structure as get_match_prediction but with model_type='dixon_coles'
    and includes rho / home_advantage when available.
    Falls back gracefully when DC artifacts are missing.
    """
    try:
        prediction = load_score_prediction_dc(home_team, away_team)
    except Exception as exc:
        return {"error": str(exc)}
    if isinstance(prediction, dict):
        prediction["model_type"] = prediction.get("model_type", "dixon_coles")
        return prediction
    result = {
        "home_team": home_team,
        "away_team": away_team,
        "model_type": "dixon_coles",
        "model_version": "1.0",
        "home_lambda": prediction.home_lambda,
        "away_lambda": prediction.away_lambda,
        "home_win": prediction.summary.home_win,
        "draw": prediction.summary.draw,
        "away_win": prediction.summary.away_win,
        "over_2_5": prediction.summary.over_2_5,
        "btts_yes": prediction.summary.btts_yes,
        "score_matrix": _score_matrix_to_list(prediction),
        "calibration": _prediction_calibration(),
    }
    # Try to enrich with DC-specific parameters (rho, home_advantage)
    try:
        dc_path = (
            _settings().data_root / "models" / "artifacts" / "dixon_coles_results.parquet"
        )
        if dc_path.exists():


            dc_df = _read_parquet(dc_path)
            if not dc_df.empty:
                dc_row = dc_df.iloc[0].to_dict()
                if "rho" in dc_row:
                    result["rho"] = _clean_json_value(dc_row["rho"])
                if "home_advantage" in dc_row:
                    result["home_advantage"] = _clean_json_value(dc_row["home_advantage"])
    except Exception:
        pass  # enrichment is optional
    return _clean_json_value(result)


def get_head_to_head(
    home_team: str, away_team: str, limit: int = 10, form_limit: int = 10
) -> dict:
    """Return head-to-head history, team form, and matchup summary.

    Wraps :func:`scoutfootball.head_to_head.get_head_to_head` with JSON-safe
    serialization and graceful error handling so the API never crashes.
    """
    empty_form_summary = {
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0,
        "points": 0,
        "streak": [],
    }
    empty_summary = {
        "total_meetings": 0,
        "home_wins": 0,
        "draws": 0,
        "away_wins": 0,
        "home_goals_avg": 0.0,
        "away_goals_avg": 0.0,
        "last_meeting_date": None,
    }
    fallback = {
        "home_team": home_team,
        "away_team": away_team,
        "head_to_head": [],
        "home_form": [],
        "home_form_summary": empty_form_summary,
        "away_form": [],
        "away_form_summary": {**empty_form_summary},
        "summary": empty_summary,
        "data_coverage": {
            "seasons_covered": [],
            "total_matches_scanned": 0,
            "source": "Football-Data",
        },
    }
    try:
        result = _compute_head_to_head(
            home_team, away_team, limit=limit, form_limit=form_limit
        )
        return _clean_json_value(result)
    except Exception:
        return _clean_json_value(fallback)


def get_value_summary() -> dict:
    oof = load_oof_predictions()
    if oof.empty:
        return {"status": "no_data", "players": [], "metrics": {}}
    is_synthetic = (
        "is_synthetic" in oof.columns
        and bool(oof["is_synthetic"].fillna(False).all())
    )

    # Filter out records with suspiciously low market values (Transfermarkt placeholder)
    # Values <= 200k are almost certainly data errors, not real valuations
    if "actual_market_value" in oof.columns:
        oof = oof[oof["actual_market_value"] > 200000].copy()

    # Build player-level value data
    player_data = []
    for _, row in oof.iterrows():
        record = {
            "player": row.get("player_name", ""),
            "team": row.get("team_name", ""),
            "actual_value": row.get("actual_market_value"),
            "predicted_value": row.get("predicted_market_value"),
            "residual_log": row.get("residual_log"),
            "fairness_label": row.get("fairness_label", ""),
        }
        for key, value in record.items():
            if isinstance(value, float) and math.isnan(value):
                record[key] = None
        player_data.append(_clean_json_value(record))

    metrics: dict[str, Any] = {}
    results_path = _settings().data_root / "models" / "artifacts" / "value_fairness_results.parquet"
    if results_path.exists():
        try:


            results_df = _read_parquet(results_path)
            if not results_df.empty:
                metrics = _clean_json_value(results_df.iloc[0].to_dict())
        except Exception:
            pass

    mean_residual = None
    if "residual_log" in oof.columns:
        try:
            raw = oof["residual_log"].mean()
            mean_residual = float(raw) if raw == raw else None
        except Exception:
            mean_residual = None

    return _clean_json_value({
        "status": "demo" if is_synthetic else "ok",
        "data_mode": "synthetic" if is_synthetic else "artifact",
        "sample_count": len(oof),
        "fairness_distribution": oof["fairness_label"].value_counts().to_dict()
        if "fairness_label" in oof.columns
        else {},
        "mean_residual_log": mean_residual,
        "metrics": metrics,
        "players": player_data,
    })


def get_player_ratings(
    position: str | None = None,
    league: str | None = None,
    team: str | None = None,
    season: str | None = None,
    limit: int = 20000,
) -> dict:
    """Return player ratings from DuckDB, sorted by optimized_score DESC."""
    df = load_player_ratings(position=position, league=league, team=team, season=season)
    if df.empty:
        return {"count": 0, "players": []}

    # Normalize confidence_level to uppercase for frontend
    if "confidence_level" in df.columns:
        df["confidence_level"] = df["confidence_level"].str.upper()

    # Alias sub_position → position_group for frontend compatibility
    if "sub_position" in df.columns and "position_group" not in df.columns:
        df["position_group"] = df["sub_position"]

    # Limit results
    df = df.head(limit)

    players = df.to_dict(orient="records")
    # Convert NaN to None for JSON serialization
    return _clean_json_value({"count": len(players), "players": players})


def get_ratings_meta() -> dict:
    """Return model metadata and league metrics."""
    meta_df = load_model_meta()
    league_df = load_league_metrics()

    meta = {}
    if not meta_df.empty:
        meta = meta_df.iloc[0].to_dict()

    leagues = league_df.to_dict(orient="records") if not league_df.empty else []

    return _clean_json_value({"model_meta": meta, "league_metrics": leagues})


# ── Position group mapping for team strength aggregation ──────────
_POS_GROUP_MAP: dict[str, str] = {
    "GK": "GK",
    "CB": "DEF", "FB": "DEF", "LB": "DEF", "RB": "DEF", "RWB": "DEF", "LWB": "DEF",
    "DM": "MID", "CM": "MID", "AM": "MID", "CDM": "MID", "CAM": "MID", "LM": "MID", "RM": "MID",
    "W": "ATT", "ST": "ATT", "CF": "ATT", "RW": "ATT", "LW": "ATT", "WF": "ATT",
}


def _broad_position(pos: str | None) -> str:
    """Map a granular position to GK/DEF/MID/ATT."""
    if not pos:
        return "UNK"
    key = str(pos).strip().upper()
    return _POS_GROUP_MAP.get(key, "UNK")


def get_team_strength(
    league: str | None = None,
    season: str | None = None,
    limit: int = 100,
) -> dict:
    """Aggregate player ratings to team-level strength metrics.

    Returns overall team rating, position-group breakdowns, top players,
    squad depth and average confidence for each team.
    """
    df = load_player_ratings(league=league, season=season)
    if df.empty:
        return {"count": 0, "teams": []}

    # Resolve column aliases
    team_col = "team" if "team" in df.columns else (
        "team_name" if "team_name" in df.columns else None
    )
    score_col = "optimized_score" if "optimized_score" in df.columns else (
        "rating" if "rating" in df.columns else None
    )
    pos_col = "position_group" if "position_group" in df.columns else (
        "sub_position" if "sub_position" in df.columns else None
    )
    minutes_col = "minutes" if "minutes" in df.columns else None
    name_col = "player_name" if "player_name" in df.columns else (
        "player" if "player" in df.columns else None
    )
    league_col = "league" if "league" in df.columns else None
    season_col = "season" if "season" in df.columns else None
    conf_col = "confidence_level" if "confidence_level" in df.columns else None

    if team_col is None or score_col is None:
        return {"count": 0, "teams": []}

    # Filter out rows with no team or score
    df = df[df[team_col].notna() & df[score_col].notna()].copy()
    # Exclude comma-joined club histories (transferred players)
    df = df[~df[team_col].astype(str).str.contains(",", na=False)]
    # Normalize team name
    df[team_col] = df[team_col].astype(str).str.strip()
    df = df[df[team_col] != ""]

    if df.empty:
        return {"count": 0, "teams": []}

    # Add broad position group
    if pos_col:
        df["broad_pos"] = df[pos_col].map(_broad_position)
    else:
        df["broad_pos"] = "UNK"

    # Ensure numeric score
    df[score_col] = pd.to_numeric(df[score_col], errors="coerce").fillna(0.0)
    if minutes_col:
        df[minutes_col] = pd.to_numeric(df[minutes_col], errors="coerce").fillna(0.0)
    else:
        df["minutes"] = 0.0
        minutes_col = "minutes"

    teams: list[dict[str, Any]] = []

    for team_name, group in df.groupby(team_col):
        # Minutes-weighted overall rating
        total_minutes = group[minutes_col].sum()
        if total_minutes > 0:
            overall = float((group[score_col] * group[minutes_col]).sum() / total_minutes)
        else:
            overall = float(group[score_col].mean())

        # Position group breakdown
        pos_breakdown: dict[str, dict[str, Any]] = {}
        for bpos, pg in group.groupby("broad_pos"):
            pg_minutes = pg[minutes_col].sum()
            if pg_minutes > 0:
                pg_rating = float((pg[score_col] * pg[minutes_col]).sum() / pg_minutes)
            else:
                pg_rating = float(pg[score_col].mean())
            pos_breakdown[bpos] = {
                "rating": round(pg_rating, 2),
                "player_count": int(len(pg)),
                "avg_minutes": round(float(pg[minutes_col].mean()), 0) if len(pg) > 0 else 0,
            }

        # Top players by score (with minutes weighting)
        top_players_df = group.nlargest(5, score_col)
        top_players = []
        for _, row in top_players_df.iterrows():
            top_players.append({
                "name": str(row.get(name_col, "")) if name_col else "",
                "position": str(row.get(pos_col, "")) if pos_col else "",
                "broad_pos": str(row.get("broad_pos", "")),
                "rating": round(float(row[score_col]), 1),
                "minutes": int(row.get(minutes_col, 0)) if minutes_col else 0,
                "confidence": str(row.get(conf_col, "LOW")).upper() if conf_col else "LOW",
            })

        # Average confidence
        if conf_col and conf_col in group.columns:
            conf_counts = group[conf_col].astype(str).str.upper().value_counts().to_dict()
        else:
            conf_counts = {}

        team_entry = {
            "team": team_name,
            "league": str(group[league_col].iloc[0])
            if league_col and league_col in group.columns else "",
            "season": str(group[season_col].iloc[0])
            if season_col and season_col in group.columns else "",
            "overall_rating": round(overall, 2),
            "squad_size": int(len(group)),
            "total_minutes": int(total_minutes),
            "position_groups": pos_breakdown,
            "top_players": top_players,
            "confidence_distribution": conf_counts,
        }
        teams.append(team_entry)

    # Sort by overall rating descending
    teams.sort(key=lambda t: t["overall_rating"], reverse=True)

    # Apply limit
    teams = teams[:limit]

    return _clean_json_value({"count": len(teams), "teams": teams})


def get_team_comparison(team_a: str, team_b: str) -> dict:
    """Compare two teams side-by-side using team strength data.

    Returns position group diffs, top player comparison and squad metrics.
    """
    # Normalize team names for matching
    strength = get_team_strength(limit=500)
    all_teams = strength.get("teams", [])

    # Find teams by name (case-insensitive partial match)
    def _find(name):
        name_lower = name.lower().strip()
        for t in all_teams:
            if t["team"].lower() == name_lower:
                return t
        for t in all_teams:
            if name_lower in t["team"].lower():
                return t
        return None

    a = _find(team_a)
    b = _find(team_b)

    if not a:
        return {"error": f"Team '{team_a}' not found"}
    if not b:
        return {"error": f"Team '{team_b}' not found"}

    # Position group comparison
    pos_groups = ["GK", "DEF", "MID", "ATT"]
    pos_comparison = []
    for pg in pos_groups:
        pg_a = (a.get("position_groups") or {}).get(pg)
        pg_b = (b.get("position_groups") or {}).get(pg)
        rating_a = pg_a["rating"] if pg_a else None
        rating_b = pg_b["rating"] if pg_b else None
        diff = None
        advantage = "tie"
        if rating_a is not None and rating_b is not None:
            diff = round(rating_a - rating_b, 2)
            advantage = "a" if rating_a > rating_b else ("b" if rating_b > rating_a else "tie")
        pos_comparison.append({
            "group": pg,
            "rating_a": rating_a,
            "rating_b": rating_b,
            "diff": diff,
            "advantage": advantage,
            "players_a": pg_a["player_count"] if pg_a else 0,
            "players_b": pg_b["player_count"] if pg_b else 0,
        })

    # Top players side-by-side (top 5 each)
    top_a = a.get("top_players", [])
    top_b = b.get("top_players", [])
    max_top = max(len(top_a), len(top_b))
    top_comparison = []
    for i in range(max_top):
        pa = top_a[i] if i < len(top_a) else None
        pb = top_b[i] if i < len(top_b) else None
        top_comparison.append({
            "player_a": pa,
            "player_b": pb,
        })

    # Overall metrics comparison
    overall_a = a.get("overall_rating", 0)
    overall_b = b.get("overall_rating", 0)
    overall_diff = round(overall_a - overall_b, 2)

    return _clean_json_value({
        "team_a": {
            "name": a["team"],
            "league": a.get("league", ""),
            "overall_rating": overall_a,
            "squad_size": a.get("squad_size", 0),
            "total_minutes": a.get("total_minutes", 0),
            "confidence_distribution": a.get("confidence_distribution", {}),
        },
        "team_b": {
            "name": b["team"],
            "league": b.get("league", ""),
            "overall_rating": overall_b,
            "squad_size": b.get("squad_size", 0),
            "total_minutes": b.get("total_minutes", 0),
            "confidence_distribution": b.get("confidence_distribution", {}),
        },
        "overall_diff": overall_diff,
        "overall_advantage": "a" if overall_diff > 0 else ("b" if overall_diff < 0 else "tie"),
        "position_group_comparison": pos_comparison,
        "top_players_comparison": top_comparison,
        "radar_labels": ["GK", "DEF", "MID", "ATT", "Overall"],
        "radar_a": [
            (a.get("position_groups") or {}).get("GK", {}).get("rating", 0),
            (a.get("position_groups") or {}).get("DEF", {}).get("rating", 0),
            (a.get("position_groups") or {}).get("MID", {}).get("rating", 0),
            (a.get("position_groups") or {}).get("ATT", {}).get("rating", 0),
            overall_a,
        ],
        "radar_b": [
            (b.get("position_groups") or {}).get("GK", {}).get("rating", 0),
            (b.get("position_groups") or {}).get("DEF", {}).get("rating", 0),
            (b.get("position_groups") or {}).get("MID", {}).get("rating", 0),
            (b.get("position_groups") or {}).get("ATT", {}).get("rating", 0),
            overall_b,
        ],
    })


def get_prediction_summary() -> dict[str, Any]:
    """Return baseline prediction artifact metadata."""
    artifact_path = (
        _settings().data_root
        / "models"
        / "artifacts"
        / "poisson_baseline_results.parquet"
    )
    poisson_info: dict[str, Any] = {"status": "no_data"}
    if artifact_path.exists():


        try:
            frame = _read_parquet(artifact_path)
            if not frame.empty:
                poisson_info = frame.iloc[0].to_dict()
                poisson_info["status"] = "ok"
        except Exception:
            pass

    # Dixon-Coles artifact info
    dc_path = (
        _settings().data_root
        / "models"
        / "artifacts"
        / "dixon_coles_results.parquet"
    )
    dc_info: dict[str, Any] = {"status": "not_available"}
    if dc_path.exists():


        try:
            dc_frame = _read_parquet(dc_path)
            if not dc_frame.empty:
                dc_info = dc_frame.iloc[0].to_dict()
                dc_info["status"] = "ok"
        except Exception:
            dc_info["status"] = "error"

    poisson_ready = poisson_info.get("status") == "ok"
    dc_ready = dc_info.get("status") == "ok"
    preferred = dc_info if dc_ready else poisson_info

    return _clean_json_value({
        "status": "ok" if (poisson_ready or dc_ready) else "no_data",
        "model_type": preferred.get("model_type", "independent_poisson"),
        "num_teams": preferred.get("num_teams"),
        "train_rows": poisson_info.get("train_rows"),
        "coverage": poisson_info.get("coverage"),
        "poisson": poisson_info,
        "dixon_coles": dc_info,
        "available_models": (
            (["poisson"] if poisson_ready else [])
            + (["dixon_coles"] if dc_ready else [])
        ),
    })


_calibration_cache: dict[str, Any] = {"data": None, "timestamp": 0.0}
_CALIBRATION_TTL_SECONDS = 300  # 5 minutes


def get_prediction_calibration(force_refresh: bool = False) -> dict[str, Any]:
    """Return calibration metrics for match prediction models.

    Compares Poisson vs Dixon-Coles side by side.
    Includes low-score breakdown (0-0, 1-0, 0-1, 1-1) and league coverage.

    Results are cached for 5 minutes to avoid repeated parquet reads.
    Pass force_refresh=True to bypass the cache (e.g. after model retraining).
    """
    import time

    now = time.time()
    if (
        not force_refresh
        and _calibration_cache["data"] is not None
        and now - _calibration_cache["timestamp"] < _CALIBRATION_TTL_SECONDS
    ):
        return _calibration_cache["data"]
    settings = _settings()
    model_root = settings.data_root / "models"
    artifact_dir = model_root / "artifacts"

    # --- DC calibration detail ---
    dc_detail_path = artifact_dir / "dc_calibration_detail.parquet"
    dc_metrics: dict[str, Any] = {"status": "not_available"}
    dc_low_score: list[dict[str, Any]] = []
    dc_calibration_plot: list[dict[str, Any]] = []
    dc_league_coverage: list[dict[str, Any]] = []

    if dc_detail_path.exists():
        import numpy as np


        try:
            dc_df = _read_parquet(dc_detail_path)
            if not dc_df.empty:
                # Compute metrics from detail
                clipped = dc_df["exact_score_probability"].clip(lower=1e-12)
                log_loss = float(-(np.log(clipped)).mean())

                probs_1x2 = dc_df.loc[
                    :,
                    ["home_win_probability", "draw_probability", "away_win_probability"],
                ].to_numpy()
                actual_map = {
                    "home_win": [1.0, 0.0, 0.0],
                    "draw": [0.0, 1.0, 0.0],
                    "away_win": [0.0, 0.0, 1.0],
                }
                actual = np.vstack(dc_df["actual_outcome"].map(actual_map))
                brier = float(np.mean(np.sum((probs_1x2 - actual) ** 2, axis=1)))

                # RPS
                probs_rps = dc_df.loc[
                    :,
                    ["away_win_probability", "draw_probability", "home_win_probability"],
                ].to_numpy()
                actual_rps = np.vstack(
                    dc_df["actual_outcome"].map(
                        {
                            "away_win": [1.0, 0.0, 0.0],
                            "draw": [0.0, 1.0, 0.0],
                            "home_win": [0.0, 0.0, 1.0],
                        },
                    ),
                )
                cum_probs = np.cumsum(probs_rps, axis=1)
                cum_actual = np.cumsum(actual_rps, axis=1)
                rps = float(np.mean(np.sum((cum_probs - cum_actual) ** 2, axis=1) / 2.0))

                dc_metrics = {
                    "status": "ok",
                    "log_loss_exact": round(log_loss, 4),
                    "brier_1x2": round(brier, 4),
                    "rps_1x2": round(rps, 4),
                    "n_matches": len(dc_df),
                }

                # Low-score breakdown
                for bucket in ["0-0", "1-0", "0-1", "1-1"]:
                    group = dc_df[dc_df["score_bucket"] == bucket]
                    n = len(group)
                    actual_pct = n / len(dc_df) * 100.0 if len(dc_df) > 0 else 0.0
                    mean_pred = (
                        float(group["exact_score_probability"].mean()) * 100.0
                        if n > 0 else 0.0
                    )
                    dc_low_score.append({
                        "score_bucket": bucket,
                        "n_matches": n,
                        "actual_pct": round(actual_pct, 2),
                        "mean_predicted_pct": round(mean_pred, 2),
                        "calibration_error": round(abs(actual_pct - mean_pred), 2),
                    })

                # Calibration plot data (decile bins of predicted home-win)
                bin_edges = np.linspace(0, 1, 11)
                hw_probs = dc_df["home_win_probability"].to_numpy()
                hw_actual = (dc_df["actual_outcome"] == "home_win").to_numpy().astype(float)
                bin_idx = np.clip(np.digitize(hw_probs, bin_edges) - 1, 0, 9)
                for b in range(10):
                    mask = bin_idx == b
                    if mask.sum() == 0:
                        continue
                    dc_calibration_plot.append({
                        "bin_center": round(float((bin_edges[b] + bin_edges[b + 1]) / 2), 2),
                        "n_matches": int(mask.sum()),
                        "mean_predicted": round(float(hw_probs[mask].mean()), 4),
                        "mean_actual": round(float(hw_actual[mask].mean()), 4),
                    })

                # League coverage
                if "league" in dc_df.columns:
                    for league, lg in dc_df.groupby("league", sort=True):
                        n_lg = len(lg)
                        if n_lg == 0:
                            continue
                        ll_lg = float(
                            -(np.log(
                                lg["exact_score_probability"].clip(lower=1e-12)
                            )).mean()
                        )
                        probs_lg = lg.loc[
                            :, ["home_win_probability", "draw_probability", "away_win_probability"]
                        ].to_numpy()
                        actual_lg = np.vstack(lg["actual_outcome"].map(actual_map))
                        brier_lg = float(np.mean(np.sum((probs_lg - actual_lg) ** 2, axis=1)))
                        dc_league_coverage.append({
                            "league": str(league),
                            "n_matches": n_lg,
                            "mean_log_loss": round(ll_lg, 4),
                            "mean_brier": round(brier_lg, 4),
                        })

        except Exception:
            dc_metrics = {"status": "error"}

    # --- Poisson calibration (from existing results parquet) ---
    poisson_metrics: dict[str, Any] = {"status": "not_available"}
    poisson_results_path = artifact_dir / "poisson_baseline_results.parquet"
    if poisson_results_path.exists():


        try:
            pf = _read_parquet(poisson_results_path)
            if not pf.empty:
                row = pf.iloc[0].to_dict()
                poisson_metrics = {
                    "status": "ok",
                    "log_loss_exact": _clean_json_value(row.get("log_loss_exact")),
                    "brier_1x2": _clean_json_value(row.get("brier_1x2")),
                    "rps_1x2": _clean_json_value(row.get("rps_1x2")),
                    "n_matches": _clean_json_value(row.get("n_matches")),
                }
        except Exception:
            poisson_metrics = {"status": "error"}

    result = _clean_json_value({
        "dixon_coles": dc_metrics,
        "poisson": poisson_metrics,
        "low_score_breakdown": dc_low_score,
        "calibration_plot": dc_calibration_plot,
        "league_coverage": dc_league_coverage,
    })
    _calibration_cache["data"] = result
    _calibration_cache["timestamp"] = time.time()
    return result


def get_action_value_summary(
    limit: int = 20,
    offset: int = 0,
    full: bool = False,
) -> dict[str, Any]:
    """Return independently paged xT and VAEP action-value rows.

    xT is a player-team-season artifact.  VAEP is currently a player-team
    career aggregate and receives display identity plus season *context* from
    the xT artifact.  The two models are kept in separate arrays because
    joining them on a display name would blur those different granularities.

    ``full`` is retained for backwards compatibility with the static exporter;
    ``limit`` and ``offset`` apply independently to each model section.
    """
    import pandas as pd

    from scoutfootball.action_value.identity import (
        attach_team_names,
        build_identity_coverage_report,
        enrich_vaep_identities,
    )

    del full  # Compatibility flag; callers still control row count with limit.
    limit = max(0, min(int(limit), 20_000))
    offset = max(0, int(offset))
    settings = _settings()
    xt_path = settings.data_root / "gold" / "feature_store" / "player_action_value.parquet"
    vaep_path = settings.data_root / "gold" / "feature_store" / "player_vaep.parquet"
    matches_path = settings.raw_root / "statsbomb_open" / "matches_all.parquet"

    # Load xT data
    xt_df = pd.DataFrame()
    if xt_path.exists():
        try:
            xt_df = _read_parquet(xt_path)
        except Exception:
            pass

    # Load VAEP data
    vaep_df = pd.DataFrame()
    if vaep_path.exists():
        try:
            vaep_df = _read_parquet(vaep_path)
        except Exception:
            pass

    matches_df = pd.DataFrame()
    if matches_path.exists():
        try:
            matches_df = _read_parquet(matches_path)
        except Exception:
            pass

    if xt_df.empty and vaep_df.empty:
        # Fallback to legacy player_value_metrics
        frame = load_player_value_metrics()
        if frame.empty:
            return _clean_json_value({
            "status": "no_data", "count": 0, "players": [],
            "attribution_required": _STATSBOMB_ATTRIBUTION,
        })

        working = frame.copy()
        if "composite_score" in working.columns:
            working = working.sort_values("composite_score", ascending=False)

        return _clean_json_value({
            "status": "ok",
            "count": len(working),
            "data_source": "StatsBomb Open Data + xT/VAEP model",
            "attribution_required": _STATSBOMB_ATTRIBUTION,
            "metrics": {
                "players_with_xt": (
                    int(working["xT_per_90"].notna().sum())
                    if "xT_per_90" in working.columns
                    else 0
                ),
                "players_with_finishing": int(working["finishing_delta"].notna().sum())
                if "finishing_delta" in working.columns
                else 0,
                "mean_xt_per_90": (
                    float(working["xT_per_90"].dropna().mean())
                    if "xT_per_90" in working.columns
                    else None
                ),
                "mean_composite_score": float(working["composite_score"].dropna().mean())
                if "composite_score" in working.columns
                else None,
            },
            "players": working.head(limit).to_dict(orient="records"),
        })

    xt_part = attach_team_names(xt_df, matches_df)
    vaep_part = enrich_vaep_identities(vaep_df, xt_df, matches_df)
    if "xt_per_90" in xt_part.columns:
        xt_part = xt_part.sort_values("xt_per_90", ascending=False)
    if "vaep_per_90" in vaep_part.columns:
        vaep_part = vaep_part.sort_values("vaep_per_90", ascending=False)

    total_count = len(xt_part) + len(vaep_part)
    xt_page = xt_part.iloc[offset : offset + limit]
    vaep_page = vaep_part.iloc[offset : offset + limit]
    metrics: dict[str, Any] = {
        "total_rows": total_count,
        "xt_rows": len(xt_part),
        "vaep_rows": len(vaep_part),
    }
    if "xt_per_90" in xt_part.columns and xt_part["xt_per_90"].notna().any():
        metrics["mean_xt_per_90"] = round(float(xt_part["xt_per_90"].dropna().mean()), 4)
        metrics["players_with_xt"] = int(xt_part["xt_per_90"].notna().sum())
    if "vaep_per_90" in vaep_part.columns and vaep_part["vaep_per_90"].notna().any():
        metrics["mean_vaep_per_90"] = round(
            float(vaep_part["vaep_per_90"].dropna().mean()), 4
        )
        metrics["players_with_vaep"] = int(vaep_part["vaep_per_90"].notna().sum())

    return _clean_json_value({
        "status": "ok",
        "count": total_count,
        "offset": offset,
        "limit": limit,
        "data_source": "StatsBomb Open Data + xT/VAEP model",
        "attribution_required": _STATSBOMB_ATTRIBUTION,
        "model_granularity": {
            "xt": "player_team_season",
            "vaep": "player_team_career",
        },
        "metrics": metrics,
        "identity_coverage": build_identity_coverage_report(vaep_part),
        "players": xt_page.to_dict(orient="records"),
        "xt_players": xt_page.to_dict(orient="records"),
        "vaep_players": vaep_page.to_dict(orient="records"),
    })


def get_action_value_evidence_index() -> dict[str, Any]:
    """Return the players and coverage available in the match evidence sample."""
    return _clean_json_value(_get_action_value_evidence_index())


def get_action_value_evidence(player_id: str) -> dict[str, Any]:
    """Return match, action-type, zone and time evidence for one player."""
    return _clean_json_value(_get_action_value_evidence(player_id))


def get_artifacts_summary() -> dict:
    """Return artifact counts and data health for the overview page."""
    ratings = load_player_ratings()
    player_match = load_player_match()
    team_match = load_team_match()
    oof = load_oof_predictions()

    settings = _settings()

    # Count events from StatsBomb
    events_count = 0
    events_path = settings.raw_root / "statsbomb_open" / "events_all.parquet"
    if events_path.exists():
        try:

            events_count = len(_read_parquet(events_path))
        except Exception:
            events_count = 0

    # Data health flags. Demo fallback rows keep the UI usable, but must never
    # be presented as a real trained artifact.
    oof_path = settings.data_root / "models" / "oof_predictions" / "value_fairness_oof.parquet"
    oof_is_synthetic = (
        "is_synthetic" in oof.columns
        and bool(oof["is_synthetic"].fillna(False).all())
    )
    has_oof = oof_path.exists() and not oof.empty and not oof_is_synthetic
    oof_rows = len(oof) if has_oof else 0
    has_truth = False
    truth_rows = 0
    truth_path = settings.data_root / "gold" / "feature_store" / "player_truth_labels.parquet"
    if truth_path.exists():
        try:

            truth_df = _read_parquet(truth_path)
            has_truth = len(truth_df) > 0
            truth_rows = len(truth_df)
        except Exception:
            pass

    # Player match coverage
    pm_coverage = ""
    if not player_match.empty and "data_granularity" in player_match.columns:
        match_count = (player_match["data_granularity"] == "match").sum()
        proxy_count = (player_match["data_granularity"] == "season_proxy").sum()
        pm_coverage = f"{match_count} real + {proxy_count} season proxy"

    artifact_registry = [
        _artifact_file_info(
            settings.data_root / "gold" / "feature_store" / "player_match.parquet",
            "player_match",
            rows=len(player_match),
            display_root=settings.project_root,
        ),
        _artifact_file_info(
            settings.data_root / "gold" / "feature_store" / "team_match.parquet",
            "team_match",
            rows=len(team_match),
            display_root=settings.project_root,
        ),
        _artifact_file_info(
            settings.data_root / "gold" / "feature_store" / "player_ratings_optimized.parquet",
            "player_ratings_optimized",
            rows=len(ratings),
            display_root=settings.project_root,
        ),
        _artifact_file_info(
            events_path,
            "events_all",
            rows=events_count,
            display_root=settings.project_root,
        ),
        _artifact_file_info(
            oof_path,
            "value_fairness_oof",
            rows=oof_rows,
            display_root=settings.project_root,
        ),
        _artifact_file_info(
            truth_path,
            "player_truth_labels",
            rows=truth_rows,
            display_root=settings.project_root,
        ),
    ]

    return _clean_json_value({
        "player_match_rows": len(player_match),
        "team_match_rows": len(team_match),
        "rating_rows": len(ratings),
        "event_samples": events_count,
        "data_source_label": data_source_label(),
        "artifacts": artifact_registry,
        "data_health": {
            "oof_available": has_oof,
            "truth_labels_available": has_truth,
            "player_match_coverage": pm_coverage,
            "confidence_gate": "coverage < 0.90 → low confidence only",
        },
        "license_attribution": {
            "statsbomb": "StatsBomb Open Data — free for research, must attribute source",
            "fbref": "FBref via soccerdata — personal research use only",
            "football_data": "Football-Data.co.uk — free for non-commercial use",
            "understat": "Understat — public data, attribution appreciated",
            "transfermarkt": "Transfermarkt — manual import only, no automated scraping",
        },
    })


def _get_scouting_queues(force_refresh: bool = False):
    """Build and cache scouting queues to avoid redundant computation.

    Each of get_review_queue / get_watchlist / get_shortlist previously
    called build_scouting_queues independently on the full ratings
    DataFrame.  This helper computes the queues once per process and
    reuses the result for all three endpoints.

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cached = _wc_cache.get(_WC_SCOUTING_KEY)
    if cached is _MISSING or force_refresh:
        df = load_player_ratings(force_refresh=force_refresh)
        if df.empty:
            from scoutfootball.evaluation.scouting_queue import ScoutingQueues
            queues = ScoutingQueues(
                review_queue=df, watchlist=df, shortlist=df,
            )
        else:
            queues = build_scouting_queues(
                df,
                run_id=_latest_run_id(),
                reports_root=_settings().data_root / "reports",
            )
        _wc_cache.set(_WC_SCOUTING_KEY, queues)
    return _wc_cache.get(_WC_SCOUTING_KEY)


def get_review_queue(limit: int = 200) -> dict:
    """Return low-confidence players from ratings data as a review queue."""
    df = load_player_ratings()
    if df.empty:
        return {"count": 0, "players": []}

    queues = _get_scouting_queues()
    return _queue_payload(queues.review_queue, limit=limit)


def get_watchlist(limit: int = 100) -> dict:
    df = load_player_ratings()
    if df.empty:
        return {"count": 0, "players": []}
    queues = _get_scouting_queues()
    return _queue_payload(queues.watchlist, limit=limit)


def get_shortlist(limit: int = 100) -> dict:
    df = load_player_ratings()
    if df.empty:
        return {"count": 0, "players": []}
    queues = _get_scouting_queues()
    return _queue_payload(queues.shortlist, limit=limit)


def _enrich_holdout_summary(meta: dict[str, Any]) -> None:
    """Extract a flat holdout summary from metrics for easy frontend display."""
    metrics = meta.get("metrics", {})
    holdout = meta.get("holdout", {})

    # Source: prefer holdout dict, fallback to metrics dict
    src = holdout if holdout else metrics

    # Find the optimized test metrics (most relevant for reporting)
    # Metrics may be stored as JSON strings in meta.json
    def _parse(m: Any) -> dict:
        if isinstance(m, str):
            try:
                return json.loads(m)
            except (json.JSONDecodeError, TypeError):
                return {}
        return m if isinstance(m, dict) else {}

    opt_test = _parse(src.get("optimized_test", {}))
    base_test = _parse(src.get("baseline_test", {}))
    opt_train = _parse(src.get("optimized_train", {}))
    base_train = _parse(src.get("baseline_train", {}))

    def _pick(m: dict) -> dict:
        return {k: v for k, v in m.items() if k in (
            "spearman", "pearson", "rank_loss", "z_mse", "calibration_mae",
            "points_mae", "points_rmse", "points_bias",
            "points_spread_ratio", "raw_spread_ratio",
            "n_players", "n_team_seasons", "team_coverage",
            "split",
        )}

    summary: dict[str, Any] = {}
    if opt_test:
        summary["optimized_test"] = _pick(opt_test)
    elif "optimized_test" in metrics:
        summary["optimized_test"] = _pick(_parse(metrics["optimized_test"]))
    if base_test:
        summary["baseline_test"] = _pick(base_test)
    if opt_train:
        summary["optimized_train"] = _pick(opt_train)
    if base_train:
        summary["baseline_train"] = _pick(base_train)

    # Flat top-level aliases for simple frontend display
    best = opt_test or _parse(metrics.get("optimized_test", {})) or metrics
    for key in ("spearman", "pearson", "rank_loss", "calibration_mae",
                "n_players", "n_team_seasons", "team_coverage"):
        if key in best and key not in meta:
            meta[key] = best[key]

    # Overfit gap
    if "overfit_rank_loss_gap" in src:
        summary["overfit_rank_loss_gap"] = src["overfit_rank_loss_gap"]
    elif "overfit_rank_loss_gap" in metrics:
        summary["overfit_rank_loss_gap"] = metrics["overfit_rank_loss_gap"]

    meta["holdout_summary"] = summary


def _build_reproduce_command(run_id: str, args: dict[str, Any]) -> str:
    """Build a reproduce command string from stored run args."""
    parts = ["PYTHONPATH=src", "uv run python scripts/optimize_ratings_gpu.py"]
    if args.get("seed") is not None:
        parts.append(f"--seed {args['seed']}")
    if args.get("pop_size") is not None:
        parts.append(f"--pop {args['pop_size']}")
    if args.get("n_steps") is not None:
        parts.append(f"--steps {args['n_steps']}")
    if args.get("lr") is not None:
        parts.append(f"--lr {args['lr']}")
    if args.get("patience") is not None:
        parts.append(f"--patience {args['patience']}")
    if args.get("spearman_weight") is not None:
        parts.append(f"--spearman-weight {args['spearman_weight']}")
    if args.get("ndcg_weight") is not None:
        parts.append(f"--ndcg-weight {args['ndcg_weight']}")
    if args.get("position_consistency_weight") is not None:
        parts.append(f"--position-consistency-weight {args['position_consistency_weight']}")
    if args.get("points_regression_weight") is not None:
        parts.append(f"--points-regression-weight {args['points_regression_weight']}")
    if args.get("warmup_steps") is not None:
        parts.append(f"--warmup-steps {args['warmup_steps']}")
    if args.get("grad_clip") is not None:
        parts.append(f"--grad-clip {args['grad_clip']}")
    if args.get("dc_likelihood_weight") is not None and args["dc_likelihood_weight"] > 0:
        parts.append(f"--dc-likelihood-weight {args['dc_likelihood_weight']}")
    if args.get("dc_rho") is not None:
        parts.append(f"--dc-rho {args['dc_rho']}")
    return " ".join(parts)


def get_model_runs() -> dict:
    """Return model run registry from local artifacts."""
    settings = _settings()
    runs = []
    ds_label = data_source_label()

    # Check data/models/runs/ directory
    runs_dir = settings.data_root / "models" / "runs"
    if runs_dir.exists():
        for run_dir in sorted(runs_dir.iterdir(), reverse=True):
            meta_path = run_dir / "meta.json"
            if meta_path.exists():
                meta = _read_json(meta_path)
                meta["run_id"] = run_dir.name
                meta["updated_at"] = meta_path.stat().st_mtime
                meta["data_source"] = ds_label
                # Build reproduce command from stored args
                run_args = meta.get("args", {})
                meta["reproduce_command"] = _build_reproduce_command(
                    run_dir.name, run_args,
                )
                # Extract holdout metrics summary for easy frontend access
                _enrich_holdout_summary(meta)
                runs.append(meta)

    # Fallback: read optimized_params_meta.json
    if not runs:
        meta_path = settings.data_root / "gold" / "feature_store" / "optimized_params_meta.json"
        if meta_path.exists():
            meta = _read_json(meta_path)
            meta["run_id"] = "latest"
            meta["updated_at"] = meta_path.stat().st_mtime
            meta["data_source"] = ds_label
            run_args = meta.get("args", {})
            meta["reproduce_command"] = _build_reproduce_command("latest", run_args)
            _enrich_holdout_summary(meta)
            runs.append(meta)

    return _clean_json_value({"runs": runs, "count": len(runs)})


def _get_run_ids() -> list[str]:
    """Return list of available run IDs."""
    settings = _settings()
    runs_dir = settings.data_root / "models" / "runs"
    if runs_dir.exists():
        return sorted([d.name for d in runs_dir.iterdir() if d.is_dir()], reverse=True)
    return []


def get_model_run_detail(run_id: str) -> dict[str, Any]:
    """Return full details for a single model run.

    Includes run_id, timestamp, input_hash, params, metrics,
    train/test split, feature importance, and data source attribution.
    """
    settings = _settings()
    ds_label = data_source_label()
    runs_dir = settings.data_root / "models" / "runs"

    # Check the runs directory for the specific run
    if runs_dir.exists():
        run_dir = runs_dir / run_id
        meta_path = run_dir / "meta.json"
        if meta_path.exists():
            meta = _read_json(meta_path)
            meta["run_id"] = run_id
            meta["updated_at"] = meta_path.stat().st_mtime
            meta["data_source"] = ds_label

            # Build reproduce command from stored args
            run_args = meta.get("args", {})
            meta["reproduce_command"] = _build_reproduce_command(run_id, run_args)

            # Extract holdout metrics summary
            _enrich_holdout_summary(meta)

            # Load feature importance if available
            importance_path = run_dir / "feature_importance.parquet"
            if importance_path.exists():
    
                try:
                    fi_df = _read_parquet(importance_path)
                    meta["feature_importance"] = _clean_json_value(
                        fi_df.to_dict(orient="records"),
                    )
                except Exception:
                    meta["feature_importance"] = []

            # Load optimized params info
            params_path = run_dir / "optimized_params.npy"
            if params_path.exists():
                import numpy as np
                try:
                    params = np.load(params_path)
                    meta["params_summary"] = {
                        "shape": list(params.shape),
                        "mean": round(float(params.mean()), 6),
                        "std": round(float(params.std()), 6),
                        "min": round(float(params.min()), 6),
                        "max": round(float(params.max()), 6),
                    }
                except Exception:
                    pass

            # Data source attribution
            meta["data_attribution"] = {
                "primary_source": ds_label,
                "license_note": (
                    "Player ratings derived from FBref/Understat data. "
                    "Match results from Football-Data.co.uk. "
                    "Event data from StatsBomb Open Data."
                ),
                "statsbomb_attribution_required": _STATSBOMB_ATTRIBUTION,
            }

            return _clean_json_value(meta)

    # Fallback: check optimized_params_meta.json
    meta_path = settings.data_root / "gold" / "feature_store" / "optimized_params_meta.json"
    if meta_path.exists() and run_id in ("latest", "latest-local"):
        meta = _read_json(meta_path)
        meta["run_id"] = "latest"
        meta["updated_at"] = meta_path.stat().st_mtime
        meta["data_source"] = ds_label
        run_args = meta.get("args", {})
        meta["reproduce_command"] = _build_reproduce_command("latest", run_args)
        _enrich_holdout_summary(meta)
        meta["data_attribution"] = {
            "primary_source": ds_label,
            "license_note": (
                "Player ratings derived from FBref/Understat data. "
                "Match results from Football-Data.co.uk. "
                "Event data from StatsBomb Open Data."
            ),
            "statsbomb_attribution_required": _STATSBOMB_ATTRIBUTION,
        }
        return _clean_json_value(meta)

    return {"error": f"Run '{run_id}' not found", "available_runs": _get_run_ids()}


def _player_list_to_csv(player_list: list[dict]) -> str:
    """Convert a list of player dicts to CSV text."""
    import csv
    import io

    if not player_list:
        return ""
    buf = io.StringIO()
    fieldnames = list(player_list[0].keys())
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for row in player_list:
        writer.writerow(row)
    return buf.getvalue()


def _confidence_reason(minutes: float, matches_count: int, pool_size: int) -> str:
    """Return a human-readable explanation for the confidence level."""
    reasons = []
    if minutes < 450:
        reasons.append("very few minutes (<450)")
    elif minutes < 900:
        reasons.append("limited minutes (<900)")
    if matches_count < 10:
        reasons.append("few matches (<10)")
    elif matches_count < 20:
        reasons.append("below 20 matches")
    if pool_size < 10:
        reasons.append("small position pool (<10)")
    if not reasons:
        return "adequate minutes, matches, and peer pool"
    return "; ".join(reasons)


def _build_position_explanation(
    row: Any,
    pos_pool: Any,
    attack_score: float,
    defense: float,
    possession: float,
    minutes: float,
    score: float,
) -> dict[str, Any]:
    """Build position-wise explanation for each rating dimension."""
    import pandas as _pd

    def _pct_rank(value: float, pool: Any, col: str) -> float:
        clean = _pd.to_numeric(pool[col], errors="coerce").dropna()
        if clean.empty or value != value:
            return 50.0
        return float((clean < value).sum() / len(clean) * 100)

    def _confidence_label(minutes_val: float, pool_size: int) -> str:
        if minutes_val >= 2700 and pool_size >= 20:
            return "HIGH"
        if minutes_val >= 900 and pool_size >= 10:
            return "MEDIUM"
        return "LOW"

    dims: dict[str, Any] = {}
    pool_size = len(pos_pool)
    conf = _confidence_label(minutes, pool_size)

    # Attack
    attack_col = "npg_p90" if "npg_p90" in pos_pool.columns else "optimized_score"
    attack_pct = _pct_rank(attack_score, pos_pool, attack_col)
    # Adjust: add assists percentile
    if "assists_p90" in pos_pool.columns:
        assists_vals = _pd.to_numeric(
            pos_pool["assists_p90"], errors="coerce",
        ).fillna(0)
        player_assists = float(row.get("assists_p90", 0) or 0)
        assists_pct = float(
            (assists_vals < player_assists).sum()
            / max(len(assists_vals), 1) * 100
        )
        attack_pct = (attack_pct + assists_pct) / 2
    dims["attack"] = {
        "raw_score": round(attack_score, 3),
        "percentile_rank": round(attack_pct, 1),
        "contribution": round(attack_pct * 0.30, 1),
        "confidence": conf,
    }

    # Defense
    if "defense_composite" in pos_pool.columns:
        defense_pct = _pct_rank(
            defense, pos_pool, "defense_composite",
        )
    else:
        defense_pct = 50.0
    dims["defense"] = {
        "raw_score": round(defense, 2) if defense == defense else None,
        "percentile_rank": round(defense_pct, 1),
        "contribution": round(defense_pct * 0.20, 1),
        "confidence": conf,
    }

    # Possession
    if "possession_composite" in pos_pool.columns:
        poss_pct = _pct_rank(
            possession, pos_pool, "possession_composite",
        )
    else:
        poss_pct = 50.0
    dims["possession"] = {
        "raw_score": round(possession, 2) if possession == possession else None,
        "percentile_rank": round(poss_pct, 1),
        "contribution": round(poss_pct * 0.20, 1),
        "confidence": conf,
    }

    # Availability
    avail_pct = min(100.0, minutes / 2700 * 100)
    dims["availability"] = {
        "raw_score": round(minutes),
        "percentile_rank": round(min(100.0, avail_pct), 1),
        "contribution": round(avail_pct * 0.10, 1),
        "confidence": conf,
    }

    # Quality (overall score percentile)
    if "optimized_score" in pos_pool.columns:
        quality_pct = _pct_rank(
            score, pos_pool, "optimized_score",
        )
    else:
        quality_pct = 50.0
    dims["quality"] = {
        "raw_score": round(score, 1),
        "percentile_rank": round(quality_pct, 1),
        "contribution": round(quality_pct * 0.20, 1),
        "confidence": conf,
    }

    return dims


def _compute_position_percentiles(row: Any, pos_pool: Any) -> dict[str, Any]:
    """Compute within-position percentile ranks for key metrics."""
    import pandas as pd

    from scoutfootball.evaluation.position_metrics import (
        POSITION_DIMENSIONS,
        POSITION_GROUP_MAP,
        compute_dimension_percentile,
    )

    raw_position = str(row.get("position_group", ""))
    resolved = POSITION_GROUP_MAP.get(raw_position, raw_position)
    dim_defs = POSITION_DIMENSIONS.get(resolved, {})

    result: dict[str, Any] = {}
    for dim_key, dim_cfg in dim_defs.items():
        label = dim_cfg.get("label", dim_key)
        pct = compute_dimension_percentile(pos_pool, dim_cfg, row)
        result[dim_key] = {"label": label, "percentile": round(pct, 1)}

    # Add overall optimized_score percentile within position
    if "optimized_score" in pos_pool.columns:
        clean = pd.to_numeric(pos_pool["optimized_score"], errors="coerce").dropna()
        score_val = pd.to_numeric(row.get("optimized_score"), errors="coerce")
        if not clean.empty and pd.notna(score_val):
            overall_pct = float((clean < score_val).mean() * 100)
        else:
            overall_pct = None
    else:
        overall_pct = None
    result["overall_score"] = {
        "label": "综合评分",
        "percentile": round(overall_pct, 1) if overall_pct is not None else None,
    }

    return result


def _compute_low_confidence_reasons(row: Any) -> list[str]:
    """Compute low-confidence reasons using the confidence module."""
    from scoutfootball.evaluation.confidence import assess_player_confidence

    assessment = assess_player_confidence(row)
    return list(assessment.reasons)


def _compute_3season_trend(player_rows: Any) -> list[dict[str, Any]]:
    """Compute 3-season trend data for a player from their season rows."""

    if player_rows.empty:
        return []

    # Sort by season descending, take up to 3
    sorted_rows = player_rows.sort_values("season", ascending=False).head(3)

    trends = []
    for _, r in sorted_rows.iterrows():
        entry: dict[str, Any] = {
            "season": str(r.get("season", "")),
            "optimized_score": round(float(r.get("optimized_score", 0) or 0), 1),
            "goals": round(float(r.get("npg_p90", 0) or 0), 3),
            "assists": round(float(r.get("assists_p90", 0) or 0), 3),
            "minutes": round(float(r.get("minutes", 0) or 0)),
        }
        trends.append(entry)

    # Compute deltas (newest vs oldest)
    if len(trends) >= 2:
        newest = trends[0]
        oldest = trends[-1]
        delta = {
            "season_from": oldest["season"],
            "season_to": newest["season"],
            "score_change": round(newest["optimized_score"] - oldest["optimized_score"], 1),
            "goals_change": round(newest["goals"] - oldest["goals"], 3),
            "assists_change": round(newest["assists"] - oldest["assists"], 3),
            "minutes_change": round(newest["minutes"] - oldest["minutes"]),
        }
        return {"seasons": trends, "delta": delta}
    return {"seasons": trends, "delta": None}


def get_player_profile(
    player_name: str,
    season: str | None = None,
    position_group: str | None = None,
    limit: int = 50,
    offset: int = 0,
    fmt: str = "json",
) -> dict:
    """Return detailed player profile with radar dimensions.

    Supports fuzzy name matching, pagination, position/season filters,
    rating snapshot history, xT integration, confidence explanation,
    and CSV export.
    """
    import pandas as pd

    df = load_player_ratings()

    # Alias sub_position → position_group for frontend compatibility
    if "sub_position" in df.columns and "position_group" not in df.columns:
        df["position_group"] = df["sub_position"]

    # Fuzzy search: exact match first, then partial case-insensitive
    exact_mask = df["player"] == player_name
    if exact_mask.any():
        mask = exact_mask
    else:
        mask = df["player"].str.contains(player_name, case=False, na=False)
    if position_group:
        mask = mask & (df["position_group"] == position_group)
    if season:
        mask = mask & (df["season"] == season)
    rows = df[mask]
    total = int(rows.shape[0])

    # If multiple players matched (fuzzy), return list with pagination
    if not exact_mask.any() and total > 1:
        unique_names = rows["player"].unique()
        page_names = unique_names[offset : offset + limit]
        page_rows = rows[rows["player"].isin(page_names)]
        player_list = []
        for pname in page_names:
            pr = page_rows[page_rows["player"] == pname]
            best = pr.loc[pr["optimized_score"].idxmax()] if not pr.empty else pr.iloc[0]
            player_list.append(_clean_json_value({
                "player": pname,
                "found": True,
                "team": best.get("team", ""),
                "league": best.get("league", ""),
                "season": best.get("season", ""),
                "position_group": best.get("position_group", ""),
                "optimized_score": round(float(best.get("optimized_score", 0) or 0), 1),
                "minutes": round(float(best.get("minutes", 0) or 0)),
            }))
        # CSV export
        if fmt == "csv" and player_list:
            return _player_list_to_csv(player_list)
        return _clean_json_value({
            "player": player_name,
            "found": True,
            "fuzzy_match": True,
            "total": total,
            "offset": offset,
            "limit": limit,
            "players": player_list,
        })

    if rows.empty:
        return {"player": player_name, "found": False}

    # Pick the best season (highest score) if multiple
    try:
        row = rows.loc[rows["optimized_score"].idxmax()]
    except (ValueError, TypeError):
        row = rows.iloc[0]

    # Build radar dimensions from available data
    # Attack: npg_p90 + assists_p90 percentile within position
    # Possession: possession_composite
    # Defense: defense_composite
    # Reliability: minutes-based (900+ = high, 450+ = medium)
    # Impact: optimized_score percentile within position

    position = row.get("position_group", "")
    pos_pool = df[df["position_group"] == position]

    def _pct(value: float, pool: pd.Series) -> float:
        clean = pd.to_numeric(pool, errors="coerce").dropna()
        if clean.empty or value != value:
            return 50.0
        return float((clean < value).sum() / len(clean) * 100)

    npg = float(row.get("npg_p90", 0) or 0)
    assists = float(row.get("assists_p90", 0) or 0)
    attack_score = npg + assists
    defense = float(row.get("defense_composite", 0) or 0)
    possession = float(row.get("possession_composite", 0) or 0)
    minutes = float(row.get("minutes", 0) or 0)
    score = float(row.get("optimized_score", 0) or 0)

    radar = [
        round(_pct(attack_score, pos_pool["npg_p90"].fillna(0) + pos_pool["assists_p90"].fillna(0)), 1),  # noqa: E501
        round(_pct(possession, pos_pool["possession_composite"]), 1),
        round(_pct(defense, pos_pool["defense_composite"]), 1),
        round(min(100, minutes / 2700 * 100), 1),  # 2700 min = 30 full matches
        round(_pct(score, pos_pool["optimized_score"]), 1),
    ]

    # All seasons for this player
    seasons = []
    for _, r in rows.sort_values("season").iterrows():
        seasons.append({
            "season": r.get("season", ""),
            "team": r.get("team", ""),
            "league": r.get("league", ""),
            "position_group": r.get("position_group", ""),
            "optimized_score": round(float(r.get("optimized_score", 0) or 0), 1),
            "minutes": round(float(r.get("minutes", 0) or 0)),
        })

    low_appearance = bool(row.get("low_appearance", False))
    matches_count = int(row.get("matches", 0) or 0)

    # xT integration from player_value_metrics
    xt_summary: dict[str, Any] = {"available": False}
    try:
        vm = load_player_value_metrics()
        if not vm.empty and "player_name" in vm.columns:
            player_xt = vm[vm["player_name"].str.lower() == player_name.lower()]
            if not player_xt.empty:
                xt_row = player_xt.iloc[0]
                xt_per_90 = xt_row.get("xT_per_90")
                xt_total = xt_row.get("total_xt")
                # Compute xT percentile within position
                xt_pct = None
                if "xT_per_90" in vm.columns and position:
                    pos_names = df[df["position_group"] == position]["player"].unique()
                    pos_xt = vm[vm["player_name"].isin(pos_names)]["xT_per_90"].dropna()
                    if not pos_xt.empty and pd.notna(xt_per_90):
                        xt_pct = round(float((pos_xt < xt_per_90).sum() / len(pos_xt) * 100), 1)
                # xT contribution estimate
                xt_contribution = None
                if pd.notna(xt_per_90) and score > 0:
                    xt_contribution = round(float(xt_per_90 / 0.3 * 10), 1)
                xt_summary = {
                    "available": True,
                    "xT_per_90": round(float(xt_per_90), 4) if pd.notna(xt_per_90) else None,
                    "xT_total": round(float(xt_total), 4) if pd.notna(xt_total) else None,
                    "xT_percentile": xt_pct,
                    "xT_contribution": xt_contribution,
                    "coverage_note": "StatsBomb Open Data sample only",
                }
    except Exception:
        xt_summary = {"available": False, "reason": "xT data not available for this player"}

    # Confidence reason explanation
    pool_size = len(pos_pool)
    conf_reason = _confidence_reason(minutes, matches_count, pool_size)

    # Build position explanation with xT
    position_explanation = _build_position_explanation(
        row, pos_pool, attack_score, defense, possession, minutes, score,
    )
    if xt_summary.get("available"):
        _cov = xt_summary.get("coverage_note") or ""
        _xt_conf = "LOW" if "StatsBomb" in _cov else "MEDIUM"
        position_explanation["xT"] = {
            "xT_per_90": xt_summary.get("xT_per_90"),
            "percentile_rank": xt_summary.get("xT_percentile"),
            "contribution": xt_summary.get("xT_contribution"),
            "confidence": _xt_conf,
        }
    else:
        position_explanation["xT"] = {
            "xT_per_90": None,
            "percentile_rank": None,
            "contribution": None,
            "confidence": "N/A",
            "note": "xT data not available for this player",
        }

    result = _clean_json_value({
        "player": player_name,
        "found": True,
        "team": row.get("team", ""),
        "league": row.get("league", ""),
        "season": row.get("season", ""),
        "position_group": position,
        "optimized_score": round(score, 1),
        "minutes": round(minutes),
        "matches": matches_count,
        "low_appearance": low_appearance,
        "confidence_level": str(row.get("confidence_level", "LOW")).upper(),
        "confidence_reason": conf_reason,
        "npg_p90": round(npg, 3),
        "assists_p90": round(assists, 3),
        "defense_composite": round(defense, 2) if defense == defense else None,
        "possession_composite": round(possession, 2) if possession == possession else None,
        "radar": radar,
        "seasons": seasons,
        "position_explanation": position_explanation,
        "xt_summary": xt_summary,
        "position_percentiles": _compute_position_percentiles(row, pos_pool),
        "low_confidence_reasons": _compute_low_confidence_reasons(row),
        "trend_3seasons": _compute_3season_trend(rows),
    })
    # CSV export
    if fmt == "csv":
        return _player_list_to_csv([result])
    return result


# ── Player comparison ────────────────────────────────────────────────────

_RADAR_LABELS = ["Attack", "Possession", "Defense", "Reliability", "Impact"]


def get_player_comparison(player_a: str, player_b: str) -> dict:
    """Compare two players side-by-side with radar overlay and metric diffs.

    Calls get_player_profile for both players, then builds a unified
    comparison structure with per-dimension deltas.
    """
    profile_a = get_player_profile(player_a)
    profile_b = get_player_profile(player_b)

    if not profile_a.get("found"):
        return {"error": f"Player '{player_a}' not found", "found_a": False}
    if not profile_b.get("found"):
        return {"error": f"Player '{player_b}' not found", "found_b": False}

    # Build radar comparison
    radar_a = profile_a.get("radar", [0, 0, 0, 0, 0])
    radar_b = profile_b.get("radar", [0, 0, 0, 0, 0])
    # Pad to 5 elements if needed
    while len(radar_a) < 5:
        radar_a.append(0)
    while len(radar_b) < 5:
        radar_b.append(0)

    radar_comparison = []
    for i, label in enumerate(_RADAR_LABELS):
        val_a = float(radar_a[i]) if i < len(radar_a) else 0.0
        val_b = float(radar_b[i]) if i < len(radar_b) else 0.0
        radar_comparison.append({
            "dimension": label,
            "player_a": round(val_a, 1),
            "player_b": round(val_b, 1),
            "diff": round(val_a - val_b, 1),
            "advantage": "a" if val_a > val_b else ("b" if val_b > val_a else "tie"),
        })

    # Position percentiles comparison
    pp_a = profile_a.get("position_percentiles", {})
    pp_b = profile_b.get("position_percentiles", {})

    # Merge dimension keys from both
    all_dims = list(dict.fromkeys(
        list(pp_a.get("dimensions", [])) + list(pp_b.get("dimensions", []))
    ))

    pct_comparison = []
    for dim in all_dims:
        val_a = None
        val_b = None
        for d in pp_a.get("dimensions", []):
            if d.get("name") == dim:
                val_a = d.get("percentile")
                break
        for d in pp_b.get("dimensions", []):
            if d.get("name") == dim:
                val_b = d.get("percentile")
                break
        diff = None
        advantage = "tie"
        if val_a is not None and val_b is not None:
            diff = round(float(val_a) - float(val_b), 1)
            advantage = "a" if val_a > val_b else ("b" if val_b > val_a else "tie")
        pct_comparison.append({
            "dimension": dim,
            "player_a": val_a,
            "player_b": val_b,
            "diff": diff,
            "advantage": advantage,
        })

    # Key stats comparison
    stats_fields = [
        "optimized_score", "minutes", "matches", "npg_p90",
        "assists_p90", "defense_composite", "possession_composite",
    ]
    stats_comparison = []
    for field in stats_fields:
        val_a = profile_a.get(field)
        val_b = profile_b.get(field)
        diff = None
        if val_a is not None and val_b is not None:
            try:
                diff = round(float(val_a) - float(val_b), 2)
            except (ValueError, TypeError):
                pass
        stats_comparison.append({
            "metric": field,
            "player_a": val_a,
            "player_b": val_b,
            "diff": diff,
        })

    return _clean_json_value({
        "player_a": {
            "name": profile_a.get("player", player_a),
            "team": profile_a.get("team", ""),
            "league": profile_a.get("league", ""),
            "season": profile_a.get("season", ""),
            "position_group": profile_a.get("position_group", ""),
            "optimized_score": profile_a.get("optimized_score"),
            "confidence_level": profile_a.get("confidence_level", "LOW"),
        },
        "player_b": {
            "name": profile_b.get("player", player_b),
            "team": profile_b.get("team", ""),
            "league": profile_b.get("league", ""),
            "season": profile_b.get("season", ""),
            "position_group": profile_b.get("position_group", ""),
            "optimized_score": profile_b.get("optimized_score"),
            "confidence_level": profile_b.get("confidence_level", "LOW"),
        },
        "radar_labels": _RADAR_LABELS,
        "radar_a": [r["player_a"] for r in radar_comparison],
        "radar_b": [r["player_b"] for r in radar_comparison],
        "radar_comparison": radar_comparison,
        "position_percentile_comparison": pct_comparison,
        "stats_comparison": stats_comparison,
        "same_position": (
            profile_a.get("position_group", "") == profile_b.get("position_group", "")
        ),
    })


# ── World Cup endpoints ──────────────────────────────────────────────────


def get_wc_groups() -> dict:
    """Return World Cup group data with team strength ratings."""
    enriched, strengths = _get_wc_enriched_squads()

    groups_data = []
    for letter, teams in GROUPS.items():
        group_teams = []
        for team in teams:
            squad = enriched.get(team, [])
            rated = [p for p in squad if p.has_rating]
            big5_count = sum(1 for p in squad if p.club_league in BIG5_LEAGUES)
            avg_rating = (
                round(sum(p.rating for p in rated) / len(rated), 2)
                if rated else None
            )
            group_teams.append({
                "team": team,
                "is_host": team in HOSTS,
                "strength": round(strengths.get(team, 0), 3),
                "rated_players": len(rated),
                "total_players": len(squad),
                "big5_players": big5_count,
                "avg_rating": avg_rating,
            })
        groups_data.append({
            "group": letter,
            "teams": group_teams,
        })

    return _clean_json_value({
        "status": "ok",
        "source_attribution": (
            "Ratings derived from FBref/Understat data "
            "via ScoutFootball optimizer"
        ),
        "disclaimer": (
            "Squad ratings are from domestic league performance, "
            "not national team matches. Non-Big5 league players "
            "may lack rating data."
        ),
        "groups": groups_data,
    })


def get_wc_schedule(
    group: str | None = None,
    matchday: int | None = None,
) -> dict:
    """Return World Cup group stage schedule."""
    matches = generate_group_stage_matches()

    match_dicts = []
    for m in matches:
        if group and m.group != group:
            continue
        if matchday and m.matchday != matchday:
            continue
        match_dicts.append({
            "matchday": m.matchday,
            "date": m.date,
            "time_et": m.time_et,
            "home": m.home,
            "away": m.away,
            "venue": m.venue,
            "city": m.city,
            "group": m.group,
            "stage": m.stage,
        })

    return _clean_json_value({
        "status": "ok",
        "count": len(match_dicts),
        "source_attribution": (
            "Schedule generated from official FIFA fixture pattern; "
            "dates/venues are approximate"
        ),
        "matches": match_dicts,
    })


def get_wc_squad(team: str) -> dict:
    """Return a specific team's World Cup squad with player ratings."""
    enriched, _ = _get_wc_enriched_squads()
    squad = enriched.get(team, get_squad(team))

    group = get_team_group(team)
    rated = [p for p in squad if p.has_rating]
    big5_count = sum(1 for p in squad if p.club_league in BIG5_LEAGUES)
    avg_rating = (
        round(sum(p.rating for p in rated) / len(rated), 2)
        if rated else None
    )

    players = []
    for p in squad:
        players.append({
            "name": p.name,
            "position": p.position,
            "club": p.club,
            "club_league": p.club_league,
            "has_rating": p.has_rating,
            "rating": round(p.rating, 2) if p.rating is not None else None,
            "rating_confidence": p.rating_confidence,
        })

    # Sort: rated players first, then by rating desc
    players.sort(key=lambda p: (not p["has_rating"], -(p["rating"] or 0)))

    return _clean_json_value({
        "status": "ok",
        "team": team,
        "group": group,
        "is_host": team in HOSTS,
        "total_players": len(squad),
        "rated_players": len(rated),
        "big5_players": big5_count,
        "avg_rating": avg_rating,
        "source_attribution": (
            "Ratings derived from FBref/Understat data "
            "via ScoutFootball optimizer"
        ),
        "disclaimer": (
            "Squad rosters are placeholder lists; official 26-man "
            "squads not yet announced. Ratings from domestic league "
            "performance only."
        ),
        "players": players,
    })


def get_wc_predictions() -> dict:
    """Return World Cup group stage predictions based on team strengths."""
    enriched, strengths = _get_wc_enriched_squads()
    strength_details = _get_wc_strength_details()
    group_preds = compute_group_predictions(strengths)

    # Build 48-team ranking
    ranked = sorted(strengths.items(), key=lambda x: x[1], reverse=True)
    ranking = []
    for rank, (team, strength) in enumerate(ranked, 1):
        group = get_team_group(team)
        squad = enriched.get(team, [])
        rated = [p for p in squad if p.has_rating]
        ranking.append({
            "rank": rank,
            "team": team,
            "group": group,
            "strength": round(strength, 3),
            "rated_players": len(rated),
            "coverage": strength_details.get(team, {}).get("coverage"),
            "core_avg_rating": strength_details.get(team, {}).get("core_avg_rating"),
            "shrunk_avg_rating": strength_details.get(team, {}).get("shrunk_avg_rating"),
        })

    # Best 3rd-place predictions
    third_place = []
    for gp in group_preds:
        teams = gp["teams"]
        if len(teams) >= 3:
            third = teams[2]
            third["group"] = gp["group"]
            third_place.append(third)
    third_place.sort(key=lambda x: x["strength"], reverse=True)

    return _clean_json_value({
        "status": "ok",
        "source_attribution": (
            "Predictions based on squad ratings from "
            "FBref/Understat data and Opta public priors"
        ),
        "disclaimer": (
            "Probabilities are rough estimates from a simplified "
            "strength-ratio model. Non-Big5 league team strengths "
            "may be underestimated. Not a real match prediction."
        ),
        "groups": group_preds,
        "ranking": ranking,
        "best_third_place": third_place[:8],
    })


def get_wc_teams() -> dict:
    """Return all 48 World Cup teams with strength ratings and group info."""
    enriched, strengths = _get_wc_enriched_squads()
    strength_details = _get_wc_strength_details()

    teams_data = []
    for letter, team_names in GROUPS.items():
        for team in team_names:
            squad = enriched.get(team, [])
            rated = [p for p in squad if p.has_rating]
            big5_count = sum(1 for p in squad if p.club_league in BIG5_LEAGUES)
            avg_rating = (
                round(sum(p.rating for p in rated) / len(rated), 2)
                if rated else None
            )
            details = strength_details.get(team, {})
            teams_data.append({
                "team": team,
                "group": letter,
                "is_host": team in HOSTS,
                "strength": round(strengths.get(team, 0), 3),
                "rated_players": len(rated),
                "total_players": len(squad),
                "big5_players": big5_count,
                "avg_rating": avg_rating,
                "coverage": details.get("coverage"),
                "observed_avg_rating": details.get("observed_avg_rating"),
                "proxy_avg_rating": details.get("proxy_avg_rating"),
                "shrunk_avg_rating": details.get("shrunk_avg_rating"),
                "core_avg_rating": details.get("core_avg_rating"),
                "depth_avg_rating": details.get("depth_avg_rating"),
                "reserve_avg_rating": details.get("reserve_avg_rating"),
                "squad_quality_rating": details.get("squad_quality_rating"),
                "rating_score": details.get("rating_score"),
                "opta_score": details.get("opta_score"),
                "league_score": details.get("league_score"),
                "coverage_score": details.get("coverage_score"),
                "big5_score": details.get("big5_score"),
            })

    return _clean_json_value({
        "status": "ok",
        "count": len(teams_data),
        "source_attribution": (
            "Ratings derived from FBref/Understat data "
            "via ScoutFootball optimizer"
        ),
        "disclaimer": (
            "Squad ratings are from domestic league performance, "
            "not national team matches. Non-Big5 league players "
            "may lack rating data."
        ),
        "teams": teams_data,
    })
