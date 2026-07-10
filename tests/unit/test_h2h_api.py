"""Tests for the head-to-head API wrapper and FastAPI endpoint.

Covers:
- scoutfootball.api.get_head_to_head wrapper returns a valid, JSON-safe dict
- GET /predictions/{home_team}/{away_team}/h2h returns 200 with correct shape
- limit and form_limit query parameters are honored
- Non-existent teams return 200 with an empty structure (not 500)
- Responses are JSON-serializable (no numpy types or NaN leak through)
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from scoutfootball.api import get_head_to_head
from scoutfootball.api_server import create_app

_TOP_LEVEL_KEYS = {
    "home_team",
    "away_team",
    "head_to_head",
    "home_form",
    "home_form_summary",
    "away_form",
    "away_form_summary",
    "summary",
    "data_coverage",
}


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Create a FastAPI TestClient (module-scoped for speed)."""
    return TestClient(create_app())


# ---------------------------------------------------------------------------
# Wrapper function (scoutfootball.api.get_head_to_head)
# ---------------------------------------------------------------------------


class TestApiWrapper:
    """The api.get_head_to_head wrapper returns JSON-safe dicts."""

    def test_wrapper_returns_dict_with_all_keys(self) -> None:
        result = get_head_to_head("Arsenal", "Chelsea", limit=5, form_limit=5)
        assert isinstance(result, dict)
        assert _TOP_LEVEL_KEYS.issubset(result.keys())
        assert result["home_team"] == "Arsenal"
        assert result["away_team"] == "Chelsea"

    def test_wrapper_result_is_json_serializable(self) -> None:
        result = get_head_to_head("Arsenal", "Chelsea", limit=3, form_limit=3)
        json.dumps(result)

    def test_wrapper_with_nonexistent_teams(self) -> None:
        result = get_head_to_head("NoSuchTeamA", "NoSuchTeamB")
        assert _TOP_LEVEL_KEYS.issubset(result.keys())
        assert result["head_to_head"] == []
        assert result["summary"]["total_meetings"] == 0

    def test_wrapper_swallows_compute_failure(self) -> None:
        """If the underlying compute layer raises, the wrapper returns the
        empty fallback structure instead of propagating the exception."""
        with patch(
            "scoutfootball.api._compute_head_to_head",
            side_effect=RuntimeError("boom"),
        ):
            result = get_head_to_head("Arsenal", "Chelsea")
        assert _TOP_LEVEL_KEYS.issubset(result.keys())
        assert result["head_to_head"] == []
        assert result["summary"]["total_meetings"] == 0
        json.dumps(result)


# ---------------------------------------------------------------------------
# FastAPI endpoint
# ---------------------------------------------------------------------------


class TestH2HEndpoint:
    """GET /predictions/{home_team}/{away_team}/h2h."""

    def test_endpoint_returns_200_with_structure(self, client: TestClient) -> None:
        response = client.get("/predictions/Arsenal/Chelsea/h2h")
        assert response.status_code == 200
        data = response.json()
        assert _TOP_LEVEL_KEYS.issubset(data.keys())
        assert data["home_team"] == "Arsenal"
        assert data["away_team"] == "Chelsea"
        assert isinstance(data["head_to_head"], list)
        assert isinstance(data["home_form"], list)
        assert isinstance(data["summary"], dict)

    def test_endpoint_with_limit_and_form_limit(self, client: TestClient) -> None:
        response = client.get(
            "/predictions/Arsenal/Chelsea/h2h?limit=2&form_limit=3",
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["head_to_head"]) <= 2
        assert len(data["home_form"]) <= 3
        assert len(data["away_form"]) <= 3

    def test_endpoint_nonexistent_teams_returns_200_not_500(
        self, client: TestClient,
    ) -> None:
        response = client.get("/predictions/NoSuchTeamA/NoSuchTeamB/h2h")
        assert response.status_code == 200
        data = response.json()
        assert data["head_to_head"] == []
        assert data["summary"]["total_meetings"] == 0

    def test_endpoint_response_is_json_serializable(
        self, client: TestClient,
    ) -> None:
        """The response body is already JSON (from TestClient), but we also
        re-dumps to confirm no NaN/numpy artifacts survive serialization."""
        response = client.get("/predictions/Liverpool/Manchester%20City/h2h")
        assert response.status_code == 200
        data = response.json()
        json.dumps(data)

    def test_endpoint_h2h_rows_have_expected_fields(
        self, client: TestClient,
    ) -> None:
        response = client.get("/predictions/Arsenal/Chelsea/h2h?limit=3")
        assert response.status_code == 200
        data = response.json()
        if data["head_to_head"]:
            row = data["head_to_head"][0]
            assert {"date", "home_team", "away_team", "home_goals", "away_goals"}.issubset(
                row.keys(),
            )
            assert row["queried_home_result"] in {"W", "D", "L"}

    @pytest.mark.parametrize(
        "query",
        ["limit=0", "limit=101", "form_limit=0", "form_limit=51"],
    )
    def test_endpoint_rejects_out_of_range_limits(
        self,
        client: TestClient,
        query: str,
    ) -> None:
        response = client.get(f"/predictions/Arsenal/Chelsea/h2h?{query}")
        assert response.status_code == 422
