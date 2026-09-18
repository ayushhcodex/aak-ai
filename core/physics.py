"""
AIMATRY Core: Physics-Based Micromechanics & Composite Calculator
Calculates macro composite properties from fiber constituent ratios using:
- Voigt & Reuss Rule-of-Mixtures (Modulus, Tensile Strength, Density)
- Empirical & Thermal Transport Models (Thermal Resistance R_ct, Evaporative Resistance R_et)
- Limiting Oxygen Index (LOI) linear blending
- Areal density (GSM) & Weave architecture factors
"""

from typing import Dict, Any, Tuple
import numpy as np


# Standardized Physical & Chemical Database of High-Performance Protective Fibers
FIBER_SPECS = {
    "Meta-aramid (Nomex)": {
        "density_g_cm3": 1.38,
        "tensile_strength_gpa": 0.65,
        "tensile_modulus_gpa": 17.5,
        "elongation_pct": 22.0,
        "loi_pct": 29.0,
        "max_temp_c": 370.0,
        "thermal_conductivity_w_mk": 0.13,
        "moisture_regain_pct": 4.5,
        "flexibility_factor": 0.85,
        "synthesizability_factor": 0.90,
        "cost_usd_kg": 38.0,
        "cost_inr_kg": 3150.0,
        "co2_kg": 31.0,
        "water_L": 80.0,
        "bio_pct": 0.0,
        "recyclable": "Partial",
    },
    "Para-aramid (Kevlar/Twaron)": {
        "density_g_cm3": 1.44,
        "tensile_strength_gpa": 3.60,
        "tensile_modulus_gpa": 112.0,
        "elongation_pct": 3.6,
        "loi_pct": 30.0,
        "max_temp_c": 450.0,
        "thermal_conductivity_w_mk": 0.04,
        "moisture_regain_pct": 3.5,
        "flexibility_factor": 0.50,
        "synthesizability_factor": 0.75,
        "cost_usd_kg": 55.0,
        "cost_inr_kg": 4550.0,
        "co2_kg": 32.5,
        "water_L": 110.0,
        "bio_pct": 0.0,
        "recyclable": "No",
    },
    "UHMWPE (Dyneema/Spectra)": {
        "density_g_cm3": 0.97,
        "tensile_strength_gpa": 3.40,
        "tensile_modulus_gpa": 110.0,
        "elongation_pct": 3.5,
        "loi_pct": 18.5,
        "max_temp_c": 140.0,
        "thermal_conductivity_w_mk": 20.0,
        "moisture_regain_pct": 0.0,
        "flexibility_factor": 0.65,
        "synthesizability_factor": 0.65,
        "cost_usd_kg": 75.0,
        "cost_inr_kg": 6200.0,
        "co2_kg": 26.0,
        "water_L": 95.0,
        "bio_pct": 0.0,
        "recyclable": "Partial",
    },
    "PBO (Zylon)": {
        "density_g_cm3": 1.56,
        "tensile_strength_gpa": 5.80,
        "tensile_modulus_gpa": 270.0,
        "elongation_pct": 2.5,
        "loi_pct": 68.0,
        "max_temp_c": 650.0,
        "thermal_conductivity_w_mk": 0.28,
        "moisture_regain_pct": 2.0,
        "flexibility_factor": 0.40,
        "synthesizability_factor": 0.50,
        "cost_usd_kg": 180.0,
        "cost_inr_kg": 14900.0,
        "co2_kg": 48.0,
        "water_L": 160.0,
        "bio_pct": 0.0,
        "recyclable": "No",
    },
    "Polyimide (Kapton/P84)": {
        "density_g_cm3": 1.41,
        "tensile_strength_gpa": 0.85,
        "tensile_modulus_gpa": 4.5,
        "elongation_pct": 30.0,
        "loi_pct": 38.0,
        "max_temp_c": 500.0,
        "thermal_conductivity_w_mk": 0.12,
        "moisture_regain_pct": 3.0,
        "flexibility_factor": 0.70,
        "synthesizability_factor": 0.60,
        "cost_usd_kg": 95.0,
        "cost_inr_kg": 7850.0,
        "co2_kg": 38.0,
        "water_L": 90.0,
        "bio_pct": 0.0,
        "recyclable": "No",
    },
    "Basalt Fiber": {
        "density_g_cm3": 2.65,
        "tensile_strength_gpa": 3.10,
        "tensile_modulus_gpa": 89.0,
        "elongation_pct": 3.15,
        "loi_pct": 75.0,
        "max_temp_c": 700.0,
        "thermal_conductivity_w_mk": 0.035,
        "moisture_regain_pct": 0.1,
        "flexibility_factor": 0.30,
        "synthesizability_factor": 0.80,
        "cost_usd_kg": 12.0,
        "cost_inr_kg": 990.0,
        "co2_kg": 6.5,
        "water_L": 12.0,
        "bio_pct": 0.0,
        "recyclable": "Yes",
    },
    "Carbon Fiber (PAN-based)": {
        "density_g_cm3": 1.78,
        "tensile_strength_gpa": 4.10,
        "tensile_modulus_gpa": 230.0,
        "elongation_pct": 1.8,
        "loi_pct": 55.0,
        "max_temp_c": 600.0,
        "thermal_conductivity_w_mk": 15.0,
        "moisture_regain_pct": 0.1,
        "flexibility_factor": 0.20,
        "synthesizability_factor": 0.55,
        "cost_usd_kg": 45.0,
        "cost_inr_kg": 3720.0,
        "co2_kg": 35.0,
        "water_L": 65.0,
        "bio_pct": 0.0,
        "recyclable": "Partial",
    },
    "FR Viscose (Lenzing FR)": {
        "density_g_cm3": 1.50,
        "tensile_strength_gpa": 0.32,
        "tensile_modulus_gpa": 9.0,
        "elongation_pct": 18.0,
        "loi_pct": 29.5,
        "max_temp_c": 220.0,
        "thermal_conductivity_w_mk": 0.07,
        "moisture_regain_pct": 12.5,
        "flexibility_factor": 0.95,
        "synthesizability_factor": 0.95,
        "cost_usd_kg": 8.5,
        "cost_inr_kg": 700.0,
        "co2_kg": 4.2,
        "water_L": 45.0,
        "bio_pct": 85.0,
        "recyclable": "Yes",
    },
    "Milkweed Floss (Asclepias)": {
        "density_g_cm3": 0.25,
        "tensile_strength_gpa": 0.18,
        "tensile_modulus_gpa": 3.2,
        "elongation_pct": 4.0,
        "loi_pct": 24.0,
        "max_temp_c": 180.0,
        "thermal_conductivity_w_mk": 0.022,
        "moisture_regain_pct": 10.0,
        "flexibility_factor": 0.90,
        "synthesizability_factor": 0.70,
        "cost_usd_kg": 18.0,
        "cost_inr_kg": 1490.0,
        "co2_kg": 2.1,
        "water_L": 15.0,
        "bio_pct": 100.0,
        "recyclable": "Yes",
    },
    "PTFE (Teflon / Gore membrane)": {
        "density_g_cm3": 2.20,
        "tensile_strength_gpa": 0.04,
        "tensile_modulus_gpa": 0.5,
        "elongation_pct": 300.0,
        "loi_pct": 95.0,
        "max_temp_c": 260.0,
        "thermal_conductivity_w_mk": 0.25,
        "moisture_regain_pct": 0.0,
        "flexibility_factor": 0.80,
        "synthesizability_factor": 0.85,
        "cost_usd_kg": 32.0,
        "cost_inr_kg": 2650.0,
        "co2_kg": 18.0,
        "water_L": 30.0,
        "bio_pct": 0.0,
        "recyclable": "No",
    },
    "Antistatic Grid (Belltron / Stainless steel)": {
        "density_g_cm3": 7.90,
        "tensile_strength_gpa": 1.20,
        "tensile_modulus_gpa": 190.0,
        "elongation_pct": 35.0,
        "loi_pct": 100.0,
        "max_temp_c": 900.0,
        "thermal_conductivity_w_mk": 16.0,
        "moisture_regain_pct": 0.0,
        "flexibility_factor": 0.40,
        "synthesizability_factor": 0.90,
        "cost_usd_kg": 25.0,
        "cost_inr_kg": 2070.0,
        "co2_kg": 12.0,
        "water_L": 20.0,
        "bio_pct": 0.0,
        "recyclable": "Yes",
    },
    "Silica Aerogel Nanocomposite": {
        "density_g_cm3": 0.12,
        "tensile_strength_gpa": 0.02,
        "tensile_modulus_gpa": 0.01,
        "elongation_pct": 1.0,
        "loi_pct": 100.0,
        "max_temp_c": 650.0,
        "thermal_conductivity_w_mk": 0.018,
        "moisture_regain_pct": 0.5,
        "flexibility_factor": 0.70,
        "synthesizability_factor": 0.60,
        "cost_usd_kg": 60.0,
        "cost_inr_kg": 4970.0,
        "co2_kg": 15.0,
        "water_L": 35.0,
        "bio_pct": 0.0,
        "recyclable": "No",
    },
}


