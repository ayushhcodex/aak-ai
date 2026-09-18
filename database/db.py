"""
AIMATRY Data Layer: Structured Materials & Monomer Database
Implements SQLite storage for:
- Curated Monomers (Diamines, Diacids, Heterocycles, Silanes) with SMILES and RDKit ECFP4 fingerprints
- High-Performance Fiber Test Records
- Historical Lab Trials & Formulations
"""

import os
import sqlite3
from typing import Dict, List, Any, Optional
import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "materials.db")


CURATED_MONOMERS = [
    {
        "name": "m-Phenylenediamine (MPD)",
        "smiles": "Nc1cccc(N)c1",
        "category": "Aromatic Diamine",
        "primary_use": "Meta-aramid (Nomex) synthesis",
        "supplier": "DuPont / Gujarat Alkalies",
        "cost_inr_kg": 420.0,
    },
    {
        "name": "p-Phenylenediamine (PPD)",
        "smiles": "Nc1ccc(N)cc1",
        "category": "Aromatic Diamine",
        "primary_use": "Para-aramid (Kevlar/Twaron) synthesis",
        "supplier": "Teijin / Aarti Industries",
        "cost_inr_kg": 560.0,
    },
    {
        "name": "Isophthaloyl Chloride (IPC)",
        "smiles": "ClC(=O)c1cccc(C(=O)Cl)c1",
        "category": "Diacid Chloride",
        "primary_use": "Nomex polycondensation",
        "supplier": "Lanxess / Deepak Nitrite",
        "cost_inr_kg": 680.0,
    },
    {
        "name": "Terephthaloyl Chloride (TPC)",
        "smiles": "ClC(=O)c1ccc(C(=O)Cl)cc1",
        "category": "Diacid Chloride",
        "primary_use": "Kevlar polycondensation",
        "supplier": "DuPont / Atul Ltd",
        "cost_inr_kg": 750.0,
    },
    {
        "name": "Pyromellitic Dianhydride (PMDA)",
        "smiles": "O=C1OC(=O)c2cc3c(=O)oc(=O)c3cc21",
        "category": "Dianhydride",
        "primary_use": "Kapton Polyimide synthesis",
        "supplier": "Mitsubishi Gas / Lonza",
        "cost_inr_kg": 1850.0,
    },
    {
        "name": "4,4'-Oxydianiline (ODA)",
        "smiles": "Nc1ccc(Oc2ccc(N)cc2)cc1",
        "category": "Aromatic Diamine",
        "primary_use": "Kapton Polyimide flexible backbone",
        "supplier": "Seika / Tokyo Chemical Industry",
        "cost_inr_kg": 2400.0,
    },
    {
        "name": "4,6-Diaminoresorcinol (DAR)",
        "smiles": "Nc1cc(N)c(O)cc1O",
        "category": "Heterocyclic Precursor",
        "primary_use": "PBO (Zylon) synthesis",
        "supplier": "Toyobo / Mitsui Chemicals",
        "cost_inr_kg": 6500.0,
    },
    {
        "name": "Tetraethyl Orthosilicate (TEOS)",
        "smiles": "CCO[Si](OCC)(OCC)OCC",
        "category": "Alkoxysilane",
        "primary_use": "Silica Aerogel Sol-Gel Precursor",
        "supplier": "Evonik / Wacker Chemie",
        "cost_inr_kg": 890.0,
    },
    {
        "name": "Acrylonitrile (AN)",
        "smiles": "N#CC=C",
        "category": "Vinyl Monomer",
        "primary_use": "PAN Carbon Fiber Precursor",
        "supplier": "Reliance Industries / Asahi Kasei",
        "cost_inr_kg": 160.0,
    },
    {
        "name": "Tetrafluoroethylene (TFE)",
        "smiles": "FC(F)=C(F)F",
        "category": "Fluoromonomer",
        "primary_use": "PTFE (Gore Membrane) Polymerization",
        "supplier": "Chemours / Gujarat Fluorochemicals",
        "cost_inr_kg": 1250.0,
    },
]


def init_database(db_path: str = DB_PATH):
    """Initializes SQLite database schemas and seeds default monomer records."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS monomers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        smiles TEXT NOT NULL,
        category TEXT,
        primary_use TEXT,
        supplier TEXT,
        mol_weight REAL,
        logp REAL,
        tpsa REAL,
        rotatable_bonds INTEGER,
        aromatic_rings INTEGER,
        cost_inr_kg REAL,
        fingerprint_ecfp4 TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lab_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blend_name TEXT NOT NULL,
        composition_json TEXT NOT NULL,
        gsm REAL,
        weave_type TEXT,
        measured_htp REAL,
        measured_thl REAL,
        measured_tensile_gpa REAL,
        measured_loi REAL,
        pass_status TEXT,
        date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Seed Monomer records if empty
    cur.execute("SELECT COUNT(*) FROM monomers")
    count = cur.fetchone()[0]
    if count == 0:
        for m in CURATED_MONOMERS:
            smi = m["smiles"]
            mol = Chem.MolFromSmiles(smi)
            if mol is not None:
                mw = round(float(Descriptors.MolWt(mol)), 2)
                logp = round(float(Descriptors.MolLogP(mol)), 2)
                tpsa = round(float(Descriptors.TPSA(mol)), 2)
                rot = int(Descriptors.NumRotatableBonds(mol))
                rings = int(rdMolDescriptors.CalcNumAromaticRings(mol))
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=512)
                fp_bits = fp.ToBitString()
            else:
                mw, logp, tpsa, rot, rings, fp_bits = 0, 0, 0, 0, 0, ""

            cur.execute("""
            INSERT OR IGNORE INTO monomers (
                name, smiles, category, primary_use, supplier,
                mol_weight, logp, tpsa, rotatable_bonds, aromatic_rings,
                cost_inr_kg, fingerprint_ecfp4
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                m["name"], smi, m["category"], m["primary_use"], m["supplier"],
                mw, logp, tpsa, rot, rings, m["cost_inr_kg"], fp_bits
            ))

    conn.commit()
    conn.close()


def query_monomers(db_path: str = DB_PATH) -> pd.DataFrame:
    """Retrieves all monomer records as a pandas DataFrame."""
    if not os.path.exists(db_path):
        init_database(db_path)
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT id, name, smiles, category, primary_use, supplier, mol_weight, logp, tpsa, aromatic_rings, cost_inr_kg FROM monomers", conn)
    conn.close()
    return df


init_database()
