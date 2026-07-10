"""Identity enrichment for player-level action-value artifacts.

VAEP is aggregated from the internal action schema by StatsBomb identifiers.
Those identifiers are stable inside the source dataset, but the action rows do
not always carry display names or season metadata.  This module bridges VAEP
rows to the xT artifact using the exact ``player_id`` + ``team_id`` pair and
adds team names from the StatsBomb matches table.

Season metadata is deliberately exposed as context.  A VAEP row represents a
player-team career aggregate, so its value must not be described as belonging
to one season when the underlying matches span several seasons.
"""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from typing import Any

import pandas as pd

IDENTITY_SCHEMA = "scoutfootball.vaep-identity-coverage"
IDENTITY_SCHEMA_VERSION = "1.1.0"
IDENTITY_GRANULARITY = "player_team_career"


def _text(value: Any) -> str:
    """Return a trimmed string while treating pandas nulls as empty."""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def _identifier(value: Any) -> str:
    """Normalize identifiers read as either strings or integral floats."""
    text = _text(value)
    if text.endswith(".0"):
        integer = text[:-2]
        if integer.lstrip("-").isdigit():
            return integer
    return text


def _ordered_values(values: pd.Series) -> list[str]:
    """Return deterministic, de-duplicated non-empty values."""
    unique = {_text(value) for value in values}
    unique.discard("")
    return sorted(unique)


def _most_common(values: pd.Series) -> str:
    """Choose a deterministic display value from duplicate source rows."""
    candidates = [_text(value) for value in values]
    candidates = [value for value in candidates if value]
    if not candidates:
        return ""
    counts = Counter(candidates)
    return sorted(counts, key=lambda value: (-counts[value], value.casefold()))[0]


