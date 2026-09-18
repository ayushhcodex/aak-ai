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
from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem
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


def generate_3d_molblock(smiles: str) -> Optional[str]:
    """
    Generates an energy-minimized 3D conformation for a SMILES string using RDKit's ETKDGv3
    and MMFF94 force field optimization. Returns a MolBlock string.
    """
    mol = parse_molecule(smiles)
    if mol is None:
        return None
    try:
        mol_h = Chem.AddHs(mol)
        params = AllChem.ETKDGv3()
        params.randomSeed = 42
        embed_status = AllChem.EmbedMolecule(mol_h, params)
        if embed_status != 0:
            AllChem.EmbedMolecule(mol_h, useRandomCoords=True)
        try:
            AllChem.MMFFOptimizeMolecule(mol_h, maxIters=300)
        except Exception:
            try:
                AllChem.UFFOptimizeMolecule(mol_h, maxIters=300)
            except Exception:
                pass
        return Chem.MolToMolBlock(mol_h)
    except Exception:
        try:
            AllChem.Compute2DCoords(mol)
            return Chem.MolToMolBlock(mol)
        except Exception:
            return None


def render_3dmol_html(
    smiles: str,
    height: int = 340,
    style: str = "stick",
    show_surface: bool = False,
    bg_color: str = "#0b0f19",
    spin: bool = True,
) -> str:
    """
    Renders an interactive, WebGL-accelerated 3D molecular viewer using 3Dmol.js.
    Supports real-time mouse rotation, zooming, surface rendering, and multiple atom styles.
    """
    molblock = generate_3d_molblock(smiles)
    if not molblock:
        return f'<div style="color:#94a3b8; padding:20px; text-align:center; background:#0b0f19; border-radius:6px;">3D conformation unavailable for: <code>{smiles}</code></div>'

    escaped_molblock = molblock.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

    surface_js = ""
    if show_surface:
        surface_js = "viewer.addSurface($3Dmol.SurfaceType.VDW, {opacity: 0.35, color: '#38bdf8'});"

    if style == "sphere" or style == "spacefill":
        style_js = "viewer.setStyle({}, {sphere: {scale: 0.35}, stick: {radius: 0.14}});"
    elif style == "line":
        style_js = "viewer.setStyle({}, {line: {lineWidth: 2}});"
    else:  # stick / default
        style_js = "viewer.setStyle({}, {stick: {radius: 0.18, colorscheme: 'Jmol'}});"

    spin_js = "viewer.spin(true);" if spin else ""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js"></script>
        <style>
            * {{ box-sizing: border-box; }}
            body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: {bg_color}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
            #viewer_3d {{ width: 100%; height: {height}px; position: relative; border-radius: 8px; border: 1px solid #1e293b; }}
            .toolbar {{ position: absolute; bottom: 8px; right: 8px; z-index: 100; display: flex; gap: 4px; background: rgba(15, 23, 42, 0.85); padding: 4px 6px; border-radius: 6px; border: 1px solid #334155; }}
            .btn-tool {{ background: #1e293b; color: #cbd5e1; border: 1px solid #475569; border-radius: 4px; padding: 3px 8px; font-size: 11px; cursor: pointer; transition: all 0.15s; }}
            .btn-tool:hover {{ background: #2563eb; color: #ffffff; border-color: #3b82f6; }}
            .badge-3d {{ position: absolute; top: 8px; left: 8px; z-index: 100; background: rgba(15, 23, 42, 0.85); color: #38bdf8; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 4px; border: 1px solid #334155; }}
        </style>
    </head>
    <body>
        <div id="viewer_3d">
            <span class="badge-3d">WebGL · 3Dmol.js</span>
            <div class="toolbar">
                <button class="btn-tool" onclick="resetCam()">⟲ Reset</button>
                <button class="btn-tool" onclick="toggleSpin()">🔄 Spin</button>
                <button class="btn-tool" onclick="toggleStyle()">🎨 Style</button>
            </div>
        </div>
        <script>
            let viewer = null;
            let currentStyleIdx = 0;
            let isSpinning = {str(spin).lower()};

            document.addEventListener("DOMContentLoaded", function() {{
                let element = document.getElementById("viewer_3d");
                let config = {{ backgroundColor: "{bg_color}" }};
                viewer = $3Dmol.createViewer(element, config);
                let molData = `{escaped_molblock}`;
                viewer.addModel(molData, "mol");
                {style_js}
                {surface_js}
                viewer.zoomTo();
                viewer.render();
                {spin_js}
            }});

            function resetCam() {{
                if (viewer) {{
                    viewer.zoomTo();
                    viewer.render();
                }}
            }}

            function toggleSpin() {{
                if (viewer) {{
                    isSpinning = !isSpinning;
                    viewer.spin(isSpinning);
                }}
            }}

            function toggleStyle() {{
                if (!viewer) return;
                currentStyleIdx = (currentStyleIdx + 1) % 3;
                if (currentStyleIdx === 0) {{
                    viewer.setStyle({{}}, {{stick: {{radius: 0.18, colorscheme: 'Jmol'}}}});
                }} else if (currentStyleIdx === 1) {{
                    viewer.setStyle({{}}, {{sphere: {{scale: 0.35}}, stick: {{radius: 0.14}}}});
                }} else {{
                    viewer.setStyle({{}}, {{sphere: {{}}, stick: {{radius: 0.05}}}});
                }}
                viewer.render();
            }}
        </script>
    </body>
    </html>
    """
    return html

