# Changelog

All notable changes to ScoutFootball will be documented in this file.

## [1.0.3] - 2026-07-11

### New Features

- **Server-side scouting workspace persistence:** scouting workspaces can now be saved to and loaded from the local API with conflict-safe optimistic concurrency (If-Match revisions), atomic writes, immutable backups, and loopback-only access control.
- **H2H form trend momentum and rating:** the head-to-head view now shows a form-trend card for each team with a 0-100 form rating, momentum indicator (improving/declining/stable), goals scored/conceded per game trends, clean sheets, failed-to-score count, and a cumulative points sparkline.
- **Multi-section player scouting report export:** the single-row player CSV export is replaced with a full scouting report available in both CSV and JSON formats, covering profile, radar, position percentiles, xT summary, 3-season trend, low-confidence reasons, scouting notes, and season history.
- **Player comparison CSV export:** the comparison result panel now has an export button that downloads a multi-section CSV covering player profiles, radar dimensions, stats comparison, and position percentile comparison.

### Frontend

- Restored the Scouting and Action Value navigation entries after fixing their pending payload bugs.
- Scouting now preserves the current queue contract, supports search/status filters, local review workflow, explicit snapshots, CSV export, and merged local watchlist/shortlist selections.
- Action Value now supports the current xT/VAEP payloads, model/search/competition/minutes filters, sample summaries, low-sample warnings, and guarded tactical-board handoff.
- Plain static servers now fall back to mapped `frontend/data/` snapshots after API-route 404 responses.
- Added frontend feature contract tests and synchronized the roadmap, status, API/static sync, task, agent, and user documentation.
- API status pill now distinguishes LIVE (API online), STATIC (fallback from snapshot), and OFFLINE (neither available).
- Review queue is now paginated at 50 items per page to avoid rendering thousands of cards at once.
- NaN/undefined numeric values are now guarded and display as "N/A" instead of raw strings.
- World Cup page status pill is now dynamic based on actual data source.
- Loading failure is shown when both API and static cache are unavailable.

### Fixed

- Fixed player profile field name mismatch: the API returns `position_percentiles` (plural dict) but the frontend read `position_percentile` (singular, always undefined).
- Fixed radar label mismatch: the frontend used `Volume`/`Overall` but the API defines `Reliability`/`Impact`.
- Static export no longer writes Python repr strings for dataclass/Pydantic responses (`health.json`, `players_list.json` were affected). The export script now requires JSON-safe serialization and fails loudly on non-serializable objects instead of falling back to `str()`.

### Testing

- Added `compute_form_trend` unit tests covering empty data, all-win high rating, declining negative momentum, cumulative points trend, rating boundaries, and real H2H response integration.
- Added frontend contract tests for scouting report export buttons, position percentiles field name fix, form trend rendering, and player comparison export.
- Added API JSON cleaning regression tests covering `_clean_json_value` for numpy types, inf, and NaN.
- Added static frontend JSON contract tests validating that `frontend/data/` files are valid JSON dicts/lists without repr strings.
- Added empty data handling tests for API and frontend degradation.

### Changed

- Bump version to 1.0.3 across all modules (pyproject.toml, __init__.py, package.json, frontend, preload, tests, health.json, uv.lock).

## [1.0.2] - 2026-06-13

### Changed

- Bump version to 1.0.2 across all modules (pyproject.toml, __init__.py, package.json, frontend, preload, tests, health.json).

## [1.0.0] - 2026-06-11

### Highlights

First stable release of ScoutFootball — a local-first football analytics platform for the 2026 FIFA World Cup.

### Core Pipeline

- End-to-end data pipeline: `ingest` → `build-features` → `train`
- Five data sources: FBref, Football-Data, Understat, StatsBomb Open Data, Club Elo
- Data validation: `scoutfootball validate` checks integrity before training
- DuckDB + Parquet storage with raw/silver/gold/models/reports/logs layering

### Player Ratings

- PyTorch GPU optimizer with composite objective (Spearman + soft NDCG@20 + position consistency + train-fitted points/league calibration + distribution/tail/league-bias losses + player-score guardrails + optional player truth-label anchor)
- Holdout evaluation with 3-fold CV (Spearman=0.706 on 2526 holdout)
- Position-specific weights for 8 positions (GK/CB/FB/DM/CM/AM/W/ST)
- Availability caps (0.18-0.20) preventing attendance-driven gaming
- Robust team aggregation (capped minutes + core rotation)
- Coverage confidence gates (HIGH/MEDIUM/LOW)
- Finishing shrinkage (empirical Bayes, K=50)
- Truth label schema and validation (`player_truth_labels.parquet`)
- Rating feature matrix with missing-field flags and position-median fallback
- Neural network candidate entry (`scoutfootball train-rating-nn`)

