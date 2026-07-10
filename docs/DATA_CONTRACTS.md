# Data Contracts

This document defines the schema contracts for all data artifacts in
ScoutFootball. Changes to these schemas require updating this document,
the downstream consumers, and the validation tests.

---

## 1. StatsBomb Events Schema

**File**: `data/raw/statsbomb_open/events_all.parquet`
**Source**: StatsBomb Open Data (free for research, must attribute)
**Coverage**: Sample only (3 matches, ~12K events). NOT full league coverage.

| Column | Type | Description |
|---|---|---|
| match_id | str | StatsBomb match identifier |
| event_id | int | Unique event identifier within match |
| index | int | Event sequence index |
| period | int | 1=1st half, 2=2nd half, etc. |
| timestamp | str | Time within match (HH:MM:SS.mmm) |
| minute | int | Minute of event |
| second | int | Second within minute |
| possession | int | Possession sequence number |
| duration | float | Duration of event in seconds |
| type_id | int | StatsBomb event type ID |
| event_type | str | Event type name (Pass, Shot, Carry, etc.) |
| possession_team_id | int | Team in possession |
| possession_team_name | str | Team name in possession |
| team_id | int | Team performing action |
| team_name | str | Team name |
| player_id | int | StatsBomb player ID |
| player_name | str | Player name |
| location | list[float] | [x, y] start location (120x80 pitch) |
| pass_end_location | list[float] | [x, y] pass end location |
| carry_end_location | list[float] | [x, y] carry end location |
| shot_end_location | list[float] | [x, y] shot end location |
| shot_statsbomb_xg | float | StatsBomb xG for shot |
| pass_recipient_id | int | Pass recipient player ID |
| pass_recipient_name | str | Pass recipient name |
| pass_length | float | Pass length in yards |
| pass_angle | float | Pass angle in radians |
| pass_outcome_id | int | Pass outcome ID (null=complete) |
| pass_outcome_name | str | Pass outcome name |
| shot_outcome_id | int | Shot outcome ID |
| shot_outcome_name | str | Shot outcome name |
| ... | ... | Additional qualifier columns |

**Coordinate system**: StatsBomb uses 120x80 (x: 0=own goal, 120=opponent goal).

---

## 2. Internal Actions Schema

**Defined in**: `src/scoutfootball/action_value/schema.py`
**Coordinate system**: 0-100 normalized (x: left-to-right, y: bottom-to-top)
**Direction**: Always attack-to-defense (left-to-right after normalization)

| Field | Type | Description |
|---|---|---|
| action_id | int | Unique ID within match |
| provider_action_id | str | Original action ID from source |
| match_id | str | Match identifier |
| team_id | str | Team identifier |
| player_id | str | Player identifier |
| period | int | 1=1st half, 2=2nd half |
| minute | int | Minute of action |
| second | int | Second within minute |
| action_type | ActionType | Standardized type (SPADL-compatible) |
| result | ActionResult | Outcome: success/failure/unknown |
| start_x | float | Start x coordinate (0-100) |
| start_y | float | Start y coordinate (0-100) |
| end_x | float | End x coordinate (0-100) |
| end_y | float | End y coordinate (0-100) |
| body_part | str | Body part used |
| qualifier | dict | Additional metadata |
| source | str | Data provider name |
| source_coverage | str | Coverage flag: full/partial/sample |

**ActionTypes**: pass, dribble, shot, freeze, take_on, clearance,
interception, tackle, block, goalkeeper, receipt, carry, unknown

**ActionResults**: success, failure, unknown

---

## 3. SPADL Mapping

StatsBomb events are converted to InternalAction via
`src/scoutfootball/action_value/spadl_adapter.py`.

| StatsBomb Type | InternalAction Type |
|---|---|
| Pass | pass |
| Carry | carry |
| Shot | shot |
| Dribble | dribble |
| Ball Receipt* | receipt |
| Clearance | clearance |
| Interception | interception |
| Duel | tackle |
| Block | block |
| Goalkeeper | goalkeeper |
| Take On | take_on |
| Ball Recovery | clearance |
| Miscontrol | failure (pass) |
| Foul Committed | freeze |

