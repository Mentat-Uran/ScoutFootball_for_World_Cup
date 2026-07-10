"""Unified data loader: reads local Parquet when available, falls back to demo data."""
from __future__ import annotations

import logging
import os
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

from scoutfootball.config import PlatformSettings

logger = logging.getLogger(__name__)


# ── TTL cache infrastructure ──────────────────────────────────────
_MISSING = object()


class _TTLCache:
    """Simple TTL cache with force_refresh support.

    Stores values with timestamps and expires them after
    SCOUTFOOTBALL_CACHE_TTL_SECONDS (default 300s). No external deps.
    """

    _DEFAULT_TTL = 300.0

    def __init__(self) -> None:
        self._ttl = self._read_ttl()
        self._store: dict[Any, tuple[Any, float]] = {}

    @staticmethod
    def _read_ttl() -> float:
        raw = os.environ.get("SCOUTFOOTBALL_CACHE_TTL_SECONDS")
        if not raw:
            return _TTLCache._DEFAULT_TTL
        try:
            val = float(raw)
            return val if val > 0 else _TTLCache._DEFAULT_TTL
        except (TypeError, ValueError):
            return _TTLCache._DEFAULT_TTL

    def get(self, key: Any) -> Any:
        """Return cached value if fresh, else ``_MISSING``."""
        entry = self._store.get(key)
        if entry is None:
            return _MISSING
        value, ts = entry
        if time.time() - ts > self._ttl:
            return _MISSING
        return value

    def set(self, key: Any, value: Any) -> None:
        self._store[key] = (value, time.time())

    def invalidate(self, key: Any) -> None:
        self._store.pop(key, None)


_ttl_cache = _TTLCache()


@lru_cache(maxsize=1)
def _settings() -> PlatformSettings:
    return PlatformSettings.from_root()


def _parquet_path(relative_path: str):
    return _settings().data_root / relative_path


def _parquet_exists(relative_path: str) -> bool:
    path = _parquet_path(relative_path)
    return path.exists() and path.suffix == ".parquet"


def _mark_synthetic(df: pd.DataFrame) -> pd.DataFrame:
    """Add is_synthetic=True column to a demo DataFrame."""
    df = df.copy()
    df["is_synthetic"] = True
    return df


def _duckdb_path() -> Path:
    return _settings().data_root / "gold" / "scoutlab.duckdb"


def _duckdb_exists() -> bool:
    return _duckdb_path().exists()


def _minutes_to_confidence(minutes: float) -> str:
    if minutes >= 900:
        return "HIGH"
    if minutes >= 450:
        return "MEDIUM"
    return "LOW"


def _safe_read_parquet(relative_path: str) -> pd.DataFrame | None:
    """Read a Parquet file via DuckDB (avoids pyarrow dependency), returning None on any error."""
    if not _parquet_exists(relative_path):
        return None
    try:
        import duckdb

        # The module-level ``duckdb.read_parquet`` helper uses a shared default
        # connection. Concurrent FastAPI requests can close each other's
        # pending result and incorrectly trigger the synthetic-data fallback.
        # Give every read its own short-lived connection instead.
        con = duckdb.connect()
        try:
            return con.execute(
                "SELECT * FROM read_parquet(?)",
                [str(_parquet_path(relative_path))],
            ).fetchdf()
        finally:
            con.close()
    except Exception:
        logger.warning("Failed to read %s", relative_path, exc_info=True)
        return None


def _normalize_ratings_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    result = df.copy()
    if "sub_position" in result.columns and "position_group" not in result.columns:
        result = result.rename(columns={"sub_position": "position_group"})

    if "minutes" in result.columns:
        result["minutes"] = pd.to_numeric(result["minutes"], errors="coerce").fillna(0.0)

    if "confidence_level" not in result.columns:
        if "minutes" in result.columns:
            result["confidence_level"] = result["minutes"].map(_minutes_to_confidence)
        else:
            result["confidence_level"] = "LOW"
    else:
        result["confidence_level"] = result["confidence_level"].astype(str).str.upper()

    if "player" in result.columns and "player_name" not in result.columns:
        result["player_name"] = result["player"]
    if "team" in result.columns and "team_name" not in result.columns:
        result["team_name"] = result["team"]

    return result


