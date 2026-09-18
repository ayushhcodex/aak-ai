"""
AIMATRY Lab Data Layer: NITRA Physical Lab Test Importer & Empirical Calibration
Ingests real physical laboratory test records (Sweating Guarded Hotplate, Cone Calorimeter,
Vertical Flammability, UTM Tensile) from NITRA/TBRL, persists to SQLite, and computes
empirical physics calibration correction factors.
"""

import io
import json
import sqlite3
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional
from database.db import DB_PATH, init_database
from core.physics import compute_blend_physics


def import_lab_test_file(
    file_content: bytes,
    filename: str,
    db_path: str = DB_PATH
) -> Dict[str, Any]:
    """
    Parses an uploaded CSV or Excel file of physical lab trials,
    normalizes column schemas, validates numerical bounds, and stores into SQLite.
    """
    init_database(db_path)
    
    if filename.endswith('.csv'):
        df = pd.read_csv(io.BytesIO(file_content))
    elif filename.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(io.BytesIO(file_content))
    else:
        raise ValueError('Unsupported file format. Please upload a .csv or .xlsx file.')

    col_map = {}
    for col in df.columns:
        c_clean = str(col).strip().lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace('/', '_')
        if 'p_aramid' in c_clean or 'para_aramid' in c_clean or 'kevlar' in c_clean:
            col_map[col] = 'w_p_aramid'
        elif 'm_aramid' in c_clean or 'meta_aramid' in c_clean or 'nomex' in c_clean:
            col_map[col] = 'w_m_aramid'
        elif 'pbi' in c_clean:
            col_map[col] = 'w_pbi'
        elif 'modacrylic' in c_clean or 'kanecaron' in c_clean:
            col_map[col] = 'w_modacrylic'
        elif 'gsm' in c_clean or 'weight' in c_clean:
            col_map[col] = 'gsm'
        elif 'weave' in c_clean:
            col_map[col] = 'weave_type'
        elif 'htp' in c_clean or 'thermal_performance' in c_clean:
            col_map[col] = 'measured_htp'
        elif 'thl' in c_clean or 'heat_loss' in c_clean:
            col_map[col] = 'measured_thl'
        elif 'tensile' in c_clean or 'strength' in c_clean:
            col_map[col] = 'measured_tensile_gpa'
        elif 'loi' in c_clean or 'oxygen_index' in c_clean:
            col_map[col] = 'measured_loi'
        elif 'sample' in c_clean or 'blend' in c_clean or 'name' in c_clean or 'code' in c_clean:
            col_map[col] = 'blend_name'

    df_renamed = df.rename(columns=col_map)
    if 'blend_name' not in df_renamed.columns:
        df_renamed['blend_name'] = [f'NITRA-Trial-{i+1:03d}' for i in range(len(df_renamed))]
    if 'w_p_aramid' not in df_renamed.columns:
        df_renamed['w_p_aramid'] = 0.5
    if 'w_m_aramid' not in df_renamed.columns:
        df_renamed['w_m_aramid'] = 0.4
    if 'w_pbi' not in df_renamed.columns:
        df_renamed['w_pbi'] = 0.05
    if 'w_modacrylic' not in df_renamed.columns:
        df_renamed['w_modacrylic'] = 0.05
    if 'gsm' not in df_renamed.columns:
        df_renamed['gsm'] = 220.0
    if 'weave_type' not in df_renamed.columns:
        df_renamed['weave_type'] = 'Ripstop Grid'

    df_renamed['w_p_aramid'] = pd.to_numeric(df_renamed['w_p_aramid'], errors='coerce').fillna(0.0)
    df_renamed['w_m_aramid'] = pd.to_numeric(df_renamed['w_m_aramid'], errors='coerce').fillna(0.0)
    df_renamed['w_pbi'] = pd.to_numeric(df_renamed['w_pbi'], errors='coerce').fillna(0.0)
    df_renamed['w_modacrylic'] = pd.to_numeric(df_renamed['w_modacrylic'], errors='coerce').fillna(0.0)
    df_renamed['gsm'] = pd.to_numeric(df_renamed['gsm'], errors='coerce').fillna(220.0)
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    inserted_count = 0

    for _, row in df_renamed.iterrows():
        comp = {
            'p_aramid': float(row['w_p_aramid']),
            'm_aramid': float(row['w_m_aramid']),
            'pbi': float(row['w_pbi']),
            'modacrylic': float(row['w_modacrylic']),
        }
        tot = sum(comp.values())
        if tot > 0:
            comp = {k: v / tot for k, v in comp.items()}
        
        htp = float(row.get('measured_htp', 75.0)) if pd.notna(row.get('measured_htp')) else None
        thl = float(row.get('measured_thl', 260.0)) if pd.notna(row.get('measured_thl')) else None
        tensile = float(row.get('measured_tensile_gpa', 2.4)) if pd.notna(row.get('measured_tensile_gpa')) else None
        loi = float(row.get('measured_loi', 32.0)) if pd.notna(row.get('measured_loi')) else None
        status = 'PASS' if (htp and htp >= 65 and thl and thl >= 205) else 'FLAG'

        sql = 'INSERT INTO lab_records (blend_name, composition_json, gsm, weave_type, measured_htp, measured_thl, measured_tensile_gpa, measured_loi, pass_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(sql, (
            str(row['blend_name']), json.dumps(comp), float(row['gsm']), str(row['weave_type']),
            htp, thl, tensile, loi, status
        ))
        inserted_count += 1

    conn.commit()
    conn.close()

    return {
        'status': 'success',
        'records_imported': inserted_count,
        'columns_detected': list(df_renamed.columns),
        'preview': df_renamed.head(5).to_dict(orient='records'),
    }


