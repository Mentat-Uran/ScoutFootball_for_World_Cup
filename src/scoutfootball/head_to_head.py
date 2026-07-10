"""Head-to-head match history and team form computation from Football-Data results."""
from __future__ import annotations

import logging
import warnings

import pandas as pd

from scoutfootball.app.data_loader import _MISSING, _safe_read_parquet, _ttl_cache
from scoutfootball.entities.normalize import normalize_team_name

logger = logging.getLogger(__name__)

_COMBINED_RESULTS_REL = "raw/football_data/combined_results.parquet"
_MATCH_RESULTS_CACHE_KEY = "head_to_head.match_results"
_REQUIRED_COLUMNS = {"Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"}


def load_match_results(force_refresh: bool = False) -> pd.DataFrame:
    """Load combined_results.parquet, parse dates, and sort descending.

    Returns an empty DataFrame if the file is missing or corrupt.
    """
    if not force_refresh:
        cached = _ttl_cache.get(_MATCH_RESULTS_CACHE_KEY)
        if cached is not _MISSING:
            return cached

    df = _safe_read_parquet(_COMBINED_RESULTS_REL)
    if df is None or df.empty:
        result = pd.DataFrame()
        _ttl_cache.set(_MATCH_RESULTS_CACHE_KEY, result)
        return result
    missing_columns = _REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        logger.warning(
            "combined_results.parquet is missing required columns: %s",
            sorted(missing_columns),
        )
        result = pd.DataFrame()
        _ttl_cache.set(_MATCH_RESULTS_CACHE_KEY, result)
        return result
    df = df.copy()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["_home_team_norm"] = df["HomeTeam"].map(_normalize_team)
    df["_away_team_norm"] = df["AwayTeam"].map(_normalize_team)
    df = df.sort_values("Date", ascending=False, na_position="last").reset_index(drop=True)
    _ttl_cache.set(_MATCH_RESULTS_CACHE_KEY, df)
    return df


def _normalize_team(name: str) -> str:
    """Normalize a team name for matching against Football-Data records."""
    return normalize_team_name(name)


def _to_int(value) -> int:
    """Safely convert a numpy/pandas scalar to a native int (0 on failure)."""
    try:
        if pd.isna(value):
            return 0
        return int(value)
    except (TypeError, ValueError):
        return 0


def _iso_date(value) -> str | None:
    """Return ISO date string or None for NaT/NaN."""
    if value is None or pd.isna(value):
        return None
    try:
        ts = pd.Timestamp(value)
        if pd.isna(ts):
            return None
        return ts.date().isoformat()
    except (TypeError, ValueError):
        return None


def _bounded_limit(value: int, maximum: int) -> int:
    """Clamp internal callers to a safe positive row limit."""
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = 1
    return max(1, min(parsed, maximum))


def _match_result(ftr: object, home_goals: int, away_goals: int) -> str:
    """Return H/D/A, deriving it from the score when the source is incomplete."""
    result = "" if pd.isna(ftr) else str(ftr).upper()
    if result in {"H", "D", "A"}:
        return result
    if home_goals == away_goals:
        return "D"
    return "H" if home_goals > away_goals else "A"


def compute_head_to_head(home_team: str, away_team: str, limit: int = 10) -> list[dict]:
    """Return recent head-to-head matches between two teams (newest first)."""
    df = load_match_results()
    if df.empty:
        return []
    home_norm = _normalize_team(home_team)
    away_norm = _normalize_team(away_team)
    if not home_norm or not away_norm:
        return []

    limit = _bounded_limit(limit, 100)
    home_home = df["_home_team_norm"]
    away_away = df["_away_team_norm"]
    mask = (
        (home_home == home_norm) & (away_away == away_norm)
    ) | (
        (home_home == away_norm) & (away_away == home_norm)
    )
    mask &= df["FTHG"].notna() & df["FTAG"].notna()
    matches = df.loc[mask].head(limit)
    results: list[dict] = []
    for _, row in matches.iterrows():
        home_goals = _to_int(row.get("FTHG"))
        away_goals = _to_int(row.get("FTAG"))
        result = _match_result(row.get("FTR"), home_goals, away_goals)
        queried_home_is_match_home = row.get("_home_team_norm") == home_norm
        queried_home_result = (
            "D"
            if result == "D"
            else "W"
            if (result == "H") == queried_home_is_match_home
            else "L"
        )
        results.append({
            "date": _iso_date(row.get("Date")),
            "season": str(row.get("season", "")) if not pd.isna(row.get("season")) else "",
            "league": str(row.get("league", "")) if not pd.isna(row.get("league")) else "",
            "home_team": str(row.get("HomeTeam", "")) if not pd.isna(row.get("HomeTeam")) else "",
            "away_team": str(row.get("AwayTeam", "")) if not pd.isna(row.get("AwayTeam")) else "",
            "home_goals": home_goals,
            "away_goals": away_goals,
            "result": result,
            "queried_home_result": queried_home_result,
        })
    return results


