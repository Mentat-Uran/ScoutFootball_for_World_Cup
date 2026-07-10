# Codex Continuous Development State

## Last Updated
2026-07-10

## Recently Merged
- **Team Strength Analysis** (PR #38, 2026-07-10): New `GET /teams/strength` API endpoint and frontend "Teams" view with minutes-weighted team ratings, position group breakdowns (GK/DEF/MID/ATT), top players per team, and ECharts stacked bar chart.
- **Scouting queue caching** (PR #38): Fixed redundant `build_scouting_queues()` calls across review/watchlist/shortlist endpoints.
- **MP4 upload limit** (PR #38): Added 50MB size limit on tactical board MP4 export endpoint.
- **Pipeline dead code fix** (PR #38): Implemented actual score log-loss tracking in DC calibration report (was a `pass` placeholder).
- **Import fix** (PR #38): Moved `Path` import to top of `api_server.py`.

## Currently In Development
- Branch: `codex/player-comparison-vaep-mapping`
- Status: Ready for PR
- Contents:
  - New Feature: Player comparison API (`GET /players/compare`) with radar overlay, position percentile diff, and stats comparison
  - New Feature: Frontend "Compare" view with dual-input search, ECharts radar chart, and comparison tables
  - Bug Fix: VAEP player_id → player_name mapping via xT bridge and events_all.parquet
  - Bug Fix: Calibration cache invalidation (replaced `@lru_cache(maxsize=1)` with 5-minute TTL cache)

## Known Blockers
- None currently.

## Next Round Candidates
1. **Action value three-level drill-down**: Transform the flat action value leaderboard into player → team → match drill-down with pass/carry/shot breakdowns.
2. **Server-side scouting write-back**: Add POST endpoints for scouting workspace persistence (ROADMAP Phase B).
3. **Duplicate endpoint cleanup**: Remove `/prediction/{home}/{away}`, `/ratings/snapshots`, `/reports/model-runs` aliases.
4. **Team comparison tool**: Extend team strength analysis with head-to-head team comparison view.
5. **Player search enhancement**: Add autocomplete/suggestions to player search inputs.
6. **Static data export for compare endpoint**: Generate static fallback data for player comparisons.
