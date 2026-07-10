"""Tests for the head-to-head match history and team form computation module.

Covers compute_head_to_head, compute_team_form, compute_h2h_summary, and the
aggregating get_head_to_head entry point. Uses real data from
combined_results.parquet (68,953 rows, 10 seasons, 20 leagues) plus a mocked
empty-data path to verify graceful degradation.
"""

from __future__ import annotations

import json
from unittest.mock import patch

import pandas as pd

from scoutfootball.app.data_loader import _ttl_cache
from scoutfootball.entities.normalize import normalize_team_name
from scoutfootball.head_to_head import (
    _MATCH_RESULTS_CACHE_KEY,
    compute_h2h_summary,
    compute_head_to_head,
    compute_team_form,
    get_head_to_head,
    load_match_results,
)

# ---------------------------------------------------------------------------
# compute_head_to_head
# ---------------------------------------------------------------------------

_H2H_KEYS = {
    "date",
    "season",
    "league",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
    "result",
    "queried_home_result",
}


class TestComputeHeadToHead:
    """compute_head_to_head returns recent meetings between two teams."""

    def test_arsenal_chelsea_returns_list_of_dicts_with_keys(self) -> None:
        results = compute_head_to_head("Arsenal", "Chelsea", limit=5)
        assert isinstance(results, list)
        assert len(results) > 0
        assert len(results) <= 5
        for row in results:
            assert isinstance(row, dict)
            assert _H2H_KEYS.issubset(row.keys())
            assert isinstance(row["home_goals"], int)
            assert isinstance(row["away_goals"], int)
            assert row["result"] in {"H", "D", "A", ""}
            # Only Arsenal and Chelsea may appear on either side
            assert {row["home_team"], row["away_team"]} <= {"Arsenal", "Chelsea"}

    def test_teams_with_no_h2h_history_returns_empty(self) -> None:
        # Two real Premier League teams from different eras won't share a match
        # in this dataset — use a pair that never meets in the data. Easiest
        # robust path: pick a real team against a non-existent one.
        results = compute_head_to_head("Arsenal", "Brighton", limit=10)
        # Brighton and Arsenal do meet in PL, so this should be non-empty.
        # Instead, test two teams that cannot meet:
        results = compute_head_to_head("Barcelona", "Bayern Munich", limit=10)
        # Barcelona (La Liga) and Bayern (Bundesliga) do not meet in league
        # play in combined_results.parquet, so this should be empty.
        assert results == []

    def test_nonexistent_teams_returns_empty(self) -> None:
        assert compute_head_to_head("FooBarUnited", "BazQuxCity") == []

    def test_alias_matching_man_city_resolves_to_manchester_city(self) -> None:
        # "Man City" is an alias in TEAM_NAME_ALIASES -> "Manchester City".
        # Chelsea vs Manchester City is a real PL fixture, so we expect hits.
        # The parquet stores both "Manchester City" and "Man City" as raw
        # team names across different seasons/leagues; the alias lookup maps
        # both to "Manchester City" for matching, but the returned row keeps
        # the raw parquet value. Accept either spelling on the result side.
        results = compute_head_to_head("Man City", "Chelsea", limit=5)
        assert len(results) > 0
        for row in results:
            teams = {row["home_team"], row["away_team"]}
            assert "Chelsea" in teams
            assert teams & {"Manchester City", "Man City"}
            assert row["queried_home_result"] in {"W", "D", "L"}
            match_home_is_query = normalize_team_name(row["home_team"]) == "Manchester City"
            expected = (
                "D"
                if row["result"] == "D"
                else "W"
                if (row["result"] == "H") == match_home_is_query
                else "L"
            )
            assert row["queried_home_result"] == expected

    def test_case_insensitivity(self) -> None:
        # normalize_team_name lowercases before alias lookup.
        lower = compute_head_to_head("arsenal", "chelsea", limit=3)
        proper = compute_head_to_head("Arsenal", "Chelsea", limit=3)
        assert len(lower) == len(proper)
        assert lower == proper

    def test_limit_parameter_caps_results(self) -> None:
        full = compute_head_to_head("Arsenal", "Chelsea", limit=100)
        capped = compute_head_to_head("Arsenal", "Chelsea", limit=2)
        assert len(capped) <= 2
        # The capped slice should be the first N of the full list (newest first)
        if len(full) > 2:
            assert capped == full[:2]

    def test_missing_source_result_is_derived_from_score(self) -> None:
        frame = pd.DataFrame(
            [
                {
                    "Date": pd.Timestamp("2026-01-03"),
                    "season": "2526",
                    "league": "Test League",
                    "HomeTeam": "Man City",
                    "AwayTeam": "Chelsea",
                    "FTHG": 2,
                    "FTAG": 1,
                    "FTR": None,
                    "_home_team_norm": "Manchester City",
                    "_away_team_norm": "Chelsea",
                }
            ]
        )
        with patch("scoutfootball.head_to_head.load_match_results", return_value=frame):
            results = compute_head_to_head("Manchester City", "Chelsea")
        assert results[0]["result"] == "H"
        assert results[0]["queried_home_result"] == "W"


