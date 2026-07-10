"""Export ScoutFootball API data to static JSON files for the frontend.

This script calls the service layer in scoutfootball.api directly (no HTTP
server needed) and writes the results to static JSON files.

Used by:
- Local development: ``PYTHONPATH=src python scripts/export_static_frontend_data.py``
- Release export: ``PYTHONPATH=src python scripts/export_static_frontend_data.py --profile release``
- GitHub Actions: ``.github/workflows/export-static-data.yml``
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

# ─ project root ──────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = REPO_ROOT / "frontend"
RELEASE_DATA_DIR = FRONTEND_DIR / "data"
LOCAL_DATA_DIR = FRONTEND_DIR / "local-data"

# Default limits for static-export size control
DEFAULT_RATINGS_LIMIT = 3000
DEFAULT_ACTION_VALUES_LIMIT = 500
DEFAULT_QUEUE_LIMIT = 200
DEFAULT_COMPARE_LIMIT = 10

DATA_DIR = RELEASE_DATA_DIR
WORLDCUP_DIR = DATA_DIR / "worldcup"
SQUADS_DIR = WORLDCUP_DIR / "squads"
MANIFEST_PATH = FRONTEND_DIR / "data_manifest.json"


def configure_output_paths(profile: str) -> None:
    global DATA_DIR, WORLDCUP_DIR, SQUADS_DIR, MANIFEST_PATH

    if profile == "release":
        DATA_DIR = RELEASE_DATA_DIR
        MANIFEST_PATH = FRONTEND_DIR / "data_manifest.json"
    else:
        DATA_DIR = LOCAL_DATA_DIR
        MANIFEST_PATH = FRONTEND_DIR / "local-data-manifest.json"

    WORLDCUP_DIR = DATA_DIR / "worldcup"
    SQUADS_DIR = WORLDCUP_DIR / "squads"


def _team_slug(team_name: str) -> str:
    """Convert a team display name to a safe filename slug."""
    return team_name.replace(" ", "_").replace("/", "_")


def _clean(obj: object) -> object:
    """Recursively convert objects to JSON-safe values.

    Handles Pydantic v1/v2 models, dataclasses, numpy/pandas scalars,
    NaN/inf, and standard containers.  Raises TypeError for objects
    that cannot be safely serialized instead of falling back to str().
    """
    import dataclasses
    try:
        import numpy as np
    except ImportError:
        np = None
    try:
        import pandas as pd
    except ImportError:
        pd = None

    if obj is None:
        return None
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int):
        return obj
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return {str(k): _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if np is not None:
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            f = float(obj)
            if math.isnan(f) or math.isinf(f):
                return None
            return f
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return [_clean(v) for v in obj.tolist()]
    if pd is not None:
        if obj is pd.NA or getattr(obj, "name", None) == "NaT":
            return None
    # Pydantic v2 model
    if hasattr(obj, "model_dump"):
        return _clean(obj.model_dump(mode="json"))
    # Pydantic v1 model
    if hasattr(obj, "dict") and hasattr(obj, "__fields__"):
        return _clean(obj.dict())
    # dataclass
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return _clean(dataclasses.asdict(obj))
    raise TypeError(
        f"Cannot safely serialize {type(obj).__name__!r} object to JSON. "
        f"Add a handler or convert before passing to _clean()."
    )


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(
        _clean(payload),
        ensure_ascii=False,
        separators=(",", ":"),
    )
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == serialized:
            return
    path.write_text(serialized, encoding="utf-8")


def export_ratings(limit: int) -> int:
    """Export full ratings + metadata. Returns record count."""
    from scoutfootball.api import get_player_ratings, get_ratings_meta

    ratings = get_player_ratings(limit=limit)
    meta = get_ratings_meta()
    _write_json(DATA_DIR / "ratings.json", ratings)
    _write_json(DATA_DIR / "ratings_meta.json", meta)
    count = ratings.get("count", 0)
    print(f"  ratings.json: {count} players")
    return count


def export_basics() -> None:
    from scoutfootball.api import (
        get_artifacts_summary,
        health_check,
        list_players,
        list_teams,
    )

    _write_json(DATA_DIR / "health.json", health_check())
    _write_json(DATA_DIR / "artifacts.json", get_artifacts_summary())
    teams = list_teams()
    _write_json(DATA_DIR / "teams.json", {"teams": teams})
    players = list_players()
    _write_json(DATA_DIR / "players_list.json", players)
    pc = (
        players.player_count
        if hasattr(players, "player_count")
        else len(players.get("players", []))
    )

    from scoutfootball.api import get_team_strength

    _write_json(DATA_DIR / "team_strength.json", get_team_strength())
    print(
        f"  health.json, artifacts.json, teams.json ({len(teams)}), "
        f"players_list.json ({pc}), team_strength.json"
    )


def export_value_summary() -> None:
    from scoutfootball.api import get_value_summary

    _write_json(DATA_DIR / "value_summary.json", get_value_summary())
    print("  value_summary.json")


def export_predictions_meta() -> None:
    from scoutfootball.api import get_prediction_calibration, get_prediction_summary

    _write_json(DATA_DIR / "predictions_meta.json", get_prediction_summary())
    _write_json(DATA_DIR / "predictions_calibration.json", get_prediction_calibration())
    print("  predictions_meta.json, predictions_calibration.json")


def export_action_values(limit: int) -> None:
    from scoutfootball.api import get_action_value_summary

    # The API pages xT and VAEP independently, so one call exports the top-N
    # rows for both granularities without a synthetic cross-model offset.
    data = get_action_value_summary(limit=limit, full=True)
    _write_json(DATA_DIR / "action_values.json", data)
    xt_n = len(data.get("xt_players", data.get("players", [])))
    vaep_n = len(data.get("vaep_players", []))
    print(f"  action_values.json (xt={xt_n}, vaep={vaep_n})")


def export_scouting(queue_limit: int) -> None:
    from scoutfootball.api import get_review_queue, get_shortlist, get_watchlist

    _write_json(DATA_DIR / "review_queue.json", get_review_queue(limit=queue_limit))
    _write_json(DATA_DIR / "watchlist.json", get_watchlist(limit=12))
    _write_json(DATA_DIR / "shortlist.json", get_shortlist(limit=12))
    print("  review_queue.json, watchlist.json, shortlist.json")


def export_model_runs() -> None:
    from scoutfootball.api import get_model_runs

    _write_json(DATA_DIR / "model_runs.json", get_model_runs())
    print("  model_runs.json")


def export_worldcup() -> int:
    """Export all World Cup data: teams, groups, schedule, 48 squads, predictions."""
    from scoutfootball.api import (
        get_wc_groups,
        get_wc_predictions,
        get_wc_schedule,
        get_wc_squad,
        get_wc_teams,
    )
    from scoutfootball.worldcup.data import GROUPS

    _write_json(WORLDCUP_DIR / "teams.json", get_wc_teams())
    _write_json(WORLDCUP_DIR / "groups.json", get_wc_groups())
    _write_json(WORLDCUP_DIR / "schedule.json", get_wc_schedule())
    _write_json(WORLDCUP_DIR / "predictions.json", get_wc_predictions())

    # 48 team squads
    squad_count = 0
    for team_name in [t for ts in GROUPS.values() for t in ts]:
        squad = get_wc_squad(team_name)
        filename = f"{_team_slug(team_name)}.json"
        _write_json(SQUADS_DIR / filename, squad)
        squad_count += 1

    print("  worldcup/teams.json, groups.json, schedule.json, predictions.json")
    print(f"  worldcup/squads/*.json ({squad_count} teams)")
    return squad_count


def export_sample_player_profiles(limit: int = 30) -> None:
    """Pre-export top-N player profiles so click-to-detail works offline."""
    from scoutfootball.api import get_player_profile, get_player_ratings

    ratings = get_player_ratings(limit=limit)
    players = ratings.get("players", [])
    profiles_dir = DATA_DIR / "player_profiles"
    exported = 0
    for player in players:
        name = player.get("player") or player.get("player_name")
        if not name:
            continue
        try:
            profile = get_player_profile(name)
            # Skip profile-only artifacts that are too big or failed
            _write_json(profiles_dir / f"{_team_slug(name)}.json", profile)
            exported += 1
        except Exception:
            continue
    print(f"  player_profiles/*.json ({exported} players)")


def _meaningful_pair_indices(n: int, max_pairs: int = 10) -> list[tuple[int, int]]:
    """Generate up to ``max_pairs`` meaningful comparison indices from top-N items.

    Produces top-1 vs next-4, then adjacent rivals (1v2, 2v3, 3v4), deduped.
    """
    if n < 2:
        return []
    pairs: list[tuple[int, int]] = []
    # Top item vs each of the next few
    for j in range(1, min(n, 5)):
        pairs.append((0, j))
    # Adjacent rivals
    for i in range(1, min(n - 1, 4)):
        pairs.append((i, i + 1))
    # Deduplicate while preserving order
    seen: set[tuple[int, int]] = set()
    result: list[tuple[int, int]] = []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            result.append(p)
        if len(result) >= max_pairs:
            break
    return result


def export_compare(limit: int = DEFAULT_COMPARE_LIMIT) -> None:
    """Export player and team comparison pairs for static/offline fallback.

    Picks the top-N players by rating and top-N teams by strength, generates
    a set of meaningful pairs (top vs next, adjacent rivals), and writes the
    comparison results to ``player_compare_pairs.json`` and
    ``team_compare_pairs.json``.  Pairs that error are skipped; if all fail,
    an empty ``{"pairs": []}`` file is still written.
    """
    from scoutfootball.api import (
        get_player_comparison,
        get_player_ratings,
        get_team_comparison,
        get_team_strength,
    )

    pair_indices = _meaningful_pair_indices(limit)

    # ── Player comparison pairs ───────────────────────────────────
    ratings = get_player_ratings(limit=limit)
    players = ratings.get("players", [])

    def _player_name(p: dict) -> str | None:
        return p.get("player") or p.get("player_name")

    player_pairs: list[dict] = []
    for i, j in pair_indices:
        if i >= len(players) or j >= len(players):
            continue
        name_a = _player_name(players[i])
        name_b = _player_name(players[j])
        if not name_a or not name_b:
            continue
        try:
            comparison = get_player_comparison(name_a, name_b)
            if "error" in comparison:
                print(
                    f"  WARN: player compare {name_a} vs {name_b}: "
                    f"{comparison['error']}"
                )
                continue
            player_pairs.append(
                {"a": name_a, "b": name_b, "comparison": comparison}
            )
        except Exception as exc:
            print(f"  WARN: player compare {name_a} vs {name_b} failed: {exc}")
            continue

    _write_json(DATA_DIR / "player_compare_pairs.json", {"pairs": player_pairs})

    # ── Team comparison pairs ─────────────────────────────────────
    strength = get_team_strength(limit=limit)
    teams = strength.get("teams", [])

    team_pairs: list[dict] = []
    for i, j in pair_indices:
        if i >= len(teams) or j >= len(teams):
            continue
        name_a = teams[i].get("team")
        name_b = teams[j].get("team")
        if not name_a or not name_b:
            continue
        try:
            comparison = get_team_comparison(name_a, name_b)
            if "error" in comparison:
                print(
                    f"  WARN: team compare {name_a} vs {name_b}: "
                    f"{comparison['error']}"
                )
                continue
            team_pairs.append(
                {"a": name_a, "b": name_b, "comparison": comparison}
            )
        except Exception as exc:
            print(f"  WARN: team compare {name_a} vs {name_b} failed: {exc}")
            continue

    _write_json(DATA_DIR / "team_compare_pairs.json", {"pairs": team_pairs})

    print(
        f"  player_compare_pairs.json ({len(player_pairs)} pairs), "
        f"team_compare_pairs.json ({len(team_pairs)} pairs)"
    )


def write_manifest() -> None:
    """Write a small manifest file so the frontend can show last-updated time."""
    import datetime as dt

    files = []
    latest_mtime = 0.0
    for p in sorted(DATA_DIR.rglob("*.json")):
        rel = p.relative_to(FRONTEND_DIR).as_posix()
        size_kb = p.stat().st_size / 1024
        latest_mtime = max(latest_mtime, p.stat().st_mtime)
        files.append({"path": f"/{rel}", "kb": round(size_kb, 1)})

    manifest = {
        "generated_at": (
            dt.datetime.fromtimestamp(latest_mtime, dt.UTC).isoformat()
            if latest_mtime
            else None
        ),
        "file_count": len(files),
        "total_kb": round(sum(f["kb"] for f in files), 1),
        "files": files,
    }
    _write_json(MANIFEST_PATH, manifest)
    print(f"  {MANIFEST_PATH.name} ({len(files)} files, {manifest['total_kb']:.0f} KB)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ratings-limit", type=int, default=DEFAULT_RATINGS_LIMIT,
        help=f"Max ratings rows to export (default: {DEFAULT_RATINGS_LIMIT})",
    )
    parser.add_argument(
        "--action-values-limit", type=int, default=DEFAULT_ACTION_VALUES_LIMIT,
        help=f"Max action-value rows to export (default: {DEFAULT_ACTION_VALUES_LIMIT})",
    )
    parser.add_argument(
        "--queue-limit", type=int, default=DEFAULT_QUEUE_LIMIT,
        help=f"Max review-queue rows to export (default: {DEFAULT_QUEUE_LIMIT})",
    )
    parser.add_argument(
        "--player-profiles", type=int, default=200,
        help="If >0, also export top-N player profile JSON files (default: 200)",
    )
    parser.add_argument(
        "--compare-limit", type=int, default=DEFAULT_COMPARE_LIMIT,
        help=(
            f"Top-N players/teams to pair for comparison export "
            f"(default: {DEFAULT_COMPARE_LIMIT})"
        ),
    )
    parser.add_argument(
        "--skip",
        nargs="*",
        default=[],
        choices=[
            "basics", "ratings", "value", "predictions",
            "action_values", "scouting", "model_runs",
            "worldcup", "compare", "player_profiles", "manifest",
        ],
        help="Sections to skip",
    )
    parser.add_argument(
        "--profile",
        choices=["local", "release"],
        default="local",
        help="Write either a local ignored snapshot or the tracked release snapshot",
    )
    args = parser.parse_args()

    configure_output_paths(args.profile)

    # Ensure PYTHONPATH includes src if called directly
    src_root = str(REPO_ROOT / "src")
    if src_root not in sys.path:
        sys.path.insert(0, src_root)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WORLDCUP_DIR.mkdir(parents=True, exist_ok=True)
    SQUADS_DIR.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    print(f"Exporting ScoutFootball static data [{args.profile}] -> {DATA_DIR}")
    print("-" * 72)

    failures = []

    sections = [
        ("basics", lambda: export_basics()),
        ("ratings", lambda: export_ratings(args.ratings_limit)),
        ("value", lambda: export_value_summary()),
        ("predictions", lambda: export_predictions_meta()),
        ("action_values", lambda: export_action_values(args.action_values_limit)),
        ("scouting", lambda: export_scouting(args.queue_limit)),
        ("model_runs", lambda: export_model_runs()),
        ("worldcup", lambda: export_worldcup()),
        ("compare", lambda: export_compare(args.compare_limit)),
    ]

    for name, fn in sections:
        if name in args.skip:
            print(f"  [{name}] skipped")
            continue
        try:
            fn()
        except Exception as exc:
            print(f"  [{name}] FAILED: {exc}")
            failures.append(name)

    if args.player_profiles > 0 and "player_profiles" not in args.skip:
        try:
            export_sample_player_profiles(limit=args.player_profiles)
        except Exception as exc:
            print(f"  [player_profiles] FAILED: {exc}")
            failures.append("player_profiles")

    if "manifest" not in args.skip:
        try:
            write_manifest()
        except Exception as exc:
            print(f"  [manifest] FAILED: {exc}")
            failures.append("manifest")

    dt_s = time.time() - t0
    print("-" * 72)
    print(f"Done in {dt_s:.1f}s. Failures: {', '.join(failures) if failures else 'none'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
