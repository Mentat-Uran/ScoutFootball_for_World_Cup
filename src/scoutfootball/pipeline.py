"""Pipeline orchestration: daily ingest, feature build, weekly training."""

from __future__ import annotations

import logging
import math
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from scoutfootball.config import DEFAULT_INGEST_CONFIG, IngestConfig, PlatformSettings
from scoutfootball.entities.normalize import normalize_country_name, normalize_person_name
from scoutfootball.evaluation.validation import run_pre_training_validation
from scoutfootball.features.player_match import build_player_match_features
from scoutfootball.features.player_rolling import build_player_rolling_features
from scoutfootball.features.rating_matrix import build_rating_feature_matrix, write_feature_manifest
from scoutfootball.features.team_match import build_team_match_features
from scoutfootball.features.team_rolling import build_team_rolling_features
from scoutfootball.models.match_prediction import (
    fit_dixon_coles,
    fit_independent_poisson,
)

logger = logging.getLogger(__name__)


def _settings() -> PlatformSettings:
    return PlatformSettings.from_root()


def _log_path() -> Path:
    p = _settings().log_root / "ingestion"
    p.mkdir(parents=True, exist_ok=True)
    return p


def run_daily_ingest(
    sources: tuple[str, ...] = ("statsbomb_open", "football_data", "clubelo", "understat"),
    *,
    settings: PlatformSettings | None = None,
    ingest_config: IngestConfig | None = None,
) -> dict[str, str]:
    resolved = settings or _settings()
    config = ingest_config or DEFAULT_INGEST_CONFIG
    results: dict[str, str] = {}
    timestamp = datetime.now(tz=UTC).isoformat()

    for source in sources:
        try:
            if source == "statsbomb_open":
                results[source] = _ingest_statsbomb(resolved, ingest_config=config)
            elif source == "football_data":
                results[source] = _ingest_football_data(resolved, ingest_config=config)
            elif source == "clubelo":
                results[source] = _ingest_clubelo(resolved)
            elif source == "understat":
                results[source] = _ingest_understat(resolved, ingest_config=config)
            elif source == "sofascore":
                results[source] = _ingest_sofascore(resolved, ingest_config=config)
            elif source == "sofifa":
                results[source] = _ingest_sofifa(resolved, ingest_config=config)
            elif source == "api_football":
                results[source] = _ingest_api_football(resolved, ingest_config=config)
            elif source == "transfermarkt_datasets":
                results[source] = _ingest_transfermarkt_datasets(resolved, ingest_config=config)
            else:
                results[source] = f"skipped: unknown source '{source}'"
        except Exception as exc:
            results[source] = f"failed: {exc}"
            logger.error("Ingest failed for %s: %s", source, exc)

    logger.info("Daily ingest completed at %s: %s", timestamp, results)
    return results


def run_build_features(
    *,
    settings: PlatformSettings | None = None,
) -> dict[str, str]:
    resolved = settings or _settings()
    results: dict[str, str] = {}

    try:
        team_match = _build_team_match_from_football_data(resolved)
        team_match_path = resolved.gold_root / "feature_store" / "team_match.parquet"
        team_match.to_parquet(team_match_path, index=False)
        results["team_match"] = f"ok ({len(team_match)} rows -> {team_match_path.name})"

        team_rolling = build_team_rolling_features(team_match, windows=(3, 5))
        team_rolling_path = resolved.gold_root / "feature_store" / "team_rolling.parquet"
        team_rolling.to_parquet(team_rolling_path, index=False)
        results["team_rolling"] = f"ok ({len(team_rolling)} rows -> {team_rolling_path.name})"

        # Combine StatsBomb per-match data (if available) with FBref season proxy
        sb_match = _build_player_match_from_statsbomb(resolved)
        fbref_proxy = _build_player_match_proxy_from_fbref(resolved)

        if not sb_match.empty:
            player_match = pd.concat([sb_match, fbref_proxy], ignore_index=True, sort=False)
            match_count = (player_match["data_granularity"] == "match").sum()
            proxy_count = (player_match["data_granularity"] == "season_proxy").sum()
            granularity_info = f"{match_count} match-level + {proxy_count} season-proxy"
        else:
            player_match = fbref_proxy
            granularity_info = "season-level FBref proxy only"

        player_match_path = resolved.gold_root / "feature_store" / "player_match.parquet"
        player_match.to_parquet(player_match_path, index=False)
        results["player_match"] = (
            f"ok ({len(player_match)} rows -> {player_match_path.name}; {granularity_info})"
        )

        player_rolling = build_player_rolling_features(player_match, windows=(2, 3))
        player_rolling_path = resolved.gold_root / "feature_store" / "player_rolling.parquet"
        player_rolling.to_parquet(player_rolling_path, index=False)
        results["player_rolling"] = (
            f"ok ({len(player_rolling)} rows -> {player_rolling_path.name}; built from proxy)"
        )

        # --- Rating feature matrix ---
        try:
            rating_matrix = build_rating_feature_matrix(player_match, player_rolling)
            if not rating_matrix.empty:
                rating_matrix_path = (
                    resolved.gold_root / "feature_store" / "rating_feature_matrix.parquet"
                )
                rating_matrix.to_parquet(rating_matrix_path, index=False)
                write_feature_manifest(rating_matrix, rating_matrix_path)
                results["rating_feature_matrix"] = (
                    f"ok ({len(rating_matrix)} rows -> {rating_matrix_path.name})"
                )
            else:
                results["rating_feature_matrix"] = "skipped: empty matrix produced"
        except Exception as exc:
            results["rating_feature_matrix"] = f"failed: {exc}"
            logger.error("Rating feature matrix build failed: %s", exc)

        # --- Truth labels: only create template if file does not exist ---
        try:
            from scoutfootball.evaluation.truth_labels import create_empty_truth_labels

            truth_labels_path = (
                resolved.gold_root / "feature_store" / "player_truth_labels.parquet"
            )
            if not truth_labels_path.exists():
                truth_labels = create_empty_truth_labels()
                truth_labels.to_parquet(truth_labels_path, index=False)
                results["player_truth_labels"] = (
                    f"ok (empty template -> {truth_labels_path.name})"
                )
            else:
                results["player_truth_labels"] = (
                    f"ok (existing -> {truth_labels_path.name})"
                )
        except Exception as exc:
            results["player_truth_labels"] = f"failed: {exc}"
            logger.error("Truth labels template creation failed: %s", exc)
    except Exception as exc:
        results["features"] = f"failed: {exc}"
        logger.error("Feature build failed: %s", exc)

    return results


