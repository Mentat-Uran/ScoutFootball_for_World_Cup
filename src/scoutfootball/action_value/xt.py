"""Expected Threat (xT) model.

xT assigns a value to each location on the pitch representing the
probability that possession from that location will lead to a goal
within the next N actions.

The model divides the pitch into a grid (e.g., 12x8) and iteratively
computes the threat value of each cell based on:
- Shot probability from that cell (fraction of possessions that result in a shot)
- Goal probability given a shot from that cell
- Transition probability to other cells (move/pass/carry)

Reference: Karun Singh, "Expected Threat" (2018)
https://karun.in/blog/expected-threat.html

Current status: P2. Full StatsBomb Open Data (7.7M actions).
Grid dimensions: 16x12 for full dataset.
"""
from __future__ import annotations

import logging
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd

from scoutfootball.action_value.schema import ActionResult, ActionType, InternalAction

logger = logging.getLogger(__name__)

# Grid for full dataset (7.7M actions)
DEFAULT_X_CELLS = 16
DEFAULT_Y_CELLS = 12

# Action types used for xT grid computation
POSSESSION_TYPES = frozenset({
    ActionType.PASS, ActionType.CARRY, ActionType.DRIBBLE,
    ActionType.TACKLE, ActionType.INTERCEPTION,
    ActionType.CLEARANCE, ActionType.BLOCK,
    ActionType.GOALKEEPER, ActionType.TAKE_ON,
})
MOVE_TYPES = frozenset({ActionType.PASS, ActionType.CARRY, ActionType.DRIBBLE})

# Paths
ACTIONS_PATH = Path("data/gold/feature_store/actions_all.parquet")
XT_GRID_PATH = Path("data/gold/feature_store/xt_grid.npy")
MATCHES_PATH = Path("data/raw/statsbomb_open/matches_all.parquet")
EVENTS_PATH = Path("data/raw/statsbomb_open/events_all.parquet")


