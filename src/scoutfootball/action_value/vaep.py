"""VAEP (Valuing Actions by Estimating Probabilities) model.

VAEP assigns a value to each action by estimating:
  - P(scores | action, gamestate): probability that the team scores
    within the same possession after this action
  - P(concedes | action, gamestate): probability that the team concedes
    during the opponent's next possession after this action

  VAEP value = P(scores) - P(concedes)

Reference: Robberechts et al., "Valuing Actions in Soccer" (2019)
https://doi.org/10.1007/978-3-030-17274-9_2

Current status: P2. Uses StatsBomb Open Data (7.7M SPADL actions).
Output must NOT be treated as full league action value data.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from scoutfootball.action_value.identity import (
    build_identity_coverage_report,
    enrich_vaep_identities,
)

logger = logging.getLogger(__name__)

SOURCE_ATTRIBUTION = "StatsBomb Open Data"
COVERAGE_NOTE = "StatsBomb Open Data. NOT full league coverage."

# Action types that end a possession (ball lost to opponent)
POSSESSION_END_TYPES = frozenset({"shot", "clearance", "goalkeeper"})

# All known action types for one-hot encoding
ALL_ACTION_TYPES = [
    "pass", "receipt", "carry", "tackle", "interception",
    "block", "shot", "goalkeeper", "clearance", "dribble",
]

ALL_RESULTS = ["success", "failure", "unknown"]

# Default paths
ACTIONS_PATH = Path("data/gold/feature_store/actions_all.parquet")
OUTPUT_PATH = Path("data/gold/feature_store/player_vaep.parquet")
XT_OUTPUT_PATH = Path("data/gold/feature_store/player_action_value.parquet")
MATCHES_PATH = Path("data/raw/statsbomb_open/matches_all.parquet")


def _goal_distance(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Distance from (x, y) to the center of the opponent goal (100, 50).

    Coordinates are 0-100 normalized.
    """
    return np.sqrt((100.0 - x) ** 2 + (50.0 - y) ** 2)