def _load_all_player_ratings(force_refresh: bool = False) -> pd.DataFrame:
    """Load all player ratings into memory (cached with TTL).

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cache_key = "_load_all_player_ratings"
    if not force_refresh:
        cached = _ttl_cache.get(cache_key)
        if cached is not _MISSING:
            return cached

    if _duckdb_exists():
        try:
            import duckdb

            con = duckdb.connect(str(_duckdb_path()), read_only=True)
            try:
                df = con.execute(
                    "SELECT * FROM player_ratings ORDER BY optimized_score DESC"
                ).fetchdf()
                result = _normalize_ratings_frame(df)
                _ttl_cache.set(cache_key, result)
                return result
            finally:
                con.close()
        except Exception:
            logger.warning("DuckDB read failed, falling back to Parquet", exc_info=True)

    # Fallback to Parquet
    rel = "gold/feature_store/player_ratings_optimized.parquet"
    df = _safe_read_parquet(rel)
    if df is not None:
        df = _normalize_ratings_frame(df)
        result = df.sort_values("optimized_score", ascending=False).reset_index(drop=True)
        _ttl_cache.set(cache_key, result)
        return result

    logger.warning("No ratings data found — falling back to synthetic demo data")
    from scoutfootball.app.demo_data import generate_player_match

    demo = generate_player_match()
    demo["optimized_score"] = demo.get("rating", 0.5)
    demo["position_group"] = demo.get("position", "MF")
    demo["confidence_level"] = "MEDIUM"
    result = _mark_synthetic(_normalize_ratings_frame(demo))
    _ttl_cache.set(cache_key, result)
    return result


def load_player_ratings(
    position: str | None = None,
    league: str | None = None,
    team: str | None = None,
    season: str | None = None,
    min_score: float | None = None,
    force_refresh: bool = False,
) -> pd.DataFrame:
    """Load player ratings from DuckDB or Parquet, with optional filters.

    Falls back to player_ratings_optimized.parquet, then demo data.
    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    df = _load_all_player_ratings(force_refresh=force_refresh)
    if position and "position_group" in df.columns:
        df = df[df["position_group"] == position]
    if league and "league" in df.columns:
        df = df[df["league"] == league]
    if team and "team" in df.columns:
        df = df[df["team"] == team]
    if season and "season" in df.columns:
        df = df[df["season"] == season]
    if min_score is not None and "optimized_score" in df.columns:
        df = df[df["optimized_score"] >= min_score]
    return df.reset_index(drop=True)


def load_model_meta(force_refresh: bool = False) -> pd.DataFrame:
    """Load model metadata from DuckDB or JSON (cached with TTL).

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cache_key = "load_model_meta"
    if not force_refresh:
        cached = _ttl_cache.get(cache_key)
        if cached is not _MISSING:
            return cached

    if _duckdb_exists():
        try:
            import duckdb

            con = duckdb.connect(str(_duckdb_path()), read_only=True)
            try:
                result = con.execute("SELECT * FROM model_meta").fetchdf()
                _ttl_cache.set(cache_key, result)
                return result
            finally:
                con.close()
        except Exception:
            logger.warning("DuckDB model_meta read failed, falling back to JSON", exc_info=True)

    # Fallback to JSON
    json_path = _parquet_path("gold/feature_store/optimized_params_meta.json")
    if json_path.exists():
        import json

        with open(json_path) as f:
            meta = json.load(f)
        holdout = meta.get("holdout", {}).get("optimized_test", {})
        result = pd.DataFrame([{
            "run_id": meta.get("timestamp", "unknown"),
            "timestamp": meta.get("timestamp", ""),
            "n_params": meta.get("n_params", 0),
            "spearman": holdout.get("spearman", 0),
            "pearson": holdout.get("pearson", 0),
            "overfit_gap": meta.get("holdout", {}).get("overfit_rank_loss_gap", 0),
        }])
        _ttl_cache.set(cache_key, result)
        return result

    result = pd.DataFrame()
    _ttl_cache.set(cache_key, result)
    return result


def load_league_metrics(force_refresh: bool = False) -> pd.DataFrame:
    """Load league metrics from DuckDB or Parquet (cached with TTL).

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cache_key = "load_league_metrics"
    if not force_refresh:
        cached = _ttl_cache.get(cache_key)
        if cached is not _MISSING:
            return cached

    if _duckdb_exists():
        try:
            import duckdb

            con = duckdb.connect(str(_duckdb_path()), read_only=True)
            try:
                result = con.execute("SELECT * FROM league_metrics").fetchdf()
                _ttl_cache.set(cache_key, result)
                return result
            finally:
                con.close()
        except Exception:
            logger.warning("DuckDB league_metrics failed, falling back", exc_info=True)

    rel = "gold/feature_store/rating_league_metrics.parquet"
    df = _safe_read_parquet(rel)
    if df is not None:
        _ttl_cache.set(cache_key, df)
        return df

    result = pd.DataFrame()
    _ttl_cache.set(cache_key, result)
    return result