def compute_team_form(team: str, limit: int = 10) -> tuple[list[dict], dict]:
    """Return a team's recent form list and aggregate summary."""
    empty_summary = {
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "goals_for": 0,
        "goals_against": 0,
        "points": 0,
        "streak": [],
    }
    df = load_match_results()
    if df.empty:
        return [], empty_summary
    team_norm = _normalize_team(team)
    if not team_norm:
        return [], empty_summary

    limit = _bounded_limit(limit, 50)
    home_norm = df["_home_team_norm"]
    away_norm = df["_away_team_norm"]
    mask = (home_norm == team_norm) | (away_norm == team_norm)
    mask &= df["FTHG"].notna() & df["FTAG"].notna()
    matches = df.loc[mask].head(limit)

    form_list: list[dict] = []
    wins = draws = losses = 0
    goals_for_total = goals_against_total = 0
    streak: list[str] = []

    for _, row in matches.iterrows():
        is_home = _normalize_team(row.get("HomeTeam")) == team_norm
        hg = _to_int(row.get("FTHG"))
        ag = _to_int(row.get("FTAG"))
        ftr = _match_result(row.get("FTR"), hg, ag)

        if is_home:
            goals_for, goals_against = hg, ag
            opponent = str(row.get("AwayTeam", "")) if not pd.isna(row.get("AwayTeam")) else ""
            venue = "H"
        else:
            goals_for, goals_against = ag, hg
            opponent = str(row.get("HomeTeam", "")) if not pd.isna(row.get("HomeTeam")) else ""
            venue = "A"

        if ftr == "H":
            result = "W" if is_home else "L"
        elif ftr == "A":
            result = "L" if is_home else "W"
        elif ftr == "D":
            result = "D"
        else:
            if goals_for == goals_against:
                result = "D"
            elif goals_for > goals_against:
                result = "W"
            else:
                result = "L"

        if result == "W":
            wins += 1
        elif result == "D":
            draws += 1
        else:
            losses += 1
        goals_for_total += goals_for
        goals_against_total += goals_against
        if len(streak) < 5:
            streak.append(result)

        form_list.append({
            "date": _iso_date(row.get("Date")),
            "season": str(row.get("season", "")) if not pd.isna(row.get("season")) else "",
            "league": str(row.get("league", "")) if not pd.isna(row.get("league")) else "",
            "opponent": opponent,
            "venue": venue,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "result": result,
        })

    summary = {
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goals_for": goals_for_total,
        "goals_against": goals_against_total,
        "points": wins * 3 + draws,
        "streak": streak,
    }
    return form_list, summary


def compute_h2h_summary(home_team: str, away_team: str) -> dict:
    """Aggregate head-to-head summary from the home_team's perspective."""
    empty = {
        "total_meetings": 0,
        "home_wins": 0,
        "draws": 0,
        "away_wins": 0,
        "home_goals_avg": 0.0,
        "away_goals_avg": 0.0,
        "last_meeting_date": None,
    }
    matches = compute_head_to_head(home_team, away_team, limit=10000)
    if not matches:
        return empty

    home_norm = _normalize_team(home_team)
    home_wins = away_wins = draws = 0
    home_goals_total = away_goals_total = 0
    last_meeting_date = None

    for match in matches:
        hg = match["home_goals"]
        ag = match["away_goals"]
        queried_home_result = match["queried_home_result"]

        if _normalize_team(match["home_team"]) == home_norm:
            home_goals_total += hg
            away_goals_total += ag
        else:
            home_goals_total += ag
            away_goals_total += hg

        if queried_home_result == "W":
            home_wins += 1
        elif queried_home_result == "D":
            draws += 1
        else:
            away_wins += 1

        match_date = match.get("date")
        if match_date:
            if last_meeting_date is None or match_date > last_meeting_date:
                last_meeting_date = match_date

    total = len(matches)
    return {
        "total_meetings": total,
        "home_wins": home_wins,
        "draws": draws,
        "away_wins": away_wins,
        "home_goals_avg": round(home_goals_total / total, 2) if total else 0.0,
        "away_goals_avg": round(away_goals_total / total, 2) if total else 0.0,
        "last_meeting_date": last_meeting_date,
    }


def get_head_to_head(
    home_team: str,
    away_team: str,
    limit: int = 10,
    form_limit: int = 10,
) -> dict:
    """Aggregate head-to-head, form, and summary for a matchup."""
    try:
        h2h = compute_head_to_head(home_team, away_team, limit=limit)
        home_form, home_form_summary = compute_team_form(home_team, limit=form_limit)
        away_form, away_form_summary = compute_team_form(away_team, limit=form_limit)
        summary = compute_h2h_summary(home_team, away_team)

        df = load_match_results()
        if df.empty:
            seasons_covered: list[str] = []
            total_scanned = 0
        else:
            seasons_covered = sorted(
                str(s) for s in df["season"].dropna().unique()
            ) if "season" in df.columns else []
            total_scanned = int(len(df))
    except Exception:
        logger.warning("get_head_to_head failed", exc_info=True)
        h2h = []
        home_form, home_form_summary = [], {
            "wins": 0, "draws": 0, "losses": 0,
            "goals_for": 0, "goals_against": 0, "points": 0, "streak": [],
        }
        away_form, away_form_summary = [], {
            "wins": 0, "draws": 0, "losses": 0,
            "goals_for": 0, "goals_against": 0, "points": 0, "streak": [],
        }
        summary = {
            "total_meetings": 0, "home_wins": 0, "draws": 0, "away_wins": 0,
            "home_goals_avg": 0.0, "away_goals_avg": 0.0, "last_meeting_date": None,
        }
        seasons_covered = []
        total_scanned = 0

    return {
        "home_team": home_team,
        "away_team": away_team,
        "head_to_head": h2h,
        "home_form": home_form,
        "home_form_summary": home_form_summary,
        "away_form": away_form,
        "away_form_summary": away_form_summary,
        "summary": summary,
        "data_coverage": {
            "seasons_covered": seasons_covered,
            "total_matches_scanned": total_scanned,
            "source": "Football-Data",
        },
    }
