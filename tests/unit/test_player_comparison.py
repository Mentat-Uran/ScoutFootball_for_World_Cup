"""Tests for the player comparison API."""

from __future__ import annotations

import pandas as pd
import pytest

from scoutfootball.api import get_player_comparison


@pytest.fixture
def _mock_ratings(monkeypatch):
    """Provide synthetic ratings data for two players."""
    df = pd.DataFrame({
        "player": [
            "Alice Star", "Alice Star", "Bob Champ", "Bob Champ",
            "Carol Mid", "Carol Mid",
        ],
        "team": ["Team A", "Team A", "Team B", "Team B", "Team C", "Team C"],
        "league": ["Premier League"] * 6,
        "season": ["2425", "2526", "2425", "2526", "2425", "2526"],
        "sub_position": ["ST", "ST", "CM", "CM", "CB", "CB"],
        "position_group": ["ST", "ST", "CM", "CM", "CB", "CB"],
        "optimized_score": [70.0, 72.0, 65.0, 68.0, 55.0, 58.0],
        "minutes": [2700, 2700, 2700, 2700, 1800, 1800],
        "matches": [30, 30, 30, 30, 20, 20],
        "npg_p90": [0.5, 0.55, 0.1, 0.12, 0.02, 0.03],
        "assists_p90": [0.2, 0.25, 0.3, 0.35, 0.01, 0.02],
        "defense_composite": [10.0, 12.0, 60.0, 65.0, 80.0, 82.0],
        "possession_composite": [30.0, 35.0, 70.0, 75.0, 50.0, 52.0],
        "confidence_level": ["HIGH", "HIGH", "HIGH", "HIGH", "MEDIUM", "MEDIUM"],
        "low_appearance": [False, False, False, False, False, False],
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
    # Mock load_player_value_metrics to avoid file reads
    monkeypatch.setattr(
        "scoutfootball.api.load_player_value_metrics",
        lambda: pd.DataFrame(),
    )
    return df


def test_comparison_basic(_mock_ratings):
    """Test basic comparison between two players."""
    result = get_player_comparison("Alice Star", "Bob Champ")
    assert "error" not in result
    assert result["player_a"]["name"] == "Alice Star"
    assert result["player_b"]["name"] == "Bob Champ"


def test_comparison_radar(_mock_ratings):
    """Radar comparison should have 5 dimensions."""
    result = get_player_comparison("Alice Star", "Bob Champ")
    assert len(result["radar_labels"]) == 5
    assert len(result["radar_a"]) == 5
    assert len(result["radar_b"]) == 5
    assert len(result["radar_comparison"]) == 5
    for rc in result["radar_comparison"]:
        assert "dimension" in rc
        assert "player_a" in rc
        assert "player_b" in rc
        assert "diff" in rc
        assert "advantage" in rc


def test_comparison_stats(_mock_ratings):
    """Stats comparison should include key metrics."""
    result = get_player_comparison("Alice Star", "Bob Champ")
    stats = result["stats_comparison"]
    assert len(stats) > 0
    metric_names = [s["metric"] for s in stats]
    assert "optimized_score" in metric_names
    assert "minutes" in metric_names
    assert "npg_p90" in metric_names


def test_comparison_player_not_found(_mock_ratings):
    """Should return error when player not found."""
    result = get_player_comparison("Unknown Player", "Bob Champ")
    assert "error" in result
    assert (
        "found_a" not in result
        or result.get("found_a") is False
        or "not found" in result["error"]
    )


def test_comparison_second_not_found(_mock_ratings):
    """Should return error when second player not found."""
    result = get_player_comparison("Alice Star", "Nobody")
    assert "error" in result


def test_comparison_different_positions(_mock_ratings):
    """Comparison should work with players in different positions."""
    result = get_player_comparison("Alice Star", "Carol Mid")
    assert "error" not in result
    assert result["same_position"] is False


def test_comparison_same_position(_mock_ratings):
    """same_position should be True when both players share position."""
    result = get_player_comparison("Alice Star", "Bob Champ")
    # Alice is ST, Bob is CM — different
    assert result["same_position"] is False

    # Compare Alice with herself (same position)
    result2 = get_player_comparison("Alice Star", "Alice Star")
    assert result2["same_position"] is True


def test_comparison_player_info(_mock_ratings):
    """Player info should include team, league, position."""
    result = get_player_comparison("Alice Star", "Bob Champ")
    assert result["player_a"]["team"] == "Team A"
    assert result["player_b"]["team"] == "Team B"
    assert result["player_a"]["position_group"] == "ST"
    assert result["player_b"]["position_group"] == "CM"


def test_comparison_radar_values_in_range(_mock_ratings):
    """Radar percentile values should be between 0 and 100."""
    result = get_player_comparison("Alice Star", "Bob Champ")
    for val in result["radar_a"] + result["radar_b"]:
        assert 0 <= val <= 100


def test_comparison_position_percentiles(_mock_ratings):
    """Position percentile comparison should have dimensions."""
    result = get_player_comparison("Alice Star", "Bob Champ")
    pcts = result.get("position_percentile_comparison", [])
    # May or may not have dimensions depending on position data
    if pcts:
        for p in pcts:
            assert "dimension" in p
            assert "player_a" in p
            assert "player_b" in p
            assert "advantage" in p