def build_xt_identity_context(xt_df: pd.DataFrame) -> pd.DataFrame:
    """Build one identity/context row per StatsBomb player-team pair."""
    columns = [
        "player_id",
        "team_id",
        "mapped_player_name",
        "season_context",
        "season_count",
        "competition_context",
        "competition_count",
    ]
    required = {"player_id", "team_id"}
    if xt_df.empty or not required.issubset(xt_df.columns):
        return pd.DataFrame(columns=columns)

    working = xt_df.copy()
    working["player_id"] = working["player_id"].map(_identifier)
    working["team_id"] = working["team_id"].map(_identifier)
    working = working[(working["player_id"] != "") & (working["team_id"] != "")]

    rows: list[dict[str, Any]] = []
    for (player_id, team_id), group in working.groupby(
        ["player_id", "team_id"], sort=True, dropna=False
    ):
        seasons = _ordered_values(group.get("season", pd.Series(dtype="object")))
        competitions = _ordered_values(
            group.get("competition", pd.Series(dtype="object"))
        )
        rows.append(
            {
                "player_id": player_id,
                "team_id": team_id,
                "mapped_player_name": _most_common(
                    group.get("player_name", pd.Series(dtype="object"))
                ),
                "season_context": " | ".join(seasons),
                "season_count": len(seasons),
                "competition_context": " | ".join(competitions),
                "competition_count": len(competitions),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def build_team_name_map(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Return one deterministic team name per StatsBomb team identifier."""
    columns = ["team_id", "mapped_team_name"]
    if matches_df.empty:
        return pd.DataFrame(columns=columns)

    parts: list[pd.DataFrame] = []
    for side in ("home", "away"):
        id_col = f"{side}_team_id"
        name_col = f"{side}_team_name"
        if {id_col, name_col}.issubset(matches_df.columns):
            part = matches_df[[id_col, name_col]].rename(
                columns={id_col: "team_id", name_col: "team_name"}
            )
            parts.append(part)
    if not parts:
        return pd.DataFrame(columns=columns)

    teams = pd.concat(parts, ignore_index=True)
    teams["team_id"] = teams["team_id"].map(_identifier)
    teams = teams[teams["team_id"] != ""]
    mapped = (
        teams.groupby("team_id", sort=True)["team_name"]
        .apply(_most_common)
        .rename("mapped_team_name")
        .reset_index()
    )
    return mapped[columns]


def attach_team_names(frame: pd.DataFrame, matches_df: pd.DataFrame) -> pd.DataFrame:
    """Fill a ``team_name`` column without overwriting existing names."""
    result = frame.copy()
    if result.empty or "team_id" not in result.columns:
        return result
    result["team_id"] = result["team_id"].map(_identifier)
    team_map = build_team_name_map(matches_df)
    if team_map.empty:
        if "team_name" not in result.columns:
            result["team_name"] = ""
        return result

    result = result.merge(team_map, on="team_id", how="left")
    existing = (
        result["team_name"].map(_text)
        if "team_name" in result.columns
        else pd.Series("", index=result.index, dtype="object")
    )
    result["team_name"] = existing.where(
        existing != "", result["mapped_team_name"].map(_text)
    )
    return result.drop(columns=["mapped_team_name"], errors="ignore")


def enrich_vaep_identities(
    vaep_df: pd.DataFrame,
    xt_df: pd.DataFrame,
    matches_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Add display identity and honest season context to VAEP rows.

    The original VAEP row count and ordering are preserved.  Unmapped rows are
    retained with an explicit status so callers can safely fall back to the
    source identifier.
    """
    result = vaep_df.copy()
    if result.empty:
        return result
    for column in ("player_id", "team_id"):
        if column not in result.columns:
            result[column] = ""
        result[column] = result[column].map(_identifier)

    context = build_xt_identity_context(xt_df)
    if not context.empty:
        result = result.merge(context, on=["player_id", "team_id"], how="left")
    else:
        for column in context.columns:
            if column not in {"player_id", "team_id"}:
                result[column] = "" if not column.endswith("_count") else 0

    existing_name = (
        result["player_name"].map(_text)
        if "player_name" in result.columns
        else pd.Series("", index=result.index, dtype="object")
    )
    mapped_name = result.get(
        "mapped_player_name", pd.Series("", index=result.index, dtype="object")
    ).map(_text)
    result["player_name"] = existing_name.where(existing_name != "", mapped_name)
    result["player_name_source"] = "unmapped"
    result.loc[mapped_name != "", "player_name_source"] = "xt_player_team_bridge"
    result.loc[existing_name != "", "player_name_source"] = "vaep_output"

    result = attach_team_names(result, matches_df if matches_df is not None else pd.DataFrame())
    result["team_name_source"] = result["team_name"].map(
        lambda value: "statsbomb_matches" if _text(value) else "unmapped"
    )
    result["season_context"] = result.get(
        "season_context", pd.Series("", index=result.index, dtype="object")
    ).map(_text)
    result["competition_context"] = result.get(
        "competition_context", pd.Series("", index=result.index, dtype="object")
    ).map(_text)
    for column in ("season_count", "competition_count"):
        result[column] = pd.to_numeric(result.get(column, 0), errors="coerce").fillna(0).astype(int)

    has_name = result["player_name"].map(bool)
    has_team = result["team_name"].map(bool)
    has_season = result["season_context"].map(bool)
    completed = has_name.astype(int) + has_team.astype(int) + has_season.astype(int)
    result["identity_status"] = "unmapped"
    result.loc[completed.between(1, 2), "identity_status"] = "partial"
    result.loc[completed == 3, "identity_status"] = "mapped"
    result["identity_mapped"] = result["identity_status"] == "mapped"
    result["identity_source"] = result["player_name_source"]

    return result.drop(columns=["mapped_player_name"], errors="ignore")


def build_identity_coverage_report(frame: pd.DataFrame) -> dict[str, Any]:
    """Summarize the identity fields present in the actual VAEP output."""
    total = len(frame)

    def count_nonempty(column: str) -> int:
        if column not in frame.columns:
            return 0
        return int(frame[column].map(_text).map(bool).sum())

    def rate(count: int) -> float:
        return round(count / total, 6) if total else 0.0

    statuses = (
        frame.get("identity_status", pd.Series("unmapped", index=frame.index))
        .fillna("unmapped")
        .astype(str)
    )
    mapped = int((statuses == "mapped").sum())
    partial = int((statuses == "partial").sum())
    unmapped = total - mapped - partial
    name_rows = count_nonempty("player_name")
    team_rows = count_nonempty("team_name")
    season_rows = count_nonempty("season_context")
    season_counts = pd.to_numeric(frame.get("season_count", 0), errors="coerce")
    if not isinstance(season_counts, pd.Series):
        season_counts = pd.Series(season_counts, index=frame.index)

    source_counts = (
        frame.get("identity_source", pd.Series("unmapped", index=frame.index))
        .fillna("unmapped")
        .astype(str)
        .value_counts()
        .sort_index()
        .to_dict()
    )
    return {
        "schema": IDENTITY_SCHEMA,
        "version": IDENTITY_SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "granularity": IDENTITY_GRANULARITY,
        "identity_source": "xt_player_team_bridge + statsbomb_matches",
        "total_rows": total,
        "mapped_rows": mapped,
        "partial_rows": partial,
        "unmapped_rows": unmapped,
        "coverage_rate": rate(mapped),
        "unmapped_rate": rate(unmapped),
        "player_name_rows": name_rows,
        "player_name_coverage_rate": rate(name_rows),
        "team_name_rows": team_rows,
        "team_name_coverage_rate": rate(team_rows),
        "season_context_rows": season_rows,
        "season_context_coverage_rate": rate(season_rows),
        "single_season_rows": int((season_counts == 1).sum()),
        "multi_season_rows": int((season_counts > 1).sum()),
        "source_counts": {key: int(value) for key, value in source_counts.items()},
        "season_context_semantics": (
            "Context only: VAEP values are aggregated across the player-team career row, "
            "not allocated to individual seasons."
        ),
    }