def run_weekly_train(
    *,
    skip_if_validation_fails: bool = True,
    settings: PlatformSettings | None = None,
) -> dict[str, str]:
    resolved = settings or _settings()
    report = run_pre_training_validation(resolved)
    if skip_if_validation_fails and not report.passed:
        return {
            "status": "skipped",
            "reason": report.summary(),
        }

    results: dict[str, str] = {}
    try:
        results["validation"] = report.summary() if not report.passed else "Validation: PASS"

        # --- value_fairness training ---
        try:
            results["value_fairness"] = _train_value_fairness(resolved)
        except Exception as exc:
            results["value_fairness"] = f"failed: {exc}"
            logger.error("Value fairness training failed: %s", exc)

        # --- supervised player-rating NN candidate ---
        try:
            results["player_rating_nn"] = _train_player_rating_nn_candidate(resolved)
        except Exception as exc:
            results["player_rating_nn"] = f"failed: {exc}"
            logger.error("Player rating NN training failed: %s", exc)

        team_match_path = resolved.gold_root / "feature_store" / "team_match.parquet"
        if not team_match_path.exists():
            results["match_prediction"] = (
                "skipped: missing team_match.parquet, run `scoutfootball build-features` first"
            )
            return results

        team_match = pd.read_parquet(team_match_path)
        if len(team_match) < 20:
            results["match_prediction"] = "skipped: team_match.parquet has fewer than 20 rows"
            return results

        poisson_model = fit_independent_poisson(team_match)
        _save_poisson_artifacts(poisson_model, team_match, resolved)
        results["match_prediction"] = (
            "ok (trained IndependentPoissonModel and wrote artifacts to data/models/artifacts)"
        )

        # --- Dixon-Coles training (with time decay) ---
        try:
            dc_decay = 0.005  # Dixon-Coles (1997) paper recommended value
            dc_model = fit_dixon_coles(team_match, decay=dc_decay)
            _save_dixon_coles_artifacts(dc_model, team_match, resolved)
            results["dixon_coles"] = (
                f"ok (trained DixonColesModel with decay={dc_decay} "
                f"and wrote artifacts to data/models/artifacts)"
            )
        except Exception as exc:
            results["dixon_coles"] = f"failed: {exc}"
            logger.error("Dixon-Coles training failed: %s", exc)

        # --- DC calibration backtest ---
        try:
            from scoutfootball.evaluation.backtests import run_dc_calibration_backtest

            cal_result = run_dc_calibration_backtest(
                team_match, resolved.model_root, save_detail=True,
            )
            ll = cal_result.metrics["log_loss_exact"]
            brier = cal_result.metrics["brier_1x2"]
            n = int(cal_result.metrics["n_matches"])
            # Save calibration report
            artifact_dir = resolved.model_root / "artifacts"
            artifact_dir.mkdir(parents=True, exist_ok=True)
            cal_result.calibration.to_parquet(
                artifact_dir / "dc_calibration_report.parquet", index=False,
            )
            results["dc_calibration"] = (
                f"ok ({n} matches, log_loss={ll:.4f}, brier_1x2={brier:.4f})"
            )
        except Exception as exc:
            results["dc_calibration"] = f"failed: {exc}"
            logger.error("DC calibration backtest failed: %s", exc)

        # --- DC probability calibration (isotonic) ---
        try:
            from scoutfootball.evaluation.backtests import run_dc_backtest_with_calibration

            dc_cal_bt = run_dc_backtest_with_calibration(
                team_match, decay=dc_decay, calibration_method="isotonic",
            )
            # Save calibration report to feature_store
            cal_store_dir = resolved.gold_root / "feature_store"
            cal_store_dir.mkdir(parents=True, exist_ok=True)
            if dc_cal_bt.calibration.calibrated_predictions is not None:
                dc_cal_bt.calibration.calibrated_predictions.to_parquet(
                    cal_store_dir / "dc_calibration_report.parquet", index=False,
                )
            b_before = dc_cal_bt.metrics["brier_1x2_before"]
            b_after = dc_cal_bt.metrics["brier_1x2_after"]
            rps_before = dc_cal_bt.metrics["rps_before"]
            rps_after = dc_cal_bt.metrics["rps_after"]
            results["dc_prob_calibration"] = (
                f"ok (Brier {b_before:.4f}->{b_after:.4f}, "
                f"RPS {rps_before:.4f}->{rps_after:.4f}, "
                f"n={dc_cal_bt.metrics['n_matches']})"
            )
        except Exception as exc:
            results["dc_prob_calibration"] = f"failed: {exc}"
            logger.error("DC probability calibration failed: %s", exc)

        # --- availability diagnostic ---
        try:
            results["availability_diagnostic"] = _run_availability_diagnostic(resolved)
        except Exception as exc:
            results["availability_diagnostic"] = f"failed: {exc}"
            logger.error("Availability diagnostic failed: %s", exc)
    except Exception as exc:
        results["training"] = f"failed: {exc}"
        logger.error("Training failed: %s", exc)

    return results