# ---------------------------------------------------------------------------
# compute_team_form
# ---------------------------------------------------------------------------

_FORM_SUMMARY_KEYS = {
    "wins",
    "draws",
    "losses",
    "goals_for",
    "goals_against",
    "points",
    "streak",
}
_FORM_ROW_KEYS = {
    "date",
    "season",
    "league",
    "opponent",
    "venue",
    "goals_for",
    "goals_against",
    "result",
}


class TestComputeTeamForm:
    """compute_team_form returns a form list and aggregate summary."""

    def test_arsenal_form_returns_tuple_with_expected_shape(self) -> None:
        form_list, form_summary = compute_team_form("Arsenal", limit=10)
        assert isinstance(form_list, list)
        assert len(form_list) > 0
        assert len(form_list) <= 10
        assert isinstance(form_summary, dict)
        assert _FORM_SUMMARY_KEYS.issubset(form_summary.keys())

        for row in form_list:
            assert _FORM_ROW_KEYS.issubset(row.keys())
            assert row["venue"] in {"H", "A"}
            assert row["result"] in {"W", "D", "L"}

    def test_form_summary_aggregates_are_consistent(self) -> None:
        form_list, form_summary = compute_team_form("Liverpool", limit=10)
        assert form_summary["wins"] + form_summary["draws"] + form_summary["losses"] == len(
            form_list
        )
        assert form_summary["points"] == form_summary["wins"] * 3 + form_summary["draws"]
        assert isinstance(form_summary["streak"], list)
        assert len(form_summary["streak"]) <= 5

    def test_nonexistent_team_returns_empty_and_zero_summary(self) -> None:
        form_list, form_summary = compute_team_form("NoSuchTeamXYZ", limit=5)
        assert form_list == []
        assert form_summary == {
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "points": 0,
            "streak": [],
        }

    def test_limit_parameter_caps_form_list(self) -> None:
        capped, _ = compute_team_form("Chelsea", limit=3)
        assert len(capped) <= 3


# ---------------------------------------------------------------------------
# compute_h2h_summary
# ---------------------------------------------------------------------------

_H2H_SUMMARY_KEYS = {
    "total_meetings",
    "home_wins",
    "draws",
    "away_wins",
    "home_goals_avg",
    "away_goals_avg",
    "last_meeting_date",
}


class TestComputeH2HSummary:
    """compute_h2h_summary aggregates from the home_team's perspective."""

    def test_arsenal_chelsea_summary_has_expected_keys(self) -> None:
        summary = compute_h2h_summary("Arsenal", "Chelsea")
        assert _H2H_SUMMARY_KEYS.issubset(summary.keys())
        assert summary["total_meetings"] > 0
        assert (
            summary["home_wins"] + summary["draws"] + summary["away_wins"]
            == summary["total_meetings"]
        )
        assert isinstance(summary["home_goals_avg"], float)
        assert isinstance(summary["away_goals_avg"], float)
        assert summary["last_meeting_date"] is not None

    def test_no_h2h_history_returns_zeroed_summary(self) -> None:
        summary = compute_h2h_summary("Barcelona", "Bayern Munich")
        assert summary == {
            "total_meetings": 0,
            "home_wins": 0,
            "draws": 0,
            "away_wins": 0,
            "home_goals_avg": 0.0,
            "away_goals_avg": 0.0,
            "last_meeting_date": None,
        }


# ---------------------------------------------------------------------------
# get_head_to_head (aggregation)
# ---------------------------------------------------------------------------

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


