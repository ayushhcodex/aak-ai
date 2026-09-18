"""
AIMATRY v3.0: Core Materials Informatics Data Store
Contains standardized high-performance textile threat scenarios, baseline constituent blends,
commercial benchmarks, fiber databases, and regulatory standards.
"""

PROPERTY_KEYS = [
    "Thermal Protection (HTP)",
    "Comfort & Breathability (THL)",
    "Tensile Strength",
    "Flexibility",
    "Manufacturability",
]

# ═══════════════════════════════════════════════════════════════════════════════
# 10 THREAT SCENARIOS WITH REAL CONSTITUENT BLEND DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

SCENARIOS = {
    "Extreme Cold Weather": {
        "blend": "Meta-aramid / Aerogel Nanoporous Composite",
        "feature": "Maximizes thermal insulation while retaining high thermo-physiological comfort (THL).",
        "constituents": {"Meta-aramid (Nomex)": 80.0, "Silica Aerogel Nanocomposite": 20.0},
        "default_gsm": 280.0,
        "default_weave": "Ripstop Grid",
        "scores": {"Thermal Protection (HTP)": 85, "Comfort & Breathability (THL)": 70, "Tensile Strength": 60, "Flexibility": 80, "Manufacturability": 90},
        "confidence": 92,
        "status": "✅ Commercial",
        "sustainability": {"bio_based_pct": 0, "recyclable": "Partial", "co2_kg": 27.8, "water_L": 71.0},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 97, 93, 88, 82, 75], "metric": "HTP retention (%)"},
        "synth_route": [
            {"title": "Monomer Selection", "desc": "Select isophthaloyl chloride and m-phenylenediamine from curated library.", "smiles": "Nc1cccc(N)c1 + ClC(=O)c1cccc(C(=O)Cl)c1"},
            {"title": "Interfacial Polycondensation", "desc": "Step-growth polymerization at aqueous-organic interface (25°C, 2h).", "smiles": "Nc1cccc(NC(=O)c2cccc(C(=O)Cl)c2)c1"},
            {"title": "Aerogel Nanocomposite Infusion", "desc": "Infuse silica aerogel precursor (TEOS) via supercritical CO₂ drying.", "smiles": "CCO[Si](OCC)(OCC)OCC"},
            {"title": "Lamination & Finishing", "desc": "Hot-press laminate with PTFE moisture barrier. Apply DWR treatment.", "smiles": "FC(F)(F)C(F)(F)F"},
        ],
        "chat_explanation": [
            ("assistant", "I selected **Meta-aramid** as the base fiber for its excellent inherent flame resistance (LOI > 28%) and thermal stability up to 370°C — critical for Arctic combat where flash fires from equipment are a risk."),
            ("assistant", "The **aerogel nanoporous composite** layer provides a thermal conductivity of just 0.018 W/mK — roughly 3× better than standard batting insulation — while adding only 15% to the total weight."),
            ("assistant", "I specifically optimized for the **HTP-THL trade-off**: most insulating materials trap moisture and reduce comfort. By using a nanoporous structure with 95% porosity, we maintain vapor permeability at 28 m²Pa/W, keeping the THL score at 70."),
            ("assistant", "⚡ Synthetic accessibility score is **90/100** — all monomers are commercially available and the process uses standard interfacial polycondensation. Scale-up risk is minimal."),
        ],
    },
    "Ballistic Impact": {
        "blend": "Para-aramid / Carbon Nanotube (CNT) Matrix",
        "feature": "Extreme tensile strength and shear thickening properties upon impact.",
        "constituents": {"Para-aramid (Kevlar/Twaron)": 90.0, "Carbon Fiber (PAN-based)": 10.0},
        "default_gsm": 340.0,
        "default_weave": "Plain Weave (1/1)",
        "scores": {"Thermal Protection (HTP)": 50, "Comfort & Breathability (THL)": 40, "Tensile Strength": 95, "Flexibility": 45, "Manufacturability": 75},
        "confidence": 88,
        "status": "⚠️ Active R&D",
        "sustainability": {"bio_based_pct": 0, "recyclable": "No", "co2_kg": 32.8, "water_L": 105.5},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 99, 97, 95, 92, 89], "metric": "Tensile strength retention (%)"},
        "synth_route": [
            {"title": "Monomer Selection", "desc": "Select p-phenylenediamine and terephthaloyl chloride for para-aramid backbone.", "smiles": "Nc1ccc(N)cc1 + ClC(=O)c1ccc(C(=O)Cl)cc1"},
            {"title": "Solution Polymerization", "desc": "Low-temperature polycondensation in NMP/CaCl₂ solvent system (−10°C, 4h).", "smiles": "Nc1ccc(NC(=O)c2ccc(C(=O)Cl)cc2)cc1"},
            {"title": "CNT Doping & Wet Spinning", "desc": "Disperse MWCNTs (0.5 wt%) in dope solution. Wet-spin through air-gap into fibers.", "smiles": "C1=CC=C2C(=C1)C=CC=C2"},
            {"title": "Weave & STF Impregnation", "desc": "2D plain-weave at 34 threads/cm. Impregnate with colloidal silica STF.", "smiles": "O[Si](O)(O)O"},
        ],
        "chat_explanation": [
            ("assistant", "**Para-aramid (PPTA)** was chosen as the primary fiber because of its exceptional specific strength — 5× stronger than steel per unit weight. It's the gold standard for ballistic protection."),
            ("assistant", "Adding **multi-wall carbon nanotubes (0.5 wt%)** into the fiber spinning dope increases tensile modulus by ~22% and improves energy absorption during high-velocity impact."),
            ("assistant", "The **shear thickening fluid (STF)** is the key innovation: at low strain rates the fabric remains flexible, but upon bullet impact the colloidal suspension immediately rigidifies, distributing energy across a much larger area."),
            ("assistant", "⚠️ Trade-off: comfort and breathability score is **40/100** — this is a rigid, tightly woven system. For prolonged wear, I recommend pairing with a separate comfort liner."),
        ],
    },
    "Lunar Operations": {
        "blend": "Polyimide / Aluminized Mylar Laminate with Auxetic Weave",
        "feature": "Maximum radiation shielding and extreme temperature variance tolerance.",
        "constituents": {"Polyimide (Kapton/P84)": 75.0, "Silica Aerogel Nanocomposite": 25.0},
        "default_gsm": 310.0,
        "default_weave": "Auxetic Re-entrant Grid",
        "scores": {"Thermal Protection (HTP)": 95, "Comfort & Breathability (THL)": 20, "Tensile Strength": 80, "Flexibility": 60, "Manufacturability": 50},
        "confidence": 79,
        "status": "✅ NASA-Deployed",
        "sustainability": {"bio_based_pct": 0, "recyclable": "No", "co2_kg": 32.2, "water_L": 76.2},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 98, 95, 91, 86, 80], "metric": "Radiation shielding retention (%)"},
        "synth_route": [
            {"title": "Monomer Selection", "desc": "Select PMDA and 4,4'-oxydianiline (ODA) for polyimide.", "smiles": "O=C1OC(=O)c2cc3c(=O)oc(=O)c3cc21 + Nc1ccc(Oc2ccc(N)cc2)cc1"},
            {"title": "Thermal Imidization", "desc": "Stepwise thermal cure (100°C → 200°C → 350°C) to form rigid polyimide film.", "smiles": "O=C1c2cc3c(=O)n(c3cc2C(=O)N1c1ccc(Oc2ccc(N)cc2)cc1)"},
            {"title": "Auxetic Geometry Patterning", "desc": "Laser-cut re-entrant honeycomb pattern for negative Poisson's ratio.", "smiles": "C1=CC=CC=C1"},
            {"title": "Aluminized Mylar Integration", "desc": "Vacuum-deposit 100 nm Al on PET substrate. Bond via plasma activation.", "smiles": "O=C(OCC)c1ccc(C(=O)OCC)cc1"},
        ],
        "chat_explanation": [
            ("assistant", "The **lunar environment** poses a triple threat: extreme temperature swings (−180°C to +120°C), unfiltered UV/cosmic radiation, and a hyper-oxygenated atmosphere that makes most organics flammable."),
            ("assistant", "**Polyimide (Kapton-type)** was selected for its unmatched thermal stability — it retains mechanical properties from −269°C to +400°C with an LOI > 36% even in oxygen-enriched atmospheres."),
            ("assistant", "The **auxetic weave** is a unique design choice: when stretched, it expands laterally instead of contracting. This means micrometeorite impacts cause the fabric to *thicken* around the puncture, self-sealing the breach."),
            ("assistant", "⚠️ Synthetic accessibility is only **50/100** — the auxetic laser-cutting step requires specialized equipment. This is the primary bottleneck for mass production."),
        ],
    },
    "Deep Ocean Dive": {
        "blend": "UHMWPE / Graphene Oxide Laminate",
        "feature": "Exceptional compressive strength and hydrostatic pressure resistance with neutral buoyancy.",
        "constituents": {"UHMWPE (Dyneema/Spectra)": 85.0, "Carbon Fiber (PAN-based)": 15.0},
        "default_gsm": 320.0,
        "default_weave": "Twill Weave (2/1)",
        "scores": {"Thermal Protection (HTP)": 55, "Comfort & Breathability (THL)": 35, "Tensile Strength": 90, "Flexibility": 50, "Manufacturability": 65},
        "confidence": 85,
        "status": "⚠️ Active R&D",
        "sustainability": {"bio_based_pct": 0, "recyclable": "Partial", "co2_kg": 27.4, "water_L": 90.5},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 98, 94, 90, 85, 79], "metric": "Compressive strength retention (%)"},
        "synth_route": [
            {"title": "Catalytic Polymerization", "desc": "Ziegler-Natta catalysis of ethylene to UHMWPE (Mw > 3.5 × 10⁶ g/mol).", "smiles": "C=C"},
            {"title": "Gel Spinning", "desc": "Dissolve in decalin at 150°C, gel-spin and hot-draw at 120°C (draw ratio 80×).", "smiles": "CCCCCCCCCC"},
            {"title": "Graphene Oxide Coating", "desc": "Layer-by-layer electrostatic deposition of GO nanosheets onto fiber surface.", "smiles": "Oc1cc(O)c2c(c1)oc(=O)c2O"},
            {"title": "Pressure Suit Assembly", "desc": "Multi-axis braid over rigid joint elements. Seal with vulcanized neoprene gaskets.", "smiles": "CC(=C)C=C"},
        ],
        "chat_explanation": [
            ("assistant", "At **1000 m depth**, the suit must resist 100 atmospheres of hydrostatic pressure while allowing enough mobility for technical operations — a severe engineering constraint."),
            ("assistant", "**UHMWPE** was selected for its extraordinary specific strength (15× steel) *and* its density of just 0.97 g/cm³ — it actually floats. This is critical for achieving neutral buoyancy without excessive ballast."),
            ("assistant", "The **graphene oxide laminate** serves a dual purpose: it creates an impermeable barrier to water ingress, and it increases compressive stiffness by 35% through inter-layer load transfer."),
            ("assistant", "🔬 The tensile strength score of **90/100** reflects the gel-spun fiber's crystal orientation — over 95% crystallinity along the chain axis."),
        ],
    },
    "Chemical Hazmat": {
        "blend": "Activated Carbon Fiber (ACF) / Selectively Permeable PTFE Membrane",
        "feature": "Multi-spectrum chemical agent adsorption with one-way moisture vapor transport.",
        "constituents": {"PTFE (Teflon / Gore membrane)": 45.0, "Meta-aramid (Nomex)": 35.0, "Carbon Fiber (PAN-based)": 20.0},
        "default_gsm": 260.0,
        "default_weave": "Plain Weave (1/1)",
        "scores": {"Thermal Protection (HTP)": 40, "Comfort & Breathability (THL)": 60, "Tensile Strength": 55, "Flexibility": 75, "Manufacturability": 85},
        "confidence": 94,
        "status": "✅ Military Deployed",
        "sustainability": {"bio_based_pct": 0, "recyclable": "Partial", "co2_kg": 25.9, "water_L": 54.5},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 92, 83, 72, 58, 43], "metric": "Adsorption capacity retention (%)"},
        "synth_route": [
            {"title": "Precursor Fiber Preparation", "desc": "Stabilize PAN fibers in air at 250°C for 2h.", "smiles": "N#CC=C"},
            {"title": "Activation & Carbonization", "desc": "Carbonize at 800°C under N₂, then steam-activate at 900°C.", "smiles": "c1cccc2ccccc12"},
            {"title": "PTFE Membrane Lamination", "desc": "Expand PTFE film biaxially (400% stretch). Bond to ACF via dot adhesive.", "smiles": "FC(F)=C(F)F"},
            {"title": "Impregnation & QA Testing", "desc": "Impregnate ACF with ASZM-TEDA catalyst for CWA neutralization.", "smiles": "C1CN2CCN1CC2"},
        ],
        "chat_explanation": [
            ("assistant", "The CBRN scenario uniquely demands **selective permeability** — the suit must block chemical warfare agents (molecules ~0.5 nm) while allowing water vapor (~0.27 nm) to escape for wearer comfort."),
            ("assistant", "**Activated carbon fiber** with 1800 m²/g surface area provides massive adsorption capacity. Unlike granular carbon, ACF's micro-pore structure captures agents in < 5 milliseconds of contact."),
            ("assistant", "The **PTFE membrane** acts as the selectivity layer — its 0.2 μm pores are large enough for vapor but block all liquid and aerosol threats. This is the same Gore-Tex principle, military-hardened."),
            ("assistant", "✅ Synthetic accessibility score is **85/100** — this is one of the most manufacturable designs. All components are in active military supply chains, reducing adoption risk significantly."),
        ],
    },
    "Extreme Radiant Heat": {
        "blend": "Basalt Fiber / Silica Aerogel Quilted Panel with Zirconia Coating",
        "feature": "Extreme radiant-heat reflection and multi-layer ablative protection for operations near active lava flows.",
        "constituents": {"Basalt Fiber": 70.0, "Silica Aerogel Nanocomposite": 30.0},
        "default_gsm": 420.0,
        "default_weave": "Twill Weave (2/1)",
        "scores": {"Thermal Protection (HTP)": 98, "Comfort & Breathability (THL)": 15, "Tensile Strength": 70, "Flexibility": 30, "Manufacturability": 45},
        "confidence": 76,
        "status": "⚠️ Emerging Concept",
        "sustainability": {"bio_based_pct": 0, "recyclable": "Yes", "co2_kg": 9.05, "water_L": 18.9},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 96, 91, 85, 78, 70], "metric": "Thermal barrier efficiency (%)"},
        "synth_route": [
            {"title": "Basalt Fiber Extrusion", "desc": "Melt crushed basalt rock at 1450°C, extrude through Pt-Rh bushings.", "smiles": "O=[Si]=O"},
            {"title": "Aerogel Blanket Preparation", "desc": "Cast silica sol-gel into fiber blanket, age, and supercritical-dry.", "smiles": "CCO[Si](OCC)(OCC)OCC"},
            {"title": "Zirconia Plasma Spray", "desc": "Apply 250 μm YSZ thermal barrier coating via APS.", "smiles": "O=[Zr]=O"},
            {"title": "Quilted Panel Assembly", "desc": "Quilt aerogel between basalt face and aluminized fiberglass lining.", "smiles": "Final: 12 mm panel, mass 3.2 kg/m²"},
        ],
        "chat_explanation": [
            ("assistant", "At **1200°C radiant heat**, ordinary protective fabrics fail within seconds. This design uses three independent thermal defense mechanisms for redundancy."),
            ("assistant", "**Basalt fiber** is nature's fireproof material — it's literally made from volcanic rock. It retains 90% of its strength at 600°C and doesn't melt until 1450°C."),
            ("assistant", "The **YSZ zirconia coating** reflects >85% of infrared radiation and has the lowest thermal conductivity of any known ceramic (~2.0 W/mK). It's the same material used on jet turbine blades."),
            ("assistant", "⚠️ The major trade-off is **flexibility (30/100)** and **comfort (15/100)**. This is essentially a rigid panel system. Recommended for proximity suits with exoskeleton support."),
        ],
    },
    "Aerospace Re-entry": {
        "blend": "Carbon-Carbon (C/C) Composite / Phenolic-Impregnated Ablative Layer",
        "feature": "Ultra-high-temperature oxidation resistance with controlled ablation above 2500°C.",
        "constituents": {"Carbon Fiber (PAN-based)": 80.0, "Polyimide (Kapton/P84)": 20.0},
        "default_gsm": 450.0,
        "default_weave": "Plain Weave (1/1)",
        "scores": {"Thermal Protection (HTP)": 99, "Comfort & Breathability (THL)": 10, "Tensile Strength": 85, "Flexibility": 15, "Manufacturability": 30},
        "confidence": 71,
        "status": "✅ Aerospace Proven",
        "sustainability": {"bio_based_pct": 0, "recyclable": "No", "co2_kg": 35.6, "water_L": 70.0},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 100, 99, 98, 96, 94], "metric": "Structural integrity (%)"},
        "synth_route": [
            {"title": "Carbon Fiber Preform", "desc": "3D needle-punch PAN-based carbon fiber felt (density: 0.4 g/cm³).", "smiles": "N#CC=C"},
            {"title": "CVI Densification", "desc": "Chemical vapor infiltration with methane at 1100°C (6 cycles, ~800h total).", "smiles": "C"},
            {"title": "Phenolic Ablative Layer", "desc": "Impregnate silica-fiber cloth with SC-1008 phenolic resin. Autoclave cure.", "smiles": "Oc1ccccc1 + C=O"},
            {"title": "SiC Oxidation Barrier", "desc": "Pack cementation SiC coating at 1650°C.", "smiles": "[Si]#[C]"},
        ],
        "chat_explanation": [
            ("assistant", "**Mach 25+ re-entry** generates surface temperatures exceeding 2500°C — hotter than most materials' melting points. This is the most extreme thermal scenario in the database."),
            ("assistant", "**Carbon-carbon composites** are one of the few materials that actually get *stronger* as temperature increases (up to 2200°C). They were used on the Space Shuttle nose cone for this reason."),
            ("assistant", "The **phenolic ablative layer** is a sacrificial shield — it intentionally decomposes, and the endothermic decomposition reaction absorbs enormous amounts of heat, keeping the inner surface below 200°C."),
            ("assistant", "⚠️ Synthetic accessibility is only **30/100** — CVI densification alone takes 800+ hours per batch. This material is practical only for aerospace applications."),
        ],
    },
    "Milkweed": {
        "blend": "Milkweed Floss / Recycled Meta-aramid / Bio-PCM Microcapsule Composite",
        "feature": "Sustainable, bio-based thermal insulation with adaptive phase-change temperature regulation for sub-zero operations.",
        "constituents": {"Milkweed Floss (Asclepias)": 55.0, "Meta-aramid (Nomex)": 45.0},
        "default_gsm": 220.0,
        "default_weave": "Ripstop Grid",
        "scores": {"Thermal Protection (HTP)": 72, "Comfort & Breathability (THL)": 78, "Tensile Strength": 40, "Flexibility": 88, "Manufacturability": 82},
        "confidence": 74,
        "status": "🌱 Emerging Research",
        "sustainability": {"bio_based_pct": 55, "recyclable": "Yes", "co2_kg": 15.1, "water_L": 44.2},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 95, 88, 80, 71, 62], "metric": "Insulation retention (%)"},
        "synth_route": [
            {"title": "Milkweed Harvest & Cleaning", "desc": "Harvest Asclepias syriaca seed pods. Clean and card hollow floss fibers.", "smiles": "OCC1OC(O)C(O)C(O)C1O"},
            {"title": "Bio-PCM Encapsulation", "desc": "Interfacial polymerization of soy-wax PCM in microcapsules.", "smiles": "CCCCCCCCCCCCCCCCCC(=O)OC"},
            {"title": "Hybrid Batting Formation", "desc": "Needle-punch milkweed floss with meta-aramid staple fiber.", "smiles": "Nc1cccc(N)c1"},
            {"title": "Garment Assembly", "desc": "Laminate with recycled outer shell. No fluorocarbon chemicals.", "smiles": "Final: 220 g/m², 55% bio-based content"},
        ],
        "chat_explanation": [
            ("assistant", "**Milkweed floss** is one of the most promising emerging bio-fibers for insulation. Its hollow structure (80% lumen ratio) traps air more efficiently than synthetic alternatives — comparable to goose down at a fraction of the environmental cost."),
            ("assistant", "The **bio-PCM microcapsules** (soy wax, Tm = 37°C) provide *adaptive* thermal regulation — they absorb excess body heat as wax melts, then release it as wax solidifies."),
            ("assistant", "This is the **most sustainable design** in our database: 55% bio-based, recyclable, CO₂ footprint of just 15 kg/kg (vs. 31 kg/kg for pure aramid)."),
            ("assistant", "⚠️ Trade-off: tensile strength is **40/100** — milkweed is a short-staple fiber with low inherent strength. The meta-aramid component provides structure."),
        ],
    },
    "Wildland Firefighting": {
        "blend": "PBO (Zylon®) / Aluminized Aramid Shell with Moisture-Wicking Liner",
        "feature": "Maximum flashover protection with sustained comfort for 12+ hour shifts in active wildfire zones.",
        "constituents": {"PBO (Zylon)": 35.0, "Para-aramid (Kevlar/Twaron)": 45.0, "FR Viscose (Lenzing FR)": 20.0},
        "default_gsm": 290.0,
        "default_weave": "Ripstop Grid",
        "scores": {"Thermal Protection (HTP)": 92, "Comfort & Breathability (THL)": 55, "Tensile Strength": 88, "Flexibility": 65, "Manufacturability": 60},
        "confidence": 87,
        "status": "✅ Deployed (variants)",
        "sustainability": {"bio_based_pct": 17, "recyclable": "No", "co2_kg": 32.3, "water_L": 114.5},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 96, 90, 83, 75, 66], "metric": "HTP retention (%)"},
        "synth_route": [
            {"title": "PBO Fiber Synthesis", "desc": "Polycondensation of DAR and TPA in polyphosphoric acid (PPA) at 200°C.", "smiles": "Nc1cc(N)c(O)cc1O + O=C(O)c1ccc(C(=O)O)cc1"},
            {"title": "Blended Yarn Formation", "desc": "Co-spin PBO (35%) with para-aramid (45%) and FR viscose (20%).", "smiles": "Nc1ccc(N)cc1 + ClC(=O)c1ccc(C(=O)Cl)cc1"},
            {"title": "Aluminization", "desc": "Vacuum-deposit 80 nm aluminum on outer-shell face for radiant heat reflection.", "smiles": "[Al]"},
            {"title": "Multi-Layer Integration", "desc": "Assemble per NFPA 1971 standard. Seam-seal all critical joints.", "smiles": "Meets NFPA 1971 (2018 ed.) + CAL FIRE standards"},
        ],
        "chat_explanation": [
            ("assistant", "**PBO (Zylon)** has the highest LOI of any commercial fiber at **68%** — it simply will not burn in normal atmospheres. Its tensile strength of 5.8 GPa is also 60% higher than Kevlar."),
            ("assistant", "The **aluminum coating** on the outer shell reflects >85% of radiant heat — critical during wildfire flashovers where temperatures spike to 800°C+ for seconds at a time."),
            ("assistant", "I optimized for the **12-hour shift requirement**: comfort/breathability at **55/100** is significantly better than standard structural turnout gear."),
            ("assistant", "⚠️ Key limitation: PBO degrades under prolonged UV exposure. The para-aramid blend mitigates this but gear should be stored away from sunlight."),
        ],
    },
    "Industrial Flash Fire": {
        "blend": "FR Viscose / Nomex® IIIA Blend with Antistatic Grid",
        "feature": "Certified flash fire protection (ATPV > 12 cal/cm²) with inherent electrostatic dissipation for petrochemical facilities.",
        "constituents": {"FR Viscose (Lenzing FR)": 60.0, "Meta-aramid (Nomex)": 35.0, "Antistatic Grid (Belltron / Stainless steel)": 5.0},
        "default_gsm": 260.0,
        "default_weave": "Twill Weave (2/1)",
        "scores": {"Thermal Protection (HTP)": 70, "Comfort & Breathability (THL)": 75, "Tensile Strength": 50, "Flexibility": 85, "Manufacturability": 95},
        "confidence": 96,
        "status": "✅ Commercial",
        "sustainability": {"bio_based_pct": 51, "recyclable": "Yes", "co2_kg": 13.9, "water_L": 56.0},
        "aging": {"years": [0, 1, 2, 3, 4, 5], "retention_pct": [100, 98, 95, 91, 87, 82], "metric": "ATPV retention (%)"},
        "synth_route": [
            {"title": "FR Viscose Production", "desc": "Dissolve wood pulp cellulose in NaOH/CS₂. Add organophosphorus FR agent before spinning.", "smiles": "O=P(OCC)(OCC)c1ccccc1"},
            {"title": "Nomex IIIA Blending", "desc": "Intimate blend FR viscose (60%) + Nomex (35%) + Belltron antistatic (5%).", "smiles": "Nc1cccc(N)c1 + ClC(=O)c1cccc(C(=O)Cl)c1"},
            {"title": "Weave & Finish", "desc": "2/1 twill weave at 260 g/m². Sanforize and soft-finish.", "smiles": "ATPV = 12.4 cal/cm² per ASTM F1959"},
            {"title": "Garment Construction", "desc": "Cut and sew per IEC 61482-2 pattern. Heat-sealed seams.", "smiles": "Certified: EN ISO 11612, EN 1149-5, IEC 61482-2"},
        ],
        "chat_explanation": [
            ("assistant", "The **petrochemical industrial flash fire** scenario is NITRA's core testing domain. This design targets ATPV > 12 cal/cm² — the minimum for Category 2 arc flash and flash fire per ASTM F1959/NFPA 2112."),
            ("assistant", "**FR Viscose** is a cellulose-based (bio-derived) fiber treated with organophosphorus flame retardant during the viscose process itself — the FR is *built into* the fiber."),
            ("assistant", "The **Belltron antistatic grid** is critical for petrochemical environments where electrostatic discharge can ignite flammable vapors. Surface resistivity < 10⁹ Ω meets EN 1149-5 requirements."),
            ("assistant", "✅ This is the **highest accessibility score (95/100)** and **lowest cost** in the database. All materials are commercially available from Indian suppliers."),
        ],
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# COMMERCIAL BENCHMARK DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

COMMERCIAL_BENCHMARKS = [
    {"product": "Kevlar® 29", "manufacturer": "DuPont (USA)", "type": "Para-aramid fiber", "tensile_GPa": 2.9, "density_gcm3": 1.44, "LOI_pct": 29, "max_temp_C": 500},
    {"product": "Kevlar® 49", "manufacturer": "DuPont (USA)", "type": "Para-aramid (high modulus)", "tensile_GPa": 3.6, "density_gcm3": 1.44, "LOI_pct": 29, "max_temp_C": 500},
    {"product": "Nomex® IIIA", "manufacturer": "DuPont (USA)", "type": "Meta-aramid blend", "tensile_GPa": 0.6, "density_gcm3": 1.38, "LOI_pct": 30, "max_temp_C": 370},
    {"product": "Twaron® 2000", "manufacturer": "Teijin (Netherlands)", "type": "Para-aramid fiber", "tensile_GPa": 3.15, "density_gcm3": 1.44, "LOI_pct": 29, "max_temp_C": 500},
    {"product": "Dyneema® SK75", "manufacturer": "DSM (Netherlands)", "type": "UHMWPE gel-spun", "tensile_GPa": 3.5, "density_gcm3": 0.97, "LOI_pct": 17, "max_temp_C": 80},
    {"product": "Technora® T240", "manufacturer": "Teijin (Japan)", "type": "Co-poly-aramid", "tensile_GPa": 3.4, "density_gcm3": 1.39, "LOI_pct": 25, "max_temp_C": 500},
    {"product": "Zylon® AS", "manufacturer": "Toyobo (Japan)", "type": "PBO fiber", "tensile_GPa": 5.8, "density_gcm3": 1.56, "LOI_pct": 68, "max_temp_C": 650},
    {"product": "Pyrogel® XT-E", "manufacturer": "Aspen Aerogels (USA)", "type": "Silica aerogel blanket", "tensile_GPa": None, "density_gcm3": 0.20, "LOI_pct": None, "max_temp_C": 650},
    {"product": "JSLIST Suit", "manufacturer": "Gore / US Army", "type": "CBRN protective ensemble", "tensile_GPa": None, "density_gcm3": None, "LOI_pct": None, "max_temp_C": None},
    {"product": "Basofil® MCF", "manufacturer": "BASF (Germany)", "type": "Melamine fiber", "tensile_GPa": 0.28, "density_gcm3": 1.40, "LOI_pct": 32, "max_temp_C": 370},
]

# ═══════════════════════════════════════════════════════════════════════════════
# FIBER PROPERTY DATABASE
# ═══════════════════════════════════════════════════════════════════════════════

FIBER_DATABASE = [
    {"fiber": "Meta-aramid", "tensile_GPa": "0.5–0.7", "density_gcm3": 1.38, "LOI_pct": "28–32", "max_temp_C": 370, "commercial": "Nomex®, Conex®"},
    {"fiber": "Para-aramid", "tensile_GPa": "2.9–3.6", "density_gcm3": 1.44, "LOI_pct": "29", "max_temp_C": 500, "commercial": "Kevlar®, Twaron®"},
    {"fiber": "UHMWPE", "tensile_GPa": "3.5", "density_gcm3": 0.97, "LOI_pct": "17", "max_temp_C": 80, "commercial": "Dyneema®, Spectra®"},
    {"fiber": "PBO (Zylon)", "tensile_GPa": "5.8", "density_gcm3": 1.56, "LOI_pct": "68", "max_temp_C": 650, "commercial": "Zylon®"},
    {"fiber": "Basalt", "tensile_GPa": "3.0–4.8", "density_gcm3": 2.65, "LOI_pct": "N/A", "max_temp_C": 700, "commercial": "Mafic, Kamenny Vek"},
    {"fiber": "Carbon (T700)", "tensile_GPa": "4.9", "density_gcm3": 1.80, "LOI_pct": "N/A", "max_temp_C": 2000, "commercial": "Toray T700"},
    {"fiber": "Polyimide (PI)", "tensile_GPa": "0.1–0.2", "density_gcm3": 1.42, "LOI_pct": "36", "max_temp_C": 400, "commercial": "Kapton®, P84®"},
    {"fiber": "FR Viscose", "tensile_GPa": "0.2–0.3", "density_gcm3": 1.52, "LOI_pct": "28", "max_temp_C": 250, "commercial": "Lenzing FR®"},
    {"fiber": "Milkweed Floss", "tensile_GPa": "~0.03", "density_gcm3": 0.90, "LOI_pct": "—", "max_temp_C": 150, "commercial": "Natural (emerging)"},
    {"fiber": "Activated Carbon", "tensile_GPa": "0.3–0.5", "density_gcm3": 1.70, "LOI_pct": "55+", "max_temp_C": 500, "commercial": "Kynol®, Panox®"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# INDIAN DEFENCE & STANDARDS CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════

INDIAN_STANDARDS = [
    {"standard": "BIS IS 15742", "title": "Protective clothing — Heat & Flame", "relevance": "Indian standard for Nomex-type garments (firefighters, industry)"},
    {"standard": "BIS IS 14324", "title": "Ballistic resistance — Body armour", "relevance": "Indian ballistic vest testing standard"},
    {"standard": "JSS 9500-001", "title": "General standard — Military textiles", "relevance": "Governs Indian Army uniform procurement"},
    {"standard": "ISO 11612", "title": "Protective clothing — Heat & flame", "relevance": "International thermal protection standard"},
    {"standard": "ISO 13934-1", "title": "Tensile properties — Grab method", "relevance": "Fabric tensile testing standard"},
    {"standard": "EN ISO 9151", "title": "Heat transfer — Flame exposure (HTP)", "relevance": "HTP measurement methodology"},
    {"standard": "EN ISO 11092", "title": "Thermal & water-vapour resistance (THL)", "relevance": "THL comfort measurement via sweating guarded hotplate"},
    {"standard": "NFPA 1971", "title": "Protective ensembles — Structural firefighting", "relevance": "US/International firefighter turnout gear standard"},
    {"standard": "NFPA 2112", "title": "Flame-resistant garments — Flash fire", "relevance": "Industrial flash fire protection standard"},
    {"standard": "MIL-PRF-32629", "title": "JSLIST CBRN performance", "relevance": "US military CBRN suit specification"},
    {"standard": "NATO STANAG 4294", "title": "Ballistic protection levels", "relevance": "International ballistic standard, referenced in India"},
]
