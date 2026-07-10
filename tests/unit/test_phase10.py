"""Tests for Phase 10: validation, calibration, pipeline, API."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from scoutfootball.evaluation.calibration import (
    brier_score,
    calibrate_probabilities_isotonic,
)
from scoutfootball.evaluation.validation import (
    ValidationCheckResult,
    ValidationReport,
    validate_no_null_keys,
    validate_parquet_exists,
    validate_row_count,
)


def _data_dir(tmp_path):
    return tmp_path / "data"


def _make_settings(tmp_path):
    from scoutfootball.config import PlatformSettings

    return PlatformSettings.from_root(tmp_path)


class TestValidationReport:
    def test_passed_when_all_pass(self):
        report = ValidationReport(
            checks=[
                ValidationCheckResult("a", True, "ok"),
                ValidationCheckResult("b", True, "ok"),
            ]
        )
        assert report.passed
        assert len(report.failures) == 0

    def test_failed_when_any_fails(self):
        report = ValidationReport(
            checks=[
                ValidationCheckResult("a", True, "ok"),
                ValidationCheckResult("b", False, "bad"),
            ]
        )
        assert not report.passed
        assert len(report.failures) == 1
        assert "FAIL" in report.summary()

    def test_empty_report_passes(self):
        report = ValidationReport()
        assert report.passed


class TestValidateParquetExists:
    def test_missing_file(self, tmp_path):
        result = validate_parquet_exists(
            "nonexistent.parquet",
            settings=_make_settings(tmp_path),
        )
        assert not result.passed
        assert "Missing" in result.message

    def test_existing_file(self, tmp_path):
        gold = _data_dir(tmp_path) / "gold" / "feature_store"
        gold.mkdir(parents=True)
        df = pd.DataFrame({"x": [1, 2]})
        df.to_parquet(gold / "test.parquet")
        result = validate_parquet_exists(
            "gold/feature_store/test.parquet",
            settings=_make_settings(tmp_path),
        )
        assert result.passed


class TestValidateRowCount:
    def test_below_minimum(self, tmp_path):
        gold = _data_dir(tmp_path) / "gold" / "feature_store"
        gold.mkdir(parents=True)
        df = pd.DataFrame({"x": [1]})
        df.to_parquet(gold / "small.parquet")
        result = validate_row_count(
            "gold/feature_store/small.parquet",
            min_rows=10,
            settings=_make_settings(tmp_path),
        )
        assert not result.passed

    def test_above_minimum(self, tmp_path):
        gold = _data_dir(tmp_path) / "gold" / "feature_store"
        gold.mkdir(parents=True)
        df = pd.DataFrame({"x": range(20)})
        df.to_parquet(gold / "big.parquet")
        result = validate_row_count(
            "gold/feature_store/big.parquet",
            min_rows=10,
            settings=_make_settings(tmp_path),
        )
        assert result.passed


class TestValidateNoNullKeys:
    def test_with_nulls(self, tmp_path):
        gold = _data_dir(tmp_path) / "gold" / "feature_store"
        gold.mkdir(parents=True)
        df = pd.DataFrame({"match_id": ["a", None], "player_id": ["p1", "p2"]})
        df.to_parquet(gold / "nulls.parquet")
        result = validate_no_null_keys(
            "gold/feature_store/nulls.parquet",
            ("match_id", "player_id"),
            settings=_make_settings(tmp_path),
        )
        assert not result.passed

    def test_without_nulls(self, tmp_path):
        gold = _data_dir(tmp_path) / "gold" / "feature_store"
        gold.mkdir(parents=True)
        df = pd.DataFrame({"match_id": ["a", "b"], "player_id": ["p1", "p2"]})
        df.to_parquet(gold / "clean.parquet")
        result = validate_no_null_keys(
            "gold/feature_store/clean.parquet",
            ("match_id", "player_id"),
            settings=_make_settings(tmp_path),
        )
        assert result.passed


class TestCalibration:
    def test_isotonic_improves_or_maintains(self):
        rng = np.random.default_rng(99)
        y_true = rng.binomial(1, 0.3, size=500)
        y_prob = np.clip(y_true * 0.5 + rng.normal(0, 0.2, size=500), 0, 1)
        calibrated, result = calibrate_probabilities_isotonic(y_true, y_prob)
        assert result.method == "isotonic"
        assert result.brier_after <= result.brier_before + 1e-6
        assert len(calibrated) == len(y_prob)

    def test_brier_score_perfect(self):
        y_true = np.array([1.0, 0.0, 1.0])
        y_prob = np.array([1.0, 0.0, 1.0])
        assert brier_score(y_true, y_prob) == pytest.approx(0.0)

    def test_brier_score_worst(self):
        y_true = np.array([1.0, 0.0])
        y_prob = np.array([0.0, 1.0])
        assert brier_score(y_true, y_prob) == pytest.approx(1.0)

    def test_small_sample_returns_uncalibrated(self):
        y_true = np.array([1.0, 0.0])
        y_prob = np.array([0.8, 0.2])
        calibrated, result = calibrate_probabilities_isotonic(y_true, y_prob)
        assert result.improvement == 0.0


class TestPipeline:
    def test_daily_ingest_returns_results(self):
        from scoutfootball.pipeline import run_daily_ingest

        results = run_daily_ingest(sources=("statsbomb_open",))
        # In CI (no LFS data), statsbomb_open may fail gracefully
        if results.get("statsbomb_open", "").startswith("failed"):
            pytest.skip("statsbomb_open not available (missing LFS data in CI)")
        assert "statsbomb_open" in results

    def test_build_features_returns_results(self):
        from scoutfootball.pipeline import run_build_features

        results = run_build_features()
        # In CI (no LFS data), player_ratings_optimized.parquet is a pointer
        # file, so the features step may fail gracefully.
        if "player_match" not in results:
            pytest.skip("player_match not available (missing LFS data in CI)")
        assert "player_match" in results

    def test_weekly_train_skips_on_validation_failure(self, tmp_path):
        from scoutfootball.pipeline import run_weekly_train

        results = run_weekly_train(
            skip_if_validation_fails=True,
            settings=_make_settings(tmp_path),
        )
        assert results.get("status") == "skipped"


class TestAPI:
    def test_health_check(self):
        from scoutfootball.api import health_check

        resp = health_check()
        assert resp.status == "ok"
        assert resp.version == "1.0.3"

    def test_list_players(self):
        from scoutfootball.api import list_players

        resp = list_players()
        assert resp.player_count >= 0
        assert isinstance(resp.players, list)

    def test_list_teams(self):
        from scoutfootball.api import list_teams

        teams = list_teams()
        assert isinstance(teams, list)

    def test_get_match_prediction(self):
        from scoutfootball.api import get_match_prediction

        result = get_match_prediction("Arsenal", "Chelsea")
        if "error" in result:
            # If real data isn't available, verify error response structure
            assert isinstance(result["error"], str)
        else:
            assert "home_win" in result
            assert "away_win" in result
            assert result["home_team"] == "Arsenal"
            assert result["away_team"] == "Chelsea"

    def test_get_value_summary(self):
        from scoutfootball.api import get_value_summary

        result = get_value_summary()
        assert "sample_count" in result

    def test_get_artifacts_summary(self):
        from scoutfootball.api import get_artifacts_summary

        result = get_artifacts_summary()
        assert "player_match_rows" in result
        assert "artifacts" in result
        assert isinstance(result["artifacts"], list)

    def test_get_prediction_summary(self):
        from scoutfootball.api import get_prediction_summary

        result = get_prediction_summary()
        assert "poisson" in result
        assert "dixon_coles" in result
        assert "available_models" in result

    def test_get_model_runs(self):
        from scoutfootball.api import get_model_runs

        result = get_model_runs()
        assert "count" in result
        assert "runs" in result

    def test_get_watchlist(self):
        from scoutfootball.api import get_watchlist

        result = get_watchlist(limit=10)
        assert "count" in result
        assert "players" in result

    def test_get_shortlist(self):
        from scoutfootball.api import get_shortlist

        result = get_shortlist(limit=10)
        assert "count" in result
        assert "players" in result

    def test_get_action_value_summary(self):
        from scoutfootball.api import get_action_value_summary

        result = get_action_value_summary(limit=5)
        assert "status" in result
        assert "players" in result
        if result["status"] == "ok":
            assert len(result["xt_players"]) <= 5
            assert len(result["vaep_players"]) <= 5
            assert result["model_granularity"]["vaep"] == "player_team_career"
            assert result["identity_coverage"]["total_rows"] == result["metrics"]["vaep_rows"]
