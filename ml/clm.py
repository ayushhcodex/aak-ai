"""
AIMATRY Generative Chemistry: Conditional Monomer & Polymer Discovery Engine
Implements generative chemical grammar for next-generation flame-retardant,
high-temperature polymer repeat units and monomers with RDKit filtering.
"""

import random
from typing import Dict, List, Any, Optional, Tuple
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem, DataStructs
from core.chemistry import calculate_sascore, render_mol_svg
from database.db import query_monomers, DB_PATH, init_database


# Core chemical scaffolds for high-performance polymers
AROMATIC_CORES = [
    ('1,4-Phenylene Core', 'c1cc([R1])ccc1[R2]'),
    ('1,3-Phenylene Core', 'c1cc([R1])cc([R2])c1'),
    ("4,4'-Biphenylene Core", 'c1cc([R1])ccc1-c2ccc([R2])cc2'),
    ("4,4'-Oxydiphenylene Core", 'c1cc([R1])ccc1Oc2ccc([R2])cc2'),
    ("4,4'-Sulfonyldiphenylene Core", 'c1cc([R1])ccc1S(=O)(=O)c2ccc([R2])cc2'),
    ('2,6-Naphthylene Core', 'c1cc2cc([R1])ccc2cc1[R2]'),
    ('Benzoxazole Core', 'c1cc2nc([R1])oc2cc1[R2]'),
    ('Benzimidazole Core', 'c1cc2nc([R1])[nH]c2cc1[R2]'),
    ('Phosphine Oxide Core', 'c1cc([R1])ccc1P(=O)(c2ccccc2)c3ccc([R2])cc3'),
]

FUNCTIONAL_HEADS = {
    'Diamine (Polyamide/Polyimide)': ('N', 'N'),
    'Diacyl Chloride (Aramid)': ('C(=O)Cl', 'C(=O)Cl'),
    'Dicarboxylic Acid': ('C(=O)O', 'C(=O)O'),
    'Bisphenol (Polyarylate)': ('O', 'O'),
    'Dicyanate / Cyanate Ester': ('OC#N', 'OC#N'),
}

FLAME_RETARDANT_SIDE_CHAINS = [
    ('', 'Standard Polymer Backbone'),
    ('P(=O)(OCC)OCC', 'Diethyl Phosphonate (Char Promoter)'),
    ('C(F)(F)F', 'Trifluoromethyl (Hydrophobic/Thermal)'),
    ('S(=O)(=O)N', 'Sulfonamide (Synergistic FR)'),
    ('C#N', 'Nitrile (High Crosslinking)'),
]


class GenerativeMonomerEngine:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        init_database(db_path)
        self.benchmark_df = query_monomers(db_path)
        self.benchmark_fps = self._load_benchmark_fps()

    def _load_benchmark_fps(self) -> List[Tuple[str, Any]]:
        fps = []
        for _, row in self.benchmark_df.iterrows():
            mol = Chem.MolFromSmiles(row['smiles'])
            if mol is not None:
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=512)
                fps.append((row['name'], fp))
        return fps

    def generate_candidate_monomers(
        self,
        target_category: str = 'Diamine (Polyamide/Polyimide)',
        include_fr_sidechains: bool = True,
        max_candidates: int = 6,
        target_max_sascore: float = 4.5,
    ) -> List[Dict[str, Any]]:
        """
        Generates novel monomer structures, validates valency and SAScore,
        and computes estimated decomposition temperature (Td) and LOI boost.
        """
        r1_term, r2_term = FUNCTIONAL_HEADS.get(target_category, ('N', 'N'))
        results = []
        seen_smiles = set()

        # Seed known monomers first to avoid duplicates
        for _, row in self.benchmark_df.iterrows():
            seen_smiles.add(Chem.CanonSmiles(row['smiles']))

        attempts = 0
        while len(results) < max_candidates and attempts < 100:
            attempts += 1
            core_name, core_template = random.choice(AROMATIC_CORES)
            
            # Optionally attach flame-retardant side chain
            if include_fr_sidechains and random.random() > 0.4:
                fr_group, fr_desc = random.choice(FLAME_RETARDANT_SIDE_CHAINS[1:])
            else:
                fr_group, fr_desc = ('', 'Unsubstituted Backbone')

            # Assemble SMILES template
            smi = core_template.replace('[R1]', r1_term).replace('[R2]', r2_term)
            
            # Simple substitution logic if sidechain present
            if fr_group:
                smi = smi.replace('c1cc', f'c1c({fr_group})c', 1)

            try:
                mol = Chem.MolFromSmiles(smi)
                if mol is None:
                    continue
                Chem.SanitizeMol(mol)
                canon_smi = Chem.CanonSmiles(Chem.MolToSmiles(mol))
                
                if canon_smi in seen_smiles:
                    continue
                seen_smiles.add(canon_smi)

                mw = round(float(Descriptors.MolWt(mol)), 2)
                logp = round(float(Descriptors.MolLogP(mol)), 2)
                tpsa = round(float(Descriptors.TPSA(mol)), 2)
                rot_bonds = int(Descriptors.NumRotatableBonds(mol))
                aromatic_rings = int(rdMolDescriptors.CalcNumAromaticRings(mol))
                sascore = calculate_sascore(mol)

                if sascore > target_max_sascore or mw > 650.0:
                    continue

                # Estimate thermal decomposition temperature Td (approximate group contribution)
                heteroatoms = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() in ['N', 'O', 'S', 'P', 'F'])
                est_td_c = round(320.0 + (42.0 * aromatic_rings) + (18.0 * heteroatoms) - (14.0 * rot_bonds), 1)
                est_td_c = max(350.0, min(580.0, est_td_c))

                # Estimate LOI contribution potential
                has_p = any(atom.GetSymbol() == 'P' for atom in mol.GetAtoms())
                has_f = any(atom.GetSymbol() == 'F' for atom in mol.GetAtoms())
                est_loi_boost = round(28.0 + (2.5 * aromatic_rings) + (6.0 if has_p else 0.0) + (3.0 if has_f else 0.0), 1)

                # Compute maximum similarity to commercial database
                cand_fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=512)
                max_sim, closest_benchmark = 0.0, 'None'
                for b_name, b_fp in self.benchmark_fps:
                    sim = DataStructs.TanimotoSimilarity(cand_fp, b_fp)
                    if sim > max_sim:
                        max_sim = sim
                        closest_benchmark = b_name

                svg_b64 = render_mol_svg(canon_smi, width=320, height=200)

                results.append({
                    'candidate_id': f'GEN-POLY-{len(results)+1:02d}',
                    'smiles': canon_smi,
                    'core_scaffold': core_name,
                    'sidechain_feature': fr_desc,
                    'category': target_category,
                    'mol_weight': mw,
                    'logp': logp,
                    'tpsa': tpsa,
                    'aromatic_rings': aromatic_rings,
                    'sascore': sascore,
                    'estimated_td_c': est_td_c,
                    'estimated_loi_potential': est_loi_boost,
                    'tanimoto_similarity': round(max_sim, 3),
                    'closest_commercial_analog': closest_benchmark,
                    'svg_b64': svg_b64,
                })

            except Exception:
                continue

        return results