def _ingest_statsbomb(
    settings: PlatformSettings,
    *,
    ingest_config: IngestConfig | None = None,
) -> str:
    """Read cached StatsBomb open-data JSONs and consolidate into parquet."""
    from scoutfootball.adapters.statsbomb_open import load_matches

    config = ingest_config or DEFAULT_INGEST_CONFIG

    match_dir = settings.raw_root / "statsbomb_open" / "matches"
    if not match_dir.exists():
        return "skipped: no cached StatsBomb match directory"

    combos: list[tuple[int, int]] = []
    for comp_dir in match_dir.iterdir():
        if comp_dir.is_dir():
            for season_file in comp_dir.glob("*.json"):
                combos.append((int(comp_dir.name), int(season_file.stem)))

    if not combos:
        return "skipped: no cached StatsBomb match JSONs found"

    # Filter by configured season range
    valid_seasons = set(config.seasons)
    combos = [(cid, sid) for cid, sid in combos if sid in valid_seasons]

    if not combos:
        return "skipped: no StatsBomb seasons within configured range"

    frames: list[pd.DataFrame] = []
    for competition_id, season_id in sorted(combos):
        try:
            result = load_matches(
                competition_id,
                season_id,
                settings=settings,
            )
            frames.append(result.dataframe)
        except Exception as exc:
            logger.warning(
                "StatsBomb load_matches failed for comp=%d season=%d: %s",
                competition_id,
                season_id,
                exc,
            )

    if not frames:
        return "failed: no StatsBomb matches could be loaded from cache"

    combined = pd.concat(frames, ignore_index=True, sort=False)
    output_path = settings.raw_root / "statsbomb_open" / "big5_matches.parquet"
    combined.to_parquet(output_path, index=False)
    return f"ok ({len(combined)} matches from {len(combos)} season(s) -> {output_path.name})"


def _ingest_football_data(
    settings: PlatformSettings,
    *,
    ingest_config: IngestConfig | None = None,
) -> str:
    """Read cached Football-Data CSVs and consolidate into combined_results.parquet."""
    from scoutfootball.adapters.football_data import download_csv

    config = ingest_config or DEFAULT_INGEST_CONFIG

    fd_dir = settings.raw_root / "football_data"
    if not fd_dir.exists():
        return "skipped: no Football-Data cache directory"

    fd_leagues = config.football_data_leagues
    league_codes = [lg.football_data_code for lg in fd_leagues]
    league_name_map = {lg.football_data_code: lg.name for lg in fd_leagues}
    season_codes = config.football_data_season_codes

    frames: list[pd.DataFrame] = []
    loaded = 0

    for season in season_codes:
        for league_code in league_codes:
            csv_path = fd_dir / season / f"{league_code}.csv"
            if not csv_path.exists():
                continue
            try:
                result = download_csv(
                    league_code,
                    season,
                    settings=settings,
                )
                frame = result.dataframe.copy()
                frame["league"] = league_name_map.get(league_code, league_code)
                frame["season"] = season
                frames.append(frame)
                loaded += 1
            except Exception as exc:
                logger.warning(
                    "Football-Data load failed for %s/%s: %s",
                    season,
                    league_code,
                    exc,
                )

    if not frames:
        return "failed: no Football-Data CSVs could be loaded"

    combined = pd.concat(frames, ignore_index=True, sort=False)
    output_path = fd_dir / "combined_results.parquet"
    combined.to_parquet(output_path, index=False)
    return f"ok ({len(combined)} rows from {loaded} CSV(s) -> {output_path.name})"


def _ingest_clubelo(settings: PlatformSettings) -> str:
    """Try to fetch Club Elo ratings for today. Degrades gracefully on timeout."""
    from datetime import date

    from scoutfootball.adapters.clubelo import fetch_elo_by_date

    try:
        result = fetch_elo_by_date(date.today(), settings=settings)
        return f"ok ({result.metadata.record_count} teams)"
    except Exception as exc:
        logger.warning("Club Elo fetch failed (expected if API is down): %s", exc)
        return f"degraded: Club Elo API unavailable ({type(exc).__name__})"


def _ingest_understat(
    settings: PlatformSettings,
    *,
    ingest_config: IngestConfig | None = None,
) -> str:
    """Try to fetch Understat league player stats. Degrades gracefully on failure."""
    from scoutfootball.adapters.understat import fetch_league_players

    config = ingest_config or DEFAULT_INGEST_CONFIG
    understat_leagues = config.understat_leagues
    leagues = [(lg.understat_name, season) for lg in understat_leagues for season in config.seasons]

    total = 0
    errors: list[str] = []

    for league, season in leagues:
        try:
            result = fetch_league_players(league, season, settings=settings)
            total += result.metadata.record_count
        except Exception as exc:
            errors.append(f"{league}/{season}: {type(exc).__name__}")
            logger.warning("Understat fetch failed for %s %d: %s", league, season, exc)

    if total > 0:
        return f"ok ({total} player records)"
    return f"degraded: all Understat fetches failed ({'; '.join(errors)})"


def _ingest_sofascore(
    settings: PlatformSettings,
    *,
    ingest_config: IngestConfig | None = None,
) -> str:
    """Fetch SofaScore player match stats for configured leagues and seasons."""
    from scoutfootball.adapters.sofascore import fetch_player_match_stats

    config = ingest_config or DEFAULT_INGEST_CONFIG
    total = 0
    errors: list[str] = []

    for lg in config.leagues:
        if lg.sofascore_id is None:
            continue
        for season_year in config.seasons:
            season_str = f"{season_year}-{season_year + 1}"
            try:
                result = fetch_player_match_stats(lg.name, season_str, settings=settings)
                total += result.metadata.record_count
            except Exception as exc:
                errors.append(f"{lg.name}/{season_str}: {type(exc).__name__}")
                logger.warning("SofaScore fetch failed for %s %s: %s", lg.name, season_str, exc)

    if total > 0:
        return f"ok ({total} records)"
    if errors:
        return f"degraded: all SofaScore fetches failed ({'; '.join(errors)})"
    return "skipped: no leagues with sofascore_id configured"