Coordinate transformation: `x_internal = x_statsbomb / 120 * 100`

---

## 4. player_ratings_optimized.parquet

**File**: `data/gold/feature_store/player_ratings_optimized.parquet`
**Rows**: ~30,000 (all seasons, all leagues)
**Source**: Rating optimizer GPU pipeline

| Column | Type | Description |
|---|---|---|
| player | str | Player name |
| team | str | Club team name |
| league | str | League name (Premier League, La Liga, etc.) |
| season | str | Season code (e.g., "2425") |
| source_position | str | Raw position string from source |
| sub_position | str | Mapped position group (GK/CB/FB/DM/CM/AM/W/ST) |
| pos_idx | int | Position index (0-7) |
| position_source | str | Position mapping source |
| position_confidence | str | Position mapping confidence (low/medium/high) |
| matches | float | Number of matches played |
| starts | float | Number of starts |
| minutes | float | Total minutes played |
| npg_p90 | float | Non-penalty goals per 90 minutes |
| assists_p90 | float | Assists per 90 minutes |
| g_a_volume | float | Total goals + assists |
| tackles_p90 | float | Tackles per 90 |
| interceptions_p90 | float | Interceptions per 90 |
| crosses_p90 | float | Crosses per 90 |
| fouls_drawn_p90 | float | Fouls drawn per 90 |
| fouls_p90 | float | Fouls committed per 90 |
| defense_composite | float | Defense composite score (0-100) |
| possession_composite | float | Possession composite score (0-100) |
| season_rank | int | Rank within season |
| npg_trend | float | Attack trend metric |
| def_trend | float | Defense trend metric |
| pos_trend | float | Possession trend metric |
| experience_factor | float | Experience adjustment factor |
| low_appearance | bool | True if <20 matches (penalized) |
| optimized_score | float | Final optimized rating (0-100) |
| same_position_score | float | Rating within same position group (0-100) |

---

## 5. rating_feature_matrix.parquet

**File**: `data/gold/feature_store/rating_feature_matrix.parquet`
**Purpose**: Input features for the rating optimizer

| Column | Type | Description |
|---|---|---|
| player_id | str | Player identifier |
| season_id | str | Season identifier |
| goals | int | Goals scored |
| assists | int | Assists |
| shots | int | Total shots |
| shots_on_target | int | Shots on target |
| minutes_played | int | Total minutes |
| starts | int | Number of starts |
| npxg | float | Non-penalty expected goals |
| xa | float | Expected assists |
| available_flag | bool | Data availability flag |
| tackles | int | Tackles made |
| passes | int | Passes attempted |
| xT_added | float | Expected threat added |
| player_name | str | Player name |
| team_id | str | Team identifier |
| team_name | str | Team name |
| competition_id | str | Competition identifier |
| position_group | str | Mapped position group |
| defense_missing | bool | Defense data missing flag |
| possession_missing | bool | Possession data missing flag |
| xT_VAEP_missing | bool | xT/VAEP data missing flag |
| goalkeeper_missing | bool | GK data missing flag |
| finishing_raw | float | Raw finishing metric |
| finishing_shrunk | float | Shrunk finishing metric |
| statsbomb_open_source_covered | bool | StatsBomb coverage flag |
| fbref_source_covered | bool | FBref coverage flag |
| has_expected_metrics | bool | xG/xA data available |
| has_ball_value_data | bool | Ball value data available |

---

## 6. player_truth_labels.parquet

**File**: `data/gold/feature_store/player_truth_labels.parquet`
**Purpose**: Ground truth labels for rating validation

| Column | Type | Description |
|---|---|---|
| player_id | str | Player identifier |
| season | str | Season code |
| label_source | str | Source of truth label |
| label_confidence | str | Confidence in label (low/medium/high) |
| label_value | float | Label value |
| as_of_date | str | Date label was assigned |
| position_scope | str | Position scope for label |
| manual_review_flag | bool | Requires manual review |

**Status**: Schema exists; data rows are currently empty.

---

## 7. team_match.parquet

**File**: `data/gold/feature_store/team_match.parquet`
**Rows**: ~10,000
**Source**: Football-Data.co.uk match results

