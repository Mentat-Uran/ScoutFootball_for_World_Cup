"""Compute World Cup 2026 group-stage match predictions and export as JSON.

Uses the team-strength pipeline from scoutfootball.worldcup.data plus a
simple Poisson model for win/draw/loss probabilities and expected scores.

Output:
- release profile: frontend/data/worldcup/*.json
- local profile: frontend/local-data/worldcup/*.json

Usage:
    python scripts/compute_worldcup_predictions.py
    python scripts/compute_worldcup_predictions.py --profile release
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
RELEASE_DATA_DIR = REPO_ROOT / "frontend" / "data" / "worldcup"
LOCAL_DATA_DIR = REPO_ROOT / "frontend" / "local-data" / "worldcup"

BASE_GOALS_PER_GAME = 2.6
HOME_ADVANTAGE = 1.08
HOST_NATIONS = {"United States", "Canada", "Mexico"}


def poisson_pmf(lmbda: float, k: int) -> float:
    return (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)


def compute_match_prediction(home: str, away: str, strengths: dict[str, float]) -> dict:
    s_home = max(strengths.get(home, 0.3), 0.15)
    s_away = max(strengths.get(away, 0.3), 0.15)

    exp_home = 1.3 * (s_home / s_away) ** 0.5 * HOME_ADVANTAGE
    exp_away = 1.3 * (s_away / s_home) ** 0.5

    # Additional 10% boost for host nations at home
    if home in HOST_NATIONS:
        exp_home *= 1.10

    exp_home = max(0.3, min(exp_home, 4.5))
    exp_away = max(0.3, min(exp_away, 4.5))

    win_p = 0.0
    draw_p = 0.0
    loss_p = 0.0
    best_score = (0, 0)
    best_prob = 0.0

    score_probs: list[tuple[int, int, float]] = []
    for h in range(10):
        for a in range(10):
            p = poisson_pmf(exp_home, h) * poisson_pmf(exp_away, a)
            if p < 1e-5:
                continue
            score_probs.append((h, a, p))
            if h > a:
                win_p += p
            elif h == a:
                draw_p += p
            else:
                loss_p += p
            if p > best_prob:
                best_prob = p
                best_score = (h, a)

    score_probs.sort(key=lambda x: -x[2])
    top_5 = [
        {"home_goals": h, "away_goals": a, "probability": round(p, 5)}
        for h, a, p in score_probs[:5]
    ]

    total = win_p + draw_p + loss_p
    if total > 0:
        win_p /= total
        draw_p /= total
        loss_p /= total

    exp_points_home = win_p * 3 + draw_p * 1
    exp_points_away = loss_p * 3 + draw_p * 1

    # Build 6x6 score probability matrix (0-5 goals each)
    score_matrix = []
    for h in range(6):
        row = []
        for a in range(6):
            p = poisson_pmf(exp_home, h) * poisson_pmf(exp_away, a)
            row.append(round(p, 4))
        score_matrix.append(row)

    return {
        "home": home,
        "away": away,
        "exp_home_goals": round(exp_home, 2),
        "exp_away_goals": round(exp_away, 2),
        "home_win_p": round(win_p, 4),
        "draw_p": round(draw_p, 4),
        "away_win_p": round(loss_p, 4),
        "most_likely_score": f"{best_score[0]}-{best_score[1]}",
        "top_scorelines": top_5,
        "exp_points_home": round(exp_points_home, 2),
        "exp_points_away": round(exp_points_away, 2),
        "home_strength": round(s_home, 3),
        "away_strength": round(s_away, 3),
        "score_matrix": score_matrix,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        choices=["local", "release"],
        default="local",
        help="Write either ignored local World Cup snapshots or tracked release snapshots",
    )
    args = parser.parse_args()

    data_dir = RELEASE_DATA_DIR if args.profile == "release" else LOCAL_DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)

    src_root = str(REPO_ROOT / "src")
    if src_root not in sys.path:
        sys.path.insert(0, src_root)

    from scoutfootball.worldcup.data import (
        GROUPS,
        OPTA_WIN_PROBABILITY,
        compute_team_strengths,
        generate_group_stage_matches,
    )

    strengths = compute_team_strengths()
    matches = generate_group_stage_matches()

    predictions: list[dict] = []
    for m in matches:
        pred = compute_match_prediction(m.home, m.away, strengths)
        predictions.append({
            "group": m.group,
            "matchday": m.matchday,
            "date": m.date,
            "time_et": m.time_et,
            "venue": m.venue,
            "city": m.city,
            "stage": m.stage,
            **pred,
        })

    match_out = data_dir / "match_predictions.json"
    with open(match_out, "w", encoding="utf-8") as f:
        json.dump({
            "model": "poisson_strength_ratio",
            "base_goals_per_game": BASE_GOALS_PER_GAME,
            "home_advantage": HOME_ADVANTAGE,
            "group_count": len(GROUPS),
            "match_count": len(predictions),
            "teams": sorted(set(m["home"] for m in predictions)),
            "matches": predictions,
        }, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(predictions)} match predictions -> {match_out}")

    group_summaries: list[dict] = []
    for letter, teams in GROUPS.items():
        group_matches = [p for p in predictions if p["group"] == letter]

        table: dict[str, dict] = {
            team: {"team": team, "exp_points": 0.0, "exp_gf": 0.0, "exp_ga": 0.0, "exp_gd": 0.0}
            for team in teams
        }
        for m in group_matches:
            table[m["home"]]["exp_points"] += m["exp_points_home"]
            table[m["home"]]["exp_gf"] += m["exp_home_goals"]
            table[m["home"]]["exp_ga"] += m["exp_away_goals"]
            table[m["away"]]["exp_points"] += m["exp_points_away"]
            table[m["away"]]["exp_gf"] += m["exp_away_goals"]
            table[m["away"]]["exp_ga"] += m["exp_home_goals"]

        for t in table.values():
            t["exp_gd"] = round(t["exp_gf"] - t["exp_ga"], 2)
            t["exp_points"] = round(t["exp_points"], 2)
            t["exp_gf"] = round(t["exp_gf"], 2)
            t["exp_ga"] = round(t["exp_ga"], 2)

        ranked = sorted(table.values(), key=lambda x: (-x["exp_points"], -x["exp_gd"]))
        for rank, row in enumerate(ranked, start=1):
            row["projected_rank"] = rank
            row["strength"] = round(strengths.get(row["team"], 0.3), 3)
            row["opta_win_prob"] = round(OPTA_WIN_PROBABILITY.get(row["team"], 0.01), 3)

        group_summaries.append({
            "group": letter,
            "projected_table": ranked,
            "matches": [
                {k: v for k, v in m.items() if k in (
                    "home", "away", "matchday", "date",
                    "exp_home_goals", "exp_away_goals",
                    "home_win_p", "draw_p", "away_win_p",
                    "most_likely_score",
                )}
                for m in group_matches
            ],
        })

    group_out = data_dir / "group_predictions.json"
    with open(group_out, "w", encoding="utf-8") as f:
        json.dump({
            "model": "poisson_strength_ratio",
            "groups": group_summaries,
        }, f, ensure_ascii=False, indent=2)

    print(f"Wrote group predictions for {len(group_summaries)} groups -> {group_out}")

    index = {
        "model": "poisson_strength_ratio",
        "sources": ["scoutfootball_ratings", "opta_win_probability", "big5_league_count"],
        "files": {
            "match_predictions": "match_predictions.json",
            "group_predictions": "group_predictions.json",
        },
        "summary": {
            "matches": len(predictions),
            "groups": len(GROUPS),
            "teams": 48,
        },
    }
    index_out = data_dir / "predictions_index.json"
    with open(index_out, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"Wrote predictions index -> {index_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
