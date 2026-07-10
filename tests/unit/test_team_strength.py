"""Tests for the team strength aggregation API."""

from __future__ import annotations

import pandas as pd
import pytest

from scoutfootball.api import (
    _broad_position,
    get_team_strength,
)

# ── _broad_position ────────────────────────────────────────────────


@pytest.mark.parametrize(
    "pos,expected",
    [
        ("GK", "GK"),
        ("CB", "DEF"),
        ("FB", "DEF"),
        ("LB", "DEF"),
        ("RB", "DEF"),
        ("DM", "MID"),
        ("CM", "MID"),
        ("AM", "MID"),
        ("W", "ATT"),
        ("ST", "ATT"),
        ("CF", "ATT"),
        ("RW", "ATT"),
        ("LW", "ATT"),
        (None, "UNK"),
        ("", "UNK"),
        ("XYZ", "UNK"),
        ("gk", "GK"),
        ("cm", "MID"),
    ],
)
def test_broad_position_mapping(pos, expected):
    assert _broad_position(pos) == expected


# ── get_team_strength with synthetic data ─────────────────────────


@pytest.fixture
def _mock_ratings(monkeypatch):
    """Provide a synthetic ratings DataFrame for testing."""
    df = pd.DataFrame({
        "player_name": [
            "Player A", "Player B", "Player C", "Player D", "Player E",
            "Player F", "Player G", "Player H",
        ],
        "team": [
            "Team Alpha", "Team Alpha", "Team Alpha", "Team Alpha",
            "Team Beta", "Team Beta", "Team Beta", "Team Beta",
        ],
        "league": [
            "Premier League", "Premier League", "Premier League", "Premier League",
            "La Liga", "La Liga", "La Liga", "La Liga",
        ],
        "season": ["2526"] * 8,
        "position_group": ["GK", "CB", "CM", "ST", "GK", "FB", "AM", "W"],
        "optimized_score": [55.0, 60.0, 65.0, 70.0, 50.0, 55.0, 58.0, 62.0],
        "minutes": [900, 1800, 2700, 1800, 900, 1800, 2700, 1800],
        "confidence_level": ["HIGH", "HIGH", "HIGH", "HIGH", "MEDIUM", "HIGH", "HIGH", "HIGH"],
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


def test_team_strength_basic(_mock_ratings):
    """Test basic team strength aggregation."""
    result = get_team_strength()
    assert result["count"] == 2
    assert len(result["teams"]) == 2


def test_team_strength_sorted_by_rating(_mock_ratings):
    """Teams should be sorted by overall rating descending."""
    result = get_team_strength()
    teams = result["teams"]
    assert teams[0]["overall_rating"] >= teams[1]["overall_rating"]
    # Team Alpha has higher-rated players overall
    assert teams[0]["team"] == "Team Alpha"


def test_team_strength_position_groups(_mock_ratings):
    """Each team should have position group breakdowns."""
    result = get_team_strength()
    for team in result["teams"]:
        assert "position_groups" in team
        pos_groups = team["position_groups"]
        # Should have GK, DEF, MID, ATT groups
        assert "GK" in pos_groups
        # Each group should have rating, player_count, avg_minutes
        for pg in pos_groups.values():
            assert "rating" in pg
            assert "player_count" in pg
            assert "avg_minutes" in pg


def test_team_strength_top_players(_mock_ratings):
    """Each team should have top players list."""
    result = get_team_strength()
    for team in result["teams"]:
        assert "top_players" in team
        assert len(team["top_players"]) <= 5
        for player in team["top_players"]:
            assert "name" in player
            assert "rating" in player
            assert "position" in player
            assert "broad_pos" in player
            assert "minutes" in player
            assert "confidence" in player


def test_team_strength_squad_size(_mock_ratings):
    """Squad size should match the number of players per team."""
    result = get_team_strength()
    for team in result["teams"]:
        assert team["squad_size"] == 4  # 4 players per team in mock


def test_team_strength_league_filter(_mock_ratings):
    """League filter should narrow results."""
    result = get_team_strength(league="La Liga")
    assert result["count"] == 1
    assert result["teams"][0]["team"] == "Team Beta"
    assert result["teams"][0]["league"] == "La Liga"


def test_team_strength_limit(_mock_ratings):
    """Limit should cap the number of teams returned."""
    result = get_team_strength(limit=1)
    assert result["count"] == 1
    assert len(result["teams"]) == 1


def test_team_strength_minutes_weighted(_mock_ratings):
    """Overall rating should be minutes-weighted, not simple average."""
    result = get_team_strength()
    alpha = next(t for t in result["teams"] if t["team"] == "Team Alpha")
    # Manual calculation: (55*900 + 60*1800 + 65*2700 + 70*1800) / (900+1800+2700+1800)
    expected = (55.0 * 900 + 60.0 * 1800 + 65.0 * 2700 + 70.0 * 1800) / 7200
    assert abs(alpha["overall_rating"] - round(expected, 2)) < 0.1


def test_team_strength_confidence_distribution(_mock_ratings):
    """Confidence distribution should be present."""
    result = get_team_strength()
    for team in result["teams"]:
        assert "confidence_distribution" in team
        conf = team["confidence_distribution"]
        assert isinstance(conf, dict)


def test_team_strength_excludes_comma_teams(monkeypatch):
    """Players with comma-joined team names should be excluded."""
    df = pd.DataFrame({
        "player_name": ["Player A", "Player B"],
        "team": ["Team Alpha", "Team Alpha, Team Beta"],
        "league": ["Premier League", "Premier League"],
        "season": ["2526", "2526"],
        "position_group": ["CM", "ST"],
        "optimized_score": [65.0, 70.0],
        "minutes": [1800, 1800],
        "confidence_level": ["HIGH", "HIGH"],
    })
    monkeypatch.setattr(
        "scoutfootball.api.load_player_ratings",
        lambda **kwargs: df.copy(),
    )
    result = get_team_strength()
    assert result["count"] == 1
    assert result["teams"][0]["squad_size"] == 1


def test_team_strength_empty_data(monkeypatch):
    """Empty ratings should return empty result."""
    monkeypatch.setattr(
        "scoutfootball.api.load_player_ratings",
        lambda **kwargs: pd.DataFrame(),
    )
    result = get_team_strength()
    assert result["count"] == 0
    assert result["teams"] == []


def test_team_strength_no_team_column(monkeypatch):
    """Missing team column should return empty result."""
    df = pd.DataFrame({
        "player_name": ["Player A"],
        "optimized_score": [65.0],
    })
    monkeypatch.setattr(
        "scoutfootball.api.load_player_ratings",
        lambda **kwargs: df.copy(),
    )
    result = get_team_strength()
    assert result["count"] == 0


def test_team_strength_fallback_to_rating_column(monkeypatch):
    """Should work with 'rating' column if 'optimized_score' is missing."""
    df = pd.DataFrame({
        "player_name": ["Player A", "Player B"],
        "team": ["Team Alpha", "Team Alpha"],
        "league": ["Premier League", "Premier League"],
        "season": ["2526", "2526"],
        "position_group": ["CM", "ST"],
        "rating": [65.0, 70.0],
        "minutes": [1800, 1800],
        "confidence_level": ["HIGH", "HIGH"],
    })
    monkeypatch.setattr(
        "scoutfootball.api.load_player_ratings",
        lambda **kwargs: df.copy(),
    )
    result = get_team_strength()
    assert result["count"] == 1
    assert result["teams"][0]["squad_size"] == 2


def test_team_strength_total_minutes(_mock_ratings):
    """Total minutes should be the sum of all player minutes."""
    result = get_team_strength()
    alpha = next(t for t in result["teams"] if t["team"] == "Team Alpha")
    assert alpha["total_minutes"] == 900 + 1800 + 2700 + 1800
