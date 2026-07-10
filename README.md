# ScoutFootball for World Cup

## link
https://scoutfootball.vercel.app/

> **Your local-first football analytics toolkit for the 2026 FIFA World Cup.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-Fast-magenta)](https://github.com/astral-sh/uv)
[![DuckDB](https://img.shields.io/badge/DuckDB-Fast%20Analytics-yellow)](https://duckdb.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-Optimized-ee4c2c)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)](https://streamlit.io/)

**English** | **[中文](docs/README_ZH.md)**

---

### The 2026 World Cup Is Coming

The 2026 FIFA World Cup kicks off June 11 across the US, Canada, and Mexico — 48 teams, 104 matches, one trophy. ScoutFootball for World Cup is built to help you make sense of it all: who's overperforming, who's flying under the radar, and what the numbers say about every squad.

### What It Does

ScoutFootball is a local-first football analytics platform that turns public data, manual imports, interpretable player ratings, and match predictions into a reproducible research pipeline.

The focus right now: upgrading the rating system into an interpretable, evaluable scouting tool — fixing true impact labels and training targets first, then integrating event action values, football-specific visualizations, and model cards.

### Core Capabilities

- **Pipeline:** End-to-end `ingest` -> `build-features` -> `train`.
- **Data Validation:** `scoutfootball validate` checks data integrity before training.
- **Local Data Layer:** DuckDB + Parquet, organized into raw/silver/gold/models/reports/logs.
- **Player Ratings:** PyTorch optimizer with composite objective (Spearman + soft NDCG@20 + position consistency + train-fitted points/league calibration + distribution/tail/league-bias losses + player-score guardrails + optional player truth-label anchor), holdout evaluation, availability caps, quality caps, robust team pooling, coverage reports, and model run registry.
- **Truth Label Contracts:** Schema and validation for `player_truth_labels.parquet` — transfermarkt value, awards, expert tiers, manual calibration. The current local table has 41,389 rows, but label independence and temporal evaluation remain release gates.
- **Neural Rating Candidate:** `scoutfootball train-rating-nn` trains a supervised sklearn MLP candidate from `rating_feature_matrix.parquet` + `player_truth_labels.parquet` and writes artifacts to `data/models/player_rating_nn/`; it does not replace `player_ratings_optimized.parquet` unless it beats the current optimizer on the same holdout and baseline checks.
- **Model Evaluation & Cards:** Data sources, label definitions, bounds, and known biases documented in `docs/MODEL_CARD.md`.
- **Match Prediction:** Independent Poisson baseline with score probability matrices, plus Football-Data head-to-head history and recent-form comparison with offline snapshots.
- **Product & Visuals:** 15-page Streamlit console with artifact overview, scouting queue, and action-value sample pages. Liquid Glass static frontend with 7 analysis views (Overview, Players, Value, Matches, Scouting, Action Values, Reports), 4 World Cup views (Schedule, Squads, Compare, Probability), and a first-slice local tactical board. FastAPI read-only backend serves artifacts, player profiles, rating snapshots, predictions, review queue, watchlist, shortlist, action-value samples, and model runs. `mplsoccer` powers pitch plots, pizza charts, and shot maps. The scouting desk exports and imports a versioned browser-local workspace with revision/timestamp audit fields, import previews, conflict detection, safe merge, and explicit replacement. Frontend rendering escapes API/local JSON strings, CSV exports guard against spreadsheet formula injection, and tactical-board JSON imports pass through a schema sanitizer. API status pill distinguishes LIVE / STATIC / OFFLINE; review queue is paginated (50 per page); NaN/undefined values are guarded; static export no longer writes repr strings for dataclass/Pydantic responses.

### Liquid Glass Frontend

The `frontend/` directory contains a static analysis workbench with a consistent geometric icon system (no emojis). All navigation icons use minimal Unicode symbols (◎ ◇ € △ □ ⌁ ▣ ⬡ ⊕ ⟷ ⊞) for visual consistency. API, local Parquet-derived JSON, demo strings, and imported tactical-board project fields are escaped or sanitized before entering HTML.

**7 Analysis Views:**

| View | Description | Data Source |
| --- | --- | --- |
| **Overview** (◎) | Artifact registry, data health, coverage metrics | `/artifacts` API |
| **Players** (◇) | Player pool, radar charts, position percentiles | `/ratings`, `/players/{name}` API |
| **Value** (€) | Value deviation scatter, over/under-valued rankings | `/value-summary` API |
| **Matches** (△) | Match prediction, score probability matrix, head-to-head history and recent form | `/predictions/{home}/{away}`, `/predictions/{home}/{away}/h2h` API |
| **Scouting** (□) | Review queue filters, local status/notes, watchlist snapshots, CSV plus versioned workspace import/export | `/review-queue`, `/watchlist`, `/shortlist` API + browser-local workspace JSON |
| **Actions** (⌁) | xT/VAEP ranking, sample filters, tactical heatmap handoff | `/action-values` API |
| **Reports** (▣) | Model runs, backend contracts, metrics | `/reports/model-runs` API |

**4 World Cup Views:**

| View | Description |
| --- | --- |
| **Schedule** (⬡) | Group stage fixtures, team groups, venues |
| **Squads** (⊕) | Team rosters with club, league, rating, confidence |
| **Compare** (⟷) | Head-to-head team comparison with radar overlay |
| **Probability** (⊞) | Group advancement probabilities, 48-team strength ranking |

### Live Demo

**https://scoutfootball.vercel.app/**

Frontend hosted on Vercel, backend on Render (free tier — first request may take ~30s to wake up).

### LAN / Campus Network Deployment

For access from other devices on the same campus network, run the backend on your computer and let it serve both the frontend and API:

```bash
uv sync
uv run python -m scoutfootball serve --host 0.0.0.0 --port 8000
```

Then open `http://YOUR-PC-IP:8000` from another device on the same network.

Windows users can use:

```bat
scripts\start-lan.bat
```

Notes:

- `frontend/` is mounted by FastAPI at `/`, so one port is enough.
- Local/LAN deployments now default to same-origin API mode.
- A plain static server falls back to the tracked JSON snapshot under `frontend/data/` when mapped API routes return 404.
- Allow TCP `8000` through Windows Firewall, or choose another port if needed.

### Docker Deployment

Build and run the API plus static frontend in one container:

```bash
docker build -t scoutfootball:local .
docker run --rm -p 8000:8000 scoutfootball:local
```

Open `http://localhost:8000` and verify the backend with:

```bash
curl http://localhost:8000/health
```

For local development with your full `data/` directory mounted into the
container:

```bash
docker compose up --build
```

If Docker Hub or apt mirrors are blocked on your local network, override the
build image and skip optional system packages for a smoke test:

```powershell
$env:SCOUTFOOTBALL_PYTHON_IMAGE="mcr.microsoft.com/devcontainers/python:1-3.11-bookworm"
$env:SCOUTFOOTBALL_INSTALL_SYSTEM_PACKAGES="0"
docker compose up --build
```

The container reads `SCOUTFOOTBALL_DATA_ROOT` and defaults it to `/app/data`.
Mounting `./data:/app/data` lets Docker use local Parquet/model artifacts and
write tactical-board exports under `data/reports/tactical_exports/`.

Release builds publish a GHCR image and upload a Docker archive:

```bash
docker pull ghcr.io/mentaturan/scoutfootball_for_world_cup:latest
docker run --rm -p 8000:8000 ghcr.io/mentaturan/scoutfootball_for_world_cup:latest
```

### Static Snapshot Layout

- `frontend/data/` is the tracked release snapshot used by the static demo and refreshed by GitHub Actions.
- `frontend/local-data/` is the ignored local snapshot for ad-hoc exports on your machine.

Local export:

```bash
uv run python scripts/export_static_frontend_data.py
uv run python scripts/compute_worldcup_predictions.py
```

Release export:

```bash
uv run python scripts/export_static_frontend_data.py --profile release
uv run python scripts/compute_worldcup_predictions.py --profile release
```

### Demo Data

The frontend falls back to built-in demo data when the FastAPI backend is unavailable or when specific artifacts are missing. Views using demo data display a **DEMO** badge.

To see real data:

```bash
# 1. Start the FastAPI backend (serves local Parquet/DuckDB artifacts)
PYTHONPATH=src uv run python -m scoutfootball serve

# 2. In another terminal, start the frontend
python3 -m http.server 8600 --directory frontend

# 3. Open http://localhost:8600 in your browser
```

To generate the rating artifacts the frontend reads:

```bash
uv sync
PYTHONPATH=src uv run python -m scoutfootball ingest
PYTHONPATH=src uv run python -m scoutfootball build-features
PYTHONPATH=src uv run python -m scoutfootball train

# Optional supervised NN candidate; skips until player_truth_labels has enough rows
PYTHONPATH=src uv run python -m scoutfootball train-rating-nn
```

### World Cup Readiness

| Feature | Status |
| --- | --- |
| 48-team squad rating coverage | In progress — current data covers Big 5 leagues; World Cup squads need additional league data |
| Match prediction (Independent Poisson) | Working baseline |
| Player radar / pizza chart | Available via mplsoccer |
| Position-relative rankings | Available with confidence badges |
| Score probability matrix | Available in Streamlit |
| Electronic tactical board | Local canvas, animation, PNG/PDF/WebM/GIF export, optional MP4, report snapshots, and schema migration available |
| Dixon-Coles with time decay | Implemented baseline with calibration metrics |

### Current Known Limitations

**Rating System:**
- Truth labels exist, but Transfermarkt-derived and self-referential labels are not an independent proof of player impact
- Rating system is in calibration phase; strong teams (Barcelona, Real Madrid) may be systematically undervalued
- League intercept bias exists (Serie A -16.6, Ligue 1 -11.3)

**Data Coverage:**
- Action value artifacts contain 15,062 xT/VAEP rows derived from the current StatsBomb Open Data sample; they are not full-league coverage
- FBref data limited to 5 seasons; coarse position mapping needs StatsBomb/formation data
- World Cup squads are populated, but rating coverage remains incomplete outside the major leagues

**Frontend:**
- Frontend falls back to a tracked static snapshot when mapped API routes are unavailable; it is cached data, not live data
- API status pill shows LIVE (API online), STATIC (fallback from snapshot), or OFFLINE (neither available)
- Review queue is paginated at 50 items per page to avoid rendering thousands of cards at once
- Scouting review states and notes remain browser-local, but they can be moved or backed up with the versioned workspace JSON. Audit metadata records local revisions and timestamps; it is not a server-side identity or cross-device audit service.
- Some VAEP rows only have `player_id`; identity mapping remains incomplete
- Tactical board MP4 export requires ffmpeg installed on the system

**Not Included in v1.0:**
- Spatial/video analysis (StatsBomb 360, tracking data)
- Real-time collaboration on tactical board
- Mobile-optimized tactical board editing

### Electronic Tactical Board

The tactical board is available as a local-first coaching and analysis workspace inside `frontend/`, aligned with products such as [Tactico](https://tactico.pro/), [DrawTactics](https://drawtactics.com/animated-tactics-board), [TacticSlate](https://tacticslate.com/football-tactic-board), [JLA Tactics Board](https://jlatacticsboard.com/), and [Metrica Tactical Boards](https://www.metrica-sports.com/help-center/tactical-boards). It includes normalized pitch coordinates, formations and set pieces, drawing tools, frame/path animation, local JSON projects, schema migration, report snapshots, and PNG/PDF/WebM/GIF export. MP4 remains an optional local-backend capability requiring ffmpeg; public links, cloud sync, video telestration, tracking import, and real-time collaboration remain later work.

Long-term sequencing and engineering gates are documented in [`docs/ROADMAP.md`](docs/ROADMAP.md).

The remaining P1.5 work is release hardening and selective sharing: clipboard image export, read-only local presentation links, stricter migration fixtures, and browser CI. Cloud sync, video telestration, tracking-data import, 2D/3D synchronized views, live collaboration, and behind-goal views remain later extensions.

### Desktop App (macOS)

A standalone desktop application is available for macOS (Apple Silicon / arm64). It bundles the Python backend, frontend, and pre-computed data into a single native app with auto-update support.

| Feature | Status |
|---|---|
| macOS arm64 (.dmg) | Built and verified |
| Auto-update via GitHub releases | Implemented (electron-updater) |
| System tray | Implemented |
| Bundled data | Player ratings, match results, models |
| Windows build | Not yet (requires Windows machine) |

Build from source:

```bash
cd desktop && npm install
bash scripts/build-desktop.sh --mac
```

Output: `desktop/dist/ScoutFootball-1.0.0-arm64.dmg`

### Local Data Overview

| Source | Cache | Coverage |
| --- | --- | --- |
| **FBref** | 14,356 rows per table | 5 seasons, standard/shooting/misc |
| **Football-Data** | 68,953 raw CSV rows | 10 seasons, 20 divisions |
| **Understat** | 31,902 player-season rows | 10 seasons, 6 leagues |
| **StatsBomb Open Data** | 126 matches / 11,871 events | Public match & event sample |
| **Ratings** | 30,483 rows | Optimized player ratings |
| **Feature Matrix** | 8,141 rows | With missing-field flags and position-median fallback |

### Architecture

10-layer roadmap. Layers 1-7 are the current trunk; 8-10 expand into scouting workflows, prediction calibration, and spatial/video research:

1. **Data & Compliance** — caching, cleaning, merging
2. **Standard Facts** — unified entities (matches, players, events)
3. **Cross-Provider Standardization** — SPADL, kloppy/floodlight compatibility
4. **Event Action Value** — xT -> VAEP
5. **Player Truth & Rating** — model cards, truth labels, season stats
6. **Evaluation & Reporting** — baselines, error analysis
7. **Product & API** — FastAPI, Streamlit, mplsoccer, electronic tactical board
8. **Scout Decision** — watchlist, expert review queue, tactical notes
9. **Score Prediction & Calibration** — Dixon-Coles + time decay
10. **Spatial/Video/Off-Ball** — StatsBomb 360, tracking, xG+

### Quick Start

**Prerequisites:** Python 3.11+ and [uv](https://docs.astral.sh/uv/) (fast Python package manager).

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/Mentaturan/ScoutFootball_for_World_Cup.git
cd ScoutFootball_for_World_Cup
uv sync

# One-command demo (validates data, runs pipeline, starts servers)
bash scripts/demo.sh

# Or step by step:
PYTHONPATH=src uv run python -m scoutfootball info      # Project info
PYTHONPATH=src uv run python -m scoutfootball validate   # Validate data
PYTHONPATH=src uv run python -m scoutfootball ingest     # Ingest data
PYTHONPATH=src uv run python -m scoutfootball build-features
PYTHONPATH=src uv run python -m scoutfootball train      # Train ratings

# Start web UI (two terminals)
PYTHONPATH=src uv run python -m scoutfootball serve      # API on :8600
python3 -m http.server 8601 --directory frontend         # Frontend on :8601
```

Open http://localhost:8601 for the Liquid Glass frontend, or run Streamlit:

```bash
uv run streamlit run src/scoutfootball/app/streamlit_app.py
```

**First run note:** The pipeline will download and cache public data on first run. This requires an internet connection. Subsequent runs use local cache.

### Tech Stack & Compliance

- **Stack:** Python, uv, DuckDB + Parquet, pandas, scikit-learn, Streamlit, Plotly, mplsoccer, FastAPI, PyTorch.
- **Compliance:**
  - No CAPTCHA bypass or aggressive scraping.
  - Commercial sources (Transfermarkt etc.) only via manual or authorized import.
  - Public StatsBomb Open Data derivatives must attribute the source.

---
*ScoutFootball for World Cup — built for the beautiful game's biggest stage.*