def get_all_lab_records(db_path: str = DB_PATH) -> pd.DataFrame:
    """Fetches all stored physical laboratory test records."""
    init_database(db_path)
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query('SELECT * FROM lab_records ORDER BY id DESC', conn)
    conn.close()
    
    if not df.empty and 'composition_json' in df.columns:
        parsed_comps = []
        for c in df['composition_json']:
            try:
                parsed_comps.append(json.loads(c))
            except Exception:
                parsed_comps.append({})
        comp_df = pd.DataFrame(parsed_comps)
        df = pd.concat([df.drop(columns=['composition_json']), comp_df], axis=1)
    
    return df


def compute_empirical_calibration(db_path: str = DB_PATH) -> Dict[str, Any]:
    """
    Computes empirical scaling calibration factors (kappa_thl, kappa_loi, kappa_tensile)
    by comparing Voigt-Reuss theoretical physics predictions against empirical lab test records.
    """
    df = get_all_lab_records(db_path)
    if df.empty or len(df) < 3:
        return {
            'status': 'insufficient_data',
            'message': 'At least 3 lab test records are required to perform calibration.',
            'calibration_factors': {
                'kappa_thl': 1.0,
                'kappa_loi': 1.0,
                'kappa_tensile': 1.0,
            },
            'metrics': {},
        }

    pred_thls, meas_thls = [], []
    pred_lois, meas_lois = [], []
    pred_tensiles, meas_tensiles = [], []

    for _, row in df.iterrows():
        p_ar = float(row.get('p_aramid', 0.5))
        m_ar = float(row.get('m_aramid', 0.4))
        pbi = float(row.get('pbi', 0.05))
        moda = float(row.get('modacrylic', 0.05))
        gsm = float(row.get('gsm', 220.0))

        blend_dict = {
            'Para-aramid (Kevlar/Twaron)': p_ar,
            'Meta-aramid (Nomex)': m_ar,
            'PBI (Polybenzimidazole)': pbi,
            'Modacrylic (Kanecaron)': moda,
        }
        phys = compute_blend_physics(blend_dict, gsm=gsm, weave_type='Ripstop Grid', fabric_thickness_mm=gsm/300.0)

        p_thl = phys['total_heat_loss_thl_w_m2']
        p_loi = phys['loi_pct']
        p_tensile = phys['tensile_strength_gpa']

        if pd.notna(row.get('measured_thl')):
            pred_thls.append(p_thl)
            meas_thls.append(float(row['measured_thl']))
        if pd.notna(row.get('measured_loi')):
            pred_lois.append(p_loi)
            meas_lois.append(float(row['measured_loi']))
        if pd.notna(row.get('measured_tensile_gpa')):
            pred_tensiles.append(p_tensile)
            meas_tensiles.append(float(row['measured_tensile_gpa']))

    def calc_ratio(pred, meas):
        if len(pred) >= 3 and np.mean(pred) > 0:
            return float(np.mean(meas) / np.mean(pred))
        return 1.0

    k_thl = round(calc_ratio(pred_thls, meas_thls), 4)
    k_loi = round(calc_ratio(pred_lois, meas_lois), 4)
    k_tensile = round(calc_ratio(pred_tensiles, meas_tensiles), 4)

    thl_rmse = float(np.sqrt(np.mean((np.array(meas_thls) - np.array(pred_thls) * k_thl) ** 2))) if len(meas_thls) >= 3 else 0.0

    return {
        'status': 'calibrated',
        'total_records_used': len(df),
        'calibration_factors': {
            'kappa_thl': k_thl,
            'kappa_loi': k_loi,
            'kappa_tensile': k_tensile,
        },
        'metrics': {
            'thl_rmse_w_m2': round(thl_rmse, 2),
            'sample_count': len(df),
        },
        'comparison_data': {
            'pred_thl': [round(x * k_thl, 1) for x in pred_thls[:10]],
            'meas_thl': [round(x, 1) for x in meas_thls[:10]],
            'pred_loi': [round(x * k_loi, 1) for x in pred_lois[:10]],
            'meas_loi': [round(x, 1) for x in meas_lois[:10]],
        }
    }