def _ingest_sofifa(
    settings: PlatformSettings,
    *,
    ingest_config: IngestConfig | None = None,
) -> str:
    """Fetch SoFIFA player ratings for configured leagues and seasons."""
    config = ingest_config or DEFAULT_INGEST_CONFIG

    sofifa_leagues = [lg for lg in config.leagues if lg.sofifa_id is not None]
    if not sofifa_leagues:
        return "skipped: no leagues with sofifa_id configured"

    # SoFIFA adapter not yet implemented — placeholder
    logger.warning("SoFIFA adapter not yet implemented; skipping ingest")
    return "skipped: SoFIFA adapter not yet implemented"


def _ingest_api_football(
    settings: PlatformSettings,
    *,
    ingest_config: IngestConfig | None = None,
) -> str:
    """Fetch API-Football data (injuries, transfers, coaches) for configured leagues."""
    from scoutfootball.adapters.api_football import ApiKeyMissingError, fetch_injuries

    config = ingest_config or DEFAULT_INGEST_CONFIG

    api_leagues = [lg for lg in config.leagues if lg.api_football_id is not None]
    if not api_leagues:
        return "skipped: no leagues with api_football_id configured"

    total = 0
    errors: list[str] = []

    for lg in api_leagues:
        for season_year in config.seasons:
            try:
                result = fetch_injuries(lg.api_football_id, season_year, settings=settings)
                total += result.metadata.record_count
            except ApiKeyMissingError:
                return "skipped: API_FOOTBALL_KEY not configured"
            except Exception as exc:
                errors.append(f"{lg.name}/{season_year}: {type(exc).__name__}")
                logger.warning("API-Football fetch failed for %s %d: %s", lg.name, season_year, exc)

    if total > 0:
        return f"ok ({total} injury records)"
    if errors:
        return f"degraded: all API-Football fetches failed ({'; '.join(errors)})"
    return "skipped: no data fetched from API-Football"


def _ingest_transfermarkt_datasets(
    settings: PlatformSettings,
    *,
    ingest_config: IngestConfig | None = None,
) -> str:
    """Import Transfermarkt dataset files from the manual import directory."""
    tm_dir = settings.raw_root / "transfermarkt_manual"
    if not tm_dir.exists():
        return "skipped: no transfermarkt_manual directory"

    from scoutfootball.adapters.transfermarkt_manual import load_snapshot

    csv_files = sorted(f for f in tm_dir.glob("*.csv") if not f.name.startswith("."))
    if not csv_files:
        return "skipped: no CSV files in transfermarkt_manual"

    total = 0
    errors: list[str] = []

    for csv_file in csv_files:
        try:
            result = load_snapshot(csv_file)
            total += result.metadata.record_count
        except Exception as exc:
            errors.append(f"{csv_file.name}: {type(exc).__name__}")
            logger.warning("Transfermarkt import failed for %s: %s", csv_file.name, exc)

    if total > 0:
        return f"ok ({total} player records from {len(csv_files)} file(s))"
    if errors:
        return f"degraded: all Transfermarkt imports failed ({'; '.join(errors)})"
    return "skipped: no valid Transfermarkt data found"


def _build_team_match_from_football_data(settings: PlatformSettings) -> pd.DataFrame:
    input_path = settings.raw_root / "football_data" / "combined_results.parquet"
    if not input_path.exists():
        raise FileNotFoundError(f"Missing Football-Data artifact: {input_path}")

    matches = pd.read_parquet(input_path).copy()
    matches["match_date"] = pd.to_datetime(
        matches["Date"], dayfirst=True, format="mixed", errors="raise"
    )
    matches = matches.sort_values(["match_date", "league", "HomeTeam", "AwayTeam"]).reset_index(
        drop=True
    )
    matches["match_id"] = matches.index.map(lambda idx: f"fd-match-{idx + 1}")
    matches["competition_id"] = matches["league"].astype("string")
    matches["season_id"] = matches["season"].astype("string")
    matches["home_team_id"] = matches["HomeTeam"].astype("string")
    matches["home_team_name"] = matches["HomeTeam"].astype("string")
    matches["away_team_id"] = matches["AwayTeam"].astype("string")
    matches["away_team_name"] = matches["AwayTeam"].astype("string")
    matches["home_goals"] = pd.to_numeric(matches["FTHG"], errors="raise")
    matches["away_goals"] = pd.to_numeric(matches["FTAG"], errors="raise")
    matches["home_shots"] = pd.to_numeric(matches.get("HS"), errors="coerce")
    matches["away_shots"] = pd.to_numeric(matches.get("AS"), errors="coerce")
    matches["home_shots_on_target"] = pd.to_numeric(matches.get("HST"), errors="coerce")
    matches["away_shots_on_target"] = pd.to_numeric(matches.get("AST"), errors="coerce")

    return build_team_match_features(matches)