| Column | Type | Description |
|---|---|---|
| match_id | str | Match identifier |
| match_date | str | Match date (YYYY-MM-DD) |
| competition_id | str | Competition identifier |
| season_id | str | Season identifier |
| team_id | str | Team identifier |
| team_name | str | Team name |
| opponent_team_id | str | Opponent identifier |
| opponent_team_name | str | Opponent name |
| is_home | bool | Home team flag |
| goals_for | int | Goals scored |
| goals_against | int | Goals conceded |
| goal_diff | int | Goal difference |
| result_points | int | Points earned (3/1/0) |
| shots | int | Shots taken |
| has_shots_data | bool | Shot data available flag |
| shots_on_target | int | Shots on target |
| has_shots_on_target_data | bool | SOT data available flag |
| xg | float | Expected goals for |
| xg_against | float | Expected goals against |
| has_xg_data | bool | xG data available flag |
| rest_days | int | Days since last match |
| elo_pre | float | ELO rating before match |
| opponent_elo_pre | float | Opponent ELO before match |
| elo_diff | float | ELO difference |

---

## 8. player_value_metrics.parquet

**File**: `data/gold/feature_store/player_value_metrics.parquet`
**Source**: StatsBomb Open Data sample only
**Coverage**: ~10 sample players from 3 matches

| Column | Type | Description |
|---|---|---|
| player_id | str | Player identifier |
| player_name | str | Player name |
| team_id | str | Team identifier |
| estimated_minutes | float | Estimated playing time |
| n_matches | int | Number of matches |
| shots | int | Total shots |
| shots_per_90 | float | Shots per 90 minutes |
| xG_total | float | Total expected goals |
| xG_per_90 | float | xG per 90 minutes |
| goals | int | Actual goals |
| goals_per_90 | float | Goals per 90 |
| finishing_delta | float | Goals minus xG |
| passes_per_90 | float | Passes per 90 |
| pass_completion_rate | float | Pass completion rate |
| forward_pass_rate | float | Forward pass rate |
| total_xt | float | Total xT accumulated |
| xT_per_90 | float | xT per 90 minutes |
| tackles_per_90 | float | Tackles per 90 |
| interceptions_per_90 | float | Interceptions per 90 |
| blocks_per_90 | float | Blocks per 90 |
| duel_win_rate | float | Duel win rate |
| duels_per_90 | float | Duels per 90 |
| touches_per_90 | float | Touches per 90 |
| progressive_carries_per_90 | float | Progressive carries per 90 |
| final_third_touches_per_90 | float | Final third touches per 90 |
| penalty_area_touches_per_90 | float | Penalty area touches per 90 |
| composite_score | float | Composite action value score |
| source | str | Data source |
| source_attribution | str | Attribution text |
| coverage_note | str | Coverage limitation note |

---

## 9. API Endpoint Contracts

### GET /health
Returns server health status.

**Response**: `{ status, data_source, version }`

### GET /ratings
Returns player ratings with optional filters.

**Query params**: `position`, `league`, `team`, `season`, `limit`
**Response**: `{ count, players: [...] }`

### GET /players/{player_name}
Returns detailed player profile with fuzzy search support.

**Query params**:
- `season` (str, optional): Filter by season
- `position_group` (str, optional): Filter by position group
- `limit` (int, default=50): Pagination limit for fuzzy matches
- `offset` (int, default=0): Pagination offset for fuzzy matches
- `format` (str, default="json"): Response format ("json" or "csv")