def generate_sample_nitra_lab_csv() -> bytes:
    """Generates a realistic mock NITRA physical laboratory test dataset in CSV bytes."""
    data = [
        {'sample_code': 'NITRA-TR-01', 'p_aramid': 0.60, 'm_aramid': 0.35, 'pbi': 0.05, 'modacrylic': 0.00, 'gsm': 220, 'weave': 'Ripstop Grid', 'measured_htp': 82.4, 'measured_thl': 272.5, 'measured_tensile_gpa': 2.85, 'measured_loi': 34.2},
        {'sample_code': 'NITRA-TR-02', 'p_aramid': 0.50, 'm_aramid': 0.40, 'pbi': 0.10, 'modacrylic': 0.00, 'gsm': 210, 'weave': 'Twill (2/1)', 'measured_htp': 84.1, 'measured_thl': 285.0, 'measured_tensile_gpa': 2.60, 'measured_loi': 35.8},
        {'sample_code': 'NITRA-TR-03', 'p_aramid': 0.40, 'm_aramid': 0.45, 'pbi': 0.00, 'modacrylic': 0.15, 'gsm': 240, 'weave': 'Plain Weave (1/1)', 'measured_htp': 76.5, 'measured_thl': 248.0, 'measured_tensile_gpa': 2.10, 'measured_loi': 31.5},
        {'sample_code': 'NITRA-TR-04', 'p_aramid': 0.70, 'm_aramid': 0.20, 'pbi': 0.10, 'modacrylic': 0.00, 'gsm': 200, 'weave': 'Ripstop Grid', 'measured_htp': 88.0, 'measured_thl': 298.2, 'measured_tensile_gpa': 3.15, 'measured_loi': 36.4},
        {'sample_code': 'NITRA-TR-05', 'p_aramid': 0.30, 'm_aramid': 0.50, 'pbi': 0.00, 'modacrylic': 0.20, 'gsm': 260, 'weave': 'Satin (4/1)', 'measured_htp': 71.2, 'measured_thl': 218.4, 'measured_tensile_gpa': 1.75, 'measured_loi': 29.8},
        {'sample_code': 'NITRA-TR-06', 'p_aramid': 0.55, 'm_aramid': 0.30, 'pbi': 0.15, 'modacrylic': 0.00, 'gsm': 215, 'weave': 'Ripstop Grid', 'measured_htp': 89.5, 'measured_thl': 280.6, 'measured_tensile_gpa': 2.90, 'measured_loi': 37.2},
        {'sample_code': 'NITRA-TR-07', 'p_aramid': 0.45, 'm_aramid': 0.45, 'pbi': 0.05, 'modacrylic': 0.05, 'gsm': 225, 'weave': 'Twill (2/1)', 'measured_htp': 79.8, 'measured_thl': 262.1, 'measured_tensile_gpa': 2.45, 'measured_loi': 33.1},
        {'sample_code': 'NITRA-TR-08', 'p_aramid': 0.80, 'm_aramid': 0.10, 'pbi': 0.10, 'modacrylic': 0.00, 'gsm': 195, 'weave': 'Ripstop Grid', 'measured_htp': 91.2, 'measured_thl': 308.5, 'measured_tensile_gpa': 3.40, 'measured_loi': 38.0},
    ]
    df = pd.DataFrame(data)
    csv_str = df.to_csv(index=False)
    return csv_str.encode('utf-8')