def load_player_match() -> pd.DataFrame:
    df = _safe_read_parquet("gold/feature_store/player_match.parquet")
    if df is not None:
        return df
    logger.warning("player_match.parquet not found — falling back to synthetic demo data")
    from scoutfootball.app.demo_data import generate_player_match

    return _mark_synthetic(generate_player_match())


def load_team_match() -> pd.DataFrame:
    df = _safe_read_parquet("gold/feature_store/team_match.parquet")
    if df is not None:
        return df
    logger.warning("team_match.parquet not found — falling back to synthetic demo data")
    from scoutfootball.app.demo_data import generate_team_match

    return _mark_synthetic(generate_team_match())


def load_player_rolling(force_refresh: bool = False) -> pd.DataFrame:
    """Load player rolling features from Parquet (cached with TTL).

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cache_key = "load_player_rolling"
    if not force_refresh:
        cached = _ttl_cache.get(cache_key)
        if cached is not _MISSING:
            return cached

    df = _safe_read_parquet("gold/feature_store/player_rolling.parquet")
    if df is not None:
        _ttl_cache.set(cache_key, df)
        return df
    logger.warning("player_rolling.parquet not found — falling back to synthetic demo data")
    from scoutfootball.app.demo_data import generate_player_match, generate_player_rolling

    result = _mark_synthetic(generate_player_rolling(generate_player_match()))
    _ttl_cache.set(cache_key, result)
    return result


def load_team_rolling(force_refresh: bool = False) -> pd.DataFrame:
    """Load team rolling features from Parquet (cached with TTL).

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cache_key = "load_team_rolling"
    if not force_refresh:
        cached = _ttl_cache.get(cache_key)
        if cached is not _MISSING:
            return cached

    df = _safe_read_parquet("gold/feature_store/team_rolling.parquet")
    if df is not None:
        _ttl_cache.set(cache_key, df)
        return df
    logger.warning("team_rolling.parquet not found — falling back to synthetic demo data")
    from scoutfootball.app.demo_data import generate_team_match, generate_team_rolling

    result = _mark_synthetic(generate_team_rolling(generate_team_match()))
    _ttl_cache.set(cache_key, result)
    return result


def load_oof_predictions() -> pd.DataFrame:
    df = _safe_read_parquet("models/oof_predictions/value_fairness_oof.parquet")
    if df is not None:
        return df
    logger.warning("value_fairness_oof.parquet not found — falling back to synthetic demo data")
    from scoutfootball.app.demo_data import generate_oof_predictions

    return _mark_synthetic(generate_oof_predictions())


def load_player_value_metrics(force_refresh: bool = False) -> pd.DataFrame:
    """Load player value metrics from Parquet (cached with TTL).

    Pass ``force_refresh=True`` to bypass the cache (e.g. after model retraining).
    """
    cache_key = "load_player_value_metrics"
    if not force_refresh:
        cached = _ttl_cache.get(cache_key)
        if cached is not _MISSING:
            return cached

    df = _safe_read_parquet("gold/feature_store/player_value_metrics.parquet")
    result = df if df is not None else pd.DataFrame()
    _ttl_cache.set(cache_key, result)
    return result


def load_score_prediction(home_team: str | None = None, away_team: str | None = None):
    if _parquet_exists("models/artifacts/poisson_baseline_results.parquet"):
        from scoutfootball.models.match_prediction import (
            fit_independent_poisson,
            predict_match,
        )

        team_match = load_team_match()
        model = fit_independent_poisson(team_match)
        team_id_series = team_match.get("team_id", pd.Series(dtype="string"))
        team_ids = [
            team_id
            for team_id in team_id_series.dropna().astype(str).unique()
        ]
        if len(team_ids) >= 2:
            resolved_home = _resolve_team_id(home_team, team_ids) if home_team else team_ids[0]
            resolved_away = _resolve_team_id(away_team, team_ids) if away_team else team_ids[1]
            if resolved_home is None:
                raise ValueError(
                    f"Home team '{home_team}' not found. "
                    f"Available: {', '.join(sorted(team_ids)[:15])}..."
                )
            if resolved_away is None:
                raise ValueError(
                    f"Away team '{away_team}' not found. "
                    f"Available: {', '.join(sorted(team_ids)[:15])}..."
                )
            return predict_match(model, resolved_home, resolved_away)
        logger.warning("Only %d team_ids found; need >= 2 for prediction", len(team_ids))
    logger.warning("Poisson artifacts not found — falling back to synthetic demo prediction")
    from scoutfootball.app.demo_data import generate_score_matrix

    return generate_score_matrix()