def _build_player_match_from_statsbomb(settings: PlatformSettings) -> pd.DataFrame:
    """Aggregate StatsBomb events into per-player-per-match appearances."""
    events_path = settings.raw_root / "statsbomb_open" / "events_all.parquet"
    if not events_path.exists():
        events_path = settings.raw_root / "statsbomb_open" / "events_sample.parquet"
    matches_path = settings.raw_root / "statsbomb_open" / "big5_matches.parquet"

    if not events_path.exists() or not matches_path.exists():
        return pd.DataFrame()

    events = pd.read_parquet(events_path)
    matches = pd.read_parquet(matches_path)

    if events.empty or matches.empty:
        return pd.DataFrame()

    # Filter to events with a player
    events = events.dropna(subset=["player_id"]).copy()

    # Per-player-per-match aggregation
    agg_records: list[dict] = []
    for (match_id, player_id), group in events.groupby(["match_id", "player_id"]):
        player_name = group["player_name"].iloc[0]
        team_id = group["team_id"].iloc[0]
        team_name = group["team_name"].iloc[0]

        # Minutes: last event minute (rough estimate)
        minutes = int(group["minute"].max()) + 1 if not group.empty else 0

        # Goals: shots with outcome "Goal"
        shots = group[group["event_type"] == "Shot"]
        goals = int((shots["shot_outcome_name"] == "Goal").sum())
        shots_total = len(shots)
        shots_on = int(shots["shot_outcome_name"].isin(["Goal", "Saved", "Saved To Post"]).sum())
        xg = (
            float(shots["shot_statsbomb_xg"].sum())
            if "shot_statsbomb_xg" in shots.columns
            else 0.0
        )

        # Assists: passes with goal_assist flag
        assists = int(group.get("pass_goal_assist", pd.Series(False)).sum())

        # Passes
        passes = int((group["event_type"] == "Pass").sum())

        # Tackles
        tackles = int((group["event_type"] == "Duel").sum())

        # Position from tactics
        position_name = (
            group["position_name"].dropna().iloc[0]
            if "position_name" in group.columns
            and group["position_name"].notna().any()
            else None
        )

        agg_records.append({
            "match_id": str(match_id),
            "player_id": str(player_id),
            "player_name": player_name,
            "team_id": str(team_id),
            "team_name": team_name,
            "minutes_played": minutes,
            "goals": goals,
            "assists": assists,
            "shots": shots_total,
            "shots_on_target": shots_on,
            "npxg": xg if xg > 0 else pd.NA,
            "xa": pd.NA,
            "passes": passes,
            "tackles": tackles,
            "xT_added": pd.NA,
            "position_name": position_name,
        })

    if not agg_records:
        return pd.DataFrame()

    player_match = pd.DataFrame(agg_records)

    # Merge match metadata
    match_meta = matches[["match_id", "match_date", "home_team_id", "away_team_id"]].copy()
    match_meta["match_id"] = match_meta["match_id"].astype(str)
    player_match = player_match.merge(match_meta, on="match_id", how="left")

    # Determine is_home and opponent
    player_match["is_home"] = player_match["team_id"] == player_match["home_team_id"].astype(str)
    player_match["opponent_team_id"] = player_match.apply(
        lambda r: r["away_team_id"] if r["is_home"] else r["home_team_id"], axis=1,
    )

    # Map position names to position groups
    pos_map = {
        "Goalkeeper": "GK",
        "Center Back": "DF", "Left Back": "DF", "Right Back": "DF",
        "Left Wing Back": "DF", "Right Wing Back": "DF",
        "Center Defensive Midfield": "MF", "Center Midfield": "MF",
        "Center Attacking Midfield": "MF", "Left Midfield": "MF",
        "Right Midfield": "MF", "Left Center Midfield": "MF",
        "Right Center Midfield": "MF", "Left Defensive Midfield": "MF",
        "Right Defensive Midfield": "MF",
        "Left Wing": "FW", "Right Wing": "FW", "Center Forward": "FW",
        "Secondary Striker": "FW",
    }
    player_match["position_group"] = player_match["position_name"].map(pos_map).fillna("UNK")

    # Add derived columns
    player_match["started"] = (player_match["minutes_played"] >= 30).astype(int)
    player_match["matches_played"] = 1
    player_match["data_granularity"] = "match"
    player_match["source_name"] = "statsbomb_open"
    player_match["match_date"] = pd.to_datetime(player_match["match_date"], errors="coerce")

    # Drop helper columns
    player_match = player_match.drop(
        columns=["home_team_id", "away_team_id", "position_name"],
        errors="ignore",
    )

    return build_player_match_features(player_match)


def _build_player_match_proxy_from_fbref(settings: PlatformSettings) -> pd.DataFrame:
    input_path = settings.raw_root / "fbref" / "player_stats_big5_3seasons.parquet"
    if not input_path.exists():
        raise FileNotFoundError(f"Missing FBref player artifact: {input_path}")

    frame = pd.read_parquet(input_path)
    index_frame = frame.index.to_frame(index=False)
    nation = frame.get(("nation", ""), pd.Series(pd.NA, index=frame.index)).reset_index(drop=True)
    born = pd.to_numeric(
        frame.get(("born", ""), pd.Series(pd.NA, index=frame.index)).reset_index(drop=True),
        errors="coerce",
    )
    position = frame.get(("pos", ""), pd.Series("UNK", index=frame.index)).reset_index(drop=True)
    matches_played = pd.to_numeric(
        frame.get(("Playing Time", "MP"), pd.Series(0, index=frame.index)).reset_index(drop=True),
        errors="coerce",
    ).fillna(0)
    default_series = pd.Series(0, index=frame.index)
    starts = pd.to_numeric(
        frame.get(("Playing Time", "Starts"), default_series).reset_index(drop=True),
        errors="coerce",
    ).fillna(0)
    minutes = pd.to_numeric(
        frame.get(("Playing Time", "Min"), pd.Series(0, index=frame.index)).reset_index(drop=True),
        errors="coerce",
    ).fillna(0)
    goals = pd.to_numeric(
        frame.get(("Performance", "Gls"), pd.Series(0, index=frame.index)).reset_index(drop=True),
        errors="coerce",
    ).fillna(0)
    assists = pd.to_numeric(
        frame.get(("Performance", "Ast"), pd.Series(0, index=frame.index)).reset_index(drop=True),
        errors="coerce",
    ).fillna(0)

    # Bundesliga rows have NaN league in FBref; fill before str conversion
    index_frame["league"] = index_frame["league"].fillna("GER-Bundesliga")
    proxy = pd.DataFrame(
        {
            "competition_id": index_frame["league"].astype("string"),
            "season_id": index_frame["season"].astype("string"),
            "team_id": index_frame["team"].astype("string"),
            "team_name": index_frame["team"].astype("string"),
            "player_name": index_frame["player"].astype("string"),
            "position_group": position.astype("string"),
            "minutes_played": minutes,
            "started": starts,
            "matches_played": matches_played,
            "goals": goals,
            "assists": assists,
            "nation": nation.astype("string"),
            "born": born,
        },
    )
    proxy["match_date"] = proxy["season_id"].map(_season_end_date_from_code)
    proxy["player_id"] = proxy.apply(_build_proxy_player_id, axis=1)
    proxy["match_id"] = proxy.apply(_build_proxy_match_id, axis=1)
    proxy["data_granularity"] = "season_proxy"
    proxy["source_name"] = "fbref"

    player_match = build_player_match_features(proxy)
    return player_match


