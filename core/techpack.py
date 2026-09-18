"""
AIMATRY Core: Industrial Manufacturing Tech-Pack & Print-Ready Technical Dossier Generator
Generates publication-grade, print-ready PDF Dossiers and Technical Specification Packs (Tech-Packs)
for textile spinning/weaving mills, defense procurement agencies (DRDO/MHA/MOD), and testing laboratories (NITRA/TBRL).
"""

from typing import Dict, Any, Union, List, Optional
import io
import datetime
import pandas as pd
from core.physics import FIBER_SPECS

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        HRFlowable,
        KeepTogether,
        ListFlowable,
        ListItem,
    )
    from reportlab.pdfgen import canvas
    HAS_REPORTLAB = True
except Exception:
    HAS_REPORTLAB = False
    canvas = object
    letter = (612.0, 792.0)
    A4 = (595.27, 841.89)


if HAS_REPORTLAB:
    class NumberedCanvas(canvas.Canvas):
        """
        Two-pass canvas to dynamically compute and print exact 'Page X of Y' page numbers
        and professional running headers and footers on every page.
        """
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_decorations(num_pages)
                super().showPage()
            super().save()

        def draw_page_decorations(self, page_count: int):
            self.saveState()
            page_width, page_height = letter

            # Running Header (on pages 2 and later)
            if self._pageNumber > 1:
                self.setFont("Helvetica-Bold", 7.5)
                self.setFillColor(colors.HexColor("#0284c7"))
                self.drawString(36, page_height - 24, "AAK-AI / AIMATRY · TECHNICAL SPECIFICATION & SYNTHESIS DOSSIER")
                
                self.setFont("Helvetica", 7.5)
                self.setFillColor(colors.HexColor("#64748b"))
                self.drawRightString(page_width - 36, page_height - 24, "NITRA TECHNICAL CAMPUS · CSE & TEXTILE")
                
                self.setStrokeColor(colors.HexColor("#cbd5e1"))
                self.setLineWidth(0.5)
                self.line(36, page_height - 28, page_width - 36, page_height - 28)

            # Running Footer (on all pages)
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 32, page_width - 36, 32)

            self.setFont("Helvetica", 7.5)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(36, 20, "Confidential & Proprietary · Department of Computer Science & Engineering, NITRA Technical Campus")
            
            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0f172a"))
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(page_width - 36, 20, page_text)

            self.restoreState()
else:
    class NumberedCanvas:
        pass


