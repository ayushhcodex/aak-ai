# 🧬 AIMATRY (AAK.AI) — Local Demo & Presentation Guide

This guide gives you the exact step-by-step instructions to launch the platform locally and present a complete, compelling demo to professors, NITRA researchers, defense officials, or conference evaluators.

---

## ⚡ Quick 1-Minute Launch

### Method 1: Using the One-Click Script (Easiest)
Open your Terminal on your Mac and run:
```bash
cd "/Users/ayushsingh/Documents/NITRA RESEARCH/AAK-AI"
./start.sh
```

### Method 2: Standard Command
```bash
cd "/Users/ayushsingh/Documents/NITRA RESEARCH/AAK-AI"
streamlit run app.py
```

Once the command runs, your default browser will automatically open to:
👉 **http://localhost:8501**

---

## 🎯 5-Minute Pitch & Demo Script (Recommended Presentation Flow)

When presenting to professors or evaluators, follow this 5-step flow:

### 1. Introduce the Problem & Solution (Sidebar & Main Screen)
- **What to say**: *"In traditional technical textile research at institutes like NITRA, formulating a protective fabric requires months of trial-and-error physical trials on sweating hotplates and flammability testers. AIMATRY is a closed-loop Materials Informatics and Generative Chemical AI platform that accelerates this by 10x."*
- **What to show**: Show the live dashboard, threat scenario selector, and real-time TOPSIS ranking radar chart.

### 2. Demonstrate Forward Simulation & Regulatory Compliance (Tabs 4 & 5)
- **What to say**: *"Our physics engine implements true Voigt-Reuss micromechanics and ASTM F1868 sweating guarded hotplate equations. It instantly audits the fabric against ISO 11612 (Firefighting), NFPA 1971, and Indian BIS IS 15742 standards."*
- **What to show**: Click **"📜 Regulatory Compliance"** and show the instant PASS/FLAG compliance matrix and ATPV Arc Rating.

### 3. Demonstrate the Inverse Design Solver (Sidebar Mode 2)
- **What to say**: *"Instead of guessing constituent ratios, our Inverse Material Design solver allows a defense engineer to specify target mission constraints (e.g. HTP > 85, THL > 270 W/m², Budget < ₹4,500/m²), and the Scipy SLSQP optimizer mathematically reverse-engineers the exact fiber blend, GSM, and weave."*
- **What to show**: Switch sidebar to **"Target Specs → Inverse Design Solver"**, move the target sliders, and show the discovered optimal solution.

### 4. Demonstrate Generative Chemistry & Active Learning (Tabs 2 & 3)
- **What to say**: *"We don't just optimize existing fibers—our Generative Chemical Language engine invents novel flame-retardant monomers with 2D chemical structures and synthetic accessibility scoring. Our Bayesian Active Learning engine tells the lab technician exactly which coupon to test next to minimize testing costs."*
- **What to show**: 
  - Go to **"🧬 Generative Chemistry"** $ightarrow$ Click *"Synthesize In-Silico Monomer Candidates"*.
  - Go to **"🎲 Active Learning Planner"** $ightarrow$ Click *"Compute Next Optimal Lab Experiment Coupons"*.

### 5. Demonstrate the Industrial Tech-Pack & Gemini AI Copilot (Tabs 9 & 14)
- **What to say**: *"To bridge research with manufacturing, AIMATRY generates production-ready Industrial Tech-Pack BOM PDFs for textile mills, and uses Gemini 2.5 Flash to automatically draft formal DRDO/Indian Army defense procurement proposals."*
- **What to show**: 
  - Click **"📄 Industrial Tech-Pack"** $ightarrow$ Download the generated Tech-Pack PDF.
  - Click **"💬 AI Technical Copilot"** $ightarrow$ Click *"Generate Defense Tender Proposal"*.

---

## 🛠️ Troubleshooting Cheat Sheet

1. **Port 8501 is already in use**:
   Run with a different port:
   ```bash
   streamlit run app.py --server.port=8502
   ```
   Or kill existing processes:
   ```bash
   pkill -f streamlit
   ```

2. **Verify the test suite before the presentation**:
   ```bash
   python3 -m pytest tests/ -v
   ```
   *(Confirms all 12 physics, ML, and chemistry tests are 100% passing).*

3. **Offline vs. Online**:
   - **Offline (No Internet)**: 14 out of 15 tabs work 100% offline (Physics, Inverse Design, ML Surrogates, NSGA-II Pareto, RDKit SVG Chemistry, Active Learning, Tech-Pack PDF generation).
   - **Online (Internet required)**: Only Tab 14 (Gemini AI Technical Copilot & Tender Drafter) needs an internet connection to reach the Google Gemini API.
