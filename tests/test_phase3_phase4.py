"""
Unit and Integration Tests for Phase 3 & Phase 4 Modules
- Lab Test Importer & Physical Calibration
- Gaussian Process Active Learning Acquisition
- Generative Monomer Chemical Discovery
"""

import os
import pytest
import numpy as np
from database.lab_importer import (
    import_lab_test_file,
    get_all_lab_records,
    compute_empirical_calibration,
    generate_sample_nitra_lab_csv,
)
from ml.active_learning import ActiveLearningRecommender
from ml.clm import GenerativeMonomerEngine

TEST_DB = 'database/test_p3p4.db'


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_lab_importer_csv_and_calibration():
    # 1. Generate sample CSV and import
    csv_bytes = generate_sample_nitra_lab_csv()
    result = import_lab_test_file(csv_bytes, 'sample_nitra.csv', db_path=TEST_DB)
    assert result['status'] == 'success'
    assert result['records_imported'] >= 8

    # 2. Query stored records
    df = get_all_lab_records(db_path=TEST_DB)
    assert len(df) >= 8
    assert 'measured_thl' in df.columns
    assert 'p_aramid' in df.columns

    # 3. Compute empirical calibration
    calib = compute_empirical_calibration(db_path=TEST_DB)
    assert calib['status'] == 'calibrated'
    assert 'kappa_thl' in calib['calibration_factors']
    assert calib['calibration_factors']['kappa_thl'] > 0.5


def test_active_learning_recommender():
    # Fit recommender from test database with seed data
    al = ActiveLearningRecommender(target_metric='measured_thl', maximize=True)
    count = al.fit_from_database(db_path=TEST_DB)
    assert count >= 3
    assert al.is_fitted

    # Test recommendations (EI)
    recs_ei = al.recommend_next_experiments(acquisition='Expected Improvement', top_k=3)
    assert len(recs_ei) == 3
    for r in recs_ei:
        assert 'p_aramid' in r
        assert 'gsm' in r
        assert 'predicted_mean' in r
        assert 'acquisition_score' in r
        assert r['ci_95_high'] >= r['ci_95_low']

    # Test recommendations (UCB)
    recs_ucb = al.recommend_next_experiments(acquisition='Upper Confidence Bound', top_k=3, beta=2.5)
    assert len(recs_ucb) == 3


def test_generative_monomer_engine():
    engine = GenerativeMonomerEngine(db_path=TEST_DB)
    candidates = engine.generate_candidate_monomers(
        target_category='Diamine (Polyamide/Polyimide)',
        max_candidates=3,
        target_max_sascore=4.5
    )
    assert len(candidates) >= 1
    c0 = candidates[0]
    assert 'smiles' in c0
    assert c0['mol_weight'] > 50.0
    assert c0['sascore'] <= 4.5
    assert c0['estimated_td_c'] > 300.0
    assert len(c0['svg_b64']) > 100