**Response** (exact match):
```json
{
  "player": "string",
  "found": true,
  "team": "string",
  "league": "string",
  "season": "string",
  "position_group": "string",
  "optimized_score": 85.0,
  "minutes": 2500,
  "matches": 30,
  "low_appearance": false,
  "confidence_level": "HIGH",
  "confidence_reason": "adequate minutes, matches, and peer pool",
  "npg_p90": 0.5,
  "assists_p90": 0.3,
  "defense_composite": 45.0,
  "possession_composite": 60.0,
  "radar": [80.0, 60.0, 45.0, 92.0, 85.0],
  "seasons": [
    { "season": "2425", "team": "...", "league": "...",
      "position_group": "...", "optimized_score": 85.0, "minutes": 2500 }
  ],
  "position_explanation": {
    "attack": { "raw_score", "percentile_rank", "contribution", "confidence" },
    "defense": { "raw_score", "percentile_rank", "contribution", "confidence" },
    "possession": { "raw_score", "percentile_rank", "contribution", "confidence" },
    "availability": { "raw_score", "percentile_rank", "contribution", "confidence" },
    "quality": { "raw_score", "percentile_rank", "contribution", "confidence" },
    "xT": {
      "xT_per_90": 0.5,
      "percentile_rank": 80.0,
      "contribution": 16.7,
      "confidence": "LOW"
    }
  },
  "xt_summary": {
    "available": true,
    "xT_per_90": 0.5,
    "xT_total": 12.5,
    "xT_percentile": 80.0,
    "xT_contribution": 16.7,
    "coverage_note": "StatsBomb Open Data sample only"
  }
}
```

**Response** (fuzzy match, multiple players):
```json
{
  "player": "search_term",
  "found": true,
  "fuzzy_match": true,
  "total": 15,
  "offset": 0,
  "limit": 50,
  "players": [
    { "player", "found", "team", "league", "season",
      "position_group", "optimized_score", "minutes" }
  ]
}
```

### GET /predictions/calibration
Returns calibration metrics for match prediction models.

**Response**:
```json
{
  "dixon_coles": {
    "status": "ok",
    "log_loss_exact": 2.1,
    "brier_1x2": 0.55,
    "rps_1x2": 0.22,
    "n_matches": 1000
  },
  "poisson": { "status", "log_loss_exact", "brier_1x2", "rps_1x2", "n_matches" },
  "low_score_breakdown": [
    { "score_bucket": "0-0", "n_matches": 100,
      "actual_pct": 10.0, "mean_predicted_pct": 8.0, "calibration_error": 2.0 }
  ],
  "calibration_plot": [
    { "bin_center": 0.15, "n_matches": 200,
      "mean_predicted": 0.14, "mean_actual": 0.16 }
  ],
  "league_coverage": [
    { "league": "Premier League", "n_matches": 380,
      "mean_log_loss": 2.1, "mean_brier": 0.55 }
  ]
}
```

### GET /predictions/{home_team}/{away_team}
Match prediction between two teams.

**Query params**: `model` ("poisson" or "dixon_coles")
**Response**: `{ home_team, away_team, model_type, home_lambda, away_lambda, home_win, draw, away_win, over_2_5, btts_yes }`

### GET /ratings/meta
Model metadata and league metrics.

### GET /artifacts
Artifact counts and data health summary.

### GET /action-values
Player action value summary from StatsBomb sample.

**Query params**: `limit` (default=20)

### GET /review-queue
Low-confidence players for review.

### GET /watchlist, /shortlist
Scouting watchlist and shortlist.

### GET /model-runs
Model run registry with holdout metrics.

### GET /reports/model-runs/{run_id}
Full details for a single model run.

### GET /world-cup/groups, /world-cup/schedule, /world-cup/squads/{team}, /world-cup/predictions
World Cup data endpoints.

### GET /license
Data source license attribution.

**Response**:
```json
{
  "license_attribution": {
    "statsbomb": { "name", "license", "url", "attribution_required", "note" },
    "fbref": { ... },
    "football_data": { ... },
    "understat": { ... },
    "club_elo": { ... },
    "transfermarkt": { ... }
  },
  "data_source_label": "string",
  "updated_at": 1234567890.0
}
```

### GET /value-summary
Value deviation analysis from OOF predictions.

**Response**: `{ players: [...], summary: { ... } }`

### GET /predictions/meta
Match prediction model metadata.

### GET /teams/strength

Aggregated team-level strength metrics derived from player ratings.

**Query params**: `league` (optional), `season` (optional), `limit` (default 100)

