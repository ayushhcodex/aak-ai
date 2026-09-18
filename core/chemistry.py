"""
AIMATRY Core: Cheminformatics & Molecular Property Engine
Integrates RDKit for:
- SMILES validation & canonicalization
- 2D SVG vector chemical structure rendering (dark-theme compatible)
- Molecular descriptor computation (MW, LogP, TPSA, HBD, HBA, RotBonds)
- Objective Synthetic Accessibility Scoring (SAScore: 1.0 to 10.0 scale)
"""

import os
import sys
from typing import Dict, Any, Optional, Tuple
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D

# Attempt to import RDKit's official SA_Score module
try:
    from rdkit.Chem import RDConfig
    sa_score_path = os.path.join(RDConfig.RDContribDir, "SA_Score")
    if sa_score_path not in sys.path:
        sys.path.append(sa_score_path)
    import sascorer
    HAS_SASCORER = True
except Exception:
    HAS_SASCORER = False


def clean_smiles(smiles_str: str) -> str:
    """Extracts a valid primary SMILES string from potential multi-component text."""
    if not smiles_str:
        return ""
    # Remove reactions, plus signs, brackets, annotations
    cleaned = smiles_str.strip()
    if "→" in cleaned:
        cleaned = cleaned.split("→")[-1].strip()
    if "+" in cleaned:
        # Take the first main reactant
        cleaned = cleaned.split("+")[0].strip()
    cleaned = cleaned.replace("[—", "").replace("—]", "").replace("ₙ", "")
    return cleaned.strip()


def parse_molecule(smiles: str) -> Optional[Chem.Mol]:
    """Parses a SMILES string into an RDKit Mol object with sanitization."""
    if not smiles:
        return None
    cleaned = clean_smiles(smiles)
    mol = Chem.MolFromSmiles(cleaned)
    if mol is None:
        # Try raw smiles
        mol = Chem.MolFromSmiles(smiles)
    return mol


def calculate_sascore(mol: Chem.Mol) -> float:
    """
    Computes Ertl & Schuffenhauer Synthetic Accessibility Score (1.0 = easy, 10.0 = hard).
    Falls back to topological complexity heuristic if SAScore model is unavailable.
    """
    if mol is None:
        return 5.0
    if HAS_SASCORER:
        try:
            return round(float(sascorer.calculateScore(mol)), 2)
        except Exception:
            pass

    # Heuristic fallback based on Bertz complexity, ring count, and molecular weight
    mw = Descriptors.MolWt(mol)
    rings = rdMolDescriptors.CalcNumRings(mol)
    rot_bonds = Descriptors.NumRotatableBonds(mol)
    chiral_centers = len(Chem.FindMolChiralCenters(mol, includeUnassigned=True))

    score = 1.0 + (mw / 300.0) + (rings * 0.4) + (rot_bonds * 0.15) + (chiral_centers * 0.8)
    return round(float(min(max(score, 1.0), 10.0)), 2)


def compute_molecular_descriptors(smiles: str) -> Dict[str, Any]:
    """
    Computes comprehensive cheminformatics descriptors for a given SMILES string.
    """
    mol = parse_molecule(smiles)
    if mol is None:
        return {
            "valid": False,
            "smiles": smiles,
            "error": "Invalid SMILES string structure",
            "mol_weight": 0.0,
            "logp": 0.0,
            "tpsa": 0.0,
            "hbd": 0,
            "hba": 0,
            "rotatable_bonds": 0,
            "aromatic_rings": 0,
            "sascore": 5.0,
            "manufacturability_score": 50.0,
        }

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    tpsa = Descriptors.TPSA(mol)
    hbd = Descriptors.NumHDonors(mol)
    hba = Descriptors.NumHAcceptors(mol)
    rot_bonds = Descriptors.NumRotatableBonds(mol)
    aromatic_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
    sascore = calculate_sascore(mol)

    # Convert SAScore (1 = easiest, 10 = hardest) to 0-100 Manufacturability rating
    # 1.0 -> 98%, 5.0 -> 60%, 10.0 -> 15%
    manuf_rating = round(max(10.0, 100.0 - (sascore - 1.0) * 9.5), 1)

    return {
        "valid": True,
        "smiles": Chem.MolToSmiles(mol),
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "mol_weight": round(float(mw), 2),
        "logp": round(float(logp), 2),
        "tpsa": round(float(tpsa), 2),
        "hbd": int(hbd),
        "hba": int(hba),
        "rotatable_bonds": int(rot_bonds),
        "aromatic_rings": int(aromatic_rings),
        "sascore": sascore,
        "manufacturability_score": manuf_rating,
    }


def render_mol_svg(
    smiles: str,
    width: int = 280,
    height: int = 180,
    dark_mode: bool = True,
) -> str:
    """
    Renders an RDKit Mol object into a clean 2D vector SVG graphic.
    """
    mol = parse_molecule(smiles)
    if mol is None:
        return f'<svg width="{width}" height="{height}"><text x="10" y="30" fill="#94a3b8" font-family="Inter" font-size="12">Structure unavailable</text></svg>'

    try:
        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        opts = drawer.drawOptions()
        opts.clearBackground = False  # Transparent background
        if dark_mode:
            opts.bondLineWidth = 2
            opts.highlightBondWidthMultiplier = 16
        rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        # Clean SVG header for inline HTML embedding
        if "<?xml" in svg:
            svg = svg[svg.find("<svg"):]
        return svg
    except Exception as e:
        return f'<svg width="{width}" height="{height}"><text x="10" y="30" fill="#fbbf24" font-family="Inter" font-size="12">Render error: {e}</text></svg>'
