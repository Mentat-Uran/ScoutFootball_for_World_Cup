# Codex Continuous Development State

## Last Updated
2026-07-10

## Recently Merged
- **Team Strength Analysis** (2026-07-10): New `GET /teams/strength` API endpoint and frontend "Teams" view with minutes-weighted team ratings, position group breakdowns (GK/DEF/MID/ATT), top players per team, and ECharts stacked bar chart.
- **Scouting queue caching**: Fixed redundant `build_scouting_queues()` calls across review/watchlist/shortlist endpoints.
- **MP4 upload limit**: Added 50MB size limit on tactical board MP4 export endpoint.
- **Pipeline dead code fix**: Implemented actual score log-loss tracking in DC calibration report (was a `pass` placeholder).
- **Import fix**: Moved `Path` import to top of `api_server.py`.

## Currently In Development
- Branch: `codex/team-strength-analysis`
- Status: Ready for PR

## Known Blockers
- None currently.

## Next Round Candidates
1. **VAEP player_id → player_name mapping**: Action values only show raw player_ids. Need a lookup table connecting VAEP player_ids to the player ratings ecosystem.
2. **Action value three-level drill-down**: Transform the flat action value leaderboard into player → team → match drill-down with pass/carry/shot breakdowns.
3. **Server-side scouting write-back**: Add POST endpoints for scouting workspace persistence (ROADMAP Phase B).
4. **Player comparison tool**: Side-by-side player comparison with radar chart overlay and metric diff table.
5. **Duplicate endpoint cleanup**: Remove `/prediction/{home}/{away}`, `/ratings/snapshots`, `/reports/model-runs` aliases.
6. **Calibration cache invalidation**: `@lru_cache(maxsize=1)` on `get_prediction_calibration()` returns stale data after model retraining.