**Response**:
```json
{
  "count": 2,
  "teams": [
    {
      "team": "Team Alpha",
      "league": "Premier League",
      "season": "2526",
      "overall_rating": 62.5,
      "squad_size": 20,
      "total_minutes": 25000,
      "position_groups": {
        "GK": { "rating": 55.0, "player_count": 2, "avg_minutes": 900 },
        "DEF": { "rating": 60.0, "player_count": 6, "avg_minutes": 1500 },
        "MID": { "rating": 65.0, "player_count": 7, "avg_minutes": 1800 },
        "ATT": { "rating": 68.0, "player_count": 5, "avg_minutes": 1600 }
      },
      "top_players": [
        { "name": "Player A", "position": "ST", "broad_pos": "ATT", "rating": 70.0, "minutes": 1800, "confidence": "HIGH" }
      ],
      "confidence_distribution": { "HIGH": 15, "MEDIUM": 3, "LOW": 2 }
    }
  ]
}
```

The overall rating is minutes-weighted: `sum(score * minutes) / sum(minutes)`.
Position groups are mapped from granular positions to GK, DEF, MID, ATT.
Players with comma-joined team names (transferred players) are excluded.

---

## 9.5 Static Snapshot Contracts

`frontend/data/` contains tracked release snapshots consumed by the static demo and Vercel deployment. Each file must be valid JSON (dict or list); Python repr strings are not allowed.

### health.json

**File**: `frontend/data/health.json`
**Source**: `GET /health` response

```json
{
  "status": "ok",
  "data_source": "local",
  "version": "1.0.2"
}
```

### players_list.json

**File**: `frontend/data/players_list.json`
**Source**: `GET /ratings` response

```json
{
  "count": 1234,
  "players": [
    { "player": "string", "team": "string", "league": "string",
      "season": "string", "position_group": "string",
      "optimized_score": 85.0, "minutes": 2500 }
  ]
}
```

### Static Snapshot Serialization Rules

1. All values must be JSON-serializable types: `str`, `int`, `float`, `bool`, `None`, `list`, `dict`.
2. dataclass and Pydantic response objects must be serialized via `dataclasses.asdict()` or `model.model_dump()`, not `str(obj)`.
3. `numpy.int64`, `numpy.float64`, `numpy.bool_`, `float('inf')`, and `float('nan')` must be converted to native Python types before serialization.
4. The export script must fail loudly on non-serializable objects rather than falling back to `str()`.

---

## 9.6 Browser-local Scouting Workspace

**Schema**: `scoutfootball.scouting-workspace`

**Current version**: `1.1.0`

**Implementation**: `frontend/scouting-workspace.js`

The workspace is an explicit backup and transfer format for browser-local scouting decisions. It does not change the read-only API boundary and is not a server audit log.

```json
{
  "schema": "scoutfootball.scouting-workspace",
  "version": "1.1.0",
  "exported_at": "2026-07-10T12:00:00.000Z",
  "audit": {
    "workspace_id": "uuid-or-local-id",
    "created_at": "ISO-8601",
    "updated_at": "ISO-8601",
    "revision": 3,
    "device_scope": "browser-local",
    "last_action": "local-edit|manual-export|import-merge|import-replace",
    "app_version": "1.0.2",
    "imported_from": "optional-workspace-id"
  },
  "source": {
    "rating_snapshot_ids": ["snapshot-id"],
    "attribution": "ScoutFootball local scouting decisions; server queues remain read-only"
  },
  "review": {
    "statuses": { "player-key": "pending|reviewing|approved|rejected" },
    "shortlist_notes": { "player-key": "note" },
    "watchlist_notes": { "player-key": "note" }
  },
  "selections": { "watchlist": [], "shortlist": [] },
  "watchlist_snapshot": { "player_keys": [], "saved_at": "ISO-8601|null" }
}
```

Imports are limited to 1 MB, 1,000 status/note entries and 500 selected players. Unknown statuses, forbidden object keys, oversized strings and unsupported major versions are rejected or sanitized. Safe merge unions selections and uses the workspace with the newer audit timestamp for conflicting status/note keys; explicit replacement is the only overwrite path.

---

## 10. Cross-Provider Schema Reference

### 10.1 SPADL / atomic-SPADL Compatibility

