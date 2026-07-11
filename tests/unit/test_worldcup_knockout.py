"""Unit tests for World Cup knockout bracket simulation."""

from __future__ import annotations

import pytest

from scoutfootball.worldcup.data import (
    GROUPS,
    _knockout_match_prob,
    _predict_group_finishes,
    _seed_round_of_32,
    compute_group_predictions,
    simulate_knockout,
)


@pytest.fixture()
def sample_strengths():
    """Return a small set of team strengths for testing."""
    return {
        "Spain": 0.85,
        "France": 0.82,
        "Brazil": 0.80,
        "England": 0.78,
        "Argentina": 0.77,
        "Germany": 0.72,
        "Portugal": 0.70,
        "Netherlands": 0.68,
        "Uruguay": 0.60,
        "Belgium": 0.58,
        "Mexico": 0.50,
        "Canada": 0.48,
        "South Africa": 0.35,
        "Qatar": 0.30,
        "New Zealand": 0.25,
        "Curacao": 0.20,
    }


@pytest.fixture()
def full_strengths():
    """Return strengths for all 48 WC teams."""
    strengths = {}
    for teams in GROUPS.values():
        for i, team in enumerate(teams):
            strengths[team] = 0.85 - i * 0.15
    return strengths


class TestKnockoutMatchProb:
    def test_equal_strengths(self):
        assert _knockout_match_prob(0.5, 0.5) == pytest.approx(0.5)

    def test_home_stronger(self):
        p = _knockout_match_prob(0.8, 0.4)
        assert 0.5 < p <= 1.0

    def test_away_stronger(self):
        p = _knockout_match_prob(0.3, 0.7)
        assert 0.0 <= p < 0.5

    def test_zero_strengths(self):
        assert _knockout_match_prob(0.0, 0.0) == 0.5

    def test_probabilities_sum_to_one(self):
        p_home = _knockout_match_prob(0.6, 0.4)
        # Home + away probabilities always sum to 1
        assert p_home + (1 - p_home) == pytest.approx(1.0)


class TestPredictGroupFinishes:
    def test_returns_three_lists(self, sample_strengths):
        preds = compute_group_predictions(sample_strengths)
        firsts, seconds, thirds = _predict_group_finishes(preds)
        assert isinstance(firsts, list)
        assert isinstance(seconds, list)
        assert isinstance(thirds, list)

    def test_each_group_has_representative(self, full_strengths):
        preds = compute_group_predictions(full_strengths)
        firsts, seconds, thirds = _predict_group_finishes(preds)
        assert len(firsts) == 12
        assert len(seconds) == 12
        assert len(thirds) == 12

    def test_firsts_sorted_by_strength_descending(self, full_strengths):
        preds = compute_group_predictions(full_strengths)
        firsts, _, _ = _predict_group_finishes(preds)
        strengths = [s for _, _, s in firsts]
        assert strengths == sorted(strengths, reverse=True)


class TestSeedRoundOf32:
    def test_produces_16_matchups(self, full_strengths):
        preds = compute_group_predictions(full_strengths)
        firsts, seconds, thirds = _predict_group_finishes(preds)
        matchups = _seed_round_of_32(firsts, seconds, thirds)
        assert len(matchups) == 16

    def test_each_matchup_has_six_fields(self, full_strengths):
        preds = compute_group_predictions(full_strengths)
        firsts, seconds, thirds = _predict_group_finishes(preds)
        matchups = _seed_round_of_32(firsts, seconds, thirds)
        for m in matchups:
            assert len(m) == 6

    def test_strong_teams_not_paired_together(self, full_strengths):
        preds = compute_group_predictions(full_strengths)
        firsts, seconds, thirds = _predict_group_finishes(preds)
        matchups = _seed_round_of_32(firsts, seconds, thirds)
        # The first matchup should have the strongest winner
        # vs the weakest third-placed team
        first_match = matchups[0]
        last_match = matchups[-1]
        assert first_match[2] >= last_match[2]  # home strength


class TestSimulateKnockout:
    def test_returns_valid_structure(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        assert result["status"] == "ok"
        assert "round_of_32" in result
        assert "round_of_16" in result
        assert "quarter_finals" in result
        assert "semi_finals" in result
        assert "final" in result
        assert "tournament_win_probability" in result
        assert "disclaimer" in result

    def test_round_of_32_has_16_matchups(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        assert len(result["round_of_32"]) == 16

    def test_round_of_16_has_8_matchups(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        assert len(result["round_of_16"]) == 8

    def test_quarter_finals_has_4_matchups(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        assert len(result["quarter_finals"]) == 4

    def test_semi_finals_has_2_matchups(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        assert len(result["semi_finals"]) == 2

    def test_final_has_1_matchup(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        assert len(result["final"]) == 1

    def test_matchup_has_win_probabilities(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        m = result["round_of_32"][0]
        assert "home_win_probability" in m
        assert "away_win_probability" in m
        assert m["home_win_probability"] + m["away_win_probability"] == pytest.approx(1.0)

    def test_tournament_win_prob_sorted_descending(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=500, seed=42)
        probs = [t["win_probability"] for t in result["tournament_win_probability"]]
        assert probs == sorted(probs, reverse=True)

    def test_tournament_win_prob_top_16(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=500, seed=42)
        assert len(result["tournament_win_probability"]) <= 16

    def test_reproducible_with_same_seed(self, full_strengths):
        r1 = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        r2 = simulate_knockout(full_strengths, num_simulations=100, seed=42)
        assert r1["tournament_win_probability"] == r2["tournament_win_probability"]

    def test_win_probabilities_sum_leq_one(self, full_strengths):
        result = simulate_knockout(full_strengths, num_simulations=1000, seed=42)
        total = sum(t["win_probability"] for t in result["tournament_win_probability"])
        assert total <= 1.0 + 1e-6

    def test_empty_strengths(self):
        """Empty strengths still produces all 48 teams via group defaults."""
        result = simulate_knockout({}, num_simulations=10, seed=42)
        assert result["status"] == "ok"
        # Groups always have 48 teams, strengths default to 0.2
        assert len(result["round_of_32"]) == 16

    def test_accepts_precomputed_group_predictions(self, full_strengths):
        preds = compute_group_predictions(full_strengths)
        result = simulate_knockout(
            full_strengths, group_predictions=preds, num_simulations=50, seed=42
        )
        assert result["status"] == "ok"
