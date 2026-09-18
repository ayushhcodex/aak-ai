"""
Unit Tests for Phase 2: Materials Database, ML Surrogates & Inverse Material Design
"""

import pytest
import pandas as pd
from database.db import query_monomers, init_database
from ml.surrogate import TextileMLSurrogate, get_surrogate_model
from core.inverse_design import inverse_solve_formulation


def test_database_monomers():
    init_database()
    df = query_monomers()
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 10
    assert "smiles" in df.columns
    assert "mol_weight" in df.columns
    assert "p-Phenylenediamine (PPD)" in df["name"].values


def test_ml_surrogate_predictions_and_uncertainty():
    surrogate = get_surrogate_model()
    blend = {"Meta-aramid (Nomex)": 80.0, "Silica Aerogel Nanocomposite": 20.0}
    preds = surrogate.predict_with_uncertainty(blend, gsm=280.0, weave_type="Ripstop Grid")

    assert "Tensile_Strength_GPa" in preds
    assert "LOI_pct" in preds
    assert "Rct_m2K_W" in preds
    assert "THL_W_m2" in preds

    # Check uncertainty bounds
    for prop, val in preds.items():
        assert val["mean"] >= 0
        assert val["std_uncertainty"] >= 0
        assert val["ci_95_lower"] <= val["mean"] <= val["ci_95_upper"]

    importances = surrogate.get_feature_importances()
    assert isinstance(importances, pd.DataFrame)
    assert "Feature" in importances.columns


def test_inverse_material_design():
    targets = {
        "min_htp": 80.0,
        "min_thl": 65.0,
        "min_tensile": 60.0,
        "min_loi": 28.0,
        "min_bio_pct": 0.0,
    }
    result = inverse_solve_formulation(targets, max_budget_inr=5000.0)

    assert "discovered_blend" in result
    assert len(result["discovered_blend"]) >= 1
    assert "recommended_gsm" in result
    assert "physics" in result
    assert "target_comparison" in result
    assert result["recommended_gsm"] >= 160.0
