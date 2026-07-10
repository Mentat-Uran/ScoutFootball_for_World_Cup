"""Integration tests for ScoutFootball FastAPI endpoints."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def client():
    """Create a TestClient for the FastAPI app (module-scoped for speed)."""
    from scoutfootball.api_server import create_app

    app = create_app()
    return TestClient(app)


def test_artifacts_endpoint(client: TestClient):
    """/artifacts should return 200 with artifact summary."""
    response = client.get("/artifacts")
    assert response.status_code == 200
    data = response.json()
    assert "artifacts" in data or "data_source_label" in data


def test_ratings_snapshots_endpoint(client: TestClient):
    """/ratings/snapshots should return 200."""
    response = client.get("/ratings/snapshots")
    assert response.status_code == 200


def test_predictions_meta_endpoint(client: TestClient):
    """/predictions/meta should return 200."""
    response = client.get("/predictions/meta")
    assert response.status_code == 200


def test_action_values_endpoint(client: TestClient):
    """/action-values should return 200."""
    response = client.get("/action-values")
    assert response.status_code == 200


def test_health_endpoint(client: TestClient):
    """/health should return 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_teams_strength_endpoint(client: TestClient):
    """/teams/strength should return 200 with team strength data."""
    response = client.get("/teams/strength")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "teams" in data
    assert isinstance(data["teams"], list)
    if data["teams"]:
        team = data["teams"][0]
        assert "team" in team
        assert "overall_rating" in team
        assert "squad_size" in team
        assert "position_groups" in team
        assert "top_players" in team


def test_teams_strength_with_limit(client: TestClient):
    """/teams/strength should respect limit parameter."""
    response = client.get("/teams/strength?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] <= 5
