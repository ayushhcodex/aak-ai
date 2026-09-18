"""
Unit Tests for AIMATRY Core Computational Engines
"""

import pytest
import pandas as pd
from data import SCENARIOS
from core.mcdm import topsis_rank_candidates
from core.physics import compute_blend_physics, FIBER_SPECS
from core.chemistry import compute_molecular_descriptors, render_mol_svg, parse_molecule
from core.compliance import audit_compliance
from core.techpack import generate_techpack_dict, generate_techpack_pdf
from core.optimizer import run_pareto_optimization


def test_topsis_ranking():
    weights = {
        "Thermal Protection (HTP)": 90.0,
        "Comfort & Breathability (THL)": 20.0,
        "Tensile Strength": 80.0,
        "Flexibility": 30.0,
        "Manufacturability": 40.0,
    }
    df, top_scenario = topsis_rank_candidates(SCENARIOS, weights)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == len(SCENARIOS)
    assert top_scenario in SCENARIOS
    assert "TOPSIS Score" in df.columns
    assert df.iloc[0]["Rank"] == 1


def test_physics_micromechanics():
    blend = {"Meta-aramid (Nomex)": 80.0, "Silica Aerogel Nanocomposite": 20.0}
    res = compute_blend_physics(blend, gsm=280.0, weave_type="Ripstop Grid")
    assert "scores" in res
    assert 0 <= res["scores"]["Thermal Protection (HTP)"] <= 100
    assert 0 <= res["scores"]["Comfort & Breathability (THL)"] <= 100
    assert res["tensile_strength_gpa"] > 0
    assert res["loi_pct"] >= 28.0
    assert res["composite_density_g_cm3"] > 0
    assert res["thermal_resistance_rct"] > 0


def test_chemistry_rdkit_and_sascore():
    smiles = "Nc1cccc(N)c1"  # m-phenylenediamine
    mol = parse_molecule(smiles)
    assert mol is not None

    desc = compute_molecular_descriptors(smiles)
    assert desc["valid"] is True
    assert desc["mol_weight"] > 100.0
    assert 1.0 <= desc["sascore"] <= 10.0
    assert 0 <= desc["manufacturability_score"] <= 100

    svg = render_mol_svg(smiles, width=200, height=120)
    assert "<svg" in svg


def test_compliance_auditor():
    blend = {"Meta-aramid (Nomex)": 80.0, "Silica Aerogel Nanocomposite": 20.0}
    physics_res = compute_blend_physics(blend, gsm=280.0)
    comp = audit_compliance(physics_res)
    assert "summary" in comp
    assert "standards" in comp
    assert comp["summary"]["total_standards"] >= 5
    assert comp["standards"][0]["code"] == "ISO 11612:2015"


def test_techpack_generation():
    blend = {"Meta-aramid (Nomex)": 80.0, "Silica Aerogel Nanocomposite": 20.0}
    physics_res = compute_blend_physics(blend, gsm=280.0)
    compliance_res = audit_compliance(physics_res)

    tp_dict = generate_techpack_dict("Extreme Cold Weather", "Meta-aramid / Aerogel", physics_res, compliance_res)
    assert "metadata" in tp_dict
    assert "bill_of_materials" in tp_dict
    assert len(tp_dict["bill_of_materials"]) == 2

    pdf_bytes = generate_techpack_pdf(tp_dict)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")


def test_nsga2_pareto_optimization():
    all_df, pareto_df = run_pareto_optimization(pop_size=20, n_gen=10, seed=42)
    assert isinstance(pareto_df, pd.DataFrame)
    assert not pareto_df.empty
    assert "Composite Performance Score" in pareto_df.columns
    assert "Manufacturability" in pareto_df.columns
    assert "Blend Formulation" in pareto_df.columns
