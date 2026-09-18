"""
AIMATRY Machine Learning: Gaussian Process Active Learning & Optimal Experiment Design
Implements closed-loop Bayesian Optimization with Expected Improvement (EI) and UCB
to guide NITRA textile scientists on the next optimal laboratory test coupon.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from scipy.stats import norm
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel as C
from database.lab_importer import get_all_lab_records, generate_sample_nitra_lab_csv, import_lab_test_file


class ActiveLearningRecommender:
    def __init__(self, target_metric: str = 'measured_thl', maximize: bool = True):
        self.target_metric = target_metric
        self.maximize = maximize
        # Matern 5/2 kernel with automatic relevance determination (ARD) + noise white kernel
        kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=[0.5, 0.5, 0.5, 0.5, 50.0], nu=2.5) + WhiteKernel(noise_level=1.0)
        self.gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=5, normalize_y=True, random_state=42)
        self.is_fitted = False
        self.best_y = -np.inf if maximize else np.inf
        self.X_train = None
        self.y_train = None

    def fit_from_database(self, db_path: Optional[str] = None) -> int:
        """Fits GP model on existing lab records from database."""
        kwargs = {'db_path': db_path} if db_path else {}
        df = get_all_lab_records(**kwargs)
        if df.empty or len(df) < 3:
            # Seed with sample data if database is empty
            csv_bytes = generate_sample_nitra_lab_csv()
            import_lab_test_file(csv_bytes, 'nitra_seed_trials.csv', **kwargs)
            df = get_all_lab_records(**kwargs)

        X_rows, y_vals = [], []
        for _, row in df.iterrows():
            if pd.notna(row.get(self.target_metric)):
                p_ar = float(row.get('p_aramid', 0.5))
                m_ar = float(row.get('m_aramid', 0.4))
                pbi = float(row.get('pbi', 0.05))
                moda = float(row.get('modacrylic', 0.05))
                gsm = float(row.get('gsm', 220.0))
                X_rows.append([p_ar, m_ar, pbi, moda, gsm])
                y_vals.append(float(row[self.target_metric]))

        if len(X_rows) >= 3:
            self.X_train = np.array(X_rows)
            self.y_train = np.array(y_vals)
            self.gp.fit(self.X_train, self.y_train)
            self.is_fitted = True
            self.best_y = float(np.max(self.y_train) if self.maximize else np.min(self.y_train))
            return len(X_rows)
        return 0

    def compute_expected_improvement(self, X: np.ndarray, xi: float = 0.01) -> np.ndarray:
        """Computes analytical Expected Improvement (EI)."""
        if not self.is_fitted:
            return np.zeros(len(X))
        mu, sigma = self.gp.predict(X, return_std=True)
        sigma = np.maximum(sigma, 1e-6)

        if self.maximize:
            improvement = mu - self.best_y - xi
        else:
            improvement = self.best_y - mu - xi

        Z = improvement / sigma
        ei = improvement * norm.cdf(Z) + sigma * norm.pdf(Z)
        return np.maximum(ei, 0.0)

    def compute_ucb(self, X: np.ndarray, beta: float = 2.0) -> np.ndarray:
        """Computes Upper Confidence Bound (UCB)."""
        if not self.is_fitted:
            return np.zeros(len(X))
        mu, sigma = self.gp.predict(X, return_std=True)
        if self.maximize:
            return mu + beta * sigma
        else:
            return -mu + beta * sigma

    def generate_candidate_grid(self, n_samples: int = 500) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """Generates valid physical formulation candidates with sum(w_i) == 1.0."""
        np.random.seed(101)
        candidates_X = []
        meta_list = []

        for _ in range(n_samples):
            # Dirichlet distribution ensures components sum to 1.0
            weights = np.random.dirichlet([2.0, 2.0, 0.8, 0.5])
            gsm = float(np.random.uniform(180, 280))
            candidates_X.append([weights[0], weights[1], weights[2], weights[3], gsm])
            meta_list.append({
                'p_aramid': round(float(weights[0]), 3),
                'm_aramid': round(float(weights[1]), 3),
                'pbi': round(float(weights[2]), 3),
                'modacrylic': round(float(weights[3]), 3),
                'gsm': round(gsm, 1),
                'recommended_weave': 'Ripstop' if weights[0] > 0.5 else 'Twill',
            })

        return np.array(candidates_X), meta_list

    def recommend_next_experiments(
        self,
        acquisition: str = 'Expected Improvement',
        top_k: int = 5,
        beta: float = 2.0,
        xi: float = 0.05
    ) -> List[Dict[str, Any]]:
        """
        Recommends top-K physical test coupons for the next laboratory fabrication batch.
        """
        if not self.is_fitted:
            self.fit_from_database()

        X_cand, meta = self.generate_candidate_grid(n_samples=600)
        mu, sigma = self.gp.predict(X_cand, return_std=True)

        if acquisition == 'Expected Improvement':
            acq_scores = self.compute_expected_improvement(X_cand, xi=xi)
        else:
            acq_scores = self.compute_ucb(X_cand, beta=beta)

        top_indices = np.argsort(acq_scores)[::-1][:top_k]
        recommendations = []

        for rank, idx in enumerate(top_indices, 1):
            m = meta[idx].copy()
            m['rank'] = rank
            m['predicted_mean'] = round(float(mu[idx]), 2)
            m['epistemic_std'] = round(float(sigma[idx]), 2)
            m['acquisition_score'] = round(float(acq_scores[idx]), 4)
            m['target_metric'] = self.target_metric
            m['ci_95_low'] = round(float(mu[idx] - 1.96 * sigma[idx]), 2)
            m['ci_95_high'] = round(float(mu[idx] + 1.96 * sigma[idx]), 2)
            recommendations.append(m)

        return recommendations