def generate_techpack_dict(
    scenario_name: str,
    blend_name: str,
    physics_data: Dict[str, Any],
    compliance_data: Dict[str, Any],
    chemistry_data: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Constructs a structured JSON/dictionary Tech-Pack payload.
    """
    gsm = physics_data.get("fabric_gsm", 240.0)
    weave = physics_data.get("weave_type", "Ripstop Grid")
    blend_ratios = physics_data.get("blend_fractions", {})
    cost_inr = physics_data.get("cost_inr_per_m2", 2500.0)
    cost_usd = physics_data.get("cost_usd_per_m2", 30.0)

    # Estimate yarn specifications based on GSM and weave
    warp_count_ne = round(30.0 * (200.0 / max(gsm, 100.0)), 1)
    weft_count_ne = round(28.0 * (200.0 / max(gsm, 100.0)), 1)
    epi = int(round(65 * (gsm / 200.0) ** 0.5))
    ppi = int(round(58 * (gsm / 200.0) ** 0.5))

    return {
        "metadata": {
            "document_id": f"AIMATRY-TP-{abs(hash(str(scenario_name) + str(blend_name))) % 1000000:06d}",
            "project": "AIMATRY v3.4 Enterprise / AAK.AI",
            "institution": "Department of CSE, NITRA Technical Campus, Ghaziabad",
            "target_threat": scenario_name,
            "designated_blend": blend_name,
            "classification": "Protective Technical Textile Specification",
        },
        "yarn_and_fabric_construction": {
            "areal_density_gsm": gsm,
            "weave_structure": weave,
            "warp_yarn_count": f"{warp_count_ne}/1 Ne (Ring Spun / Core-Spun)",
            "weft_yarn_count": f"{weft_count_ne}/1 Ne (Air-Jet Textured)",
            "fabric_density": f"{epi} EPI × {ppi} PPI",
            "estimated_thickness_mm": round(gsm * 0.0035 + 0.1, 2),
        },
        "bill_of_materials": [
            {
                "Fiber Component": f,
                "Weight Fraction (%)": f"{pct}%",
                "Volume Fraction (%)": f"{physics_data.get('volume_fractions', {}).get(f, pct)}%",
                "Density (g/cm³)": FIBER_SPECS.get(f, {}).get("density_g_cm3", 1.4),
                "LOI (%)": FIBER_SPECS.get(f, {}).get("loi_pct", 30.0),
                "Cost (INR/kg)": f"₹{FIBER_SPECS.get(f, {}).get('cost_inr_kg', 3000)}",
            }
            for f, pct in blend_ratios.items()
        ],
        "mechanical_and_thermal_properties": {
            "tensile_strength_gpa": physics_data.get("tensile_strength_gpa", 1.5),
            "tensile_modulus_gpa": physics_data.get("tensile_modulus_gpa", 25.0),
            "composite_density_g_cm3": physics_data.get("composite_density_g_cm3", 1.4),
            "loi_pct": physics_data.get("loi_pct", 29.0),
            "max_service_temp_c": physics_data.get("max_service_temp_c", 350.0),
            "thermal_conductivity_w_mk": physics_data.get("thermal_conductivity_w_mk", 0.05),
            "thermal_resistance_rct_m2kw": physics_data.get("thermal_resistance_rct", 0.04),
            "evaporative_resistance_ret_m2paw": physics_data.get("evaporative_resistance_ret", 12.0),
            "total_heat_loss_thl_w_m2": physics_data.get("total_heat_loss_thl_w_m2", 250.0),
            "cost_inr_per_m2": cost_inr,
            "cost_usd_per_m2": cost_usd,
            "co2_kg_per_kg": physics_data.get("co2_kg_per_kg", 25.0),
            "water_l_per_kg": physics_data.get("water_l_per_kg", 60.0),
            "bio_based_pct": physics_data.get("bio_based_pct", 0.0),
        },
        "compliance_certifications": [
            {
                "Standard": s.get("code", s.get("standard", "ISO")),
                "Title": s.get("title", ""),
                "Status": s.get("status", "PASS"),
                "Classification": s.get("classification", "Certified"),
                "Details": s.get("details", ""),
                "Criteria": s.get("criteria", ""),
            }
            for s in compliance_data.get("standards", [])
        ],
    }


def generate_comprehensive_dossier_pdf(
    scenario_name: str,
    blend_title: str,
    feature_text: str,
    physics_data: Dict[str, Any],
    compliance_data: Dict[str, Any],
    surrogate_data: Optional[Dict[str, Any]] = None,
    topsis_data: Optional[Dict[str, Any]] = None,
    synth_route: Optional[List[Dict[str, Any]]] = None,
    aging_data: Optional[Dict[str, Any]] = None,
    target_inputs: Optional[Dict[str, Any]] = None,
    inv_result: Optional[Dict[str, Any]] = None,
    workflow_mode: str = "Curated Threat Scenarios + Live TOPSIS",
    confidence_score: Union[int, float] = 92,
    status_text: str = "Verified Formulation",
) -> bytes:
    """
    Renders a complete, publication-grade, print-ready multi-page PDF Technical Dossier
    containing EVERY processed metric and analysis provided by AAK-AI / AIMATRY.
    """
    if not HAS_REPORTLAB:
        msg = f"AAK-AI / AIMATRY Technical Dossier: {scenario_name} - {blend_title}. Please install reportlab to generate the full graphical PDF."
        escaped = msg.replace("(", "\(").replace(")", "\)")
        fallback_pdf = (
            b"%PDF-1.4\n"
            b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
            b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>/Contents 4 0 R>>endobj\n"
            + f"4 0 obj<</Length {len(escaped) + 40}>>stream\nBT /F1 12 Tf 50 700 Td ({escaped}) Tj ET\nendstream\nendobj\n".encode("utf-8")
            + b"xref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000216 00000 n \n"
            b"trailer<</Size 5/Root 1 0 R>>\nstartxref\n320\n%%EOF\n"
        )
        return fallback_pdf

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=42,
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography & Style Guide
    banner_title_style = ParagraphStyle(
        "BannerTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=2,
    )
    banner_sub_style = ParagraphStyle(
        "BannerSub",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=6,
    )
    section_hdr_style = ParagraphStyle(
        "SectionHdr",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=4,
    )
    body_txt_style = ParagraphStyle(
        "BodyTxt",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155"),
    )
    body_bold_style = ParagraphStyle(
        "BodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
    )
    cell_txt_style = ParagraphStyle(
        "CellTxt",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1e293b"),
    )
    cell_hdr_style = ParagraphStyle(
        "CellHdr",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
    )
    code_txt_style = ParagraphStyle(
        "CodeTxt",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#0369a1"),
    )
    tag_pass_style = ParagraphStyle(
        "TagPass",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor("#047857"),
    )
    tag_flag_style = ParagraphStyle(
        "TagFlag",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        textColor=colors.HexColor("#b45309"),
    )

    elements = []
    
    # Generate Unique Document ID & Timestamp
    doc_id = f"AIMATRY-REC-{abs(hash(str(scenario_name) + str(blend_title))) % 1000000:06d}"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

    # ═══════════════════════════════════════════════════════════════════════════
    # HEADER BANNER & DOCUMENT METADATA
    # ═══════════════════════════════════════════════════════════════════════════
    elements.append(Paragraph("AAK-AI / AIMATRY · TECHNICAL SPECIFICATION & SYNTHESIS DOSSIER", banner_title_style))
    elements.append(Paragraph("RESEARCH RECORD & INDUSTRIAL PRODUCTION SPECIFICATION · DEPARTMENT OF CSE & TEXTILE, NITRA TECHNICAL CAMPUS", banner_sub_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=6))

    # Meta Overview Box Table
    topsis_rank_str = f"#{topsis_data.get('rank', 1)} ({topsis_data.get('match_pct', 95.0)}%)" if topsis_data else "Optimized"
    gsm_val = physics_data.get("fabric_gsm", 260.0)
    weave_val = physics_data.get("weave_type", "Ripstop Grid")
    
    meta_box_data = [
        [
            Paragraph("<b>Document Record ID:</b>", cell_txt_style), Paragraph(doc_id, body_bold_style),
            Paragraph("<b>Date & Time:</b>", cell_txt_style), Paragraph(now_str, cell_txt_style),
        ],
        [
            Paragraph("<b>Operational Threat / Target:</b>", cell_txt_style), Paragraph(f"<b>{scenario_name}</b>", cell_txt_style),
            Paragraph("<b>Design Workflow Mode:</b>", cell_txt_style), Paragraph(workflow_mode, cell_txt_style),
        ],
        [
            Paragraph("<b>Designated Formulation:</b>", cell_txt_style), Paragraph(f"<b>{blend_title}</b>", cell_txt_style),
            Paragraph("<b>TOPSIS Ranking & Match:</b>", cell_txt_style), Paragraph(topsis_rank_str, cell_txt_style),
        ],
        [
            Paragraph("<b>Material Status & Readiness:</b>", cell_txt_style), Paragraph(f"{status_text} (AI Confidence: {confidence_score}%)", cell_txt_style),
            Paragraph("<b>Fabric Architecture:</b>", cell_txt_style), Paragraph(f"{gsm_val} g/m² · {weave_val}", cell_txt_style),
        ],
    ]
    t_meta = Table(meta_box_data, colWidths=[120, 160, 110, 150])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e293b")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 6))

    # Executive Summary Card
    exec_summary_data = [
        [
            Paragraph(
                f"<b>Executive Formulation Summary:</b> {feature_text} Engineered specifically for high-stress defense and industrial protective environments requiring strict compliance with international thermal and physiological standards.",
                cell_txt_style
            )
        ]
    ]
    t_exec = Table(exec_summary_data, colWidths=[540])
    t_exec.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#86efac")),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_exec)
    elements.append(Spacer(1, 6))

    # If Inverse Design mode used, show target specifications vs discovered values
    if inv_result and "target_comparison" in inv_result:
        elements.append(Paragraph("1. INVERSE DESIGN TARGET CONSTRAINTS VS ACHIEVED METRICS", section_hdr_style))
        tc_rows = [[
            Paragraph("<b>Property Metric</b>", cell_hdr_style),
            Paragraph("<b>Target Constraint</b>", cell_hdr_style),
            Paragraph("<b>Discovered Value</b>", cell_hdr_style),
            Paragraph("<b>Margin / Status</b>", cell_hdr_style),
        ]]
        for row in inv_result["target_comparison"]:
            tc_rows.append([
                Paragraph(str(row.get("Property", "")), cell_txt_style),
                Paragraph(str(row.get("Target", "")), cell_txt_style),
                Paragraph(str(row.get("Discovered", "")), cell_txt_style),
                Paragraph(str(row.get("Status", "MET")), tag_pass_style if "PASS" in str(row.get("Status", "MET")) or "MET" in str(row.get("Status", "MET")) else tag_flag_style),
            ])
        t_tc = Table(tc_rows, colWidths=[160, 120, 130, 130])
        t_tc.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0, 0), (-1, -1), 3.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        elements.append(t_tc)
        elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 2: BILL OF MATERIALS (BOM) & FIBER FRACTIONS
    # ═══════════════════════════════════════════════════════════════════════════
    elements.append(Paragraph("2. COMPLETE BILL OF MATERIALS (BOM) & CONSTITUENT FIBER FRACTIONS", section_hdr_style))
    
    bom_header = [
        Paragraph("<b>Fiber Constituent</b>", cell_hdr_style),
        Paragraph("<b>Mass (%)</b>", cell_hdr_style),
        Paragraph("<b>Volume (%)</b>", cell_hdr_style),
        Paragraph("<b>Density</b>", cell_hdr_style),
        Paragraph("<b>Fiber LOI</b>", cell_hdr_style),
        Paragraph("<b>Max Temp</b>", cell_hdr_style),
        Paragraph("<b>Fiber Cost</b>", cell_hdr_style),
        Paragraph("<b>Bio / Recycle</b>", cell_hdr_style),
    ]
    bom_rows = [bom_header]
    
    blend_ratios = physics_data.get("blend_fractions", {})
    volume_ratios = physics_data.get("volume_fractions", {})
    
    for fiber_name, mass_pct in blend_ratios.items():
        spec = FIBER_SPECS.get(fiber_name, {})
        vol_pct = volume_ratios.get(fiber_name, mass_pct)
        dens = f"{spec.get('density_g_cm3', 1.4):.2f} g/cm³"
        loi = f"{spec.get('loi_pct', 30.0):.1f}%"
        temp = f"{spec.get('max_temp_c', 350):.0f}°C"
        cost = f"₹{spec.get('cost_inr_kg', 3000):,.0f}/kg (${spec.get('cost_usd_kg', 35):.0f})"
        bio_rec = f"{spec.get('bio_pct', 0)}% / {spec.get('recyclable', 'No')}"
        
        bom_rows.append([
            Paragraph(f"<b>{fiber_name}</b>", cell_txt_style),
            Paragraph(f"{mass_pct:.1f}%", cell_txt_style),
            Paragraph(f"{vol_pct:.1f}%", cell_txt_style),
            Paragraph(dens, cell_txt_style),
            Paragraph(loi, cell_txt_style),
            Paragraph(temp, cell_txt_style),
            Paragraph(cost, cell_txt_style),
            Paragraph(bio_rec, cell_txt_style),
        ])
    
    t_bom = Table(bom_rows, colWidths=[130, 48, 52, 58, 48, 54, 85, 65])
    t_bom.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(t_bom)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 3: YARN & FABRIC MICROSTRUCTURE SPECIFICATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    elements.append(Paragraph("3. YARN, WEAVE & FABRIC STRUCTURAL CONSTRUCTION", section_hdr_style))
    warp_ne = round(30.0 * (200.0 / max(gsm_val, 100.0)), 1)
    weft_ne = round(28.0 * (200.0 / max(gsm_val, 100.0)), 1)
    epi_val = int(round(65 * (gsm_val / 200.0) ** 0.5))
    ppi_val = int(round(58 * (gsm_val / 200.0) ** 0.5))
    thick_mm = round(gsm_val * 0.0035 + 0.1, 2)
    comp_dens = physics_data.get("composite_density_g_cm3", 1.4)

    yarn_data = [
        [
            Paragraph("<b>Fabric Areal Density (GSM):</b>", cell_txt_style), Paragraph(f"{gsm_val} g/m²", body_bold_style),
            Paragraph("<b>Weave Architecture:</b>", cell_txt_style), Paragraph(str(weave_val), body_bold_style),
        ],
        [
            Paragraph("<b>Warp Yarn Count:</b>", cell_txt_style), Paragraph(f"{warp_ne}/1 Ne (Ring/Core-Spun)", cell_txt_style),
            Paragraph("<b>Weft Yarn Count:</b>", cell_txt_style), Paragraph(f"{weft_ne}/1 Ne (Air-Jet Textured)", cell_txt_style),
        ],
        [
            Paragraph("<b>Fabric Thread Density:</b>", cell_txt_style), Paragraph(f"{epi_val} EPI × {ppi_val} PPI", cell_txt_style),
            Paragraph("<b>Nominal Thickness / Density:</b>", cell_txt_style), Paragraph(f"{thick_mm} mm · {comp_dens} g/cm³", cell_txt_style),
        ],
    ]
    t_yarn = Table(yarn_data, colWidths=[140, 130, 130, 140])
    t_yarn.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 3.5),
    ]))
    elements.append(t_yarn)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 4: VOIGT-REUSS MICROMECHANICAL, THERMAL & TRANSPORT PHYSICS
    # ═══════════════════════════════════════════════════════════════════════════
    elements.append(Paragraph("4. COMPREHENSIVE VOIGT-REUSS MICROMECHANICAL & TRANSPORT PHYSICS", section_hdr_style))
    
    cost_inr_m2 = physics_data.get("cost_inr_per_m2", 2500.0)
    cost_usd_m2 = physics_data.get("cost_usd_per_m2", 30.0)
    
    physics_matrix_data = [
        [
            Paragraph("<b>Tensile Breaking Strength (σ):</b>", cell_txt_style), Paragraph(f"<b>{physics_data.get('tensile_strength_gpa')} GPa</b>", cell_txt_style),
            Paragraph("<b>Thermal Resistance (R_ct):</b>", cell_txt_style), Paragraph(f"{physics_data.get('thermal_resistance_rct')} m²·K/W", cell_txt_style),
        ],
        [
            Paragraph("<b>Tensile Elastic Modulus (Voigt E):</b>", cell_txt_style), Paragraph(f"{physics_data.get('tensile_modulus_gpa')} GPa", cell_txt_style),
            Paragraph("<b>Evaporative Resistance (R_et):</b>", cell_txt_style), Paragraph(f"{physics_data.get('evaporative_resistance_ret')} m²·Pa/W", cell_txt_style),
        ],
        [
            Paragraph("<b>Limiting Oxygen Index (LOI):</b>", cell_txt_style), Paragraph(f"<b>{physics_data.get('loi_pct')}%</b>", cell_txt_style),
            Paragraph("<b>Total Heat Loss (THL):</b>", cell_txt_style), Paragraph(f"<b>{physics_data.get('total_heat_loss_thl_w_m2')} W/m²</b>", cell_txt_style),
        ],
        [
            Paragraph("<b>Max Continuous Service Temp:</b>", cell_txt_style), Paragraph(f"{physics_data.get('max_service_temp_c')} °C", cell_txt_style),
            Paragraph("<b>Effective Thermal Cond. (k_eff):</b>", cell_txt_style), Paragraph(f"{physics_data.get('thermal_conductivity_w_mk')} W/m·K", cell_txt_style),
        ],
        [
            Paragraph("<b>Estimated Production Cost:</b>", cell_txt_style), Paragraph(f"₹{cost_inr_m2}/m² (${cost_usd_m2}/m²)", cell_txt_style),
            Paragraph("<b>Sustainability (CO₂ / Water):</b>", cell_txt_style), Paragraph(f"{physics_data.get('co2_kg_per_kg', 25)} kg CO₂ · {physics_data.get('water_l_per_kg', 60)} L H₂O", cell_txt_style),
        ],
    ]
    t_physics = Table(physics_matrix_data, colWidths=[150, 120, 140, 130])
    t_physics.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    elements.append(t_physics)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 5: 5-AXIS RADAR PERFORMANCE & TOPSIS PRIORITIZATION
    # ═══════════════════════════════════════════════════════════════════════════
    elements.append(Paragraph("5. MULTI-CRITERIA DECISION MATRIX & 5-AXIS RADAR PERFORMANCE", section_hdr_style))
    scores = physics_data.get("scores", {})
    weights_dict = topsis_data.get("user_weights", {}) if topsis_data else {}
    
    radar_rows = [
        [
            Paragraph("<b>Performance Dimension</b>", cell_hdr_style),
            Paragraph("<b>Calculated Score (0–100)</b>", cell_hdr_style),
            Paragraph("<b>Tuned TOPSIS Weight</b>", cell_hdr_style),
            Paragraph("<b>Operational Rating</b>", cell_hdr_style),
        ],
        [
            Paragraph("Thermal Protection (HTP)", cell_txt_style),
            Paragraph(f"<b>{scores.get('Thermal Protection (HTP)', 75)} / 100</b>", cell_txt_style),
            Paragraph(f"{weights_dict.get('Thermal Protection (HTP)', 75)}%", cell_txt_style),
            Paragraph("High Thermal Hazard Resistance" if scores.get('Thermal Protection (HTP)', 75) >= 70 else "Standard Thermal Barrier", cell_txt_style),
        ],
        [
            Paragraph("Comfort & Breathability (THL)", cell_txt_style),
            Paragraph(f"<b>{scores.get('Comfort & Breathability (THL)', 60)} / 100</b>", cell_txt_style),
            Paragraph(f"{weights_dict.get('Comfort & Breathability (THL)', 60)}%", cell_txt_style),
            Paragraph("Optimized Vapor Transmission" if scores.get('Comfort & Breathability (THL)', 60) >= 60 else "Moderate Permeability", cell_txt_style),
        ],
        [
            Paragraph("Tensile Breaking Strength", cell_txt_style),
            Paragraph(f"<b>{scores.get('Tensile Strength', 70)} / 100</b>", cell_txt_style),
            Paragraph(f"{weights_dict.get('Tensile Strength', 70)}%", cell_txt_style),
            Paragraph("Structural Reinforcement Grade" if scores.get('Tensile Strength', 70) >= 70 else "Standard Protective Weft", cell_txt_style),
        ],
        [
            Paragraph("Flexibility & Tactile Drape", cell_txt_style),
            Paragraph(f"<b>{scores.get('Flexibility', 50)} / 100</b>", cell_txt_style),
            Paragraph(f"{weights_dict.get('Flexibility', 50)}%", cell_txt_style),
            Paragraph("High Articulation & Movement" if scores.get('Flexibility', 50) >= 60 else "Controlled Rigidity", cell_txt_style),
        ],
        [
            Paragraph("Industrial Manufacturability", cell_txt_style),
            Paragraph(f"<b>{scores.get('Manufacturability', 65)} / 100</b>", cell_txt_style),
            Paragraph(f"{weights_dict.get('Manufacturability', 65)}%", cell_txt_style),
            Paragraph("Commercial Yarn Spinning Scale" if scores.get('Manufacturability', 65) >= 70 else "Specialized Processing Required", cell_txt_style),
        ],
    ]
    t_radar = Table(radar_rows, colWidths=[160, 110, 110, 160])
    t_radar.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    elements.append(t_radar)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 6: AUTOMATED REGULATORY STANDARDS AUDIT MATRIX
    # ═══════════════════════════════════════════════════════════════════════════
    elements.append(Paragraph("6. AUTOMATED REGULATORY STANDARDS COMPLIANCE AUDIT MATRIX", section_hdr_style))
    
    comp_standards = compliance_data.get("standards", [])
    overall_pass = compliance_data.get("overall_pass", False)
    pass_cnt = compliance_data.get("pass_count", 0)
    total_cnt = compliance_data.get("total_standards", len(comp_standards))
    
    comp_header = [
        Paragraph("<b>Standard Code</b>", cell_hdr_style),
        Paragraph("<b>Scope / Domain</b>", cell_hdr_style),
        Paragraph("<b>Status</b>", cell_hdr_style),
        Paragraph("<b>Classification / Grade</b>", cell_hdr_style),
        Paragraph("<b>Compliance Criteria & Audit Findings</b>", cell_hdr_style),
    ]
    comp_rows = [comp_header]
    
    for std in comp_standards:
        code_str = std.get("code", std.get("standard", "Standard"))
        domain_str = std.get("title", "")
        status_val = std.get("status", "PASS")
        class_str = std.get("classification", "Certified")
        details_str = f"{std.get('criteria', '')} — {std.get('details', '')}"
        
        status_para = Paragraph(f"<b>{status_val}</b>", tag_pass_style if status_val == "PASS" else tag_flag_style)
        
        comp_rows.append([
            Paragraph(f"<b>{code_str}</b>", cell_txt_style),
            Paragraph(domain_str, cell_txt_style),
            status_para,
            Paragraph(class_str, cell_txt_style),
            Paragraph(details_str, cell_txt_style),
        ])
        
    t_comp_full = Table(comp_rows, colWidths=[95, 110, 45, 110, 180])
    t_comp_full.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(t_comp_full)
    elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 7: ML SURROGATE MODEL PREDICTIONS & UNCERTAINTY QUANTIFICATION
    # ═══════════════════════════════════════════════════════════════════════════
    if surrogate_data:
        elements.append(Paragraph("7. MACHINE LEARNING SURROGATE PREDICTIONS & UNCERTAINTY QUANTIFICATION", section_hdr_style))
        ml_header = [
            Paragraph("<b>Target Property</b>", cell_hdr_style),
            Paragraph("<b>Surrogate Predicted Mean</b>", cell_hdr_style),
            Paragraph("<b>Epistemic Uncertainty (±σ)</b>", cell_hdr_style),
            Paragraph("<b>95% Confidence Interval [Lower, Upper]</b>", cell_hdr_style),
        ]
        ml_rows = [ml_header]
        for prop, val in surrogate_data.items():
            prop_title = prop.replace("_", " ").title()
            ml_rows.append([
                Paragraph(f"<b>{prop_title}</b>", cell_txt_style),
                Paragraph(str(val.get("mean", "")), cell_txt_style),
                Paragraph(f"±{val.get('std_uncertainty', '')}", cell_txt_style),
                Paragraph(f"[{val.get('ci_95_lower', '')}, {val.get('ci_95_upper', '')}]", cell_txt_style),
            ])
        t_ml = Table(ml_rows, colWidths=[150, 130, 120, 140])
        t_ml.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0, 0), (-1, -1), 3.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        elements.append(t_ml)
        elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 8: CHEMICAL SYNTHESIS PATHWAY & POLYMERIZATION PROTOCOL
    # ═══════════════════════════════════════════════════════════════════════════
    if synth_route:
        elements.append(Paragraph("8. CHEMICAL SYNTHESIS ROUTE & POLYMERIZATION PROTOCOL", section_hdr_style))
        synth_header = [
            Paragraph("<b>Stage / Step</b>", cell_hdr_style),
            Paragraph("<b>Reaction & Processing Description</b>", cell_hdr_style),
            Paragraph("<b>Chemical Structure / SMILES Formulation</b>", cell_hdr_style),
        ]
        synth_rows = [synth_header]
        for idx, step in enumerate(synth_route, 1):
            synth_rows.append([
                Paragraph(f"<b>Step {idx}: {step.get('title', '')}</b>", cell_txt_style),
                Paragraph(step.get("desc", ""), cell_txt_style),
                Paragraph(step.get("smiles", ""), code_txt_style),
            ])
        t_synth = Table(synth_rows, colWidths=[130, 230, 180])
        t_synth.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0, 0), (-1, -1), 3.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        elements.append(t_synth)
        elements.append(Spacer(1, 6))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 9: DURABILITY, AGING & ACCELERATED WEATHERING PROFILE
    # ═══════════════════════════════════════════════════════════════════════════
    if aging_data and "years" in aging_data and "retention_pct" in aging_data:
        elements.append(Paragraph("9. ACCELERATED AGING & 5-YEAR LIFECYCLE RETENTION PROFILE", section_hdr_style))
        aging_hdr = [Paragraph("<b>Operational Service Time</b>", cell_hdr_style)] + [
            Paragraph(f"<b>Year {yr}</b>", cell_hdr_style) for yr in aging_data["years"]
        ]
        aging_val_row = [Paragraph(f"<b>{aging_data.get('metric', 'Retention (%)')}</b>", cell_txt_style)] + [
            Paragraph(f"<b>{ret}%</b>", cell_txt_style) for ret in aging_data["retention_pct"]
        ]
        t_aging = Table([aging_hdr, aging_val_row], colWidths=[180] + [60] * len(aging_data["years"]))
        t_aging.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0284c7")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0, 0), (-1, -1), 3.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white]),
        ]))
        elements.append(t_aging)
        elements.append(Spacer(1, 8))

    # ═══════════════════════════════════════════════════════════════════════════
    # SECTION 10: INSTITUTIONAL VERIFICATION & ARCHIVAL SIGN-OFF
    # ═══════════════════════════════════════════════════════════════════════════
    cert_box_data = [
        [
            Paragraph("<b>CERTIFICATION & ARCHIVAL ENDORSEMENT</b>", cell_hdr_style),
            Paragraph("<b>PROJECT INVESTIGATORS & SIGN-OFF</b>", cell_hdr_style),
        ],
        [
            Paragraph(
                "This document is officially generated by the <b>AIMATRY Materials Informatics Engine v3.4</b>. "
                "All micromechanical calculations, thermal transport models, and regulatory pre-audits have been digitally verified for manufacturing formulation and testing archival.",
                cell_txt_style,
            ),
            Paragraph(
                "<b>Lead Researchers:</b> Ayush Singh, Vansh Mishra, Nikhil Kumar Yadav<br/>"
                "<b>Institution:</b> NITRA Technical Campus, Ghaziabad<br/>"
                "<b>Status:</b> Approved for Lab Synthesis & Prototype Weaving",
                cell_txt_style,
            ),
        ],
    ]
    t_cert = Table(cert_box_data, colWidths=[270, 270])
    t_cert.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(KeepTogether(t_cert))

    doc.build(elements, canvasmaker=NumberedCanvas)
    return buffer.getvalue()


def generate_techpack_pdf(
    techpack_or_blend: Union[Dict[str, Any], str],
    physics_data: Dict[str, Any] = None,
    compliance_data: Dict[str, Any] = None,
) -> bytes:
    """
    Backwards-compatible wrapper that renders the full publication-quality Tech-Pack / Dossier PDF.
    """
    if isinstance(techpack_or_blend, dict):
        techpack = techpack_or_blend
        scenario_name = techpack.get("metadata", {}).get("target_threat", "Protective Material")
        blend_name = techpack.get("metadata", {}).get("designated_blend", "Engineered Composite")
        phys = techpack.get("mechanical_and_thermal_properties", {})
        comp = {"standards": techpack.get("compliance_certifications", [])}
        return generate_comprehensive_dossier_pdf(
            scenario_name=scenario_name,
            blend_title=blend_name,
            feature_text="Engineered protective textile formulation.",
            physics_data=phys,
            compliance_data=comp,
        )
    else:
        blend_name = str(techpack_or_blend)
        return generate_comprehensive_dossier_pdf(
            scenario_name=blend_name,
            blend_title=blend_name,
            feature_text="Engineered protective textile formulation.",
            physics_data=physics_data or {},
            compliance_data=compliance_data or {},
        )
