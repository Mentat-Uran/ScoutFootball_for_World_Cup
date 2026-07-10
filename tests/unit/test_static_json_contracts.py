"""Contract checks for frontend/data/ static JSON files.

Validates that key static JSON files:
- Are valid JSON (parseable by json.load)
- Have a dict or list top-level structure
- Contain at least one expected status or data field

These tests are intentionally coarse — they check structural integrity,
not detailed field values, to avoid brittleness from normal schema evolution.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_FRONTEND_DATA = _PROJECT_ROOT / "frontend" / "data"

# Each entry: (filename, required_top_level_keys)
# required_top_level_keys: at least one of these must be present in the dict.
# If the file is a list, we only check it's non-empty.
_STATIC_FILES: list[tuple[str, list[str]]] = [
    ("action_values.json", ["status", "count", "metrics", "players"]),
    ("action_value_evidence.json", ["status", "schema_version", "coverage", "players"]),
    ("artifacts.json", ["artifacts", "data_source_label", "license_attribution"]),
    ("ratings.json", ["count", "players"]),
    ("review_queue.json", ["count", "players"]),
    ("watchlist.json", ["count", "players"]),
    ("shortlist.json", ["count", "players"]),
    ("predictions_meta.json", ["status", "model_type", "available_models"]),
    ("predictions_calibration.json", []),
    ("predictions_default.json", ["home_team", "away_team", "home_win", "draw", "away_win"]),
    ("ratings_meta.json", ["model_meta", "league_metrics"]),
    ("model_runs.json", ["runs"]),
    ("value_summary.json", ["status", "sample_count", "fairness_distribution"]),
    ("health.json", []),
    ("players_list.json", ["player_count", "players"]),
    ("teams.json", ["teams"]),
    ("h2h_pairs.json", ["schema_version", "pairs", "team_aliases"]),
]


def _read_static_json(filename: str) -> object:
    path = _FRONTEND_DATA / filename
    if not path.exists():
        pytest.skip(f"{filename} not found in frontend/data/")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class TestStaticJsonValid:
    """Every static JSON file must be valid JSON with a dict or list top-level."""

    @pytest.mark.parametrize("filename,_", [(f, ks) for f, ks in _STATIC_FILES])
    def test_parseable_as_json(self, filename: str, _: list[str]) -> None:
        data = _read_static_json(filename)
        assert isinstance(data, (dict, list)), f"{filename} top-level must be dict or list"

    @pytest.mark.parametrize("filename,_", [(f, ks) for f, ks in _STATIC_FILES])
    def test_not_empty(self, filename: str, _: list[str]) -> None:
        data = _read_static_json(filename)
        if isinstance(data, dict):
            assert len(data) > 0, f"{filename} is an empty dict"
        else:
            assert len(data) > 0, f"{filename} is an empty list"


class TestStaticJsonRequiredKeys:
    """Dict-typed static files must contain at least one required key."""

    @pytest.mark.parametrize(
        "filename,required_keys",
        [(f, ks) for f, ks in _STATIC_FILES if ks],
    )
    def test_has_required_keys(self, filename: str, required_keys: list[str]) -> None:
        data = _read_static_json(filename)
        if not isinstance(data, dict):
            pytest.skip(f"{filename} is a list, not a dict — key check N/A")
        has_at_least_one = any(k in data for k in required_keys)
        assert has_at_least_one, (
            f"{filename} missing all required keys {required_keys}; "
            f"actual keys: {list(data.keys())[:10]}"
        )


class TestStaticJsonNoNullTopLevel:
    """Top-level dict values should not all be null (indicates broken export)."""

    @pytest.mark.parametrize("filename,_", [(f, ks) for f, ks in _STATIC_FILES])
    def test_not_all_null_values(self, filename: str, _: list[str]) -> None:
        data = _read_static_json(filename)
        if not isinstance(data, dict):
            return
        non_null_count = sum(1 for v in data.values() if v is not None)
        assert non_null_count > 0, f"{filename} has all null values — likely broken export"


def test_h2h_static_pairs_and_alias_contract() -> None:
    data = _read_static_json("h2h_pairs.json")
    assert isinstance(data, dict)
    assert data["schema_version"] == "1.0"
    assert len(data["pairs"]) == 40
    assert "Arsenal_Manchester_City" in data["pairs"]
    assert data["team_aliases"]["man_city"] == "Manchester_City"
    assert data["team_aliases"]["manchester_utd"] == "Manchester_United"
    assert all(
        row["queried_home_result"] in {"W", "D", "L"}
        for pair in data["pairs"].values()
        for row in pair["head_to_head"]
    )


def test_action_value_evidence_static_contract() -> None:
    data = _read_static_json("action_value_evidence.json")
    assert isinstance(data, dict)
    assert data["status"] == "ok"
    assert data["schema_version"] == "1.0"
    assert data["coverage"]["match_count"] == 3
    assert data["coverage"]["source_coverage"] == "sample"
    assert data["coverage"]["xt_grid_scope"] == "sample_recomputed"
    assert data["coverage"]["aggregate_comparability"] == "not_directly_comparable"
    assert "5503" in data["players"]
    assert len(data["players"]["5503"]["matches"]) == 3