def _save_poisson_artifacts(
    model,
    team_match: pd.DataFrame,
    settings: PlatformSettings,
) -> None:
    artifact_dir = settings.model_root / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    results_df = pd.DataFrame(
        [
            {
                "model_type": "independent_poisson",
                "train_rows": len(team_match),
                "league_home_rate": model.league_home_rate,
                "league_away_rate": model.league_away_rate,
                "num_teams": len(model.home_attack_strength),
                "smoothing": model.smoothing,
            }
        ]
    )
    results_df.to_parquet(artifact_dir / "poisson_baseline_results.parquet", index=False)

    team_ids = sorted(model.home_attack_strength)
    away_attack_strength = [model.away_attack_strength.get(team_id) for team_id in team_ids]
    home_defense_strength = [model.home_defense_strength.get(team_id) for team_id in team_ids]
    away_defense_strength = [model.away_defense_strength.get(team_id) for team_id in team_ids]
    strengths_df = pd.DataFrame(
        {
            "team_id": team_ids,
            "home_attack_strength": [model.home_attack_strength[team_id] for team_id in team_ids],
            "away_attack_strength": away_attack_strength,
            "home_defense_strength": home_defense_strength,
            "away_defense_strength": away_defense_strength,
        }
    )
    strengths_df.to_parquet(artifact_dir / "team_strengths.parquet", index=False)


def _save_dixon_coles_artifacts(
    model,
    team_match: pd.DataFrame,
    settings: PlatformSettings,
) -> None:
    artifact_dir = settings.model_root / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    results_df = pd.DataFrame(
        [
            {
                "model_type": "dixon_coles",
                "num_matches": model.num_matches,
                "rho": model.rho,
                "home_advantage": model.home_advantage,
                "league_mean_goals": model.league_mean_goals,
                "num_teams": len(model.team_attack),
                "half_life_days": model.half_life_days,
                "decay": model.decay,
            }
        ]
    )
    results_df.to_parquet(artifact_dir / "dixon_coles_results.parquet", index=False)

    team_ids = sorted(model.team_attack)
    strengths_df = pd.DataFrame(
        {
            "team_id": team_ids,
            "attack_strength": [model.team_attack[t] for t in team_ids],
            "defense_strength": [model.team_defense[t] for t in team_ids],
        }
    )
    strengths_df.to_parquet(artifact_dir / "dc_team_strengths.parquet", index=False)

    # Low-score calibration report
    try:
        _save_dc_calibration_report(model, team_match, artifact_dir)
    except Exception as exc:
        logger.warning("DC calibration report failed: %s", exc)


def _save_dc_calibration_report(
    model,
    team_match: pd.DataFrame,
    artifact_dir: Path,
) -> None:
    """Analyze Dixon-Coles low-score calibration against actual results."""
    from scoutfootball.models.match_prediction import predict_match_dc

    # Build match pairs
    df = team_match.copy()
    df["is_home"] = df["is_home"].astype(bool)
    home_df = df[df["is_home"]].copy()
    away_df = df[~df["is_home"]].copy()
    pairs = home_df.merge(away_df, on="match_id", suffixes=("_home", "_away"))
    if pairs.empty:
        return

    # Compute predicted probabilities for each match
    score_buckets = {
        "0-0": 0, "1-0": 0, "0-1": 0, "1-1": 0,
        "2-0": 0, "0-2": 0, "2-1": 0, "1-2": 0, "other": 0,
    }
    actual_buckets = dict(score_buckets)
    n_matches = len(pairs)

    log_loss_sum = 0.0
    log_loss_count = 0

    for _, row in pairs.iterrows():
        home_id = str(row["team_id_home"])
        away_id = str(row["team_id_away"])
        hg = int(row["goals_for_home"])
        ag = int(row["goals_for_away"])

        try:
            pred = predict_match_dc(model, home_id, away_id, max_goals=5)
        except Exception:
            continue

        # Actual score bucket
        actual_key = f"{hg}-{ag}" if f"{hg}-{ag}" in actual_buckets else "other"
        actual_buckets[actual_key] += 1

        # Track log-loss for the actual score outcome
        if hg < pred.score_matrix.shape[0] and ag < pred.score_matrix.shape[1]:
            prob = float(pred.score_matrix.iloc[hg, ag])
            if prob > 0:
                log_loss_sum += -math.log(prob)
                log_loss_count += 1

    # Write calibration report
    log_loss_exact = round(log_loss_sum / max(log_loss_count, 1), 4)
    report_rows = []
    for bucket in ["0-0", "1-0", "0-1", "1-1", "2-0", "0-2", "2-1", "1-2", "other"]:
        report_rows.append({
            "score": bucket,
            "actual_count": actual_buckets[bucket],
            "actual_pct": round(actual_buckets[bucket] / max(n_matches, 1) * 100, 1),
        })

    cal_df = pd.DataFrame(report_rows)
    cal_df["log_loss_exact"] = log_loss_exact
    cal_df["n_matches"] = n_matches
    cal_df.to_parquet(artifact_dir / "dc_low_score_calibration.parquet", index=False)


def _run_availability_diagnostic(settings: PlatformSettings) -> str:
    """Run availability shortcut diagnostic and save report."""
    from scoutfootball.evaluation.availability_diagnostic import (
        generate_availability_diagnostic,
        save_availability_diagnostic,
    )

    report = generate_availability_diagnostic(settings=settings)
    output_dir = settings.model_root / "availability_diagnostic"
    return save_availability_diagnostic(report, output_dir)


