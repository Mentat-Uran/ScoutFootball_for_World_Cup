from __future__ import annotations

import pandas as pd

from scoutfootball.action_value.identity import (
    attach_team_names,
    build_identity_coverage_report,
    build_xt_identity_context,
    enrich_vaep_identities,
)


def _xt_rows() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "player_id": 10,
                "player_name": "Ada Forward",
                "team_id": 20,
                "season": "2022/2023",
                "competition": "League",
            },
            {
                "player_id": "10",
                "player_name": "Ada Forward",
                "team_id": "20",
                "season": "2023/2024",
                "competition": "Cup",
            },
        ]
    )


def _matches() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "home_team_id": 20,
                "home_team_name": "City Women",
                "away_team_id": 21,
                "away_team_name": "United Women",
            }
        ]
    )


def test_build_xt_identity_context_keeps_multi_season_semantics() -> None:
    context = build_xt_identity_context(_xt_rows())

    assert len(context) == 1
    row = context.iloc[0]
    assert row["player_id"] == "10"
    assert row["mapped_player_name"] == "Ada Forward"
    assert row["season_context"] == "2022/2023 | 2023/2024"
    assert row["season_count"] == 2
    assert row["competition_context"] == "Cup | League"


def test_enrich_vaep_identities_preserves_rows_and_adds_exact_context() -> None:
    vaep = pd.DataFrame(
        [
            {
                "player_id": "10.0",
                "team_id": "20.0",
                "player_name": "",
                "vaep_total": 8.0,
                "vaep_per_90": 0.4,
            }
        ]
    )

    result = enrich_vaep_identities(vaep, _xt_rows(), _matches())

    assert len(result) == len(vaep)
    row = result.iloc[0]
    assert row["player_id"] == "10"
    assert row["team_id"] == "20"
    assert row["player_name"] == "Ada Forward"
    assert row["team_name"] == "City Women"
    assert row["season_count"] == 2
    assert row["identity_status"] == "mapped"
    assert bool(row["identity_mapped"])


def test_unresolved_player_is_retained_as_partial_with_team_fallback() -> None:
    vaep = pd.DataFrame([{"player_id": "999", "team_id": "21", "vaep_total": 1.0}])

    result = enrich_vaep_identities(vaep, _xt_rows(), _matches())

    assert len(result) == 1
    assert result.iloc[0]["player_name"] == ""
    assert result.iloc[0]["team_name"] == "United Women"
    assert result.iloc[0]["identity_status"] == "partial"


def test_coverage_report_is_derived_from_current_rows() -> None:
    vaep = pd.DataFrame(
        [
            {"player_id": "10", "team_id": "20"},
            {"player_id": "999", "team_id": "999"},
        ]
    )
    enriched = enrich_vaep_identities(vaep, _xt_rows(), _matches())

    report = build_identity_coverage_report(enriched)

    assert report["version"] == "1.1.0"
    assert report["granularity"] == "player_team_career"
    assert report["total_rows"] == 2
    assert report["mapped_rows"] == 1
    assert report["unmapped_rows"] == 1
    assert report["coverage_rate"] == 0.5
    assert report["multi_season_rows"] == 1


def test_attach_team_names_does_not_overwrite_existing_display_name() -> None:
    frame = pd.DataFrame([{"team_id": "20", "team_name": "Custom display"}])

    result = attach_team_names(frame, _matches())

    assert result.iloc[0]["team_name"] == "Custom display"
