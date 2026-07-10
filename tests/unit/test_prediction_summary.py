"""Tests for API prediction summary — top-level field aliases."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd

from scoutfootball.api import (
    _prediction_calibration,
    get_prediction_calibration,
    get_prediction_summary,
)


class TestGetPredictionSummary:
    """Verify get_prediction_summary returns top-level aliases."""

    @patch("scoutfootball.api._settings")
    def test_returns_top_level_status(self, mock_settings: MagicMock) -> None:
        """Response should have a top-level 'status' field."""
        mock_settings.return_value.data_root = MagicMock()
        # When no artifacts exist, status should be 'no_data'
        with patch("scoutfootball.api.Path") as mock_path:
            mock_path.return_value.exists.return_value = False
            result = get_prediction_summary()
        assert "status" in result
        assert "poisson" in result
        assert "dixon_coles" in result
        assert "available_models" in result

    @patch("scoutfootball.api._settings")
    def test_no_data_returns_no_data_status(self, mock_settings: MagicMock) -> None:
        """When no artifacts exist, status should be 'no_data'."""
        mock_root = MagicMock()
        mock_root.__truediv__ = lambda self, other: MagicMock(exists=lambda: False)
        mock_settings.return_value.data_root = mock_root
        result = get_prediction_summary()
        assert result["status"] == "no_data"

    @patch("scoutfootball.api._settings")
    def test_has_model_type_field(self, mock_settings: MagicMock) -> None:
        """Response should have a top-level 'model_type' field."""
        mock_root = MagicMock()
        mock_root.__truediv__ = lambda self, other: MagicMock(exists=lambda: False)
        mock_settings.return_value.data_root = mock_root
        result = get_prediction_summary()
        assert "model_type" in result

    @patch("scoutfootball.api._settings")
    def test_has_available_models(self, mock_settings: MagicMock) -> None:
        """Response should list available models."""
        mock_root = MagicMock()
        mock_root.__truediv__ = lambda self, other: MagicMock(exists=lambda: False)
        mock_settings.return_value.data_root = mock_root
        result = get_prediction_summary()
        assert isinstance(result["available_models"], list)

    @patch("scoutfootball.api._settings")
    def test_dc_artifact_sets_top_level_ready_state(
        self,
        mock_settings: MagicMock,
        tmp_path,
    ) -> None:
        """A usable Dixon-Coles artifact should make the service ready."""
        artifact_dir = tmp_path / "models" / "artifacts"
        artifact_dir.mkdir(parents=True)
        pd.DataFrame([
            {
                "model_type": "dixon_coles",
                "num_matches": 100,
                "rho": -0.1,
                "home_advantage": 0.2,
                "league_mean_goals": 1.3,
                "num_teams": 20,
            },
        ]).to_parquet(artifact_dir / "dixon_coles_results.parquet", index=False)
        mock_settings.return_value.data_root = tmp_path

        result = get_prediction_summary()

        assert result["status"] == "ok"
        assert result["model_type"] == "dixon_coles"
        assert result["num_teams"] == 20
        assert result["available_models"] == ["dixon_coles"]


def test_match_prediction_uses_detailed_calibration_metrics(tmp_path) -> None:
    artifact_dir = tmp_path / "models" / "artifacts"
    artifact_dir.mkdir(parents=True)
    pd.DataFrame([
        {
            "match_id": "1",
            "score_bucket": "1-0",
            "exact_score_probability": 0.2,
            "home_win_probability": 0.6,
            "draw_probability": 0.25,
            "away_win_probability": 0.15,
            "actual_outcome": "home_win",
            "home_lambda": 1.5,
            "away_lambda": 0.8,
            "league": "Test League",
        },
        {
            "match_id": "2",
            "score_bucket": "0-1",
            "exact_score_probability": 0.1,
            "home_win_probability": 0.3,
            "draw_probability": 0.25,
            "away_win_probability": 0.45,
            "actual_outcome": "away_win",
            "home_lambda": 0.9,
            "away_lambda": 1.2,
            "league": "Test League",
        },
    ]).to_parquet(artifact_dir / "dc_calibration_detail.parquet", index=False)

    get_prediction_calibration(force_refresh=True)
    with patch("scoutfootball.api._settings") as mock_settings:
        mock_settings.return_value.data_root = tmp_path
        calibration = _prediction_calibration()
    get_prediction_calibration(force_refresh=True)

    assert calibration["brier"] is not None
    assert calibration["rps"] is not None
    assert calibration["log_loss"] is not None