def create_xt_grid(
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> np.ndarray:
    """Create an initial xT grid (all zeros)."""
    return np.zeros((y_cells, x_cells))


def get_cell(
    x: float,
    y: float,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> tuple[int, int]:
    """Get grid cell indices for a normalized coordinate (0-100)."""
    xi = min(int(x / 100.0 * x_cells), x_cells - 1)
    yi = min(int(y / 100.0 * y_cells), y_cells - 1)
    return max(0, xi), max(0, yi)


def compute_shot_goal_matrices(
    actions: Sequence[InternalAction],
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute shot probability and goal probability per cell.

    shot_prob[cell] = P(shot | possession in cell)
    goal_prob[cell] = P(goal | shot from cell)

    Returns (shot_prob, goal_prob) each as (y_cells, x_cells) matrices.
    """
    possession_count = np.zeros((y_cells, x_cells))
    shot_count = np.zeros((y_cells, x_cells))
    goal_count = np.zeros((y_cells, x_cells))

    for action in actions:
        if action.action_type in (ActionType.PASS, ActionType.CARRY, ActionType.DRIBBLE,
                                   ActionType.TACKLE, ActionType.INTERCEPTION,
                                   ActionType.CLEARANCE, ActionType.BLOCK,
                                   ActionType.GOALKEEPER, ActionType.DRIBBLE,
                                   ActionType.TAKE_ON):
            xi, yi = get_cell(action.start_x, action.start_y, x_cells, y_cells)
            possession_count[yi, xi] += 1
        elif action.action_type == ActionType.SHOT:
            xi, yi = get_cell(action.start_x, action.start_y, x_cells, y_cells)
            shot_count[yi, xi] += 1
            possession_count[yi, xi] += 1
            if action.result.value == "success":
                goal_count[yi, xi] += 1

    # Shot probability: fraction of possessions that result in a shot
    with np.errstate(divide="ignore", invalid="ignore"):
        shot_prob = np.where(possession_count > 0, shot_count / possession_count, 0.0)
    # Clip to [0, 1] for safety
    shot_prob = np.clip(shot_prob, 0.0, 1.0)

    # Goal probability: fraction of shots that result in a goal
    with np.errstate(divide="ignore", invalid="ignore"):
        goal_prob = np.where(shot_count > 0, goal_count / shot_count, 0.0)
    # Default goal probability based on distance (rough heuristic for cells with no shots)
    # Closer to goal = higher goal probability
    for yi in range(y_cells):
        for xi in range(x_cells):
            if shot_count[yi, xi] == 0:
                # x position normalized: 0 = own goal, 100 = opponent goal
                x_norm = (xi + 0.5) / x_cells
                # Rough: goal prob increases with proximity to goal
                goal_prob[yi, xi] = max(0.01, 0.3 * x_norm ** 2)
    goal_prob = np.clip(goal_prob, 0.0, 1.0)

    logger.info(
        "Shot prob: min=%.4f, max=%.4f, nonzero_cells=%d",
        shot_prob.min(), shot_prob.max(), (shot_prob > 0).sum(),
    )
    logger.info(
        "Goal prob: min=%.4f, max=%.4f, nonzero_cells=%d",
        goal_prob.min(), goal_prob.max(), (goal_prob > 0).sum(),
    )

    return shot_prob, goal_prob


def compute_transition_matrix(
    actions: Sequence[InternalAction],
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> np.ndarray:
    """Compute transition probability matrix from actions.

    Returns a (y_cells*x_cells, y_cells*x_cells) matrix where
    entry [i][j] is the probability of moving from cell i to cell j
    given a move action (pass/carry/dribble).
    """
    n_cells = x_cells * y_cells
    transitions = np.zeros((n_cells, n_cells))

    for action in actions:
        if action.action_type in (ActionType.PASS, ActionType.CARRY, ActionType.DRIBBLE):
            sx, sy = get_cell(action.start_x, action.start_y, x_cells, y_cells)
            ex, ey = get_cell(action.end_x, action.end_y, x_cells, y_cells)
            from_idx = sy * x_cells + sx
            to_idx = ey * x_cells + ex
            transitions[from_idx, to_idx] += 1

    # Normalize rows
    row_sums = transitions.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        transitions = np.where(row_sums > 0, transitions / row_sums, 0.0)

    return transitions


def iterate_xt(
    shot_prob: np.ndarray,
    goal_prob: np.ndarray,
    transitions: np.ndarray,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
    n_iterations: int = 1000,
    convergence_threshold: float = 1e-6,
) -> np.ndarray:
    """Iteratively compute xT values.

    xT(cell) = shot_prob(cell) * goal_prob(cell)
             + (1 - shot_prob(cell)) * sum(transitions[cell, j] * xT(j))

    This is the standard xT formulation where:
    - shot_prob * goal_prob = expected goals from shooting
    - (1 - shot_prob) * transitions @ xT = expected goals from moving

    Returns a (y_cells, x_cells) grid of xT values.
    """
    xt = np.zeros((y_cells, x_cells))

    shot_flat = shot_prob.flatten()
    goal_flat = goal_prob.flatten()

    for iteration in range(n_iterations):
        xt_flat = xt.flatten()
        new_xt = shot_flat * goal_flat + (1 - shot_flat) * (transitions @ xt_flat)
        new_xt = new_xt.reshape(y_cells, x_cells)

        # Clip to prevent divergence
        new_xt = np.clip(new_xt, 0.0, 1.0)

        diff = np.abs(new_xt - xt).max()
        xt = new_xt

        if diff < convergence_threshold:
            logger.info("xT converged after %d iterations (diff=%.8f)", iteration + 1, diff)
            break
    else:
        logger.info("xT did not converge after %d iterations (diff=%.8f)", n_iterations, diff)

    return xt


def compute_xt(actions: Sequence[InternalAction]) -> np.ndarray:
    """Compute xT grid from a sequence of actions.

    This is the main entry point for xT computation.
    """
    if not actions:
        logger.warning("No actions provided for xT computation")
        return create_xt_grid()

    shot_prob, goal_prob = compute_shot_goal_matrices(actions)
    transitions = compute_transition_matrix(actions)
    xt = iterate_xt(shot_prob, goal_prob, transitions)

    logger.info("Computed xT grid: min=%.6f, max=%.6f, mean=%.6f", xt.min(), xt.max(), xt.mean())
    return xt


def action_xt_value(
    action: InternalAction,
    xt_grid: np.ndarray,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> float:
    """Compute the xT value added by a single action.

    xT_added = xT(end_location) - xT(start_location)

    Positive value means the action moved the ball to a more dangerous
    position. Negative means it moved to a less dangerous position.
    """
    sx, sy = get_cell(action.start_x, action.start_y, x_cells, y_cells)
    ex, ey = get_cell(action.end_x, action.end_y, x_cells, y_cells)

    start_xt = xt_grid[sy, sx]
    end_xt = xt_grid[ey, ex]

    return float(end_xt - start_xt)


# ---------------------------------------------------------------------------
# Vectorized versions for large DataFrames (7M+ rows)
# ---------------------------------------------------------------------------

def _get_cell_indices_vectorized(
    x: np.ndarray,
    y: np.ndarray,
    x_cells: int,
    y_cells: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized get_cell: returns (xi, yi) arrays."""
    xi = np.clip((x / 100.0 * x_cells).astype(np.int32), 0, x_cells - 1)
    yi = np.clip((y / 100.0 * y_cells).astype(np.int32), 0, y_cells - 1)
    return xi, yi


def compute_shot_goal_matrices_vectorized(
    df: pd.DataFrame,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> tuple[np.ndarray, np.ndarray]:
    """Vectorized shot/goal probability computation from DataFrame.

    Expects columns: action_type, result, start_x, start_y.
    """
    possession_count = np.zeros((y_cells, x_cells), dtype=np.float64)
    shot_count = np.zeros((y_cells, x_cells), dtype=np.float64)
    goal_count = np.zeros((y_cells, x_cells), dtype=np.float64)

    atype = df["action_type"].values
    result = df["result"].values
    sx = df["start_x"].values.astype(np.float64)
    sy = df["start_y"].values.astype(np.float64)

    # Possession actions (non-shot, non-receipt, non-freeze, non-unknown)
    possession_mask = np.isin(atype, [t.value for t in POSSESSION_TYPES])
    shot_mask = atype == ActionType.SHOT.value

    # Cell indices for possession actions
    pos_xi, pos_yi = _get_cell_indices_vectorized(
        sx[possession_mask], sy[possession_mask], x_cells, y_cells,
    )
    np.add.at(possession_count, (pos_yi, pos_xi), 1)

    # Cell indices for shot actions
    shot_xi, shot_yi = _get_cell_indices_vectorized(
        sx[shot_mask], sy[shot_mask], x_cells, y_cells,
    )
    np.add.at(shot_count, (shot_yi, shot_xi), 1)
    np.add.at(possession_count, (shot_yi, shot_xi), 1)

    # Goals = successful shots
    goal_mask = shot_mask & (result == ActionResult.SUCCESS.value)
    goal_xi, goal_yi = _get_cell_indices_vectorized(
        sx[goal_mask], sy[goal_mask], x_cells, y_cells,
    )
    np.add.at(goal_count, (goal_yi, goal_xi), 1)

    # Shot probability
    with np.errstate(divide="ignore", invalid="ignore"):
        shot_prob = np.where(possession_count > 0, shot_count / possession_count, 0.0)
    shot_prob = np.clip(shot_prob, 0.0, 1.0)

    # Goal probability
    with np.errstate(divide="ignore", invalid="ignore"):
        goal_prob = np.where(shot_count > 0, goal_count / shot_count, 0.0)
    # Default for cells with no shots: distance-based heuristic
    no_shot = shot_count == 0
    if no_shot.any():
        xi_arr = np.arange(x_cells)
        yi_arr = np.arange(y_cells)
        xi_grid, yi_grid = np.meshgrid(xi_arr, yi_arr)
        x_norm = (xi_grid + 0.5) / x_cells
        goal_prob[no_shot] = np.maximum(0.01, 0.3 * x_norm[no_shot] ** 2)
    goal_prob = np.clip(goal_prob, 0.0, 1.0)

    logger.info(
        "Shot prob: min=%.4f, max=%.4f, nonzero_cells=%d",
        shot_prob.min(), shot_prob.max(), (shot_prob > 0).sum(),
    )
    logger.info(
        "Goal prob: min=%.4f, max=%.4f, nonzero_cells=%d",
        goal_prob.min(), goal_prob.max(), (goal_prob > 0).sum(),
    )

    return shot_prob, goal_prob


def compute_transition_matrix_vectorized(
    df: pd.DataFrame,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> np.ndarray:
    """Vectorized transition matrix computation from DataFrame.

    Expects columns: action_type, start_x, start_y, end_x, end_y.
    """
    n_cells = x_cells * y_cells
    transitions = np.zeros((n_cells, n_cells), dtype=np.float64)

    atype = df["action_type"].values
    move_mask = np.isin(atype, [t.value for t in MOVE_TYPES])
    move_df = df.loc[move_mask]

    if move_df.empty:
        return transitions

    sx = move_df["start_x"].values.astype(np.float64)
    sy = move_df["start_y"].values.astype(np.float64)
    ex = move_df["end_x"].values.astype(np.float64)
    ey = move_df["end_y"].values.astype(np.float64)

    s_xi, s_yi = _get_cell_indices_vectorized(sx, sy, x_cells, y_cells)
    e_xi, e_yi = _get_cell_indices_vectorized(ex, ey, x_cells, y_cells)

    from_idx = s_yi * x_cells + s_xi
    to_idx = e_yi * x_cells + e_xi

    np.add.at(transitions, (from_idx, to_idx), 1)

    # Normalize rows
    row_sums = transitions.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        transitions = np.where(row_sums > 0, transitions / row_sums, 0.0)

    return transitions


def batch_action_xt_value(
    df: pd.DataFrame,
    xt_grid: np.ndarray,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
    chunk_size: int = 1_000_000,
) -> np.ndarray:
    """Compute xT value for all actions in a DataFrame (vectorized, chunked).

    Returns an array of xT deltas, same length as df.
    """
    n = len(df)
    result = np.zeros(n, dtype=np.float64)

    for start in range(0, n, chunk_size):
        end = min(start + chunk_size, n)
        chunk = df.iloc[start:end]

        sx = chunk["start_x"].values.astype(np.float64)
        sy = chunk["start_y"].values.astype(np.float64)
        ex = chunk["end_x"].values.astype(np.float64)
        ey = chunk["end_y"].values.astype(np.float64)

        s_xi, s_yi = _get_cell_indices_vectorized(sx, sy, x_cells, y_cells)
        e_xi, e_yi = _get_cell_indices_vectorized(ex, ey, x_cells, y_cells)

        start_xt = xt_grid[s_yi, s_xi]
        end_xt = xt_grid[e_yi, e_xi]

        result[start:end] = end_xt - start_xt

    return result


def compute_xt_from_actions(
    actions_path: Path = ACTIONS_PATH,
    xt_grid_path: Path = XT_GRID_PATH,
    matches_path: Path = MATCHES_PATH,
    events_path: Path = EVENTS_PATH,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> tuple[np.ndarray, pd.DataFrame]:
    """Full pipeline: read SPADL actions, compute xT grid, assign per-action xT.

    Steps:
    1. Read actions_all.parquet
    2. Compute shot_prob, goal_prob, transition matrices (vectorized)
    3. Iterate to convergence -> xT grid
    4. Save xT grid to xt_grid.npy
    5. Compute per-action xT delta (batch vectorized)
    6. Join season info from matches_all.parquet
    7. Join player_name from events_all.parquet
    8. Return (xt_grid, actions_with_xt DataFrame)

    The returned DataFrame has columns:
        player_id, player_name, team_id, match_id, season, competition,
        action_type, result, start_x, start_y, end_x, end_y, xt_delta
    """
    logger.info("Reading actions from %s", actions_path)
    df = pd.read_parquet(actions_path)
    logger.info("Loaded %d actions", len(df))

    xt_grid, df = compute_xt_values(df, x_cells=x_cells, y_cells=y_cells)

    # 3. Save xT grid
    xt_grid_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(xt_grid_path, xt_grid)
    logger.info("Saved xT grid to %s", xt_grid_path)

    # 4. Join season info
    logger.info("Joining season info from %s", matches_path)
    matches = pd.read_parquet(matches_path)
    matches["match_id"] = matches["match_id"].astype(str)
    season_map = (
        matches[["match_id", "season_name", "competition_name"]]
        .drop_duplicates("match_id")
    )
    df = df.merge(season_map, on="match_id", how="left")
    df.rename(columns={"season_name": "season", "competition_name": "competition"}, inplace=True)

    # 5. Join player_name
    logger.info("Joining player names from %s", events_path)
    events = pd.read_parquet(events_path, columns=["player_id", "player_name"])
    events["player_id"] = events["player_id"].astype(str)
    name_map = events.dropna(subset=["player_name"]).drop_duplicates("player_id")
    df = df.merge(name_map, on="player_id", how="left")
    df["player_name"] = df["player_name"].fillna("")

    logger.info(
        "Final actions with xT: %d rows, %d unique players",
        len(df), df["player_id"].nunique(),
    )
    return xt_grid, df


def compute_xt_values(
    actions_df: pd.DataFrame,
    x_cells: int = DEFAULT_X_CELLS,
    y_cells: int = DEFAULT_Y_CELLS,
) -> tuple[np.ndarray, pd.DataFrame]:
    """Compute an xT grid and per-action values without filesystem side effects.

    This is the reusable in-memory core behind :func:`compute_xt_from_actions`.
    It is intentionally independent of match/player metadata joins so small
    local samples can be explored without manufacturing full-data artifacts.
    """
    if actions_df.empty:
        return np.zeros((y_cells, x_cells), dtype=float), actions_df.copy()

    df = actions_df.copy()
    logger.info("Computing shot/goal matrices (vectorized)...")
    shot_prob, goal_prob = compute_shot_goal_matrices_vectorized(
        df,
        x_cells,
        y_cells,
    )
    logger.info("Computing transition matrix (vectorized)...")
    transitions = compute_transition_matrix_vectorized(df, x_cells, y_cells)
    logger.info("Iterating xT convergence...")
    xt_grid = iterate_xt(shot_prob, goal_prob, transitions, x_cells, y_cells)

    logger.info("Computing per-action xT values (batch)...")
    xt_delta = batch_action_xt_value(df, xt_grid, x_cells, y_cells)
    df["xt_delta"] = xt_delta
    logger.info(
        "xT sample: grid_min=%.6f grid_max=%.6f delta_mean=%.6f delta_std=%.6f",
        xt_grid.min(),
        xt_grid.max(),
        xt_delta.mean(),
        xt_delta.std(),
    )
    return xt_grid, df
