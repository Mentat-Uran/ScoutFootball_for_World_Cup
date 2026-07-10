# Codex Continuous Development State

## Last Updated
2026-07-10

## Recently Merged (5 PRs in this session)
- **PR #38 - Team Strength Analysis**: New `GET /teams/strength` API and frontend "Teams" view with minutes-weighted team ratings, position group breakdowns, top players, and ECharts stacked bar chart. Also fixed scouting queue caching, MP4 upload limit, pipeline dead code, and Path import.
- **PR #39 - Player Comparison + VAEP + Calibration**: New `GET /players/compare` API and frontend "Compare" view with dual-player radar overlay and metric diff tables. Fixed VAEP player_id→name mapping via xT bridge. Replaced permanent lru_cache with 5-minute TTL cache on calibration.
- **PR #40 - Team Comparison**: New `GET /teams/compare` API and frontend team comparison section with dual-team radar overlay, position group diff table, and top player comparison.
- **PR #41 - Action Value Drill-down & VAEP Identity Mapping**: VAEP identity enrichment via xT player_id+team_id bridge with team names, season/competition context, coverage report (mapped/partial/unmapped). Frontend action-value explorer with team/season/competition/minutes/search filters, identity coverage summary, unmapped player ID fallback.
- **PR #42 - Search Autocomplete & Static Fallback**: New `GET /search?q=&type=&limit=` typeahead endpoint with prefix-first/substring-fallback matching. Frontend `SearchTypeahead` component wired to 5 inputs (global player search, player compare A/B, team compare A/B) with 300ms debounce and keyboard navigation. Migrated data loaders (`_load_all_player_ratings`, `load_model_meta`, `load_league_metrics`, `load_player_value_metrics`, `_wc_cache`) from permanent `lru_cache` to configurable TTL cache (default 300s via `SCOUTFOOTBALL_CACHE_TTL_SECONDS`) with `force_refresh` support. Extended `scripts/export_static_frontend_data.py` with a `compare` section generating `player_compare_pairs.json` and `team_compare_pairs.json` for offline compare fallback. CI now checks `frontend/action-value-explorer.js` syntax and runs `frontend/tests/*.test.js`.

## Test Status
- Full test suite: 750+ tests passing
- ruff check: clean
- Frontend syntax: clean

## Next Round Candidates
1. **Action value three-level drill-down**: Transform flat action value leaderboard into player → team → match drill-down with pass/carry/shot breakdowns.
2. **Server-side scouting write-back**: Add POST endpoints for scouting workspace persistence (ROADMAP Phase B).
3. **Duplicate endpoint cleanup**: Remove `/prediction/{home}/{away}`, `/ratings/snapshots` aliases if no longer used by frontend.
4. **Apply TTL cache pattern to remaining loaders**: Extend TTL cache migration to `load_player_rolling`, `load_team_rolling`, and any other loaders still on permanent `lru_cache`.
5. **Frontend browser integration tests in CI**: Add real browser flow tests for scouting and action-value views, covering API, static, empty data, and mobile breakpoints (carried over from TASKS.md P1.1).
6. **Match head-to-head history view for prediction page**: Surface recent head-to-head results and form alongside the existing Independent Poisson prediction.
