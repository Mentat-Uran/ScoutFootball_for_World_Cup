# Codex Continuous Development State

## Recently Merged

- **Search autocomplete and offline compare fallback (#42):** prefix-first player/team suggestions, keyboard navigation, TTL-backed data loaders, and static player/team comparison pairs.
- **H2H history and recent form (#43):** Football-Data matchup history, alias-safe results, recent-form comparison, 40 static fallback pairs, responsive frontend states, validated query limits, and cached match normalization. Full local verification covered 920 Python tests, 13 integration tests, 31 frontend tests, CLI validation, and live/static browser flows.
- **Match-level action-value evidence (#44):** player→match→action xT drill-down, pass/carry/shot and zone/time splits, API/static fallback, mobile overflow repair, and explicit three-match sample boundaries. Local verification covered 934 Python tests, 13 integration tests, 33 frontend tests, CLI validation, and live/static browser flows.

## Current Development

- Preparing the next round from updated `main`; no uncommitted follow-up feature is carried in this state file.

## Known Blockers

- None.

## Next Round Candidates

1. Add server-side, versioned scouting workspace persistence with conflict-safe import semantics.
2. Add browser integration coverage for scouting, action-value, API/static empty states, and mobile breakpoints.
3. Generate a versioned full match-action artifact with dates, minutes, competition coverage, and independent evaluation.
4. Enrich match prediction with xG/form trends only where source coverage is explicit.
