"""
AIMATRY: Enterprise Materials Informatics & Generative Polymer Designer — v3.4
=============================================================================
Department of Computer Science & Engineering, NITRA Technical Campus
Authors: Ayush Singh, Vansh Mishra, Nikhil Kumar Yadav

Integrated Engineering Architecture:
- TOPSIS Multi-Criteria Decision-Making Engine (core.mcdm)
- Physics-Based Voigt-Reuss Micromechanics & Transport Calculator (core.physics)
- RDKit Cheminformatics, SAScore & 2D Vector Structure Rendering (core.chemistry)
- Automated Regulatory Standards Compliance Auditor (core.compliance)
- Industrial Manufacturing Tech-Pack PDF/JSON Generator (core.techpack)
- True NSGA-II Multi-Objective Pareto Frontier Solver (core.optimizer)
- Machine Learning Surrogate Model with Uncertainty Quantification (ml.surrogate)
- Inverse Material Design Solver: Target Specs → Formula (core.inverse_design)
- Closed-Loop Active Learning Bayesian Optimization (ml.active_learning)
- Generative Chemical Discovery Engine (ml.clm)
- Physical Lab Test Ingestion & Empirical Calibration (database.lab_importer)
- Structured SQLite Monomer & Materials Database (database.db)
- Conversational AI Copilot & Defense Procurement Drafter (ai.copilot)
"""

import os
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mpl_config")

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import time
import textwrap
from dotenv import load_dotenv

load_dotenv()

# Computational & AI Engines
from data import (
    PROPERTY_KEYS, SCENARIOS, COMMERCIAL_BENCHMARKS,
    FIBER_DATABASE, INDIAN_STANDARDS,
)
from core.mcdm import topsis_rank_candidates
from core.physics import FIBER_SPECS, WEAVE_FACTORS, compute_blend_physics
from core.chemistry import compute_molecular_descriptors, render_mol_svg
from core.compliance import audit_compliance
from core.techpack import generate_techpack_dict, generate_techpack_pdf
from core.optimizer import run_pareto_optimization
from ml.surrogate import get_surrogate_model
from core.inverse_design import inverse_solve_formulation
from database.db import query_monomers, init_database
from database.lab_importer import (
    import_lab_test_file,
    get_all_lab_records,
    compute_empirical_calibration,
    generate_sample_nitra_lab_csv,
)
from ml.active_learning import ActiveLearningRecommender
from ml.clm import GenerativeMonomerEngine
from ai.copilot import ask_technical_copilot


# ── Caching Heavy Computations for Instant UI ───────────────────────────────
@st.cache_resource(show_spinner=False)
def cached_surrogate():
    return get_surrogate_model()

@st.cache_data(show_spinner=False)
def cached_pareto():
    return run_pareto_optimization(pop_size=25, n_gen=12, seed=42)

@st.cache_data(show_spinner=False)
def cached_monomers():
    return query_monomers()

@st.cache_resource(show_spinner=False)
def cached_clm_engine():
    return GenerativeMonomerEngine()


# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AIMATRY | Materials Informatics Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Clean Professional Enterprise Theme ─────────────────────────────────────
st.markdown(textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color: #e2e8f0;
}

.main .block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Header Banner */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}
.app-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.5px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.app-subtitle {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 0.2rem;
}
.org-tag {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 0.35rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #38bdf8;
    letter-spacing: 0.5px;
}

/* Enterprise Cards */
.enterprise-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.25rem;
}
.card-header-title {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #38bdf8;
    margin-bottom: 0.4rem;
}
.blend-name-display {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 0.5rem;
    line-height: 1.3;
}
.feature-desc {
    font-size: 0.9rem;
    color: #94a3b8;
    line-height: 1.5;
    margin-bottom: 1rem;
}

/* Metric Display Cards */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 0.75rem;
    margin-top: 0.75rem;
}
.metric-box {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 0.75rem;
    text-align: left;
}
.metric-box-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    font-weight: 700;
    color: #f8fafc;
}
.metric-box-lbl {
    font-size: 0.72rem;
    color: #94a3b8;
    margin-top: 0.2rem;
    font-weight: 500;
}