def _goal_angle(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Angle (radians) to the goal from (x, y).

    Computed as the angle subtended by the goal mouth (7.32m wide,
    normalized to ~9.15 units in 0-100 coords) from the action position.
    """
    dx = 100.0 - x
    dy = 50.0 - y
    dist = np.sqrt(dx ** 2 + dy ** 2)
    # Goal width ~9.15 in normalized coords (7.32m / 80m * 100)
    goal_width = 9.15
    angle = np.arctan2(goal_width / 2, dist) * 2
    return angle


def create_vaep_features(actions_df: pd.DataFrame) -> pd.DataFrame:
    """Create VAEP feature matrix from SPADL actions DataFrame.

    Features include:
    - Action type one-hot (10 types)
    - Result one-hot (3 types)
    - Start/end coordinates and derived features (distance, angle)
    - Context: previous 2 actions' type and result
    - Time features: period, minute

    All operations are vectorized for performance on 7M+ rows.
    """
    n = len(actions_df)

    # Sort by match_id and time to ensure correct ordering
    df = actions_df.sort_values(
        ["match_id", "period", "minute", "second", "action_id"]
    ).reset_index(drop=True)

    logger.info("Creating features for %d actions (sorted)...", n)

    # --- Action type one-hot ---
    atype_vals = df["action_type"].values
    type_cols = {}
    for atype in ALL_ACTION_TYPES:
        type_cols[f"type_{atype}"] = (atype_vals == atype).astype(np.int8)

    # --- Result one-hot ---
    result_vals = df["result"].values
    result_cols = {}
    for res in ALL_RESULTS:
        result_cols[f"result_{res}"] = (result_vals == res).astype(np.int8)

    # --- Coordinate features ---
    sx = df["start_x"].values.astype(np.float32)
    sy = df["start_y"].values.astype(np.float32)
    ex = df["end_x"].values.astype(np.float32)
    ey = df["end_y"].values.astype(np.float32)

    coord_cols = {
        "start_x": sx, "start_y": sy, "end_x": ex, "end_y": ey,
        "start_dist_goal": (
            _goal_distance(sx.astype(np.float64), sy.astype(np.float64))
            .astype(np.float32)
        ),
        "end_dist_goal": (
            _goal_distance(ex.astype(np.float64), ey.astype(np.float64))
            .astype(np.float32)
        ),
        "start_angle_goal": (
            _goal_angle(sx.astype(np.float64), sy.astype(np.float64))
            .astype(np.float32)
        ),
        "end_angle_goal": (
            _goal_angle(ex.astype(np.float64), ey.astype(np.float64))
            .astype(np.float32)
        ),
        "dx": (ex - sx), "dy": (ey - sy),
        "movement_dist": np.sqrt((ex - sx) ** 2 + (ey - sy) ** 2),
    }

    # --- Time features ---
    time_cols = {
        "period_id": df["period"].values.astype(np.int8),
        "time_seconds": (
            (df["period"].values.clip(max=2) - 1) * 45 * 60
            + df["minute"].values * 60
            + df["second"].values
        ).astype(np.float32),
    }

    # --- Context features: previous 2 actions within same match ---
    match_ids = df["match_id"].values
    team_ids = df["team_id"].values
    context_cols = {}

    for lag in [1, 2]:
        lag_type = pd.Series(atype_vals).shift(lag)
        lag_result = pd.Series(result_vals).shift(lag)
        lag_team = pd.Series(team_ids).shift(lag)
        lag_match = pd.Series(match_ids).shift(lag)

        # Only carry over if same match
        same_match = match_ids == lag_match.values
        lag_type = lag_type.where(same_match, "none")
        lag_result = lag_result.where(same_match, "none")

        lag_type_vals = lag_type.values
        lag_result_vals = lag_result.values

        for atype in ALL_ACTION_TYPES:
            context_cols[f"prev{lag}_type_{atype}"] = (lag_type_vals == atype).astype(np.int8)
        for res in ALL_RESULTS:
            context_cols[f"prev{lag}_result_{res}"] = (lag_result_vals == res).astype(np.int8)

        # Same team flag
        context_cols[f"prev{lag}_same_team"] = (
            same_match & (team_ids == lag_team.values)
        ).astype(np.int8)

    # --- Build feature DataFrame directly from arrays ---
    all_cols = {}
    all_cols.update(type_cols)
    all_cols.update(result_cols)
    all_cols.update(coord_cols)
    all_cols.update(time_cols)
    all_cols.update(context_cols)

    features = pd.DataFrame(all_cols)

    # Fill NaN from shift operations with 0
    features = features.fillna(0)

    logger.info("Feature matrix shape: %s", features.shape)
    return features


def create_vaep_labels(actions_df: pd.DataFrame) -> pd.DataFrame:
    """Create VAEP labels from SPADL actions DataFrame.

    For each action:
    - scores: 1 if the team scores before the possession ends, else 0
    - concedes: 1 if the opponent scores during their next possession, else 0

    Uses vectorized groupby operations for performance.
    """
    df = actions_df.copy()

    # Sort by match and time
    df = df.sort_values(
        ["match_id", "period", "minute", "second", "action_id"]
    ).reset_index(drop=True)

    # --- Identify possession boundaries ---
    # A new possession starts when the team changes within a match
    prev_team = df["team_id"].shift(1)
    prev_match = df["match_id"].shift(1)
    new_possession = (df["match_id"] != prev_match) | (df["team_id"] != prev_team)
    df["possession_id"] = new_possession.cumsum()

    # --- Identify goals ---
    # A goal occurs when: action_type == "shot" and result == "success"
    df["is_goal"] = (
        (df["action_type"] == "shot") & (df["result"] == "success")
    ).astype(np.int8)

    # --- scores: did the team score in this possession? ---
    possession_goals = df.groupby("possession_id")["is_goal"].transform("max")
    df["scores"] = possession_goals

    # --- concedes: did the opponent score in the next possession? ---
    # Get the team_id for each possession
    df.groupby("possession_id")["team_id"].transform("first")

    # Get whether each possession ended in a goal
    poss_goal_map = df.groupby("possession_id")["is_goal"].max()

    # Get the next possession id for each action
    # For each possession, check if the next possession (by different team) has a goal
    poss_ids = df["possession_id"].unique()
    # Map possession_id -> next possession's goal status
    next_poss_goal = {}
    sorted_poss = sorted(poss_ids)
    for i in range(len(sorted_poss) - 1):
        curr_poss = sorted_poss[i]
        next_poss = sorted_poss[i + 1]
        # Check same match
        curr_match = df.loc[df["possession_id"] == curr_poss, "match_id"].iloc[0]
        next_match = df.loc[df["possession_id"] == next_poss, "match_id"].iloc[0]
        if curr_match == next_match:
            next_poss_goal[curr_poss] = poss_goal_map.get(next_poss, 0)
        else:
            next_poss_goal[curr_poss] = 0
    # Last possession
    next_poss_goal[sorted_poss[-1]] = 0

    df["concedes"] = df["possession_id"].map(next_poss_goal).fillna(0).astype(np.int8)

    # Drop helper columns
    labels = df[["scores", "concedes"]].copy()

    return labels


def create_vaep_labels_fast(actions_df: pd.DataFrame) -> pd.DataFrame:
    """Create VAEP labels using fast vectorized approach.

    Optimized for 7M+ rows. Avoids per-possession Python loops.
    """
    df = actions_df.copy()

    # Sort by match and time
    df = df.sort_values(
        ["match_id", "period", "minute", "second", "action_id"]
    ).reset_index(drop=True)

    # --- Identify possession boundaries ---
    prev_team = df["team_id"].shift(1)
    prev_match = df["match_id"].shift(1)
    new_possession = (df["match_id"] != prev_match) | (df["team_id"] != prev_team)
    df["possession_id"] = new_possession.cumsum()

    # --- Identify goals ---
    df["is_goal"] = (
        (df["action_type"] == "shot") & (df["result"] == "success")
    ).astype(np.int8)

    # --- scores: did the team score in this possession? ---
    # Use groupby transform for vectorized max
    df["scores"] = df.groupby("possession_id")["is_goal"].transform("max")

    # --- concedes: did the opponent score in the next possession? ---
    # For each possession, get: match_id, team_id, and whether it had a goal
    poss_info = df.groupby("possession_id").agg(
        match_id=("match_id", "first"),
        team_id=("team_id", "first"),
        has_goal=("is_goal", "max"),
    ).reset_index()

    # Sort by possession_id (already sorted since df is sorted)
    poss_info = poss_info.sort_values("possession_id").reset_index(drop=True)

    # Next possession's goal, but only if same match and different team
    next_goal = poss_info["has_goal"].shift(-1).fillna(0).astype(int)
    next_match = poss_info["match_id"].shift(-1)
    next_team = poss_info["team_id"].shift(-1)

    # Concede only if: next possession is same match AND different team AND has goal
    poss_info["next_concedes"] = (
        (poss_info["match_id"] == next_match) &
        (poss_info["team_id"] != next_team) &
        (next_goal == 1)
    ).astype(np.int8)

    # Map back to actions
    concede_map = poss_info.set_index("possession_id")["next_concedes"]
    df["concedes"] = df["possession_id"].map(concede_map).fillna(0).astype(np.int8)

    labels = df[["scores", "concedes"]].copy()
    return labels


def train_vaep_model(
    features: pd.DataFrame,
    labels: pd.DataFrame,
    model_type: str = "gb",
    sample_fraction: float = 0.5,
    random_state: int = 42,
) -> dict:
    """Train VAEP models (scores and concedes).

    Args:
        features: Feature matrix from create_vaep_features().
        labels: Label DataFrame from create_vaep_labels().
        model_type: "gb" for GradientBoostingClassifier, "lr" for LogisticRegression.
        sample_fraction: Fraction of data to use for training (for performance).
        random_state: Random seed.

    Returns:
        Dict with 'scores_model', 'concedes_model', 'scores_auc', 'concedes_auc'.
    """
    n = len(features)

    # Sample for training if dataset is large
    if sample_fraction < 1.0 and n > 100_000:
        rng = np.random.RandomState(random_state)
        train_idx = rng.choice(n, size=int(n * sample_fraction), replace=False)
        train_idx.sort()
        x_train = features.iloc[train_idx]
        y_scores_train = labels["scores"].iloc[train_idx]
        y_concedes_train = labels["concedes"].iloc[train_idx]
    else:
        x_train = features
        y_scores_train = labels["scores"]
        y_concedes_train = labels["concedes"]

    # Create model
    if model_type == "gb":
        scores_model = GradientBoostingClassifier(
            n_estimators=50,
            max_depth=3,
            learning_rate=0.1,
            min_samples_leaf=200,
            subsample=0.7,
            random_state=random_state,
        )
        concedes_model = GradientBoostingClassifier(
            n_estimators=50,
            max_depth=3,
            learning_rate=0.1,
            min_samples_leaf=200,
            subsample=0.7,
            random_state=random_state,
        )
    elif model_type == "lr":
        scores_model = LogisticRegression(
            max_iter=5000, C=1.0, random_state=random_state, solver="lbfgs",
        )
        concedes_model = LogisticRegression(
            max_iter=5000, C=1.0, random_state=random_state, solver="lbfgs",
        )
    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    # Train scores model
    logger.info("Training scores model on %d samples...", len(x_train))
    scores_model.fit(x_train, y_scores_train)

    # Train concedes model
    logger.info("Training concedes model on %d samples...", len(x_train))
    concedes_model.fit(x_train, y_concedes_train)

    # Evaluate on training sample
    scores_auc = roc_auc_score(y_scores_train, scores_model.predict_proba(x_train)[:, 1])
    concedes_auc = roc_auc_score(y_concedes_train, concedes_model.predict_proba(x_train)[:, 1])

    logger.info("Scores model AUC: %.4f", scores_auc)
    logger.info("Concedes model AUC: %.4f", concedes_auc)

    return {
        "scores_model": scores_model,
        "concedes_model": concedes_model,
        "scores_auc": scores_auc,
        "concedes_auc": concedes_auc,
    }


def predict_vaep_value(
    model: dict,
    features: pd.DataFrame,
    chunk_size: int = 1_000_000,
) -> np.ndarray:
    """Predict VAEP value for all actions.

    VAEP value = P(scores) - P(concedes)

    Processes in chunks to manage memory for 7M+ rows.

    Args:
        model: Dict from train_vaep_model() with 'scores_model' and 'concedes_model'.
        features: Feature matrix from create_vaep_features().
        chunk_size: Number of rows to process at once.

    Returns:
        Array of VAEP values, same length as features.
    """
    n = len(features)
    vaep_values = np.zeros(n, dtype=np.float64)

    scores_model = model["scores_model"]
    concedes_model = model["concedes_model"]

    for start in range(0, n, chunk_size):
        end = min(start + chunk_size, n)
        chunk = features.iloc[start:end]

        p_scores = scores_model.predict_proba(chunk)[:, 1]
        p_concedes = concedes_model.predict_proba(chunk)[:, 1]

        vaep_values[start:end] = p_scores - p_concedes

    return vaep_values


def _aggregate_to_player_season(
    actions_df: pd.DataFrame,
    vaep_values: np.ndarray,
) -> pd.DataFrame:
    """Aggregate VAEP values to player-season level.

    Returns DataFrame with per-player VAEP totals and per-90 metrics.
    """
    df = actions_df.copy()
    df["vaep_value"] = vaep_values

    # Filter out actions without player_id
    df = df[df["player_id"].notna() & (df["player_id"] != "")].copy()
    if df.empty:
        return pd.DataFrame()

    # Estimate minutes per player-match
    minutes = df.groupby(["player_id", "team_id", "match_id"]).agg(
        max_minute=("minute", "max"),
        min_minute=("minute", "min"),
    ).reset_index()
    minutes["estimated_minutes"] = (
        (minutes["max_minute"] - minutes["min_minute"]).clip(lower=1).clip(lower=45)
    )

    # Action counts per type per player-match
    atype = df["action_type"].values
    for atype_name in ["pass", "shot", "dribble", "carry", "tackle", "interception"]:
        df[f"_is_{atype_name}"] = (atype == atype_name).astype(np.int32)

    df["_is_success"] = (df["result"] == "success").astype(np.int32)

    # Aggregate per player-match
    pm_agg = df.groupby(["player_id", "team_id", "match_id"]).agg(
        vaep_total=("vaep_value", "sum"),
        vaep_mean=("vaep_value", "mean"),
        n_actions=("vaep_value", "count"),
        n_pass=("_is_pass", "sum"),
        n_shot=("_is_shot", "sum"),
        n_dribble=("_is_dribble", "sum"),
        n_carry=("_is_carry", "sum"),
        n_tackle=("_is_tackle", "sum"),
        n_interception=("_is_interception", "sum"),
        n_success=("_is_success", "sum"),
    ).reset_index()

    # Merge minutes
    pm_agg = pm_agg.merge(
        minutes[["player_id", "team_id", "match_id", "estimated_minutes"]],
        on=["player_id", "team_id", "match_id"],
        how="left",
    )

    # Aggregate to player level
    player_agg = pm_agg.groupby(["player_id", "team_id"]).agg(
        vaep_total=("vaep_total", "sum"),
        vaep_mean=("vaep_mean", "mean"),
        n_actions=("n_actions", "sum"),
        n_matches=("match_id", "nunique"),
        estimated_minutes=("estimated_minutes", "sum"),
        n_pass=("n_pass", "sum"),
        n_shot=("n_shot", "sum"),
        n_dribble=("n_dribble", "sum"),
        n_carry=("n_carry", "sum"),
        n_tackle=("n_tackle", "sum"),
        n_interception=("n_interception", "sum"),
        n_success=("n_success", "sum"),
    ).reset_index()

    # Per-90 metrics
    player_agg["minutes_90"] = (player_agg["estimated_minutes"] / 90.0).clip(lower=0.1)
    player_agg["vaep_per_90"] = player_agg["vaep_total"] / player_agg["minutes_90"]

    # Add player_name if available
    if "player_name" in df.columns:
        names = (
            df[df["player_name"] != ""]
            .groupby("player_id")["player_name"]
            .first()
            .reset_index()
        )
        player_agg = player_agg.merge(names, on="player_id", how="left")
        player_agg["player_name"] = player_agg["player_name"].fillna("")
    else:
        player_agg["player_name"] = ""

    # Metadata
    player_agg["source"] = SOURCE_ATTRIBUTION
    player_agg["source_attribution"] = SOURCE_ATTRIBUTION
    player_agg["coverage_note"] = COVERAGE_NOTE

    # Sort
    player_agg = player_agg.sort_values("vaep_total", ascending=False).reset_index(drop=True)

    return player_agg


def compute_vaep_from_actions(
    actions_path: str | Path = ACTIONS_PATH,
    output_path: str | Path = OUTPUT_PATH,
    model_type: str = "gb",
    sample_fraction: float = 0.5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Main entry point: compute VAEP values from SPADL actions.

    Steps:
    1. Load actions_all.parquet
    2. Create features and labels
    3. Train VAEP models (scores + concedes)
    4. Predict VAEP values for all actions
    5. Aggregate to player level
    6. Save to output_path

    Args:
        actions_path: Path to SPADL actions Parquet.
        output_path: Path to save player VAEP Parquet.
        model_type: "gb" or "lr".
        sample_fraction: Fraction of data for training.
        random_state: Random seed.

    Returns:
        Player-level VAEP DataFrame.
    """
    actions_path = Path(actions_path)
    output_path = Path(output_path)

    # 1. Load actions
    print(f"[VAEP] Loading actions from {actions_path}")
    logger.info("Loading actions from %s", actions_path)
    actions_df = pd.read_parquet(actions_path)
    print(f"[VAEP] Loaded {len(actions_df)} actions")
    logger.info("Loaded %d actions", len(actions_df))

    # 2. Create features
    print("[VAEP] Creating features...")
    logger.info("Creating VAEP features...")
    features = create_vaep_features(actions_df)
    print(f"[VAEP] Feature matrix shape: {features.shape}")
    logger.info("Feature matrix shape: %s", features.shape)

    # 3. Create labels
    print("[VAEP] Creating labels...")
    logger.info("Creating VAEP labels...")
    labels = create_vaep_labels_fast(actions_df)
    print(
        f"[VAEP] Labels: scores={labels['scores'].sum()} "
        f"({labels['scores'].mean() * 100:.2f}%), "
        f"concedes={labels['concedes'].sum()} "
        f"({labels['concedes'].mean() * 100:.2f}%)"
    )
    logger.info(
        "Labels: scores=%d (%.2f%%), concedes=%d (%.2f%%)",
        labels["scores"].sum(),
        labels["scores"].mean() * 100,
        labels["concedes"].sum(),
        labels["concedes"].mean() * 100,
    )

    # 4. Train models
    print(f"[VAEP] Training models (type={model_type}, sample={sample_fraction * 100:.0f}%)...")
    logger.info(
        "Training VAEP models (type=%s, sample=%.0f%%)...",
        model_type, sample_fraction * 100,
    )
    model = train_vaep_model(
        features, labels,
        model_type=model_type,
        sample_fraction=sample_fraction,
        random_state=random_state,
    )
    print(
        f"[VAEP] Model trained: scores_auc={model['scores_auc']:.4f}, "
        f"concedes_auc={model['concedes_auc']:.4f}"
    )
    logger.info(
        "Model trained: scores_auc=%.4f, concedes_auc=%.4f",
        model["scores_auc"], model["concedes_auc"],
    )

    # 5. Predict VAEP values
    print("[VAEP] Predicting VAEP values for all actions...")
    logger.info("Predicting VAEP values for all actions...")
    vaep_values = predict_vaep_value(model, features)
    print(
        f"[VAEP] VAEP values: min={vaep_values.min():.6f}, "
        f"max={vaep_values.max():.6f}, mean={vaep_values.mean():.6f}"
    )
    logger.info(
        "VAEP values: min=%.6f, max=%.6f, mean=%.6f, std=%.6f",
        vaep_values.min(), vaep_values.max(), vaep_values.mean(), vaep_values.std(),
    )

    # Free memory: release features and labels
    del features
    del labels

    # 6. Aggregate to player level
    print("[VAEP] Aggregating to player level...")
    logger.info("Aggregating to player level...")
    # Re-sort actions_df to match features order (create_vaep_features sorts)
    actions_sorted = actions_df.sort_values(
        ["match_id", "period", "minute", "second", "action_id"]
    ).reset_index(drop=True)
    player_vaep = _aggregate_to_player_season(actions_sorted, vaep_values)
    print(f"[VAEP] Player VAEP: {len(player_vaep)} rows")
    logger.info("Player VAEP: %d rows", len(player_vaep))

    # 6b. Add display identity and season context from exact StatsBomb keys.
    # VAEP remains a player-team career aggregate; the season list is context,
    # not a claim that the value belongs to one particular season.
    xt_df = pd.read_parquet(XT_OUTPUT_PATH) if XT_OUTPUT_PATH.exists() else pd.DataFrame()
    matches_df = pd.read_parquet(MATCHES_PATH) if MATCHES_PATH.exists() else pd.DataFrame()
    player_vaep = enrich_vaep_identities(player_vaep, xt_df, matches_df)
    identity_report = build_identity_coverage_report(player_vaep)
    print(
        "[VAEP] Identity coverage: "
        f"{identity_report['mapped_rows']}/{identity_report['total_rows']} "
        f"({identity_report['coverage_rate']:.1%})"
    )

    # 7. Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    player_vaep.to_parquet(output_path, index=False)
    coverage_path = output_path.with_name("player_vaep_identity_coverage.json")
    coverage_path.write_text(
        json.dumps(identity_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[VAEP] Saved player VAEP to {output_path} ({len(player_vaep)} rows)")
    print(f"[VAEP] Saved identity coverage to {coverage_path}")
    logger.info("Saved player VAEP to %s (%d rows)", output_path, len(player_vaep))

    # Print top 10
    top10 = player_vaep.head(10)
    print("[VAEP] Top 10 VAEP players:")
    for _, row in top10.iterrows():
        name = row["player_name"] or row["player_id"]
        print(
            f"  {name} (team={row['team_id']}): "
            f"vaep_total={row['vaep_total']:.3f}, "
            f"vaep_per_90={row['vaep_per_90']:.3f}, "
            f"n_actions={row['n_actions']}"
        )

    return player_vaep
