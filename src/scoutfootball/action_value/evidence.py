"""Match-level xT evidence derived from the tracked StatsBomb event sample.

The repository does not ship the full action-level dataset. This module keeps
that boundary explicit and builds a small, reproducible player -> match ->
action evidence snapshot from ``events_sample.parquet`` only.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from scoutfootball.action_value.spadl_adapter import convert_all_events
from scoutfootball.action_value.xt import compute_xt_values
from scoutfootball.app.data_loader import _MISSING, _ttl_cache
from scoutfootball.config import PlatformSettings

logger = logging.getLogger(__name__)

_CACHE_KEY = "action_value.evidence_snapshot"
_SAMPLE_RELATIVE_PATH = Path("statsbomb_open/events_sample.parquet")
_CORE_ACTION_TYPES = ("pass", "carry", "shot")
_ACTION_TYPE_ORDER = {name: index for index, name in enumerate(_CORE_ACTION_TYPES)}
_ZONE_ORDER = {
    "defensive_third": 0,
    "middle_third": 1,
    "final_third": 2,
    "penalty_area": 3,
}
_TIME_ORDER = {
    "0-15": 0,
    "16-30": 1,
    "31-45+": 2,
    "46-60": 3,
    "61-75": 4,
    "76-90+": 5,
}
_SCOPE_NOTE = (
    "Tracked 3-match StatsBomb Open Data sample only. "
    "The xT grid is recomputed from this sample, so these values are not "
    "directly comparable or additive to the full aggregate xT artifact. "
    "This is match evidence, not full competition coverage."
)


def _id_string(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip()
    try:
        number = float(text)
        return str(int(number)) if number.is_integer() else text
    except (TypeError, ValueError):
        return text


def _destination_zone(value: object) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        x = 0.0
    if x >= 83.3:
        return "penalty_area"
    if x >= 66.7:
        return "final_third"
    if x >= 33.3:
        return "middle_third"
    return "defensive_third"


def _time_bucket(value: object) -> str:
    try:
        minute = int(value)
    except (TypeError, ValueError):
        minute = 0
    if minute <= 15:
        return "0-15"
    if minute <= 30:
        return "16-30"
    if minute <= 45:
        return "31-45+"
    if minute <= 60:
        return "46-60"
    if minute <= 75:
        return "61-75"
    return "76-90+"


def _safe_round(value: object, digits: int = 6) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return round(number, digits) if pd.notna(number) else 0.0


def _breakdown(frame: pd.DataFrame, column: str, order: dict[str, int]) -> list[dict]:
    if frame.empty or column not in frame.columns:
        return []
    rows: list[dict] = []
    for label, group in frame.groupby(column, dropna=False):
        key = str(label or "unknown")
        rows.append({
            "key": key,
            "n_actions": int(len(group)),
            "xt_total": _safe_round(group["xt_delta"].sum()),
            "positive_xt": _safe_round(group["_positive_xt"].sum()),
            "negative_xt": _safe_round(group["_negative_xt"].sum()),
            "success_rate": _safe_round(group["_is_success"].mean(), 4),
        })
    return sorted(rows, key=lambda row: (order.get(row["key"], 999), row["key"]))


def _action_split(frame: pd.DataFrame) -> dict[str, int | float]:
    result: dict[str, int | float] = {}
    for action_type in _CORE_ACTION_TYPES:
        subset = frame[frame["action_type"] == action_type]
        result[f"n_{action_type}"] = int(len(subset))
        result[f"xt_{action_type}"] = _safe_round(subset["xt_delta"].sum())
    return result


def _empty_snapshot(status: str = "no_data") -> dict[str, Any]:
    return {
        "status": status,
        "schema_version": "1.0",
        "coverage": {
            "match_count": 0,
            "player_count": 0,
            "action_count": 0,
            "source": "StatsBomb Open Data",
            "source_coverage": "sample",
            "xt_grid_scope": "sample_recomputed",
            "aggregate_comparability": "not_directly_comparable",
            "scope_note": _SCOPE_NOTE,
        },
        "player_index": [],
        "players": {},
    }


def build_action_value_evidence_snapshot(
    valued_actions: pd.DataFrame,
    events_df: pd.DataFrame,
) -> dict[str, Any]:
    """Build the versioned evidence snapshot from valued actions and events."""
    required = {
        "match_id",
        "team_id",
        "player_id",
        "provider_action_id",
        "period",
        "action_type",
        "result",
        "minute",
        "second",
        "start_x",
        "start_y",
        "end_x",
        "end_y",
        "xt_delta",
    }
    if valued_actions.empty or events_df.empty or required.difference(valued_actions.columns):
        return _empty_snapshot()

    actions = valued_actions.copy()
    actions["match_id"] = actions["match_id"].map(_id_string)
    actions["team_id"] = actions["team_id"].map(_id_string)
    actions["player_id"] = actions["player_id"].map(_id_string)
    actions = actions[actions["player_id"] != ""].copy()
    if actions.empty:
        return _empty_snapshot()

    events = events_df.copy()
    events["_match_id"] = events.get("match_id", pd.Series(index=events.index)).map(_id_string)
    events["_team_id"] = events.get("team_id", pd.Series(index=events.index)).map(_id_string)
    events["_player_id"] = events.get("player_id", pd.Series(index=events.index)).map(_id_string)

    player_names = (
        events.loc[events.get("player_name", "").fillna("") != "", ["_player_id", "player_name"]]
        .drop_duplicates("_player_id")
        .set_index("_player_id")["player_name"]
        .astype(str)
        .to_dict()
        if "player_name" in events.columns
        else {}
    )
    team_rows = (
        events.loc[
            events.get("team_name", "").fillna("") != "",
            ["_match_id", "_team_id", "team_name"],
        ]
        .drop_duplicates(["_match_id", "_team_id"])
        if "team_name" in events.columns
        else pd.DataFrame(columns=["_match_id", "_team_id", "team_name"])
    )
    team_names = {
        (str(match_id), str(team_id)): str(team_name)
        for match_id, team_id, team_name in team_rows.itertuples(index=False, name=None)
    }
    match_teams: dict[str, list[str]] = {}
    for match_id, group in team_rows.groupby("_match_id", sort=False):
        match_teams[str(match_id)] = list(dict.fromkeys(group["team_name"].astype(str)))

    actions["player_name"] = actions["player_id"].map(player_names).fillna("")
    actions["team_name"] = [
        team_names.get((match_id, team_id), f"Team ID {team_id}" if team_id else "Unknown team")
        for match_id, team_id in zip(actions["match_id"], actions["team_id"], strict=False)
    ]
    actions["destination_zone"] = actions["end_x"].map(_destination_zone)
    actions["time_bucket"] = actions["minute"].map(_time_bucket)
    actions["_positive_xt"] = actions["xt_delta"].clip(lower=0.0)
    actions["_negative_xt"] = actions["xt_delta"].clip(upper=0.0)
    actions["_is_success"] = (actions["result"] == "success").astype(int)

    coverage = {
        "match_count": int(actions["match_id"].nunique()),
        "player_count": int(actions["player_id"].nunique()),
        "action_count": int(len(actions)),
        "source": "StatsBomb Open Data",
        "source_coverage": "sample",
        "xt_grid_scope": "sample_recomputed",
        "aggregate_comparability": "not_directly_comparable",
        "scope_note": _SCOPE_NOTE,
        "match_ids": sorted(actions["match_id"].unique().tolist()),
    }
    players: dict[str, dict[str, Any]] = {}
    player_index: list[dict[str, Any]] = []

    for player_id, player_actions in actions.groupby("player_id", sort=False):
        player_name = str(player_actions["player_name"].iloc[0] or f"Player ID {player_id}")
        matches: list[dict[str, Any]] = []
        for match_id, match_actions in player_actions.groupby("match_id", sort=False):
            team_name = str(match_actions["team_name"].iloc[0])
            teams = match_teams.get(str(match_id), [team_name])
            opponents = [team for team in teams if team != team_name]
            matches.append({
                "match_id": str(match_id),
                "match_label": " · ".join(teams) or f"Sample match {match_id}",
                "team_name": team_name,
                "opponents": opponents,
                "n_actions": int(len(match_actions)),
                "xt_total": _safe_round(match_actions["xt_delta"].sum()),
                "positive_xt": _safe_round(match_actions["_positive_xt"].sum()),
                "negative_xt": _safe_round(match_actions["_negative_xt"].sum()),
                **_action_split(match_actions),
            })
        matches.sort(key=lambda row: row["match_id"])

        top_actions = (
            player_actions.sort_values("xt_delta", ascending=False)
            .head(12)
        )
        top_action_rows = [{
            "match_id": str(row.match_id),
            "match_label": " · ".join(match_teams.get(str(row.match_id), []))
            or f"Sample match {row.match_id}",
            "provider_action_id": str(row.provider_action_id),
            "period": int(row.period),
            "minute": int(row.minute),
            "second": int(row.second),
            "action_type": str(row.action_type),
            "result": str(row.result),
            "xt_delta": _safe_round(row.xt_delta),
            "start_x": _safe_round(row.start_x, 2),
            "start_y": _safe_round(row.start_y, 2),
            "end_x": _safe_round(row.end_x, 2),
            "end_y": _safe_round(row.end_y, 2),
            "destination_zone": str(row.destination_zone),
        } for row in top_actions.itertuples(index=False)]

        teams = list(dict.fromkeys(player_actions["team_name"].astype(str)))
        detail = {
            "status": "ok",
            "schema_version": "1.0",
            "player_id": str(player_id),
            "player_name": player_name,
            "teams": teams,
            "n_actions": int(len(player_actions)),
            "n_matches": int(player_actions["match_id"].nunique()),
            "xt_total": _safe_round(player_actions["xt_delta"].sum()),
            "positive_xt": _safe_round(player_actions["_positive_xt"].sum()),
            "negative_xt": _safe_round(player_actions["_negative_xt"].sum()),
            "matches": matches,
            "action_types": _breakdown(player_actions, "action_type", _ACTION_TYPE_ORDER),
            "zones": _breakdown(player_actions, "destination_zone", _ZONE_ORDER),
            "time_buckets": _breakdown(player_actions, "time_bucket", _TIME_ORDER),
            "top_actions": top_action_rows,
            "coverage": coverage,
        }
        players[str(player_id)] = detail
        player_index.append({
            "player_id": str(player_id),
            "player_name": player_name,
            "teams": teams,
            "n_matches": detail["n_matches"],
            "n_actions": detail["n_actions"],
            "xt_total": detail["xt_total"],
            "positive_xt": detail["positive_xt"],
        })

    player_index.sort(key=lambda row: (-float(row["positive_xt"]), row["player_name"]))
    return {
        "status": "ok",
        "schema_version": "1.0",
        "coverage": coverage,
        "player_index": player_index,
        "players": players,
    }


def load_action_value_evidence_snapshot(force_refresh: bool = False) -> dict[str, Any]:
    """Load and cache the tracked sample evidence snapshot."""
    if not force_refresh:
        cached = _ttl_cache.get(_CACHE_KEY)
        if cached is not _MISSING:
            return cached

    settings = PlatformSettings.from_root()
    events_path = settings.raw_root / _SAMPLE_RELATIVE_PATH
    if not events_path.exists():
        result = _empty_snapshot()
        _ttl_cache.set(_CACHE_KEY, result)
        return result

    try:
        events = pd.read_parquet(events_path)
        actions = convert_all_events(events_path)
        _, valued_actions = compute_xt_values(actions)
        result = build_action_value_evidence_snapshot(valued_actions, events)
    except Exception:
        logger.warning("Failed to build action-value evidence sample", exc_info=True)
        result = _empty_snapshot(status="error")
    _ttl_cache.set(_CACHE_KEY, result)
    return result


def get_action_value_evidence_index() -> dict[str, Any]:
    """Return sample coverage and the set of players with match evidence."""
    snapshot = load_action_value_evidence_snapshot()
    return {
        "status": snapshot["status"],
        "schema_version": snapshot["schema_version"],
        "coverage": snapshot["coverage"],
        "player_index": snapshot["player_index"],
        "available_player_ids": [row["player_id"] for row in snapshot["player_index"]],
    }


def get_action_value_evidence_snapshot() -> dict[str, Any]:
    """Return the complete snapshot for the tracked static frontend export."""
    return load_action_value_evidence_snapshot()


def get_action_value_evidence(player_id: str) -> dict[str, Any]:
    """Return match/action evidence for one player ID."""
    snapshot = load_action_value_evidence_snapshot()
    normalized_id = _id_string(player_id)
    detail = snapshot["players"].get(normalized_id)
    if detail:
        return detail
    return {
        "status": "not_found" if snapshot["status"] == "ok" else snapshot["status"],
        "schema_version": snapshot["schema_version"],
        "player_id": normalized_id,
        "matches": [],
        "action_types": [],
        "zones": [],
        "time_buckets": [],
        "top_actions": [],
        "coverage": snapshot["coverage"],
    }
