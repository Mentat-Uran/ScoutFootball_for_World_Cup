"""FastAPI application factory for ScoutFootball API server."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from scoutfootball import __version__
from scoutfootball.api import (
    _clean_json_value,
    _settings,
    get_action_value_summary,
    get_artifacts_summary,
    get_match_prediction,
    get_match_prediction_dc,
    get_model_run_detail,
    get_model_runs,
    get_player_profile,
    get_player_ratings,
    get_prediction_calibration,
    get_prediction_summary,
    get_ratings_meta,
    get_review_queue,
    get_shortlist,
    get_team_strength,
    get_value_summary,
    get_watchlist,
    get_wc_groups,
    get_wc_predictions,
    get_wc_schedule,
    get_wc_squad,
    get_wc_teams,
    get_world_cup_match_prediction,
    health_check,
    list_players,
    list_teams,
)

_DEFAULT_CORS_ORIGINS = [
    "https://scoutfootball.vercel.app",
    "https://scoutfootball-for-world-cup.vercel.app",
    "http://localhost:8600",
    "http://127.0.0.1:8600",
    "http://localhost:8601",
    "http://127.0.0.1:8601",
    "http://localhost:8000",
]


def _cors_origins() -> list[str]:
    """Read allowed CORS origins from SCOUTFOOTBALL_CORS_ORIGINS env var."""
    raw = os.environ.get("SCOUTFOOTBALL_CORS_ORIGINS", "")
    if raw.strip():
        return [o.strip() for o in raw.split(",") if o.strip()]
    return _DEFAULT_CORS_ORIGINS


@asynccontextmanager
async def _lifespan(app: FastAPI):
    # Startup: warm up World Cup cache to avoid 40-50s first-request delay
    import logging
    logger = logging.getLogger(__name__)
    try:
        import time

        from scoutfootball.api import _get_wc_enriched_squads

        t0 = time.time()
        _get_wc_enriched_squads()
        logger.info("WC cache warmed up in %.1fs", time.time() - t0)
    except Exception as e:
        logger.warning("WC cache warmup failed (will compute on first request): %s", e)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="ScoutFootball API",
        version=__version__,
        description="Local-first football data research platform API",
        lifespan=_lifespan,
    )

    # Configurable CORS — set SCOUTFOOTBALL_CORS_ORIGINS env var for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # Global exception handler — return JSON instead of raw traceback
    import logging

    from fastapi.responses import JSONResponse

    logger = logging.getLogger(__name__)

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error("Unhandled exception: %s", exc, exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    @app.get("/health")
    def health():
        return health_check()

    @app.get("/license")
    def license_info():
        artifacts = get_artifacts_summary()
        artifact_list = artifacts.get("artifacts", [])
        updated = artifact_list[0].get("updated_at") if artifact_list else None
        return {
            "license_attribution": artifacts.get("license_attribution", {}),
            "data_source_label": artifacts.get("data_source_label", ""),
            "updated_at": updated,
        }

    @app.get("/players")
    def players():
        return list_players()

    @app.get("/teams")
    def teams_list():
        return {"teams": list_teams()}

    @app.get("/teams/strength")
    def teams_strength(
        league: str | None = None,
        season: str | None = None,
        limit: int = 100,
    ):
        return get_team_strength(league=league, season=season, limit=limit)

    @app.get("/prediction/{home_team}/{away_team}")
    def prediction(home_team: str, away_team: str, model: str = "poisson"):
        if model == "dixon_coles":
            return get_match_prediction_dc(home_team, away_team)
        return get_match_prediction(home_team, away_team)

    @app.get("/predictions/{home_team}/{away_team}")
    def predictions(home_team: str, away_team: str, model: str = "poisson"):
        if model == "dixon_coles":
            return get_match_prediction_dc(home_team, away_team)
        return get_match_prediction(home_team, away_team)

    @app.get("/predictions/meta")
    def predictions_meta():
        return get_prediction_summary()

    @app.get("/predictions/calibration")
    def predictions_calibration():
        return get_prediction_calibration()

    @app.get("/value-summary")
    def value_summary():
        return get_value_summary()

    @app.get("/action-values")
    def action_values(limit: int = 20):
        return get_action_value_summary(limit=limit)

    @app.get("/ratings")
    def ratings(
        position: str | None = None,
        league: str | None = None,
        team: str | None = None,
        season: str | None = None,
        limit: int = 20000,
    ):
        return get_player_ratings(
            position=position, league=league, team=team, season=season, limit=limit,
        )

    @app.get("/ratings/snapshots")
    def rating_snapshots(
        position: str | None = None,
        league: str | None = None,
        team: str | None = None,
        season: str | None = None,
        limit: int = 20000,
    ):
        return get_player_ratings(
            position=position, league=league, team=team, season=season, limit=limit,
        )

    @app.get("/ratings/meta")
    def ratings_meta():
        return get_ratings_meta()

    @app.get("/player/{player_name}/profile")
    def player_profile(player_name: str, season: str | None = None):
        return get_player_profile(player_name, season=season)

    @app.get("/players/{player_name}")
    def player_detail(
        player_name: str,
        season: str | None = None,
        position_group: str | None = None,
        limit: int = 50,
        offset: int = 0,
        format: str = "json",
    ):
        from fastapi.responses import PlainTextResponse

        result = get_player_profile(
            player_name,
            season=season,
            position_group=position_group,
            limit=limit,
            offset=offset,
            fmt=format,
        )
        if format == "csv" and isinstance(result, str):
            return PlainTextResponse(result, media_type="text/csv")
        return result

    @app.get("/artifacts")
    def artifacts():
        return get_artifacts_summary()

    @app.get("/review-queue")
    def review_queue(limit: int = 200):
        return get_review_queue(limit=limit)

    @app.get("/watchlist")
    def watchlist(limit: int = 100):
        return get_watchlist(limit=limit)

    @app.get("/shortlist")
    def shortlist(limit: int = 100):
        return get_shortlist(limit=limit)

    @app.get("/model-runs")
    def model_runs():
        return get_model_runs()

    @app.get("/reports/model-runs")
    def report_model_runs():
        return get_model_runs()

    @app.get("/reports/model-runs/{run_id}")
    def report_model_run_detail(run_id: str):
        return get_model_run_detail(run_id)

    # ── World Cup endpoints ──────────────────────────────────────────────

    @app.get("/world-cup/groups")
    def wc_groups():
        return get_wc_groups()

    @app.get("/world-cup/schedule")
    def wc_schedule(group: str | None = None, matchday: int | None = None):
        return get_wc_schedule(group=group, matchday=matchday)

    @app.get("/world-cup/squads/{team}")
    def wc_squad(team: str):
        return get_wc_squad(team)

    @app.get("/world-cup/predictions")
    def wc_predictions():
        return get_wc_predictions()

    @app.get("/world-cup/predictions/{home_team}/{away_team}")
    def wc_match_prediction(home_team: str, away_team: str):
        return get_world_cup_match_prediction(home_team, away_team)

    @app.get("/worldcup/teams")
    def wc_teams():
        return get_wc_teams()

    # ── Tactical board export helpers ─────────────────────────────
    @app.get("/tactical-board/capabilities")
    def tactical_board_capabilities():
        """Detect available export capabilities (ffmpeg, etc.)."""
        import shutil

        ffmpeg_path = shutil.which("ffmpeg")
        return {
            "ffmpeg_available": ffmpeg_path is not None,
            "ffmpeg_path": ffmpeg_path,
            "supported_formats": {
                "png": True,
                "webm": True,  # MediaRecorder-based, browser-side
                "mp4": ffmpeg_path is not None,
                "gif": True,  # gif.js-based, browser-side
                "pdf": True,  # Browser print-based
            },
            "export_dir": str(
                _settings().data_root / "reports" / "tactical_exports"
            ),
        }

    @app.post("/tactical-board/export/mp4")
    async def tactical_board_export_mp4(request: Request):
        """Convert a WebM file to MP4 using ffmpeg (backend-side)."""
        import shutil
        import subprocess
        import tempfile

        ffmpeg_path = shutil.which("ffmpeg")
        if not ffmpeg_path:
            return _clean_json_value({
                "status": "error",
                "error": "ffmpeg not found on system PATH",
            })

        try:
            body = await request.body()

            # Reject uploads larger than 50 MB to prevent abuse
            if len(body) > 50 * 1024 * 1024:
                return _clean_json_value({
                    "status": "error",
                    "error": "Upload exceeds 50 MB size limit",
                })

            export_dir = _settings().data_root / "reports" / "tactical_exports"
            export_dir.mkdir(parents=True, exist_ok=True)

            # Save uploaded WebM to temp file
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_in:
                tmp_in.write(body)
                tmp_in_path = tmp_in.name

            # Generate output path
            import time

            ts = int(time.time())
            out_path = export_dir / f"tactical-board-{ts}.mp4"

            # Convert using ffmpeg
            result = subprocess.run(
                [
                    ffmpeg_path,
                    "-y",
                    "-i", tmp_in_path,
                    "-c:v", "libx264",
                    "-preset", "fast",
                    "-crf", "23",
                    "-pix_fmt", "yuv420p",
                    str(out_path),
                ],
                capture_output=True,
                timeout=60,
            )

            # Clean up temp file
            Path(tmp_in_path).unlink(missing_ok=True)

            if result.returncode != 0:
                return _clean_json_value({
                    "status": "error",
                    "error": f"ffmpeg failed: {result.stderr.decode()[:200]}",
                })

            return _clean_json_value({
                "status": "ok",
                "path": str(out_path),
                "size_bytes": out_path.stat().st_size,
            })
        except subprocess.TimeoutExpired:
            return _clean_json_value({"status": "error", "error": "ffmpeg timeout (60s)"})
        except Exception as exc:
            return _clean_json_value({"status": "error", "error": str(exc)})

    # Serve frontend static files
    frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
    if frontend_dir.exists():
        app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

    return app


# Module-level app instance for uvicorn / PyInstaller
app = create_app()