def _train_player_rating_nn_candidate(settings: PlatformSettings) -> str:
    """Train or explicitly skip the supervised player-rating NN candidate."""
    from scoutfootball.models.player_rating_nn import (
        PlayerRatingNNConfig,
        train_player_rating_nn_from_files,
    )

    result = train_player_rating_nn_from_files(
        settings=settings,
        config=PlayerRatingNNConfig(min_labels=200),
        output_dir=settings.model_root / "player_rating_nn",
    )
    return result.status


def _train_value_fairness(settings: PlatformSettings) -> str:
    """Train value_fairness model and save OOF predictions."""
    import numpy as np

    from scoutfootball.models.value_fairness import fit_regressor

    player_rolling_path = settings.gold_root / "feature_store" / "player_rolling.parquet"
    if not player_rolling_path.exists():
        return "skipped: missing player_rolling.parquet"

    player_rolling = pd.read_parquet(player_rolling_path)
    if len(player_rolling) < 50:
        return "skipped: player_rolling.parquet has fewer than 50 rows"

    enriched = _build_market_enriched_features(player_rolling, settings)
    if "market_value" not in enriched.columns:
        return "skipped: could not attach market_value to player features"

    valid_count = enriched["market_value"].notna().sum()
    if valid_count < 50:
        return f"skipped: only {valid_count} rows with valid market_value"

    # Drop rows where market_value is NA to avoid residual computation issues
    enriched = enriched.dropna(subset=["market_value"]).reset_index(drop=True)

    result = fit_regressor(
        enriched,
        target_col="market_value",
        date_col="snapshot_date",
        feature_version="v0.3.0",
        data_version="synthetic_v1",
    )

    # Clip extreme predictions to reasonable range (€100K - €500M)
    from sklearn.metrics import mean_absolute_error

    oof = result.oof_predictions
    log_min, log_max = np.log1p(100_000), np.log1p(500_000_000)
    oof["predicted_market_value_log"] = oof["predicted_market_value_log"].clip(log_min, log_max)
    oof["predicted_market_value"] = np.expm1(oof["predicted_market_value_log"])
    oof["residual_log"] = oof["actual_market_value_log"] - oof["predicted_market_value_log"]

    # Recompute metrics after clipping
    metrics = dict(result.metrics)
    metrics["mae_model"] = float(mean_absolute_error(
        oof["actual_market_value"], oof["predicted_market_value"],
    ))
    metrics["mae_improvement_vs_baseline"] = metrics["mae_baseline"] - metrics["mae_model"]

    # Save OOF predictions
    oof_dir = settings.model_root / "oof_predictions"
    oof_dir.mkdir(parents=True, exist_ok=True)
    oof.to_parquet(oof_dir / "value_fairness_oof.parquet", index=False)

    # Save training summary
    artifact_dir = settings.model_root / "artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    summary_df = pd.DataFrame([metrics])
    summary_df["feature_version"] = result.feature_version
    summary_df["data_version"] = result.data_version
    summary_df["estimator"] = result.estimator_name
    summary_df["oof_rows"] = len(oof)
    summary_df.to_parquet(artifact_dir / "value_fairness_results.parquet", index=False)

    mae = metrics.get("mae_model", 0)
    mae_base = metrics.get("mae_baseline", 0)
    improvement = metrics.get("mae_improvement_vs_baseline", 0)
    return (
        f"ok (OOF {len(oof)} rows, "
        f"MAE={mae:,.0f} vs baseline={mae_base:,.0f}, "
        f"improvement={improvement:+,.0f})"
    )


def _build_market_enriched_features(
    player_rolling: pd.DataFrame,
    settings: PlatformSettings,
) -> pd.DataFrame:
    """Merge market_value into player features from Transfermarkt or synthetic source."""
    enriched = player_rolling.copy()

    # Try real Transfermarkt manual import first (schema-compliant CSVs)
    tm_path = settings.raw_root / "transfermarkt_manual"
    market_source = "none"
    market_df = None

    for csv_file in sorted(tm_path.glob("*.csv")):
        if csv_file.name.startswith("."):
            continue
        try:
            from scoutfootball.adapters.transfermarkt_manual import load_snapshot

            result = load_snapshot(csv_file)
            market_df = result.dataframe
            market_source = csv_file.name
            break
        except Exception:
            continue

    # Fallback: try raw Transfermarkt CSVs (player_market_value + player_profiles)
    if market_df is None:
        market_df, market_source = _load_raw_transfermarkt_csv(settings)

    if market_df is None:
        # No real Transfermarkt data — generate synthetic market values
        market_df = _generate_synthetic_market_values(enriched)
        market_source = "synthetic"

    # Normalize for merge: aggregate to player-level latest value
    market_df = market_df.copy()
    market_df["player_name_norm"] = (
        market_df["player_name"].astype("string").str.strip().str.lower()
    )
    market_df["team_name_norm"] = (
        market_df["team_name"].astype("string").str.strip().str.lower()
        if "team_name" in market_df.columns
        else pd.Series("", index=market_df.index, dtype="string")
    )

    # Take latest snapshot per player
    if "snapshot_date" in market_df.columns:
        market_df["snapshot_date"] = pd.to_datetime(market_df["snapshot_date"], errors="coerce")
        market_df = market_df.sort_values("snapshot_date").drop_duplicates(
            subset=["player_name_norm"], keep="last"
        )
    else:
        market_df = market_df.drop_duplicates(subset=["player_name_norm"], keep="last")

    # Merge on normalized player name
    enriched["player_name_norm"] = (
        enriched["player_name"].astype("string").str.strip().str.lower()
    )
    market_lookup = market_df[["player_name_norm", "market_value"]].copy()

    enriched = enriched.merge(market_lookup, on="player_name_norm", how="left")
    enriched = enriched.drop(columns=["player_name_norm"])

    # Use match_date as snapshot_date for time-series split
    if "snapshot_date" not in enriched.columns:
        enriched["snapshot_date"] = enriched["match_date"]

    # Compute age from born year
    if "age" not in enriched.columns and "born" in enriched.columns:
        enriched["age"] = (
            pd.to_datetime(enriched["match_date"]).dt.year
            - pd.to_numeric(enriched["born"], errors="coerce")
        )

    logger.info(
        "Market enrichment: source=%s, %d/%d players matched",
        market_source,
        enriched["market_value"].notna().sum(),
        len(enriched),
    )
    return enriched


