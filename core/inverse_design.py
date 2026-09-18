"""
AIMATRY Core: Inverse Material Design Solver
Reverse-engineers optimal fiber blend formulations and fabric construction parameters
directly from target performance specifications (Target Specs → Formula).
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from scipy.optimize import minimize
from core.physics import FIBER_SPECS, WEAVE_FACTORS, compute_blend_physics

FEATURE_FIBERS = list(FIBER_SPECS.keys())


def inverse_solve_formulation(
    target_specs: Dict[str, float],
    allowed_fibers: List[str] = None,
    preferred_weave: str = "Ripstop Grid",
    max_budget_inr: float = 6000.0,
) -> Dict[str, Any]:
    """
    Reverse-engineers optimal fiber ratios and GSM from desired target specifications.

    Args:
        target_specs: Dict containing:
            - "min_htp": Minimum HTP score (0-100)
            - "min_thl": Minimum THL score (0-100)
            - "min_tensile": Minimum Tensile score (0-100)
            - "min_loi": Minimum LOI % (e.g. 28.0)
            - "min_bio_pct": Minimum Bio-based % (0-100)
        allowed_fibers: List of fibers permitted in formulation.
        preferred_weave: Preferred weave architecture from WEAVE_FACTORS.
        max_budget_inr: Maximum allowed cost per square meter in INR.

    Returns:
        Discovered optimal blend dict, achieved properties, and constraint satisfaction report.
    """
    if not allowed_fibers:
        allowed_fibers = FEATURE_FIBERS[:7]

    n_fibers = len(allowed_fibers)

    target_htp = float(target_specs.get("min_htp", 75.0))
    target_thl = float(target_specs.get("min_thl", 60.0))
    target_tensile = float(target_specs.get("min_tensile", 70.0))
    target_loi = float(target_specs.get("min_loi", 28.0))
    target_bio = float(target_specs.get("min_bio_pct", 0.0))

    def loss_function(x):
        # x = [w_0, w_1, ..., w_{n-1}, gsm]
        raw_w = x[:n_fibers]
        gsm = float(x[n_fibers])

        total_w = float(raw_w.sum())
        if total_w <= 0:
            return 1e6
        norm_w = {allowed_fibers[i]: float(raw_w[i] / total_w) for i in range(n_fibers)}

        phys = compute_blend_physics(norm_w, gsm=gsm, weave_type=preferred_weave)
        scores = phys["scores"]

        # Penalties for violating targets
        p_htp = max(0.0, target_htp - scores["Thermal Protection (HTP)"]) ** 2
        p_thl = max(0.0, target_thl - scores["Comfort & Breathability (THL)"]) ** 2
        p_ten = max(0.0, target_tensile - scores["Tensile Strength"]) ** 2
        p_loi = max(0.0, target_loi - phys["loi_pct"]) ** 2
        p_bio = max(0.0, target_bio - phys["bio_based_pct"]) ** 2
        p_cost = max(0.0, phys["cost_inr_per_m2"] - max_budget_inr) ** 2

        # Regularizer: minimize unnecessary mass and CO2
        reg_co2 = phys["co2_kg_per_kg"] * 0.1
        reg_gsm = (gsm / 300.0) * 0.2

        # Sparsity penalty (prefer blends with <= 3 fibers)
        sparsity = float(np.sum(raw_w > 0.05)) * 0.5

        total_loss = (p_htp * 3.0 + p_thl * 2.5 + p_ten * 2.5 + p_loi * 2.0 + p_bio * 1.5 + p_cost * 0.01 + reg_co2 + reg_gsm + sparsity)
        return total_loss

    # Bounds: w_i in [0, 1], gsm in [160, 420]
    bounds = [(0.0, 1.0)] * n_fibers + [(160.0, 420.0)]

    # Multi-start local optimization using SLSQP
    best_res = None
    best_loss = 1e9

    np.random.seed(42)
    for _ in range(8):
        init_w = np.random.uniform(0.1, 0.9, size=n_fibers)
        init_w /= init_w.sum()
        init_gsm = np.random.uniform(200.0, 360.0)
        x0 = list(init_w) + [init_gsm]

        res = minimize(
            loss_function,
            x0,
            method="SLSQP",
            bounds=bounds,
            options={"maxiter": 100, "ftol": 1e-4},
        )
        if res.fun < best_loss:
            best_loss = res.fun
            best_res = res

    # Extract final discovered blend
    opt_x = best_res.x
    opt_raw_w = opt_x[:n_fibers]
    opt_gsm = round(float(opt_x[n_fibers]), 0)
    total_opt = float(opt_raw_w.sum())

    discovered_blend = {}
    for i in range(n_fibers):
        pct = round(float(opt_raw_w[i] / total_opt) * 100, 1)
        if pct >= 3.0:  # Prune negligible trace components
            discovered_blend[allowed_fibers[i]] = pct

    # Re-normalize to exact 100%
    tot = sum(discovered_blend.values())
    discovered_blend = {k: round((v / tot) * 100, 1) for k, v in discovered_blend.items()}

    # Compute final physical specs of discovered solution
    final_physics = compute_blend_physics(discovered_blend, gsm=opt_gsm, weave_type=preferred_weave)
    final_scores = final_physics["scores"]

    # Target comparison report
    target_comparison = [
        {"Property": "Thermal Protection (HTP)", "Target": f"≥ {target_htp}", "Achieved": f"{final_scores['Thermal Protection (HTP)']}", "Met": "✅ PASS" if final_scores["Thermal Protection (HTP)"] >= target_htp else "⚠️ CLOSE"},
        {"Property": "Comfort & Breathability (THL)", "Target": f"≥ {target_thl}", "Achieved": f"{final_scores['Comfort & Breathability (THL)']}", "Met": "✅ PASS" if final_scores["Comfort & Breathability (THL)"] >= target_thl else "⚠️ CLOSE"},
        {"Property": "Tensile Strength Score", "Target": f"≥ {target_tensile}", "Achieved": f"{final_scores['Tensile Strength']}", "Met": "✅ PASS" if final_scores["Tensile Strength"] >= target_tensile else "⚠️ CLOSE"},
        {"Property": "Limiting Oxygen Index (LOI)", "Target": f"≥ {target_loi}%", "Achieved": f"{final_physics['loi_pct']}%", "Met": "✅ PASS" if final_physics["loi_pct"] >= target_loi else "⚠️ CLOSE"},
        {"Property": "Bio-Based Content", "Target": f"≥ {target_bio}%", "Achieved": f"{final_physics['bio_based_pct']}%", "Met": "✅ PASS" if final_physics["bio_based_pct"] >= target_bio else "⚠️ CLOSE"},
        {"Property": "Production Cost / m²", "Target": f"≤ ₹{max_budget_inr}", "Achieved": f"₹{final_physics['cost_inr_per_m2']}", "Met": "✅ PASS" if final_physics["cost_inr_per_m2"] <= max_budget_inr else "⚠️ EXCEEDED"},
    ]

    blend_name = " / ".join([f"{pct}% {name.split(' ')[0]}" for name, pct in sorted(discovered_blend.items(), key=lambda x: x[1], reverse=True)])

    return {
        "success": bool(best_loss < 50.0),
        "discovered_blend": discovered_blend,
        "blend_name": blend_name,
        "recommended_gsm": opt_gsm,
        "recommended_weave": preferred_weave,
        "physics": final_physics,
        "target_comparison": target_comparison,
        "loss": round(float(best_loss), 4),
    }