ScoutFootball's `InternalAction` schema is designed to be compatible with
[socceraction](https://socceraction.readthedocs.io/)'s SPADL representation:

| SPADL Field | InternalAction Field | Notes |
|---|---|---|
| game_id | match_id | |
| period_id | period | |
| seconds | minute * 60 + second | SPADL uses absolute seconds |
| team_id | team_id | |
| player_id | player_id | |
| start_x, start_y | start_x, start_y | Both use 0-100 normalized |
| end_x, end_y | end_x, end_y | Both use 0-100 normalized |
| action_type | action_type | SPADL has 19 types; InternalAction has 13 |
| result_id | result | SPADL uses int (0/1/-1); InternalAction uses string |

**Key differences from SPADL**:
- SPADL uses integer result codes; InternalAction uses string enums.
- SPADL has separate "goalkick" and "freekick" action types; InternalAction
  maps these to existing types via the `qualifier` dict.
- SPADL coordinates are 0-105 x 0-68 (meters); InternalAction uses 0-100 x 100.

### 10.2 kloppy Compatibility

[kloppy](https://kloppy.pysport.org/) provides dataset loading and coordinate
system transformation for tracking data. Current status:

- **Evaluation**: kloppy supports StatsBomb, Opta, Wyscout, TRACAB, SkillCorner,
  Metrica, and FIFA tracking formats with configurable coordinate systems.
- **Risk**: kloppy adds a dependency chain (lxml, requests) and its own coordinate
  normalization may conflict with InternalAction's 0-100 system.
- **Decision**: Use kloppy as reference for coordinate transformation patterns,
  but do not add as direct dependency until P6 cross-provider schema is stable.
  If tracking data enters the pipeline, kloppy's `DatasetTransformer` patterns
  should be adapted rather than imported.

### 10.3 floodlight Compatibility

[floodlight](https://floodlight.readthedocs.io/) provides Game/Team/Player/Event/Frame/Segment
abstractions. Current status:

- **Evaluation**: floodlight's modular design (separate objects for positions,
  events, segments) is a good reference for future tracking data integration.
- **Decision**: Reference only. Not a direct dependency candidate until
  tracking/freeze-frame data enters the pipeline (P8+).

### 10.4 Common Data Format (CDF)

[CDF](https://www.cdf.football/) defines standardized schemas for football data exchange.

- **Evaluation**: CDF's event schema covers similar ground to InternalAction
  but focuses on interoperability between commercial providers.
- **Decision**: Use as validation reference for field completeness; do not
  adopt CDF as the primary internal schema since InternalAction is already
  tailored to the StatsBomb -> xT/VAEP pipeline.

---

## 11. Socceraction Dependency Evaluation

### Current Assessment

[socceraction](https://socceraction.readthedocs.io/en/stable/) provides:
- SPADL and atomic-SPADL action representations
- Expected Threat (xT) model training and evaluation
- VAEP model training and evaluation
- StatsBomb/Wyscout/Opta event conversion

### Dependency Risk

| Factor | Assessment |
|---|---|
| Maintenance | Active (last release 2024, regular commits) |
| Dependencies | numpy, pandas, scipy, scikit-learn (already in project) |
| License | MIT |
| Size | Lightweight (~15 modules) |
| Breaking changes | Low risk; stable API since v1.0 |
| Testing | Well-tested with StatsBomb Open Data |

### Recommendation

**Short-term (P2)**: Use socceraction's SPADL conversion and xT implementation
as reference for validating our `spadl_adapter.py` and `xt.py`. Do NOT add as
direct dependency yet — our internal adapter is already functional and adding
socceraction would require reconciling coordinate systems and action type enums.

**Medium-term (P3-P4)**: Evaluate adding socceraction as an optional dependency
for VAEP training. The key value would be reusing socceraction's VAEP pipeline
rather than reimplementing gradient-boosted feature engineering. Add as
`socceraction[statsbomb]` optional extra in `pyproject.toml` only after:
1. InternalAction schema is stable
2. xT results are validated against socceraction's reference implementation
3. VAEP is the next priority (after truth labels and rating calibration)

**Not recommended**: Using socceraction as the primary action schema.
InternalAction's string-based enums and 0-100 normalized coordinates are
better suited to our multi-source pipeline and frontend visualization needs.