class TestGetHeadToHead:
    """get_head_to_head aggregates H2H, form, summary, and data coverage."""

    def test_full_aggregation_has_all_top_level_keys(self) -> None:
        result = get_head_to_head("Arsenal", "Chelsea", limit=5, form_limit=5)
        assert _TOP_LEVEL_KEYS.issubset(result.keys())
        assert result["home_team"] == "Arsenal"
        assert result["away_team"] == "Chelsea"
        assert isinstance(result["head_to_head"], list)
        assert isinstance(result["home_form"], list)
        assert isinstance(result["away_form"], list)
        assert isinstance(result["home_form_summary"], dict)
        assert isinstance(result["away_form_summary"], dict)
        assert isinstance(result["summary"], dict)
        assert isinstance(result["data_coverage"], dict)
        assert result["data_coverage"]["source"] == "Football-Data"
        assert result["data_coverage"]["total_matches_scanned"] > 0

    def test_nonexistent_teams_returns_valid_empty_structure(self) -> None:
        result = get_head_to_head("NoSuchTeamA", "NoSuchTeamB")
        assert _TOP_LEVEL_KEYS.issubset(result.keys())
        assert result["head_to_head"] == []
        assert result["home_form"] == []
        assert result["away_form"] == []
        assert result["summary"]["total_meetings"] == 0
        assert result["summary"]["last_meeting_date"] is None

    def test_result_is_json_serializable(self) -> None:
        result = get_head_to_head("Arsenal", "Chelsea", limit=3, form_limit=3)
        # No numpy types / NaN should leak — json.dumps must succeed.
        json.dumps(result)


# ---------------------------------------------------------------------------
# Empty data handling via mocked load_match_results
# ---------------------------------------------------------------------------


class TestEmptyDataHandling:
    """When load_match_results returns an empty DataFrame, no function raises."""

    @patch("scoutfootball.head_to_head.load_match_results")
    def test_compute_head_to_head_empty(self, mock_load: patch) -> None:
        mock_load.return_value = pd.DataFrame()
        assert compute_head_to_head("Arsenal", "Chelsea") == []

    @patch("scoutfootball.head_to_head.load_match_results")
    def test_compute_team_form_empty(self, mock_load: patch) -> None:
        mock_load.return_value = pd.DataFrame()
        form_list, form_summary = compute_team_form("Arsenal")
        assert form_list == []
        assert form_summary["wins"] == 0
        assert form_summary["points"] == 0
        assert form_summary["streak"] == []

    @patch("scoutfootball.head_to_head.load_match_results")
    def test_compute_h2h_summary_empty(self, mock_load: patch) -> None:
        mock_load.return_value = pd.DataFrame()
        summary = compute_h2h_summary("Arsenal", "Chelsea")
        assert summary["total_meetings"] == 0
        assert summary["home_goals_avg"] == 0.0
        assert summary["last_meeting_date"] is None

    @patch("scoutfootball.head_to_head.load_match_results")
    def test_get_head_to_head_empty(self, mock_load: patch) -> None:
        mock_load.return_value = pd.DataFrame()
        result = get_head_to_head("Arsenal", "Chelsea")
        assert result["head_to_head"] == []
        assert result["summary"]["total_meetings"] == 0
        assert result["data_coverage"]["total_matches_scanned"] == 0
        assert result["data_coverage"]["seasons_covered"] == []

    @patch("scoutfootball.head_to_head.load_match_results")
    def test_get_head_to_head_empty_is_json_serializable(self, mock_load: patch) -> None:
        mock_load.return_value = pd.DataFrame()
        json.dumps(get_head_to_head("Arsenal", "Chelsea"))


# ---------------------------------------------------------------------------
# Sanity: load_match_results returns a non-empty DataFrame in this environment
# ---------------------------------------------------------------------------


def test_load_match_results_returns_nonempty_dataframe() -> None:
    """Guard: the real combined_results.parquet must be present for these tests."""
    df = load_match_results()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "HomeTeam" in df.columns
    assert "AwayTeam" in df.columns
    assert "FTHG" in df.columns
    assert "FTAG" in df.columns
    assert "FTR" in df.columns


def test_load_match_results_uses_ttl_cache_and_force_refresh() -> None:
    raw = pd.DataFrame(
        [
            {
                "Date": "03/01/26",
                "HomeTeam": "Arsenal",
                "AwayTeam": "Chelsea",
                "FTHG": 1,
                "FTAG": 0,
                "FTR": "H",
            }
        ]
    )
    _ttl_cache.invalidate(_MATCH_RESULTS_CACHE_KEY)
    try:
        with patch(
            "scoutfootball.head_to_head._safe_read_parquet",
            return_value=raw,
        ) as mock_read:
            first = load_match_results()
            second = load_match_results()
            refreshed = load_match_results(force_refresh=True)
        assert first is second
        assert refreshed is not first
        assert mock_read.call_count == 2
        assert first.loc[0, "_home_team_norm"] == "Arsenal"
    finally:
        _ttl_cache.invalidate(_MATCH_RESULTS_CACHE_KEY)