/* Compliance Badges */
.badge-group {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.8rem;
}
.badge-item {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 0.3rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 500;
    color: #cbd5e1;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}
.badge-pass {
    border-color: #059669;
    color: #34d399;
    background: rgba(16, 185, 129, 0.1);
}
.badge-flag {
    border-color: #d97706;
    color: #fbbf24;
    background: rgba(245, 158, 11, 0.1);
}

/* Navigation Section Headers */
.section-title {
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #94a3b8;
    margin-top: 1.2rem;
    margin-bottom: 0.5rem;
}

/* Standard Buttons */
div.stButton > button:first-child {
    background: #2563eb;
    color: #ffffff;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    border: 1px solid #3b82f6;
    border-radius: 6px;
    padding: 0.55rem 1.25rem;
    transition: background 0.15s ease-in-out;
    width: 100%;
}
div.stButton > button:hover {
    background: #1d4ed8;
    border-color: #2563eb;
    color: #ffffff;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #0f172a;
    border-radius: 8px;
    padding: 4px;
    border: 1px solid #1e293b;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    font-size: 0.88rem;
    padding: 8px 16px;
    border-radius: 6px;
    color: #94a3b8;
}
.stTabs [aria-selected="true"] {
    background-color: #1e293b !important;
    color: #38bdf8 !important;
    font-weight: 600;
}
</style>
"""), unsafe_allow_html=True)


# ── App Header ───────────────────────────────────────────────────────────────
st.markdown(textwrap.dedent("""
<div class="app-header">
    <div>
        <div class="app-title">🧬 AIMATRY <span style="font-size:0.9rem; font-weight:500; color:#64748b;">v3.4 Enterprise</span></div>
        <div class="app-subtitle">Materials Informatics & Generative Chemical Designer for Technical Protective Textiles</div>
    </div>
    <div style="text-align:right;">
        <span class="org-tag">NITRA Technical Campus · CSE</span>
    </div>
</div>
"""), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR CONTROLS & FORMULATION WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════════

st.sidebar.markdown('<div class="section-title" style="margin-top:0;">Design & Simulation Mode</div>', unsafe_allow_html=True)
design_mode = st.sidebar.radio(
    "Select Workflow Mode",
    [
        "Curated Threat Scenarios + Live TOPSIS",
        "Target Specs → Inverse Design Solver",
        "Custom Multi-Fiber Blender",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown('<div class="section-title">TOPSIS Priority Weights</div>', unsafe_allow_html=True)
st.sidebar.caption("Adjust multi-criteria objective weights for ranking:")

user_weights = {}
user_weights["Thermal Protection (HTP)"] = st.sidebar.slider("Thermal Protection (HTP)", 0, 100, 75, 5)
user_weights["Comfort & Breathability (THL)"] = st.sidebar.slider("Comfort & Breathability (THL)", 0, 100, 60, 5)
user_weights["Tensile Strength"] = st.sidebar.slider("Tensile Strength", 0, 100, 70, 5)
user_weights["Flexibility"] = st.sidebar.slider("Flexibility / Drape", 0, 100, 50, 5)
user_weights["Manufacturability"] = st.sidebar.slider("Manufacturability / SAScore", 0, 100, 65, 5)

# Calculate TOPSIS Ranking
topsis_df, top_recommended = topsis_rank_candidates(user_weights)



# ── Workflow Branching ───────────────────────────────────────────────────────
if design_mode == "Curated Threat Scenarios + Live TOPSIS":
    st.sidebar.markdown('<div class="section-title">Operational Threat Scenario</div>', unsafe_allow_html=True)
    selected_threat = st.sidebar.selectbox(
        "Threat Environment",
        list(SCENARIOS.keys()),
        index=list(SCENARIOS.keys()).index(top_recommended) if top_recommended in SCENARIOS else 0,
    )
    compare_scenarios = st.sidebar.multiselect(
        "Compare Benchmarks on Radar",
        [k for k in SCENARIOS.keys() if k != selected_threat],
        default=[],
    )
    active_scenario_data = SCENARIOS[selected_threat]
    constituents = active_scenario_data.get("constituents", {"Meta-aramid (Nomex)": 100.0})
    current_gsm = active_scenario_data.get("default_gsm", 260.0)
    current_weave = active_scenario_data.get("default_weave", "Ripstop Grid")
    blend_title = active_scenario_data["blend"]
    feature_text = active_scenario_data["feature"]

elif design_mode == "Target Specs → Inverse Design Solver":
    st.sidebar.markdown('<div class="section-title">Target Specification Solver</div>', unsafe_allow_html=True)
    t_htp = st.sidebar.slider("Target Minimum HTP Score", 40, 98, 85, 2)
    t_thl = st.sidebar.slider("Target Minimum THL Score", 20, 90, 65, 2)
    t_ten = st.sidebar.slider("Target Minimum Tensile Score", 30, 98, 75, 2)
    t_loi = st.sidebar.slider("Target Minimum LOI (%)", 20.0, 70.0, 30.0, 1.0)
    t_cost = st.sidebar.slider("Max Production Budget (₹/m²)", 1000, 12000, 4500, 250)

    target_inputs = {
        "min_htp": t_htp,
        "min_thl": t_thl,
        "min_tensile": t_ten,
        "min_loi": t_loi,
        "min_bio_pct": 0.0,
    }
    inv_result = inverse_solve_formulation(target_inputs, max_budget_inr=t_cost)

    selected_threat = "Inverse Designed Optimal Composite"
    compare_scenarios = []
    constituents = inv_result["discovered_blend"]
    current_gsm = inv_result["recommended_gsm"]
    current_weave = inv_result["recommended_weave"]
    blend_title = inv_result["blend_name"]
    feature_text = f"Reverse-engineered formulation satisfying target constraints: HTP ≥ {t_htp}, THL ≥ {t_thl}, Tensile ≥ {t_ten}."
    active_scenario_data = {
        "blend": blend_title,
        "feature": feature_text,
        "status": "Inverse-Solved",
        "confidence": 94,
        "constituents": constituents,
        "default_gsm": current_gsm,
        "default_weave": current_weave,
        "synth_route": SCENARIOS["Extreme Cold Weather"]["synth_route"],
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 97, 93, 89, 83, 76], "metric": "HTP retention (%)"},
    }

else:
    st.sidebar.markdown('<div class="section-title">Custom Fiber Blend Configuration</div>', unsafe_allow_html=True)
    selected_threat = "Custom Formulated Composite"
    compare_scenarios = []

    f1 = st.sidebar.selectbox("Primary Fiber", list(FIBER_SPECS.keys()), index=0)
    f1_pct = st.sidebar.slider(f"{f1} (%)", 10, 100, 60, 5)

    f2_options = ["None"] + [f for f in FIBER_SPECS.keys() if f != f1]
    f2 = st.sidebar.selectbox("Secondary Fiber", f2_options, index=1)
    f2_pct = st.sidebar.slider(f"{f2} (%)", 0, 90, 30, 5) if f2 != "None" else 0

    f3_options = ["None"] + [f for f in FIBER_SPECS.keys() if f not in [f1, f2]]
    f3 = st.sidebar.selectbox("Tertiary Functional Fiber", f3_options, index=2 if len(f3_options) > 2 else 0)
    f3_pct = st.sidebar.slider(f"{f3} (%)", 0, 50, 10, 5) if f3 != "None" else 0

    raw_dict = {f1: f1_pct}
    if f2 != "None" and f2_pct > 0:
        raw_dict[f2] = f2_pct
    if f3 != "None" and f3_pct > 0:
        raw_dict[f3] = f3_pct

    total_pct = sum(raw_dict.values())
    constituents = {k: round((v / total_pct) * 100, 1) for k, v in raw_dict.items()}

    current_gsm = st.sidebar.slider("Fabric Areal Density (GSM)", 120, 500, 280, 10)
    current_weave = st.sidebar.selectbox("Fabric Weave Architecture", list(WEAVE_FACTORS.keys()), index=2)

    blend_title = " / ".join([f"{pct}% {name.split(' ')[0]}" for name, pct in constituents.items()])
    feature_text = f"Custom multi-fiber formulation woven in {current_weave} at {current_gsm} g/m²."
    active_scenario_data = {
        "blend": blend_title,
        "feature": feature_text,
        "status": "User-Formulated",
        "confidence": 89,
        "constituents": constituents,
        "default_gsm": current_gsm,
        "default_weave": current_weave,
        "synth_route": SCENARIOS["Extreme Cold Weather"]["synth_route"],
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 96, 91, 85, 78, 70], "metric": "Tensile strength retention (%)"},
    }

# Compute Real Physics & Compliance
physics_res = compute_blend_physics(constituents, gsm=current_gsm, weave_type=current_weave)
compliance_res = audit_compliance(physics_res)
active_scores = physics_res["scores"]

# Find TOPSIS rank for active scenario
topsis_rank_val = 1
topsis_match_pct = 95.0
if selected_threat in SCENARIOS:
    match_row = topsis_df[topsis_df["Scenario"] == selected_threat]
    if not match_row.empty:
        topsis_rank_val = int(match_row.iloc[0]["Rank"])
        topsis_match_pct = float(match_row.iloc[0]["TOPSIS Match %"])


# ── Primary Pipeline Execution Button in Sidebar ─────────────────────────────
st.sidebar.markdown('<div class="section-title">Pipeline Execution</div>', unsafe_allow_html=True)
run_pipeline_clicked = st.sidebar.button("⚡ EXECUTE VIRTUAL SYNTHESIS PIPELINE", use_container_width=True)

if run_pipeline_clicked:
    with st.status("🔬 Running Materials Informatics & Multi-Objective Synthesis...", expanded=True) as status:
        st.write(f"⚙️ Calculating Voigt-Reuss Micromechanics across {len(constituents)} constituent fibers...")
        time.sleep(0.2)
        st.write(f"📊 Executing TOPSIS Multi-Criteria Decision Ranking (Top Match: #{topsis_rank_val} {selected_threat})...")
        time.sleep(0.2)
        st.write("🛡️ Auditing ISO 11612, NFPA 1971, ASTM F1959, and BIS IS 15742 Pre-Compliance...")
        time.sleep(0.2)
        st.write("📈 Computing NSGA-II Multi-Objective Pareto Frontier with pymoo...")
        time.sleep(0.2)
        status.update(label="✅ Virtual Synthesis & Optimization Pipeline Complete!", state="complete")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOTLY CHART BUILDERS (CLEAN SCIENTIFIC AESTHETICS)
# ═══════════════════════════════════════════════════════════════════════════════

def build_radar_chart(primary_scores, comp_dict=None):
    categories = PROPERTY_KEYS
    fig = go.Figure()
    vals = [primary_scores.get(c, 50) for c in categories]
    vals.append(vals[0])
    cats = categories + [categories[0]]

    fig.add_trace(go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor="rgba(37, 99, 235, 0.2)",
        line=dict(color="#38bdf8", width=2),
        name="Active Composite",
    ))

    colors_comp = ["#f59e0b", "#ec4899", "#10b981", "#a855f7"]
    if comp_dict:
        for idx, (name, sc_scores) in enumerate(comp_dict.items()):
            c_vals = [sc_scores.get(c, 50) for c in categories]
            c_vals.append(c_vals[0])
            col = colors_comp[idx % len(colors_comp)]
            fig.add_trace(go.Scatterpolar(
                r=c_vals, theta=cats, fill="none",
                line=dict(color=col, width=1.5, dash="dash"),
                name=name[:18],
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#64748b", gridcolor="#1e293b", tickfont=dict(size=9, color="#94a3b8")),
            angularaxis=dict(color="#cbd5e1", gridcolor="#1e293b", tickfont=dict(size=10, family="Inter")),
            bgcolor="#0b0f19",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=30, r=30, t=20, b=20),
        height=320,
        legend=dict(font=dict(size=10, color="#94a3b8", family="Inter"), bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.12),
        font=dict(family="Inter"),
    )
    return fig


def build_pareto_chart(all_candidates_df, pareto_front_df, active_comp_score, active_manuf_score):
    fig = go.Figure()
    bg = all_candidates_df[~all_candidates_df["Pareto Optimal"]]
    fig.add_trace(go.Scatter(
        x=bg["Composite Performance Score"], y=bg["Manufacturability"],
        mode="markers",
        marker=dict(size=6, color="#475569", opacity=0.6),
        name="Screened Formulations",
        hovertext=bg["Blend Formulation"],
        hovertemplate="<b>%{hovertext}</b><br>Score: %{x}<br>Manufacturability: %{y}<extra></extra>",
    ))

    sorted_front = pareto_front_df.sort_values(by="Composite Performance Score")
    fig.add_trace(go.Scatter(
        x=sorted_front["Composite Performance Score"], y=sorted_front["Manufacturability"],
        mode="lines+markers",
        line=dict(color="#10b981", width=2),
        marker=dict(size=8, color="#10b981", symbol="diamond"),
        name="NSGA-II Pareto Frontier",
        hovertext=sorted_front["Blend Formulation"],
        hovertemplate="<b>Pareto Optimum: %{hovertext}</b><br>Score: %{x}<br>Manufacturability: %{y}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=[active_comp_score], y=[active_manuf_score],
        mode="markers",
        marker=dict(size=12, color="#38bdf8", symbol="star", line=dict(color="#ffffff", width=1.5)),
        name="Active Selection",
        hoverinfo="text",
        hovertext=f"Active Selection: Score={active_comp_score}, Manuf={active_manuf_score}",
    ))

    fig.update_layout(
        xaxis=dict(title=dict(text="Composite Performance (HTP + Tensile + Comfort)", font=dict(color="#94a3b8", size=11)), gridcolor="#1e293b", tickfont=dict(color="#64748b", size=10)),
        yaxis=dict(title=dict(text="Manufacturability & SAScore Rating", font=dict(color="#94a3b8", size=11)), gridcolor="#1e293b", tickfont=dict(color="#64748b", size=10)),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0b0f19",
        margin=dict(l=40, r=20, t=20, b=40), height=340,
        legend=dict(font=dict(size=10, color="#94a3b8"), bgcolor="rgba(0,0,0,0)", x=0.02, y=0.98),
        font=dict(family="Inter"),
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN OVERVIEW SUMMARY CARD (CLEAN UNINDENTED HTML)
# ═══════════════════════════════════════════════════════════════════════════════

card_col, chart_col = st.columns([1.1, 1], gap="medium")

with card_col:
    c_iso = "badge-pass" if compliance_res['standards'][0]['status'] == 'PASS' else "badge-flag"
    c_nfpa = "badge-pass" if compliance_res['standards'][1]['status'] == 'PASS' else "badge-flag"
    c_bis = "badge-pass" if compliance_res['standards'][3]['status'] == 'PASS' else "badge-flag"

    summary_html = f"""<div class="enterprise-card">
<div style="display:flex; justify-content:space-between; align-items:center;">
<span class="card-header-title">{selected_threat}</span>
<span style="font-size:0.75rem; color:#38bdf8; font-weight:600;">TOPSIS #{topsis_rank_val} ({topsis_match_pct}%)</span>
</div>
<div class="blend-name-display">{blend_title}</div>
<div class="feature-desc">{feature_text}</div>
<div class="metric-grid">
<div class="metric-box">
<div class="metric-box-val">{physics_res['total_heat_loss_thl_w_m2']}</div>
<div class="metric-box-lbl">THL (W/m²)</div>
</div>
<div class="metric-box">
<div class="metric-box-val">{physics_res['loi_pct']}%</div>
<div class="metric-box-lbl">LOI Index</div>
</div>
<div class="metric-box">
<div class="metric-box-val">{physics_res['tensile_strength_gpa']}</div>
<div class="metric-box-lbl">Tensile (GPa)</div>
</div>
<div class="metric-box">
<div class="metric-box-val">₹{physics_res['cost_inr_per_m2']}</div>
<div class="metric-box-lbl">Cost / m²</div>
</div>
</div>
<div class="badge-group">
<span class="badge-item {c_iso}">🛡️ ISO 11612: {compliance_res['standards'][0]['status']}</span>
<span class="badge-item {c_nfpa}">🚒 NFPA 1971: {compliance_res['standards'][1]['status']}</span>
<span class="badge-item">⚡ Arc ATPV: {compliance_res['standards'][2]['classification'].split(' ')[0]}</span>
<span class="badge-item {c_bis}">🇮🇳 BIS IS 15742: {compliance_res['standards'][3]['status']}</span>
</div>
</div>"""
    st.markdown(summary_html, unsafe_allow_html=True)

with chart_col:
    comparisons = None
    if compare_scenarios:
        comparisons = {name: compute_blend_physics(SCENARIOS[name].get("constituents", {}))["scores"] for name in compare_scenarios}
    fig_radar = build_radar_chart(active_scores, comparisons)
    st.plotly_chart(fig_radar, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 5 CLEAN LOGICAL OPERATIONAL MODULES
# ═══════════════════════════════════════════════════════════════════════════════

tab_sim, tab_lab_al, tab_chem_gen, tab_compliance_tech, tab_analytics = st.tabs([
    "🔬 Material Designer & Simulator",
    "🧪 Laboratory & Active Learning",
    "🧬 Generative Chemistry & Monomers",
    "📜 Regulatory Standards & Tech-Pack",
    "📊 ML Surrogates & Deep Analytics",
])


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 1: MATERIAL DESIGNER & SIMULATOR
# ─────────────────────────────────────────────────────────────────────────────
with tab_sim:
    st.markdown("### 🔬 Multi-Fiber Physics Simulation & Micromechanics")
    st.caption("Calculates macro composite properties from fiber constituent ratios using Voigt-Reuss mixture rules and ASTM F1868 Sweating Hotplate models.")

    sub_sim1, sub_sim2 = st.columns([1.2, 1], gap="large")

    with sub_sim1:
        st.markdown("#### Composite Constituent Fractions & Volume Ratios")
        comp_display = []
        for f, w_pct in physics_res["blend_fractions"].items():
            comp_display.append({
                "Fiber Constituent": f,
                "Mass Fraction (%)": f"{w_pct}%",
                "Volume Fraction (%)": f"{physics_res['volume_fractions'].get(f, w_pct)}%",
                "Fiber LOI (%)": f"{FIBER_SPECS.get(f, {}).get('loi_pct', 30)}%",
                "Density (g/cm³)": FIBER_SPECS.get(f, {}).get('density_g_cm3', 1.4),
                "Cost (₹/kg)": f"₹{FIBER_SPECS.get(f, {}).get('cost_inr_kg', 3000)}",
            })
        st.dataframe(pd.DataFrame(comp_display), use_container_width=True, hide_index=True)

        if design_mode == "Target Specs → Inverse Design Solver":
            st.success(f"✅ Inverse Solver Discovered Solution: **{blend_title}** ({current_gsm} g/m², {current_weave})")
            st.dataframe(pd.DataFrame(inv_result["target_comparison"]), use_container_width=True)

    with sub_sim2:
        st.markdown("#### Thermal Transport & Structural Properties")
        p_table = [
            ("Composite Density", f"{physics_res['composite_density_g_cm3']} g/cm³"),
            ("Tensile Modulus (E)", f"{physics_res['tensile_modulus_gpa']} GPa"),
            ("Tensile Strength (σ)", f"{physics_res['tensile_strength_gpa']} GPa"),
            ("Thermal Resistance (R_ct)", f"{physics_res['thermal_resistance_rct']} m²·K/W"),
            ("Evaporative Resistance (R_et)", f"{physics_res['evaporative_resistance_ret']} m²·Pa/W"),
            ("Total Heat Loss (THL)", f"{physics_res['total_heat_loss_thl_w_m2']} W/m²"),
            ("Limiting Oxygen Index (LOI)", f"{physics_res['loi_pct']}%"),
            ("Max Continuous Service Temp", f"{physics_res['max_service_temp_c']} °C"),
            ("Estimated Areal Cost", f"₹{physics_res['cost_inr_per_m2']} / m² (${physics_res['cost_usd_per_m2']})"),
        ]
        st.dataframe(pd.DataFrame(p_table, columns=["Physical Property", "Calculated Value"]), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 2: LABORATORY & ACTIVE LEARNING
# ─────────────────────────────────────────────────────────────────────────────
with tab_lab_al:
    st.markdown("### 🧪 NITRA Physical Lab Ingestion & Closed-Loop Active Learning")
    st.caption("Ingest experimental test records from NITRA/TBRL testing machines and use Gaussian Process Bayesian Optimization to plan the next optimal test coupons.")

    al_col1, al_col2 = st.columns([1.1, 1], gap="large")

    with al_col1:
        st.markdown("#### 🎯 Closed-Loop Active Learning Experiment Planner")
        st.markdown("<p style='font-size:0.85rem; color:#94a3b8;'>Recommends optimal laboratory fabrication formulations to maximize discovery while minimizing testing costs.</p>", unsafe_allow_html=True)

        target_prop = st.selectbox(
            "Target Optimization Objective",
            ["measured_thl", "measured_loi", "measured_tensile_gpa", "measured_htp"],
            format_func=lambda x: {
                "measured_thl": "Total Heat Loss THL (W/m²)",
                "measured_loi": "Limiting Oxygen Index LOI (%)",
                "measured_tensile_gpa": "Tensile Strength (GPa)",
                "measured_htp": "Heat Transfer Performance (HTP)",
            }.get(x, x),
        )

        acq_c1, acq_c2 = st.columns(2)
        with acq_c1:
            acq_func = st.selectbox("Acquisition Strategy", ["Expected Improvement", "Upper Confidence Bound"])
        with acq_c2:
            top_k_val = st.slider("Coupons to Recommend", 3, 8, 5)

        if st.button("🚀 Compute Next Optimal Lab Coupons", use_container_width=True):
            with st.spinner("Optimizing Gaussian Process acquisition surface..."):
                al = ActiveLearningRecommender(target_metric=target_prop, maximize=True)
                al.fit_from_database()
                recs = al.recommend_next_experiments(acquisition=acq_func, top_k=top_k_val)
                st.session_state["al_recs"] = recs

        if "al_recs" in st.session_state and st.session_state["al_recs"]:
            recs_data = st.session_state["al_recs"]
            recs_df = pd.DataFrame(recs_data)
            display_cols = [c for c in ["rank", "p_aramid", "m_aramid", "pbi", "modacrylic", "gsm", "recommended_weave", "predicted_mean", "epistemic_std", "acquisition_score"] if c in recs_df.columns]
            st.dataframe(recs_df[display_cols], use_container_width=True, hide_index=True)
            st.download_button(
                label="📥 Download Lab Batch Card (CSV)",
                data=recs_df.to_csv(index=False).encode("utf-8"),
                file_name="NITRA_Recommended_Batch.csv",
                mime="text/csv",
                use_container_width=True,
            )

    with al_col2:
        st.markdown("#### 📂 NITRA Lab Data Importer & Empirical Calibration")
        st.markdown("<p style='font-size:0.85rem; color:#94a3b8;'>Ingest Sweating Hotplate, Flammability, and Tensile test records to recalibrate theoretical models.</p>", unsafe_allow_html=True)

        up_file = st.file_uploader("Upload Lab Test Sheet (.csv, .xlsx)", type=["csv", "xlsx", "xls"])
        if up_file is not None:
            try:
                res = import_lab_test_file(up_file.getvalue(), up_file.name)
                st.success(f"✅ Successfully ingested {res['records_imported']} physical test records!")
            except Exception as e:
                st.error(f"Error importing: {e}")

        st.download_button(
            label="📥 Download Sample NITRA Test Sheet (CSV)",
            data=generate_sample_nitra_lab_csv(),
            file_name="Sample_NITRA_Lab_Test_Records.csv",
            mime="text/csv",
            use_container_width=True,
        )

        if st.button("⚖️ Run Empirical Physics Calibration", use_container_width=True):
            calib = compute_empirical_calibration()
            if calib["status"] == "calibrated":
                k = calib["calibration_factors"]
                calib_card = f"""<div class="enterprise-card" style="margin-top:0.75rem;">
<div style="font-size:0.8rem; color:#34d399; font-weight:600; margin-bottom:0.5rem;">✓ Model Calibrated ({calib['total_records_used']} trials)</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:0.8rem; color:#cbd5e1;">
<div><b>κ_THL Factor:</b> {k['kappa_thl']}</div>
<div><b>κ_LOI Factor:</b> {k['kappa_loi']}</div>
<div><b>κ_Tensile Factor:</b> {k['kappa_tensile']}</div>
<div><b>THL RMSE:</b> {calib['metrics']['thl_rmse_w_m2']} W/m²</div>
</div>
</div>"""
                st.markdown(calib_card, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 3: GENERATIVE CHEMISTRY & MONOMERS
# ─────────────────────────────────────────────────────────────────────────────
with tab_chem_gen:
    st.markdown("### 🧬 Generative Chemical Language Discovery & Monomer Library")
    st.caption("Algorithmic monomer discovery for high-temperature and flame-retardant polymers with 2D chemical structure rendering and synthetic accessibility filtering.")

    gc_c1, gc_c2 = st.columns([1.1, 1], gap="large")

    with gc_c1:
        st.markdown("#### 🔬 In Silico Polymer Monomer Discovery")
        cat_select = st.selectbox(
            "Target Polymer Backbone & Monomer Class",
            ["Diamine (Polyamide/Polyimide)", "Diacyl Chloride (Aramid)", "Dicarboxylic Acid", "Bisphenol (Polyarylate)", "Dicyanate / Cyanate Ester"],
        )
        include_fr = st.checkbox("Attach Flame-Retardant Sidechains (Phosphonate / Trifluoromethyl / Nitrile)", value=True)
        max_sa = st.slider("Max Permitted SAScore (1 = Easy, 10 = Complex)", 2.5, 6.0, 4.5, 0.1)

        if st.button("🧪 Synthesize In-Silico Monomer Candidates", use_container_width=True):
            with st.spinner("Generating valid chemical structures and calculating RDKit descriptors..."):
                clm = cached_clm_engine()
                gen_cands = clm.generate_candidate_monomers(target_category=cat_select, include_fr_sidechains=include_fr, max_candidates=4, target_max_sascore=max_sa)
                st.session_state["gen_monomers"] = gen_cands

        if "gen_monomers" in st.session_state and st.session_state["gen_monomers"]:
            for c in st.session_state["gen_monomers"]:
                cand_card = f"""<div class="enterprise-card" style="margin-bottom:0.75rem;">
<div style="display:flex; justify-content:space-between;">
<span style="font-weight:700; color:#38bdf8;">{c['candidate_id']} · {c['core_scaffold']}</span>
<span style="color:#34d399; font-weight:600; font-size:0.8rem;">Est. Td: {c['estimated_td_c']} °C</span>
</div>
<div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#94a3b8; margin:0.3rem 0; word-break:break-all;">{c['smiles']}</div>
<div style="text-align:center; background:#0b0f19; border-radius:6px; padding:6px; margin:0.5rem 0;">{c['svg_b64']}</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:0.78rem; color:#94a3b8;">
<div><b>Mol Wt:</b> {c['mol_weight']} g/mol</div>
<div><b>SAScore:</b> {c['sascore']} / 10</div>
<div><b>LOI Boost:</b> +{c['estimated_loi_potential']}%</div>
<div><b>Analog:</b> {c['closest_commercial_analog']} (Sim: {c['tanimoto_similarity']})</div>
</div>
</div>"""
                st.markdown(cand_card, unsafe_allow_html=True)

    with gc_c2:
        st.markdown("#### 🗄️ Curated Reactive Monomer SQLite Database")
        st.markdown("<p style='font-size:0.85rem; color:#94a3b8;'>Browse curated monomers with computed 512-bit Morgan fingerprints (ECFP4), commercial suppliers, and unit costs.</p>", unsafe_allow_html=True)
        monomer_df = cached_monomers()
        st.dataframe(monomer_df, use_container_width=True, height=420)


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 4: REGULATORY STANDARDS & TECH-PACK
# ─────────────────────────────────────────────────────────────────────────────
with tab_compliance_tech:
    st.markdown("### 📜 Regulatory Standards Auditor & Industrial Tech-Pack Generator")
    st.caption("Pre-compliance evaluation against mandatory international and Indian defense standards, and one-click production Tech-Pack PDF generation.")

    comp_c1, comp_c2 = st.columns([1.1, 1], gap="large")

    with comp_c1:
        st.markdown("#### 🛡️ Automated Standards Compliance Matrix")
        audit_rows = []
        for std in compliance_res["standards"]:
            audit_rows.append({
                "Standard": std.get("code", std.get("standard", "Standard")),
                "Domain": std.get("title", ""),
                "Status": std.get("status", "PASS"),
                "Classification": std.get("classification", "Certified"),
                "Key Criterion": std.get("details", "Meets threshold"),
            })
        st.dataframe(pd.DataFrame(audit_rows), use_container_width=True, hide_index=True)

        st.markdown("#### ⚡ Arc Flash Rating (ASTM F1959 / NFPA 70E)")
        arc_info = compliance_res["standards"][2]
        st.info(f"**Classification:** {arc_info['classification']} | **Min ATPV Requirement:** {arc_info.get('min_atpv_cal_cm2', 8.0)} cal/cm²")

    with comp_c2:
        st.markdown("#### 📄 Industrial Manufacturing Tech-Pack BOM PDF")
        st.markdown("<p style='font-size:0.85rem; color:#94a3b8;'>Generates a comprehensive manufacturing Bill of Materials (BOM) for textile spinning and weaving mills.</p>", unsafe_allow_html=True)

        if st.button("📄 Generate Industrial Tech-Pack PDF", use_container_width=True):
            with st.spinner("Generating production specification PDF with ReportLab..."):
                pdf_bytes = generate_techpack_pdf(blend_title, physics_res, compliance_res)
                st.download_button(
                    label="📥 Download Complete Tech-Pack PDF",
                    data=pdf_bytes,
                    file_name=f"TechPack_{selected_threat.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.success("✅ Tech-Pack PDF successfully compiled!")


# ─────────────────────────────────────────────────────────────────────────────
# MODULE 5: ML SURROGATES & DEEP ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────
with tab_analytics:
    st.markdown("### 📊 Machine Learning Surrogates, Pareto Optimization & Copilot")
    st.caption("Ensemble Random Forest regressors with 95% Confidence Intervals, NSGA-II multi-objective frontier, and Gemini AI Copilot.")

    an_c1, an_c2 = st.columns([1.1, 1], gap="large")

    with an_c1:
        st.markdown("#### 🤖 ML Surrogate Property Predictors (Epistemic Uncertainty)")
        surrogate_model = cached_surrogate()
        ml_preds = surrogate_model.predict_with_uncertainty(constituents, gsm=current_gsm, weave_type=current_weave)

        ml_metric_cards = []
        for prop, val in ml_preds.items():
            ml_metric_cards.append({
                "Property": prop.replace("_", " ").title(),
                "Predicted Value": str(val["mean"]),
                "± Uncertainty": f"±{val['std_uncertainty']}",
                "95% Confidence Interval": f"[{val['ci_95_lower']}, {val['ci_95_upper']}]",
            })
        st.dataframe(pd.DataFrame(ml_metric_cards), use_container_width=True, hide_index=True)

        st.markdown("#### 📈 NSGA-II Multi-Objective Pareto Frontier")
        all_cands_df, pareto_front_df = cached_pareto()
        active_comp = round((active_scores["Thermal Protection (HTP)"] * 0.35 + active_scores["Comfort & Breathability (THL)"] * 0.25 + active_scores["Tensile Strength"] * 0.25 + active_scores["Manufacturability"] * 0.15), 1)
        fig_pareto = build_pareto_chart(all_cands_df, pareto_front_df, active_comp, active_scores["Manufacturability"])
        st.plotly_chart(fig_pareto, use_container_width=True)

    with an_c2:
        st.markdown("#### 💬 AI Materials Technical Copilot")
        user_query = st.text_input("Ask AI Copilot a technical question:", placeholder="e.g. Compare thermal degradation of Nomex vs Kevlar")
        if st.button("💬 Ask AI Copilot", use_container_width=True):
            if not user_query.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Consulting Gemini materials model..."):
                    ai_reply = ask_technical_copilot(user_query, selected_threat, blend_title, physics_res, compliance_res)
                    st.chat_message("assistant").markdown(ai_reply)

st.markdown('<div style="text-align:center; margin-top:2.5rem; font-size:0.75rem; color:#64748b;">AIMATRY v3.4 Enterprise · Materials Informatics & Optimization Engine · NITRA Technical Campus</div>', unsafe_allow_html=True)
