# Codex Continuous Development State

## Recently Merged

- **v1.0.3 (2026-07-11):**
  1. **Server-side scouting workspace persistence:** `ScoutingWorkspaceStore` with REST endpoints, If-Match optimistic concurrency, atomic writes, immutable backups, loopback access control.
  2. **H2H form trend momentum and rating:** `compute_form_trend()` computing momentum, form_rating (0-100), trend_label, goals trends, clean sheets, and cumulative points sparkline; frontend form trend card with SVG sparkline.
  3. **Multi-section player scouting report export (CSV/JSON):** replaced single-row CSV with 8-section scouting report; fixed `position_percentiles` field name bug and radar label mismatch (Volume/Overall → Reliability/Impact).
  4. **Player comparison CSV export:** comparison result panel now exports multi-section CSV covering profiles, radar, stats, and percentiles.
- **Search autocomplete and offline compare fallback (#42):** prefix-first player/team suggestions, keyboard navigation, TTL-backed data loaders, and static player/team comparison pairs.
- **H2H history and recent form (#43):** Football-Data matchup history, alias-safe results, recent-form comparison, 40 static fallback pairs, responsive frontend states, validated query limits, and cached match normalization.
- **Match-level action-value evidence (#44):** player→match→action xT drill-down, pass/carry/shot and zone/time splits, API/static fallback, mobile overflow repair, and explicit three-match sample boundaries.

## Current Development

- v1.0.3 release complete; preparing next round.

## Known Blockers

- None.

## Next Round Candidates

1. Add browser integration coverage for scouting, action-value, API/static empty states, and mobile breakpoints.
2. Generate a versioned full match-action artifact with dates, minutes, competition coverage, and independent evaluation.
3. Enrich match prediction with Dixon-Coles time decay and calibration backtest (Brier/RPS/log loss) comparison page.
4. Add shortlist notes persistence and watchlist diff in the scouting workflow.
5. Surface model-run registry with complete parameters, random seeds, dependency versions, input hashes, and error-case summaries in the report page.