WEAVE_FACTORS = {
    "Plain Weave (1/1)": {"strength_mult": 0.90, "flex_mult": 0.75, "permeability_mult": 0.80, "description": "Tightest interlacing, high stability, moderate drape"},
    "Twill Weave (2/1)": {"strength_mult": 0.95, "flex_mult": 0.90, "permeability_mult": 0.90, "description": "Diagonal ribs, superior tear resistance and drape"},
    "Ripstop Grid": {"strength_mult": 1.15, "flex_mult": 0.85, "permeability_mult": 0.88, "description": "Reinforced cross-grid prevents puncture and tear propagation"},
    "Satin Weave (4/1)": {"strength_mult": 0.92, "flex_mult": 1.10, "permeability_mult": 0.95, "description": "Smooth surface, maximum flexibility, snag-sensitive"},
    "Auxetic Re-entrant Grid": {"strength_mult": 1.25, "flex_mult": 0.80, "permeability_mult": 0.75, "description": "Negative Poisson's ratio; thickens and densifies under impact"},
}


def compute_blend_physics(
    blend_weights: Dict[str, float],
    gsm: float = 240.0,
    weave_type: str = "Ripstop Grid",
    fabric_thickness_mm: float = 0.85,
) -> Dict[str, Any]:
    """
    Computes analytical micromechanical, thermal, LOI, and comfort metrics
    for an arbitrary multi-fiber blend and fabric architecture.

    Args:
        blend_weights: Dict of {fiber_name: weight_fraction_or_pct}
        gsm: Fabric Areal Density in grams per square meter (g/m²)
        weave_type: Key from WEAVE_FACTORS
        fabric_thickness_mm: Total fabric thickness in millimeters

    Returns:
        Comprehensive dictionary of calculated physical properties and normalized 0-100 radar scores.
    """
    # Normalize weight percentages
    total_w = sum(blend_weights.values())
    if total_w <= 0:
        total_w = 1.0
    w_fractions = {k: v / total_w for k, v in blend_weights.items() if v > 0 and k in FIBER_SPECS}

    if not w_fractions:
        # Fallback to default Nomex
        w_fractions = {"Meta-aramid (Nomex)": 1.0}

    # Calculate Bulk Composite Density (Harmonic mean of densities weighted by mass fraction)
    # 1 / rho_c = sum(w_i / rho_i)
    inv_density = sum(w / FIBER_SPECS[f]["density_g_cm3"] for f, w in w_fractions.items())
    composite_density = 1.0 / inv_density if inv_density > 0 else 1.4

    # Calculate Volume Fractions: V_i = (w_i / rho_i) / (1 / rho_c)
    v_fractions = {f: (w / FIBER_SPECS[f]["density_g_cm3"]) * composite_density for f, w in w_fractions.items()}

    # Voigt Rule-of-Mixtures for Tensile Strength (GPa) and Tensile Modulus (GPa)
    composite_tensile_strength = sum(v * FIBER_SPECS[f]["tensile_strength_gpa"] for f, v in v_fractions.items())
    composite_tensile_modulus = sum(v * FIBER_SPECS[f]["tensile_modulus_gpa"] for f, v in v_fractions.items())

    # Reuss Rule-of-Mixtures for Transverse / Series Elastic Modulus
    inv_modulus = sum(v / max(FIBER_SPECS[f]["tensile_modulus_gpa"], 0.001) for f, v in v_fractions.items())
    reuss_modulus = 1.0 / inv_modulus if inv_modulus > 0 else composite_tensile_modulus

    # Limiting Oxygen Index (LOI) linear blending: LOI_c = sum(w_i * LOI_i)
    composite_loi = sum(w * FIBER_SPECS[f]["loi_pct"] for f, w in w_fractions.items())

    # Effective Thermal Conductivity (Harmonic/Geometric mixture) (W/m·K)
    # k_eff approx = sum(v_i * k_i) (Parallel / upper bound)
    k_eff = sum(v * FIBER_SPECS[f]["thermal_conductivity_w_mk"] for f, v in v_fractions.items())
    k_eff = max(k_eff, 0.015)

    # Maximum Continuous Service Temperature (°C) - limited by weakest or mass weighted
    max_service_temp = sum(w * FIBER_SPECS[f]["max_temp_c"] for f, w in w_fractions.items())

    # Thermal Resistance R_ct (m²·K/W) = thickness_m / k_eff
    thickness_m = (fabric_thickness_mm / 1000.0)
    r_ct = thickness_m / k_eff

    # Moisture Regain (%)
    composite_moisture_regain = sum(w * FIBER_SPECS[f]["moisture_regain_pct"] for f, w in w_fractions.items())

    # Evaporative Resistance R_et (m²·Pa/W)
    # Dependent on GSM, thickness, moisture regain, and weave permeability
    weave_data = WEAVE_FACTORS.get(weave_type, WEAVE_FACTORS["Ripstop Grid"])
    r_et = (fabric_thickness_mm * 4.5) / (max(composite_moisture_regain, 0.5) * weave_data["permeability_mult"])
    r_et = max(min(r_et, 45.0), 3.0)

    # Total Heat Loss THL (W/m²) per ASTM F1868:
    # THL approx = (10 / (R_ct + 0.04)) + (1000 / (R_et + 0.004)) (standard empirical model)
    thl_value = (10.0 / (r_ct + 0.04)) + (1000.0 / (r_et + 0.004))
    # Clip to realistic lab range: 100 to 650 W/m²
    thl_value = max(min(thl_value, 650.0), 80.0)

    # Apply Weave Multipliers to Strength
    effective_tensile_strength = composite_tensile_strength * weave_data["strength_mult"]

    # Composite Cost & Sustainability
    cost_usd = sum(w * FIBER_SPECS[f]["cost_usd_kg"] for f, w in w_fractions.items()) * (gsm / 1000.0)
    cost_inr = sum(w * FIBER_SPECS[f]["cost_inr_kg"] for f, w in w_fractions.items()) * (gsm / 1000.0)
    co2_kg = sum(w * FIBER_SPECS[f]["co2_kg"] for f, w in w_fractions.items())
    water_l = sum(w * FIBER_SPECS[f]["water_L"] for f, w in w_fractions.items())
    bio_based_pct = sum(w * FIBER_SPECS[f]["bio_pct"] for f, w in w_fractions.items())

    # ── Normalize Scores to 0-100 Radar Scale ─────────────────────────────
    # HTP Score (0-100): High LOI, Low k_eff, High Max Temp, Adequate GSM
    htp_score = (
        (min(composite_loi, 70.0) / 70.0) * 40.0
        + (min(max_service_temp, 700.0) / 700.0) * 35.0
        + (max(0, 0.30 - min(k_eff, 0.30)) / 0.30) * 25.0
    )
    htp_score = float(np.clip(htp_score, 10.0, 99.0))

    # THL / Comfort Score (0-100): Higher THL, Lower R_et, High Moisture Regain
    thl_score = (
        (min(thl_value, 550.0) / 550.0) * 50.0
        + (min(composite_moisture_regain, 12.0) / 12.0) * 25.0
        + (max(0, 35.0 - min(r_et, 35.0)) / 35.0) * 25.0
    )
    thl_score = float(np.clip(thl_score, 10.0, 98.0))

    # Tensile Strength Score (0-100): Function of GPa (0.2 to 5.0 GPa mapped to 10-100)
    tensile_score = (min(effective_tensile_strength, 5.0) / 5.0) * 100.0
    tensile_score = float(np.clip(tensile_score, 15.0, 99.0))

    # Flexibility Score (0-100): High elongation, low modulus, low density, weave factor
    flex_base = sum(w * FIBER_SPECS[f]["flexibility_factor"] for f, w in w_fractions.items())
    flex_score = (flex_base * weave_data["flex_mult"] * (300.0 / max(gsm, 150.0))) * 100.0
    flex_score = float(np.clip(flex_score, 15.0, 98.0))

    # Manufacturability Score (0-100): Blend complexity penalty + monomer availability
    synth_base = sum(w * FIBER_SPECS[f]["synthesizability_factor"] for f, w in w_fractions.items())
    # Penalty for too many components (>3 components adds spinning difficulty)
    num_components = len(w_fractions)
    comp_penalty = max(0, (num_components - 2) * 0.06)
    manuf_score = max(0.2, (synth_base - comp_penalty)) * 100.0
    manuf_score = float(np.clip(manuf_score, 20.0, 98.0))

    scores = {
        "Thermal Protection (HTP)": round(htp_score, 1),
        "Comfort & Breathability (THL)": round(thl_score, 1),
        "Tensile Strength": round(tensile_score, 1),
        "Flexibility": round(flex_score, 1),
        "Manufacturability": round(manuf_score, 1),
    }

    return {
        "blend_fractions": {f: round(w * 100, 1) for f, w in w_fractions.items()},
        "volume_fractions": {f: round(v * 100, 1) for f, v in v_fractions.items()},
        "scores": scores,
        "composite_density_g_cm3": round(composite_density, 3),
        "tensile_strength_gpa": round(effective_tensile_strength, 2),
        "tensile_modulus_gpa": round(composite_tensile_modulus, 1),
        "loi_pct": round(composite_loi, 1),
        "max_service_temp_c": round(max_service_temp, 0),
        "thermal_conductivity_w_mk": round(k_eff, 4),
        "thermal_resistance_rct": round(r_ct, 4),
        "evaporative_resistance_ret": round(r_et, 2),
        "total_heat_loss_thl_w_m2": round(thl_value, 1),
        "fabric_gsm": gsm,
        "weave_type": weave_type,
        "cost_usd_per_m2": round(cost_usd, 2),
        "cost_inr_per_m2": round(cost_inr, 1),
        "co2_kg_per_kg": round(co2_kg, 1),
        "water_l_per_kg": round(water_l, 0),
        "bio_based_pct": round(bio_based_pct, 1),
    }