def _load_raw_transfermarkt_csv(
    settings: PlatformSettings,
) -> tuple[pd.DataFrame | None, str]:
    """Load raw Transfermarkt CSVs (player_market_value + player_profiles) and
    return a DataFrame with player_name, team_name, snapshot_date, market_value columns.

    Returns (None, "none") if the required files are not found.
    """
    tm_dir = settings.raw_root / "transfermarkt"
    mv_path = tm_dir / "player_latest_market_value.csv"
    profiles_path = tm_dir / "player_profiles.csv"

    # Fallback to full history file if latest not available
    if not mv_path.exists():
        mv_path = tm_dir / "player_market_value.csv"

    if not mv_path.exists() or not profiles_path.exists():
        return None, "none"

    try:
        mv_df = pd.read_csv(mv_path)
        profiles_df = pd.read_csv(
            profiles_path,
            usecols=["player_id", "player_name", "current_club_name"],
        )

        # Join on player_id
        merged = mv_df.merge(profiles_df, on="player_id", how="left")

        # Build canonical columns
        result = pd.DataFrame(
            {
                "player_name": merged["player_name"].astype("string").str.strip(),
                "team_name": merged["current_club_name"].astype("string").str.strip(),
                "snapshot_date": pd.to_datetime(merged["date_unix"], errors="coerce"),
                "market_value": pd.to_numeric(merged["value"], errors="coerce"),
            }
        )

        # Drop rows with missing critical fields
        result = result.dropna(subset=["player_name", "market_value"])

        # Take latest snapshot per player
        result = result.sort_values("snapshot_date").drop_duplicates(
            subset=["player_name"], keep="last"
        )

        source_label = mv_path.name
        logger.info(
            "Loaded raw Transfermarkt CSV: %s, %d players with market value",
            source_label,
            len(result),
        )
        return result, source_label
    except Exception as exc:
        logger.warning("Failed to load raw Transfermarkt CSVs: %s", exc)
        return None, "none"


def _generate_synthetic_market_values(player_rolling: pd.DataFrame) -> pd.DataFrame:
    """Generate synthetic market values from FBref stats. CLEARLY LABELED AS SYNTHETIC."""
    import numpy as np

    # Aggregate per-player stats across all seasons
    agg = player_rolling.groupby("player_id", as_index=False).agg(
        player_name=("player_name", "first"),
        team_name=("team_name", "first"),
        position_group=("position_group", "first"),
        total_minutes=("minutes_played", "sum"),
        total_goals=("goals", "sum"),
        total_assists=("assists", "sum"),
        matches_played=("matches_played", "sum"),
        born=("born", "first"),
    )

    # Compute per-90 metrics
    safe_minutes = agg["total_minutes"].clip(lower=1)
    goals_p90 = (agg["total_goals"] / safe_minutes) * 90
    assists_p90 = (agg["total_assists"] / safe_minutes) * 90

    # Position base values (€)
    position_base = {"GK": 5e6, "DF": 8e6, "MF": 10e6, "FW": 12e6}
    base = agg["position_group"].map(position_base).fillna(8e6)

    # Age factor (peak at 27)
    current_year = 2025
    age = current_year - pd.to_numeric(agg["born"], errors="coerce").fillna(25)
    age_factor = np.exp(-0.5 * ((age - 27) / 5) ** 2)

    # Performance multiplier
    minute_ratio = (agg["total_minutes"] / 3000).clip(upper=1.0)
    perf = 1.0 + goals_p90 * 2.0 + assists_p90 * 1.5 + minute_ratio * 0.5

    # Synthetic market value
    rng = np.random.default_rng(42)
    noise = rng.lognormal(0, 0.3, size=len(agg))
    market_value = (base * age_factor * perf * noise).clip(lower=100_000, upper=200_000_000)

    result = pd.DataFrame(
        {
            "player_name": agg["player_name"],
            "team_name": agg["team_name"],
            "snapshot_date": pd.Timestamp("2025-01-15"),
            "market_value": market_value.round(-3),  # round to nearest 1000
        }
    )

    # Save a copy for audit trail
    output_dir = player_rolling.attrs.get("_settings_raw_root")
    if output_dir is not None:
        output_path = Path(output_dir) / "transfermarkt_manual" / "synthetic_market_values.csv"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        header_comment = (
            "# SYNTHETIC DATA — NOT REAL MARKET VALUES\n"
            "# Generated from FBref stats for pipeline validation only.\n"
            "# Replace with real Transfermarkt data when available.\n"
        )
        with open(output_path, "w") as f:
            f.write(header_comment)
            result.to_csv(f, index=False)

    return result


def _season_end_date_from_code(season_code: object) -> pd.Timestamp:
    text = str(season_code)
    if len(text) == 4 and text.isdigit():
        end_year = 2000 + int(text[2:])
        return pd.Timestamp(year=end_year, month=5, day=31)
    return pd.Timestamp("1970-01-01")


def _build_proxy_player_id(row: pd.Series) -> str:
    player_name = normalize_person_name(row["player_name"])
    nation = normalize_country_name(row["nation"])
    born = int(row["born"]) if pd.notna(row["born"]) else 0
    return f"{player_name}|{born}|{nation}"


def _build_proxy_match_id(row: pd.Series) -> str:
    return (
        "fbref-season-proxy|"
        f"{row['season_id']}|{row['team_id']}|{row['player_id']}"
    )
