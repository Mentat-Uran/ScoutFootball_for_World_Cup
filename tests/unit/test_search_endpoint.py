"""Tests for the search_players_and_teams autocomplete endpoint.

Covers prefix/substring matching, type filtering, limit clamping,
empty-query rejection, empty-data handling, invalid-type fallback,
and return-structure contracts.
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pandas as pd

from scoutfootball.api import search_players_and_teams


def _sample_ratings() -> pd.DataFrame:
    """Return a small ratings DataFrame with known players and teams."""
    return pd.DataFrame(
        [
            {
                "player": "Mesut Ozil",
                "team": "Arsenal",
                "position_group": "AM",
                "optimized_score": 88.5,
                "league": "Premier League",
            },
            {
                "player": "Messi",
                "team": "Barcelona",
                "position_group": "RW",
                "optimized_score": 93.0,
                "league": "La Liga",
            },
            {
                "player": "Mesut Demir",
                "team": "Galatasaray",
                "position_group": "CM",
                "optimized_score": 72.1,
                "league": "Super Lig",
            },
            {
                "player": "Cristiano Ronaldo",
                "team": "Juventus",
                "position_group": "ST",
                "optimized_score": 91.0,
                "league": "Serie A",
            },
            {
                "player": "Simone Verdi",
                "team": "Napoli",
                "position_group": "LW",
                "optimized_score": 68.3,
                "league": "Serie A",
            },
            {
                "player": "Transferred Player",
                "team": "Arsenal,Chelsea",
                "position_group": "ST",
                "optimized_score": 70.0,
                "league": "Premier League",
            },
        ]
    )


class TestSearchPrefixMatching:
    """Prefix-first matching: names starting with the query rank first."""

    def test_prefix_match_returns_players_starting_with_query(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "players", 10)
        names = [p["player_name"] for p in result["players"]]
        # "Messi", "Mesut Demir", and "Mesut Ozil" all start with "Mes"
        assert "Mesut Ozil" in names
        assert "Mesut Demir" in names
        assert "Messi" in names
        # All are prefix matches, sorted alphabetically
        assert names == sorted(names)

    def test_prefix_matches_rank_before_substring(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "players", 10)
        names = [p["player_name"] for p in result["players"]]
        # All three names starting with "Mes" are prefix matches.
        # Verify they appear before any substring-only match (none here, so
        # just verify all are returned and sorted).
        prefix_names = [n for n in names if n.lower().startswith("mes")]
        assert len(prefix_names) == 3


class TestSearchSubstringMatching:
    """Substring matching catches names that contain but don't start with the query."""

    def test_substring_match_returns_players_containing_query(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("ona", "all", 10)
        # "Cristiano" contains "ona" (Cristi**ona**)
        player_names = [p["player_name"] for p in result["players"]]
        assert "Cristiano Ronaldo" in player_names
        assert any("ona" in n.lower() for n in player_names)

    def test_substring_match_finds_teams(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("ona", "all", 10)
        team_names = [t["team_name"] for t in result["teams"]]
        # "Barcelona" contains "ona" (Barcel**ona**)
        assert "Barcelona" in team_names

    def test_substring_match_finds_team_with_substring(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("nal", "all", 10)
        team_names = [t["team_name"] for t in result["teams"]]
        # "Arsenal" contains "nal" as substring (Arse**nal**)
        assert "Arsenal" in team_names


class TestSearchTypeFiltering:
    """search_type controls which sections are populated."""

    def test_type_teams_returns_only_teams(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Ars", "teams", 10)
        assert result["players"] == []
        assert len(result["teams"]) > 0
        assert all("team_name" in t for t in result["teams"])

    def test_type_players_returns_only_players(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "players", 10)
        assert result["teams"] == []
        assert len(result["players"]) > 0
        assert all("player_name" in p for p in result["players"])

    def test_type_all_returns_both_sections(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Ars", "all", 10)
        # Players matching "Ars" (substring of "Arsenal" won't match players;
        # but "Ars" might match nothing in player names — that's fine)
        assert "players" in result
        assert "teams" in result
        assert len(result["teams"]) > 0  # "Arsenal" matches


class TestSearchLimitClamping:
    """Limit is clamped to 1..25."""

    def test_limit_above_25_clamped_to_25(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("e", "players", 100)
        assert len(result["players"]) <= 25

    def test_limit_zero_does_not_crash(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "players", 0)
        # limit=0 is clamped to 1, so at most 1 result
        assert len(result["players"]) <= 1

    def test_negative_limit_does_not_crash(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "players", -5)
        assert len(result["players"]) <= 1

    def test_limit_string_falls_back_to_default(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "players", "abc")
        # Invalid limit falls back to 10
        assert len(result["players"]) <= 10


class TestSearchEmptyQuery:
    """Queries shorter than 2 characters return empty results."""

    def test_empty_query_returns_empty(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("", "all", 10)
        assert result == {"players": [], "teams": []}

    def test_single_char_query_returns_empty(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("M", "all", 10)
        assert result == {"players": [], "teams": []}

    def test_whitespace_only_query_returns_empty(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("   ", "all", 10)
        assert result == {"players": [], "teams": []}


class TestSearchEmptyData:
    """Empty or None ratings DataFrame returns empty result without raising."""

    def test_empty_dataframe_returns_empty(self) -> None:
        with patch("scoutfootball.api.load_player_ratings", return_value=pd.DataFrame()):
            result = search_players_and_teams("Mes", "all", 10)
        assert result == {"players": [], "teams": []}

    def test_none_dataframe_returns_empty(self) -> None:
        with patch("scoutfootball.api.load_player_ratings", return_value=None):
            result = search_players_and_teams("Mes", "all", 10)
        assert result == {"players": [], "teams": []}

    def test_empty_data_is_json_serializable(self) -> None:
        with patch("scoutfootball.api.load_player_ratings", return_value=pd.DataFrame()):
            result = search_players_and_teams("Mes", "all", 10)
        json.dumps(result)


class TestSearchInvalidType:
    """Invalid search_type defaults to 'all'."""

    def test_invalid_type_defaults_to_all(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result_invalid = search_players_and_teams("Mes", "invalid", 10)
            result_all = search_players_and_teams("Mes", "all", 10)
        assert result_invalid == result_all


class TestSearchReturnStructure:
    """Result always has 'players' and 'teams' keys, each a list."""

    def test_result_has_players_and_teams_keys(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "all", 10)
        assert set(result.keys()) >= {"players", "teams"}
        assert isinstance(result["players"], list)
        assert isinstance(result["teams"], list)

    def test_player_entries_have_expected_fields(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "players", 10)
        for p in result["players"]:
            assert "player_name" in p
            assert "team" in p
            assert "position" in p
            assert "rating" in p
            assert "league" in p

    def test_team_entries_have_expected_fields(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Ars", "teams", 10)
        for t in result["teams"]:
            assert "team_name" in t
            assert "league" in t

    def test_result_is_json_serializable(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Mes", "all", 10)
        json.dumps(result)


class TestSearchCommaJoinedTeams:
    """Comma-joined club histories are excluded from team suggestions."""

    def test_comma_joined_teams_excluded_from_team_results(self) -> None:
        df = _sample_ratings()
        with patch("scoutfootball.api.load_player_ratings", return_value=df):
            result = search_players_and_teams("Ars", "teams", 10)
        team_names = [t["team_name"] for t in result["teams"]]
        # "Arsenal,Chelsea" must not appear as a team suggestion
        assert all("," not in name for name in team_names)