### Match Prediction

- Independent Poisson baseline with attack-defense parameters
- Dixon-Coles (1997) bivariate Poisson with low-score tau correction
- Time decay weighting (configurable half-life)
- Rolling backtest framework with time-series cross-validation
- Calibration metrics: log loss, Brier score, RPS, low-score analysis

### Frontend (Liquid Glass)

- 14-view static analysis workbench with geometric Unicode icon system
- 7 analysis views: Overview, Players, Value, Matches, Scouting, Action Values, Reports
- 4 World Cup views: Schedule, Squads, Compare, Probability
- Electronic tactical board with 15 object types, 12 formations, 6 pitch types
- Animation system: step-based, Bezier paths, ghost silhouettes, trails
- Export: PNG, PDF (print), WebM animation, MP4 (via backend ffmpeg)
- Set-piece templates, training drills, coaching points, teaching mode
- Security: HTML escaping, CSV formula injection guard, CSP meta tag, SRI, schema sanitizer

### Streamlit Console

- 15-page workbench with artifact overview, player rankings, value deviation, match prediction, scouting queue, action value samples, and World Cup pages
- Dixon-Coles vs Poisson model comparison
- Calibration visualization with Brier decomposition

### API

- FastAPI read-only backend with 20+ endpoints
- Player profiles, rating snapshots, match predictions, review queue, watchlist, shortlist
- Action value samples, model run registry, World Cup data
- License attribution and data source manifest
- CORS configurable via environment variable

### Action Value (StatsBomb)

- StatsBomb events → InternalAction (SPADL-compatible) → xT pipeline
- 12 standardized action types with 0-100 normalized coordinates
- Player xT rankings, team xT heatmaps
- StatsBomb Open Data attribution in all exports

### Scouting Workflow

- Review queue with auto-detection of low-confidence, low-appearance, role-remap, weak-coverage players
- Watchlist and shortlist with review status flow
- Watchlist diff between rating snapshots
- CSV export from all scouting views

### Documentation

- README with English/Chinese bilingual sections
- MODEL_CARD.md: data sources, label definitions, known biases, unavailable scenarios
- ALGORITHM.md: rating formula, position weights, league coefficients, Dixon-Coles
- DATA_CONTRACTS.md: all Parquet schemas, API contracts, cross-provider schema reference, socceraction evaluation
- EVALUATION.md: baselines, metrics, error analysis

### Desktop App

- Electron + PyInstaller packaging for macOS (arm64)
- Bundled Python backend, frontend, and pre-computed data (~12MB)
- Auto-update via GitHub releases (electron-updater)
- System tray integration
- One-command build: `bash scripts/build-desktop.sh --mac`
- Output: 221MB .dmg for Apple Silicon Macs

### Testing

- 582 tests across 40 test files (575 unit + 5 integration + 2 skipped)
- Coverage: action value schema, calibration, match prediction, backtests, scouting queue, cross-provider schema, frontend security, rating regression, position metrics, and more

### Known Limitations

See `docs/MODEL_CARD.md` and the "Known Limitations" section in README for details.

- Player truth labels are empty; supervised training paths skip by default
- Action value metrics are StatsBomb sample only (not full league coverage)
- World Cup views contain demo/sample data pending official squad rosters
- Rating system is still in calibration phase; strong teams may be systematically undervalued
- FBref data limited to 5 seasons; coarse position mapping needs StatsBomb/formation data to improve

### Post-Release Fixes (2026-06-12)

- **Release workflow**: Removed `publish` block from `desktop/package.json` (was causing `GH_TOKEN` error in electron-builder); fixed Windows `Join-Path` syntax (4 args → nested calls); added `-p never` to Windows electron-builder; made pipeline step `continue-on-error` with `shell: bash`
- **Test environment**: Removed broken torch namespace package (25 tests recovered from FAILED); added `httpx` dev dependency (integration tests were failing to collect); fixed `api_server.py` version from hardcoded `0.2.0` to `__version__`
- **Lint**: Removed unused `enrich_squad_with_ratings` import from `api.py`
