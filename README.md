---
title: AIMATRY Materials Informatics & Polymer Designer
emoji: 🧬
colorFrom: cyan
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🔬 AIMATRY (AAK.AI): Materials Informatics & Generative Polymer Designer

> **Version**: `v3.1 (Scientific Computing & Materials Informatics Engine)`  
> **Institution**: Department of Computer Science & Engineering (CSE), NITRA Technical Campus, Ghaziabad, UP, India  
> **Authors**: Ayush Singh, Vansh Mishra, Nikhil Kumar Yadav  
> **Domain**: Protective Technical Textiles, High-Performance Polymers & Defense Materials  

---

## 🚀 Overview

**AIMATRY** is an advanced Materials Informatics platform designed to accelerate the formulation, evaluation, and industrial specification of high-performance protective textiles.

Bridging **Computer Science & Optimization** with **Textile Science & Polymer Chemistry**, AIMATRY transitions beyond static prototypes into a deterministic, physics-grounded, and multi-objective decision-support platform.

---

## ⚡ Key Scientific & Computational Features

1. **Algorithmic Multi-Criteria Decision Making (TOPSIS Engine)** (`core/mcdm.py`):
   - Dynamically evaluates and ranks all material formulations based on user-weighted priorities (HTP, THL, Tensile Strength, Flexibility, Manufacturability).
   - Computes geometric Euclidean distances to the Positive-Ideal ($A^*$) and Negative-Ideal ($A^-$) solutions in real-time.

2. **Physics-Based Voigt-Reuss Micromechanics & Transport Calculator** (`core/physics.py`):
   - Computes composite density ($\rho$), tensile breaking strength ($\sigma$), elastic modulus ($E$), and Limiting Oxygen Index ($\text{LOI}$) using analytical micromechanical mixture rules.
   - Models thermal resistance ($R_{ct}$), evaporative resistance ($R_{et}$), and Total Heat Loss ($\text{THL}$) based on sweating guarded hotplate physics (EN ISO 11092 / ASTM F1868).

3. **RDKit Cheminformatics & SAScore Engine** (`core/chemistry.py`):
   - Dynamically parses and renders 2D vector SVG chemical structures for monomers and polymer repeating units.
   - Computes objective **Ertl & Schuffenhauer Synthetic Accessibility Scores (SAScore)** (1.0 to 10.0 scale) and molecular descriptors (Exact MW, LogP, TPSA, Rotatable Bonds, Aromatic Rings).

4. **Automated Regulatory Compliance Auditor** (`core/compliance.py`):
   - Instant pre-compliance evaluation against mandatory Indian and international testing standards:
     - **ISO 11612:2015**: Protective clothing against heat and flame ($\text{HTI}_{24}$ levels B1–B3).
     - **NFPA 1971**: Structural & proximity firefighting turnout gear ($\text{TPP} \ge 35\text{ cal/cm}^2$, $\text{THL} \ge 205\text{ W/m}^2$).
     - **ASTM F1959 / NFPA 70E**: Arc Thermal Performance Value ($\text{ATPV}$) Category 1–4 ratings.
     - **BIS IS 15742:2007**: Indian standard for thermal protective garments.
     - **BIS IS 14324 / NIJ 0101.06**: Ballistic body armor threat levels.
     - **EN ISO 11092**: Physiological breathability classifications (Class 1–4).

5. **Industrial Manufacturing Tech-Pack & BOM Generator** (`core/techpack.py`):
   - Generates production-ready Technical Specification Packs exportable directly as **publication-quality PDF documents** (via ReportLab) or **JSON payloads**.
   - Includes Bill of Materials (BOM), recommended yarn counts (Ne/Denier), weave architecture, finishing treatments, and estimated pricing in INR/USD.

6. **True NSGA-II Multi-Objective Pareto Frontier Solver** (`core/optimizer.py`):
   - Implements the **pymoo NSGA-II genetic algorithm** to dynamically resolve conflicting multi-variable objectives (Thermal Protection vs. Comfort Breathability vs. Synthetic Accessibility).

7. **Dynamic LCA & ESG Footprint Engine**:
   - Calculates cradle-to-gate carbon footprint ($\text{kg CO}_2\text{/kg fabric}$) and water usage ($\text{L/kg fabric}$) derived from Higg MSI and Ecoinvent lifecycle factors.

---

## 📂 Project Architecture

```
.
├── app.py                          # Streamlit UI with Cyber-Industrial Dark Theme & Tabs
├── data.py                         # Curated Scenarios, Benchmarks, and Standards Store
├── requirements.txt                # Dependencies (Streamlit, Plotly, RDKit, pymoo, ReportLab)
├── core/
│   ├── mcdm.py                     # TOPSIS Multi-Criteria Decision Making Algorithm
│   ├── physics.py                  # Voigt-Reuss Micromechanics & Thermal Transport Model
│   ├── chemistry.py                # RDKit SMILES Parser, SAScore & 2D SVG Generator
│   ├── compliance.py               # Automated ISO/BIS/NFPA/ASTM Standards Auditor
│   ├── techpack.py                 # Industrial Tech-Pack PDF & JSON Spec Generator
│   └── optimizer.py                # NSGA-II Multi-Objective Pareto Optimization (pymoo)
├── tests/
│   └── test_engines.py             # Pytest automated test suite for all core engines
├── CONTRIBUTOR_AND_TERMINOLOGY_GUIDE.md # Interdisciplinary Textile & AI Guide
├── PROJECT_GROUND_REALITY_REPORT.md    # Technical Forensic Audit Report
├── DATA_SOURCES.md                 # Scientific Bibliography & Data Traceability
├── SYSTEM_ARCHITECTURE.md          # Architecture Diagrams & Flowcharts
└── README.md                       # Documentation & Quickstart
```

---

## 🛠️ Quickstart Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ayushhcodex/aak.ai.git
   cd aak.ai
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Unit Tests**:
   ```bash
   python -m pytest tests/test_engines.py -v
   ```

4. **Launch the Application**:
   ```bash
   streamlit run app.py
   ```

---

## 📜 Citation & Institutional Attribution

```bibtex
@article{singh2026aimatry,
  title={AIMATRY: Materials Informatics Platform for Multi-Objective Formulation of Protective Technical Textiles},
  author={Singh, Ayush and Mishra, Vansh and Yadav, Nikhil Kumar},
  journal={Department of Computer Science & Engineering, NITRA Technical Campus},
  year={2026}
}
```
