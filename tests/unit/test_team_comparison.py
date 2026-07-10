"""Tests for the team comparison API."""

from __future__ import annotations

import pandas as pd
import pytest

from scoutfootball.api import get_team_comparison


@pytest.fixture
def _mock_ratings(monkeypatch):
    """Provide synthetic ratings data for two teams."""
    df = pd.DataFrame({
        "player_name": [
            "GK A", "DEF A1", "DEF A2", "MID A1", "MID A2", "ST A1",
            "GK B", "DEF B1", "DEF B2", "MID B1", "MID B2", "ST B1",
        ],
        "team": [
            "Team Alpha", "Team Alpha", "Team Alpha", "Team Alpha", "Team Alpha", "Team Alpha",
            "Team Beta", "Team Beta", "Team Beta", "Team Beta", "Team Beta", "Team Beta",
        ],
        "league": ["Premier League"] * 12,
        "season": ["2526"] * 12,
        "position_group": ["GK", "CB", "FB", "CM", "AM", "ST", "GK", "CB", "FB", "CM", "AM", "ST"],
        "optimized_score": [55, 60, 58, 65, 68, 72, 50, 55, 53, 60, 62, 65],
        "minutes": [900, 1800, 1800, 2700, 2700, 2700, 900, 1800, 1800, 2700, 2700, 2700],
        "confidence_level": ["HIGH"] * 12,
    })

    def _load(**kwargs):
        result = df.copy()
        league = kwargs.get("league")
        season = kwargs.get("season")
        if league and "league" in result.columns:
            result = result[result["league"] == league]
        if season and "season" in result.columns:
            result = result[result["season"] == season]
        return result.reset_index(drop=True)

    monkeypatch.setattr("scoutfootball.api.load_player_ratings", _load)
    return df


def test_comparison_basic(_mock_ratings):
    """Test basic comparison between two teams."""
    result = get_team_comparison("Team Alpha", "Team Beta")
    assert "error" not in result
    assert result["team_a"]["name"] == "Team Alpha"
    assert result["team_b"]["name"] == "Team Beta"


def test_comparison_overall_diff(_mock_ratings):
    """Overall diff should be positive when team A is stronger."""
    result = get_team_comparison("Team Alpha", "Team Beta")
    assert result["overall_diff"] > 0
    assert result["overall_advantage"] == "a"


def test_comparison_reversed(_mock_ratings):
    """When B is stronger, advantage should be 'b'."""
    result = get_team_comparison("Team Beta", "Team Alpha")
    assert result["overall_diff"] < 0
    assert result["overall_advantage"] == "b"


def test_comparison_position_groups(_mock_ratings):
    """Position group comparison should have 4 groups."""
    result = get_team_comparison("Team Alpha", "Team Beta")
    pos = result["position_group_comparison"]
    assert len(pos) == 4
    groups = [p["group"] for p in pos]
    assert groups == ["GK", "DEF", "MID", "ATT"]


def test_comparison_position_group_values(_mock_ratings):
    """Position group ratings should differ between teams."""
    result = get_team_comparison("Team Alpha", "Team Beta")
    for p in result["position_group_comparison"]:
        assert "rating_a" in p
        assert "rating_b" in p
        assert "diff" in p
        assert "advantage" in p
        assert "players_a" in p
        assert "players_b" in p


def test_comparison_radar(_mock_ratings):
    """Radar should have 5 dimensions (GK, DEF, MID, ATT, Overall)."""
    result = get_team_comparison("Team Alpha", "Team Beta")
    assert len(result["radar_labels"]) == 5
    assert len(result["radar_a"]) == 5
    assert len(result["radar_b"]) == 5


def test_comparison_top_players(_mock_ratings):
    """Top players comparison should have entries."""
    result = get_team_comparison("Team Alpha", "Team Beta")
    top = result["top_players_comparison"]
    assert len(top) > 0
    for entry in top:
        assert "player_a" in entry
        assert "player_b" in entry


def test_comparison_team_not_found(_mock_ratings):
    """Should return error when team not found."""
    result = get_team_comparison("Unknown Team", "Team Beta")
    assert "error" in result


def test_comparison_second_not_found(_mock_ratings):
    """Should return error when second team not found."""
    result = get_team_comparison("Team Alpha", "Nobody FC")
    assert "error" in result


def test_comparison_case_insensitive(_mock_ratings):
    """Team matching should be case-insensitive."""
    result = get_team_comparison("team alpha", "TEAM BETA")
    assert "error" not in result
    assert result["team_a"]["name"] == "Team Alpha"
    assert result["team_b"]["name"] == "Team Beta"


def test_comparison_partial_match(_mock_ratings):
    """Should match partial team names."""
    result = get_team_comparison("Alpha", "Beta")
    assert "error" not in result


def test_comparison_team_info(_mock_ratings):
    """Team info should include league, squad_size, etc."""
    result = get_team_comparison("Team Alpha", "Team Beta")
    assert result["team_a"]["league"] == "Premier League"
    assert result["team_a"]["squad_size"] == 6
    assert result["team_b"]["squad_size"] == 6
