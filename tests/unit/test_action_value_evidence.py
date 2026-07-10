"""Tests for match-level action-value evidence and its API contract."""

from __future__ import annotations

import json

import pandas as pd
from fastapi.testclient import TestClient

from scoutfootball.action_value.evidence import (
    build_action_value_evidence_snapshot,
)
from scoutfootball.action_value.xt import compute_xt_values
from scoutfootball.api_server import create_app


def _valued_actions() -> pd.DataFrame:
    rows = [
        (1, "pass", "success", 10, 20, 40.0, 50.0, 72.0, 50.0, 0.08),
        (2, "carry", "success", 18, 5, 45.0, 48.0, 70.0, 45.0, 0.05),
        (3, "shot", "failure", 31, 1, 88.0, 50.0, 100.0, 50.0, -0.03),
        (4, "pass", "failure", 47, 22, 55.0, 30.0, 25.0, 20.0, -0.02),
        (5, "pass", "success", 76, 0, 68.0, 25.0, 86.0, 35.0, 0.04),
    ]
    return pd.DataFrame([
        {
            "action_id": action_id,
            "provider_action_id": f"event-{action_id}",
            "match_id": "100",
            "team_id": "10",
            "player_id": "7",
            "period": 1 if minute <= 45 else 2,
            "minute": minute,
            "second": second,
            "action_type": action_type,
            "result": result,
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "xt_delta": xt_delta,
        }
        for (
            action_id,
            action_type,
            result,
            minute,
            second,
            start_x,
            start_y,
            end_x,
            end_y,
            xt_delta,
        ) in rows
    ])


def _events() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "match_id": 100,
            "team_id": 10,
            "team_name": "Alpha",
            "player_id": 7,
            "player_name": "Ada",
        },
        {
            "match_id": 100,
            "team_id": 20,
            "team_name": "Beta",
            "player_id": 8,
            "player_name": "Bea",
        },
    ])


def test_build_evidence_snapshot_has_match_action_zone_and_time_splits() -> None:
    snapshot = build_action_value_evidence_snapshot(_valued_actions(), _events())
    assert snapshot["status"] == "ok"
    assert snapshot["coverage"]["match_count"] == 1
    assert snapshot["coverage"]["player_count"] == 1
    assert snapshot["coverage"]["source_coverage"] == "sample"
    assert snapshot["coverage"]["xt_grid_scope"] == "sample_recomputed"
    assert snapshot["coverage"]["aggregate_comparability"] == "not_directly_comparable"

    detail = snapshot["players"]["7"]
    assert detail["player_name"] == "Ada"
    assert detail["matches"][0]["match_label"] == "Alpha · Beta"
    assert detail["matches"][0]["n_pass"] == 3
    assert detail["matches"][0]["n_carry"] == 1
    assert detail["matches"][0]["n_shot"] == 1
    assert [row["key"] for row in detail["action_types"][:3]] == ["pass", "carry", "shot"]
    assert {row["key"] for row in detail["zones"]} == {
        "defensive_third",
        "final_third",
        "penalty_area",
    }
    assert {row["key"] for row in detail["time_buckets"]} == {
        "0-15",
        "16-30",
        "31-45+",
        "46-60",
        "76-90+",
    }
    assert detail["top_actions"][0]["provider_action_id"] == "event-1"
    json.dumps(snapshot)


def test_build_evidence_snapshot_empty_is_explicit() -> None:
    snapshot = build_action_value_evidence_snapshot(pd.DataFrame(), pd.DataFrame())
    assert snapshot["status"] == "no_data"
    assert snapshot["players"] == {}
    assert snapshot["coverage"]["match_count"] == 0


def test_compute_xt_values_is_in_memory_and_does_not_mutate_input() -> None:
    actions = _valued_actions().drop(columns="xt_delta")
    original_columns = actions.columns.tolist()
    grid, valued = compute_xt_values(actions)
    assert grid.shape == (12, 16)
    assert "xt_delta" in valued.columns
    assert len(valued) == len(actions)
    assert actions.columns.tolist() == original_columns


def test_evidence_api_index_detail_and_missing_player() -> None:
    client = TestClient(create_app())
    index = client.get("/action-values/evidence")
    assert index.status_code == 200
    index_data = index.json()
    assert index_data["status"] == "ok"
    assert index_data["coverage"]["match_count"] == 3
    assert "5503" in index_data["available_player_ids"]

    detail = client.get("/action-values/evidence/5503")
    assert detail.status_code == 200
    detail_data = detail.json()
    assert detail_data["player_name"] == "Lionel Andrés Messi Cuccittini"
    assert len(detail_data["matches"]) == 3
    assert {row["key"] for row in detail_data["action_types"]} >= {"pass", "carry", "shot"}

    missing = client.get("/action-values/evidence/not-a-player")
    assert missing.status_code == 200
    assert missing.json()["status"] == "not_found"
