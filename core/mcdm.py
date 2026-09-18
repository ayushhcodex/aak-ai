"""
AIMATRY Core: Multi-Criteria Decision Making (MCDM) Engine
Implements the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) algorithm.
"""

from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import pandas as pd


def topsis_rank_candidates(
    candidates_or_weights: Any,
    weights_or_none: Optional[Dict[str, float]] = None,
    criteria_keys: List[str] = None,
    beneficial_criteria: Dict[str, bool] = None,
) -> Tuple[pd.DataFrame, str]:
    """
    Ranks materials using the TOPSIS algorithm based on user-defined priority weights.
    Accepts either (weights) using default scenarios, or (candidates, weights).
    """
    from data import SCENARIOS

    if weights_or_none is None:
        # Called as topsis_rank_candidates(weights)
        weights = candidates_or_weights if isinstance(candidates_or_weights, dict) else {}
        candidates = SCENARIOS
    else:
        # Called as topsis_rank_candidates(candidates, weights)
        candidates = candidates_or_weights
        weights = weights_or_none

    if not candidates:
        return pd.DataFrame(), ""

    if criteria_keys is None:
        criteria_keys = [
            "Thermal Protection (HTP)",
            "Comfort & Breathability (THL)",
            "Tensile Strength",
            "Flexibility",
            "Manufacturability",
        ]

    if beneficial_criteria is None:
        beneficial_criteria = {k: True for k in criteria_keys}

    # Normalize weights
    raw_weights = np.array([max(weights.get(k, 50.0), 0.01) for k in criteria_keys], dtype=float)
    if raw_weights.sum() > 0:
        w_norm = raw_weights / raw_weights.sum()
    else:
        w_norm = np.ones(len(criteria_keys)) / len(criteria_keys)

    # Build Decision Matrix X (m alternatives x n criteria)
    candidate_names = list(candidates.keys())
    matrix = []
    for name in candidate_names:
        row = []
        c_scores = candidates[name].get("scores", {})
        for k in criteria_keys:
            row.append(float(c_scores.get(k, 50.0)))
        matrix.append(row)

    X = np.array(matrix, dtype=float)
    m, n = X.shape

    # Step 1: Vector Normalization R = X / sqrt(sum(x_ij^2))
    denom = np.sqrt(np.sum(X ** 2, axis=0))
    denom[denom == 0] = 1e-9
    R = X / denom

    # Step 2: Weighted Normalized Matrix V = R * w
    V = R * w_norm

    # Step 3: Determine Ideal Positive (A+) and Ideal Negative (A-) Solutions
    ideal_best = np.zeros(n)
    ideal_worst = np.zeros(n)
    for j, k in enumerate(criteria_keys):
        if beneficial_criteria.get(k, True):
            ideal_best[j] = np.max(V[:, j])
            ideal_worst[j] = np.min(V[:, j])
        else:
            ideal_best[j] = np.min(V[:, j])
            ideal_worst[j] = np.max(V[:, j])

    # Step 4: Calculate Euclidean Distances S+ and S-
    S_plus = np.sqrt(np.sum((V - ideal_best) ** 2, axis=1))
    S_minus = np.sqrt(np.sum((V - ideal_worst) ** 2, axis=1))

    # Step 5: Calculate Relative Closeness to Ideal Solution C_i = S- / (S+ + S-)
    total_dist = S_plus + S_minus
    total_dist[total_dist == 0] = 1e-9
    C = S_minus / total_dist

    # Step 6: Build Output DataFrame sorted by rank
    df = pd.DataFrame({
        "Scenario": candidate_names,
        "Blend Formulation": [candidates[name].get("blend", name) for name in candidate_names],
        "TOPSIS Score": np.round(C, 4),
        "TOPSIS Match %": np.round(C * 100, 1),
    })

    # Append individual criteria scores for transparent inspection
    for j, k in enumerate(criteria_keys):
        df[k] = [candidates[name].get("scores", {}).get(k, 50) for name in candidate_names]

    df = df.sort_values(by="TOPSIS Score", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1

    top_scenario = df.iloc[0]["Scenario"] if not df.empty else ""
    return df, top_scenario