def _resolve_team_id(name: str, team_ids: list[str]) -> str | None:
    """Resolve a team name to a team_id with case-insensitive fallback."""
    # Exact match
    if name in team_ids:
        return name
    # Case-insensitive match
    lower_map = {tid.lower(): tid for tid in team_ids}
    if name.lower() in lower_map:
        return lower_map[name.lower()]
    # Substring containment (e.g., "Man" matches "Man City" or "Man United")
    candidates = [tid for tid in team_ids if name.lower() in tid.lower()]
    if len(candidates) == 1:
        return candidates[0]
    return None


def load_score_prediction_dc(home_team: str | None = None, away_team: str | None = None):
    """Predict a match using the Dixon-Coles model.

    Loads team_match data, fits the DC model, and returns predict_match_dc output.
    Falls back to the Poisson-based ``load_score_prediction`` when DC artifacts
    are unavailable.
    """
    if _parquet_exists("models/artifacts/dixon_coles_results.parquet"):
        from scoutfootball.models.match_prediction import (
            fit_dixon_coles,
            predict_match_dc,
        )

        team_match = load_team_match()
        try:
            model = fit_dixon_coles(team_match)
        except Exception:
            logger.warning("Dixon-Coles fit failed; falling back to Poisson", exc_info=True)
            return load_score_prediction(home_team, away_team)

        team_id_series = team_match.get("team_id", pd.Series(dtype="string"))
        team_ids = [
            team_id
            for team_id in team_id_series.dropna().astype(str).unique()
        ]
        if len(team_ids) >= 2:
            resolved_home = _resolve_team_id(home_team, team_ids) if home_team else team_ids[0]
            resolved_away = _resolve_team_id(away_team, team_ids) if away_team else team_ids[1]
            if resolved_home is None:
                raise ValueError(
                    f"Home team '{home_team}' not found. "
                    f"Available: {', '.join(sorted(team_ids)[:15])}..."
                )
            if resolved_away is None:
                raise ValueError(
                    f"Away team '{away_team}' not found. "
                    f"Available: {', '.join(sorted(team_ids)[:15])}..."
                )
            return predict_match_dc(model, resolved_home, resolved_away)
        logger.warning("Only %d team_ids found; need >= 2 for prediction", len(team_ids))

    # DC artifacts missing — fall back to Poisson path
    return load_score_prediction(home_team, away_team)


def data_source_label() -> str:
    """Return a granular label describing the data source state."""
    has_player_match = _parquet_exists("gold/feature_store/player_match.parquet")
    has_oof = _parquet_exists("models/oof_predictions/value_fairness_oof.parquet")
    has_poisson = _parquet_exists("models/artifacts/poisson_baseline_results.parquet")
    has_dc = _parquet_exists("models/artifacts/dixon_coles_results.parquet")

    if not has_player_match:
        return "Demo data (synthetic)"

    # Check granularity of player_match
    try:
        import duckdb
        pq_path = str(_parquet_path("gold/feature_store/player_match.parquet"))
        pm = duckdb.read_parquet(pq_path).fetchdf()
        if "data_granularity" in pm.columns:
            match_count = (pm["data_granularity"] == "match").sum()
            proxy_count = (pm["data_granularity"] == "season_proxy").sum()
            if match_count > 0 and proxy_count > 0:
                detail = f"real matches ({match_count}) + season proxy ({proxy_count})"
            elif match_count > 0:
                detail = "real match-level data"
            else:
                detail = "season proxy only (FBref)"
        else:
            detail = "local Parquet"
    except Exception:
        detail = "local Parquet"

    parts = [detail]
    if has_oof:
        parts.append("value_fairness OOF")
    if has_dc:
        parts.append("Dixon-Coles model")
    elif has_poisson:
        parts.append("Poisson model")
    return " | ".join(parts)
