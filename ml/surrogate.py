"""
AIMATRY Machine Learning Layer: Surrogate Property Predictors & Uncertainty Quantification
Trains ensemble regressors to predict multi-dimensional textile properties with
epistemic uncertainty estimation and feature sensitivity analysis.
"""

import os
from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from core.physics import FIBER_SPECS, WEAVE_FACTORS, compute_blend_physics

# Master fiber feature columns for ML vectorization
FEATURE_FIBERS = list(FIBER_SPECS.keys())


def generate_training_data(n_samples: int = 400, seed: int = 42) -> Tuple[np.ndarray, np.ndarray, List[str], List[str]]:
    """
    Generates a dense, physically grounded training matrix across the continuous multi-fiber space.
    """
    np.random.seed(seed)
    n_fibers = len(FEATURE_FIBERS)
    X_rows = []
    y_rows = []

    weave_names = list(WEAVE_FACTORS.keys())

    for _ in range(n_samples):
        # Generate Dirichlet random blend fractions
        active_count = np.random.randint(1, 4)
        active_indices = np.random.choice(n_fibers, active_count, replace=False)
        dirichlet_weights = np.random.exponential(scale=1.0, size=active_count)
        dirichlet_weights /= dirichlet_weights.sum()

        w_vec = np.zeros(n_fibers)
        w_vec[active_indices] = dirichlet_weights

        gsm = float(np.random.uniform(150.0, 450.0))
        weave_idx = np.random.randint(0, len(weave_names))
        weave = weave_names[weave_idx]
        weave_mult = WEAVE_FACTORS[weave]["strength_mult"]

        # Compute ground truth physics
        blend_dict = {FEATURE_FIBERS[i]: float(w_vec[i]) for i in range(n_fibers)}
        phys = compute_blend_physics(blend_dict, gsm=gsm, weave_type=weave)

        feat = list(w_vec) + [gsm, weave_mult]
        X_rows.append(feat)

        target = [
            phys["tensile_strength_gpa"],
            phys["loi_pct"],
            phys["thermal_resistance_rct"],
            phys["evaporative_resistance_ret"],
            phys["total_heat_loss_thl_w_m2"],
        ]
        y_rows.append(target)

    feature_names = [f"wt_{f.split(' ')[0]}" for f in FEATURE_FIBERS] + ["gsm", "weave_mult"]
    target_names = ["Tensile_Strength_GPa", "LOI_pct", "Rct_m2K_W", "Ret_m2Pa_W", "THL_W_m2"]

    return np.array(X_rows, dtype=float), np.array(y_rows, dtype=float), feature_names, target_names


class TextileMLSurrogate:
    """
    Ensemble ML Surrogate with variance-based uncertainty quantification.
    """

    def __init__(self, n_estimators: int = 25, seed: int = 42):
        self.n_estimators = n_estimators
        self.seed = seed
        self.models = {}
        self.feature_names = []
        self.target_names = []
        self._is_trained = False

    def train(self):
        """Trains Random Forest ensemble for each target property."""
        X, y, self.feature_names, self.target_names = generate_training_data(n_samples=400, seed=self.seed)

        for j, target in enumerate(self.target_names):
            rf = RandomForestRegressor(
                n_estimators=self.n_estimators,
                max_depth=10,
                min_samples_leaf=2,
                random_state=self.seed,
                n_jobs=1,
            )
            rf.fit(X, y[:, j])
            self.models[target] = rf

        self._is_trained = True

    def predict_with_uncertainty(
        self,
        blend_weights: Dict[str, float],
        gsm: float = 260.0,
        weave_type: str = "Ripstop Grid",
    ) -> Dict[str, Dict[str, float]]:
        """
        Runs ensemble inference across all trees to calculate mean predictions
        and epistemic uncertainty standard deviations.
        """
        if not self._is_trained:
            self.train()

        total_w = sum(blend_weights.values())
        if total_w <= 0:
            total_w = 1.0
        w_vec = [blend_weights.get(f, 0.0) / total_w for f in FEATURE_FIBERS]
        weave_mult = WEAVE_FACTORS.get(weave_type, WEAVE_FACTORS["Ripstop Grid"])["strength_mult"]
        x_in = np.array([w_vec + [gsm, weave_mult]], dtype=float)

        results = {}
        for target, model in self.models.items():
            tree_preds = np.array([tree.predict(x_in)[0] for tree in model.estimators_])
            mean_val = float(np.mean(tree_preds))
            std_val = float(np.std(tree_preds))
            ci_lower = max(0.0, mean_val - 1.96 * std_val)
            ci_upper = mean_val + 1.96 * std_val

            results[target] = {
                "mean": round(mean_val, 3),
                "std_uncertainty": round(std_val, 3),
                "ci_95_lower": round(ci_lower, 3),
                "ci_95_upper": round(ci_upper, 3),
            }

        return results

    def get_feature_importances(self) -> pd.DataFrame:
        """Returns relative feature importance weights across all predicted targets."""
        if not self._is_trained:
            self.train()

        df_dict = {"Feature": self.feature_names}
        for target, model in self.models.items():
            df_dict[target] = np.round(model.feature_importances_ * 100, 1)

        return pd.DataFrame(df_dict)


_surrogate_singleton = None


def get_surrogate_model() -> TextileMLSurrogate:
    global _surrogate_singleton
    if _surrogate_singleton is None:
        _surrogate_singleton = TextileMLSurrogate()
        _surrogate_singleton.train()
    return _surrogate_singleton
