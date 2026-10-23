# Codex Continuous Development State

## Recently Merged

- **World Cup Knockout Bracket Predictor (2026-07-11):**
  1. **Backend:** `simulate_knockout()` in `worldcup/data.py` — Bradley-Terry strength model with Monte Carlo tournament win probability (10,000 simulations, seeded for reproducibility). Projects Round of 32 → Round of 16 → Quarter-Finals → Semi-Finals → Final with per-match win probabilities.
  2. **API:** `GET /world-cup/knockout` endpoint returning full bracket structure and top-16 tournament win probability.
  3. **Frontend:** New "Knockout" (淘汰赛) view with 5-column bracket display, winner highlighting, probability bars, and tournament win probability table. Mobile-responsive single-column layout. Chinese/English bilingual support.
  4. **Static export:** `knockout.json` added to `export_static_frontend_data.py` for offline fallback.
  5. **Tests:** 24 unit tests covering match probability model, group finish prediction, seeding, bracket structure, Monte Carlo reproducibility, and edge cases.
- **v1.0.3 (2026-07-11):**
  1. **Server-side scouting workspace persistence:** `ScoutingWorkspaceStore` with REST endpoints, If-Match optimistic concurrency, atomic writes, immutable backups, loopback access control.
  2. **H2H form trend momentum and rating:** `compute_form_trend()` computing momentum, form_rating (0-100), trend_label, goals trends, clean sheets, and cumulative points sparkline; frontend form trend card with SVG sparkline.
  3. **Multi-section player scouting report export (CSV/JSON):** replaced single-row CSV with 8-section scouting report; fixed `position_percentiles` field name bug and radar label mismatch (Volume/Overall → Reliability/Impact).
  4. **Player comparison CSV export:** comparison result panel now exports multi-section CSV covering profiles, radar, stats, and percentiles.
- **Search autocomplete and offline compare fallback (#42):** prefix-first player/team suggestions, keyboard navigation, TTL-backed data loaders, and static player/team comparison pairs.
- **H2H history and recent form (#43):** Football-Data matchup history, alias-safe results, recent-form comparison, 40 static fallback pairs, responsive frontend states, validated query limits, and cached match normalization.
- **Match-level action-value evidence (#44):** player→match→action xT drill-down, pass/carry/shot and zone/time splits, API/static fallback, mobile overflow repair, and explicit three-match sample boundaries.

## Current Development

- World Cup knockout bracket predictor complete; preparing PR and next round.

## Known Blockers

- None.

## Next Round Candidates

1. Enrich match prediction with Dixon-Coles time decay and calibration backtest (Brier/RPS/log loss) comparison page.
2. Add shortlist notes persistence and watchlist diff in the scouting workflow.
3. Surface model-run registry with complete parameters, random seeds, dependency versions, input hashes, and error-case summaries in the report page.
4. Generate a versioned full match-action artifact with dates, minutes, competition coverage, and independent evaluation.
5. Add browser integration coverage for scouting, action-value, API/static empty states, and mobile breakpoints.
