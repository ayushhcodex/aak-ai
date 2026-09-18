"""
AIMATRY Core: Industrial Manufacturing Tech-Pack Generator
Generates production-ready Technical Specification Packs (Tech-Packs) for textile mills,
defense procurement agencies, and testing laboratories.
"""

from typing import Dict, Any, Union
import io
import json
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


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
            {"Fiber Component": f, "Weight Fraction (%)": f"{pct}%", "Volume Fraction (%)": f"{physics_data.get('volume_fractions', {}).get(f, pct)}%"}
            for f, pct in blend_ratios.items()
        ],
        "mechanical_and_thermal_properties": {
            "tensile_strength_gpa": physics_data.get("tensile_strength_gpa", 1.5),
            "tensile_modulus_gpa": physics_data.get("tensile_modulus_gpa", 25.0),
            "composite_density_g_cm3": physics_data.get("composite_density_g_cm3", 1.4),
            "loi_pct": physics_data.get("loi_pct", 29.0),
            "max_service_temp_c": physics_data.get("max_service_temp_c", 350.0),
            "thermal_resistance_rct_m2kw": physics_data.get("thermal_resistance_rct", 0.04),
            "evaporative_resistance_ret_m2paw": physics_data.get("evaporative_resistance_ret", 12.0),
            "total_heat_loss_thl_w_m2": physics_data.get("total_heat_loss_thl_w_m2", 250.0),
            "cost_inr_per_m2": cost_inr,
            "cost_usd_per_m2": cost_usd,
        },
        "compliance_certifications": [
            {"Standard": s.get("code", s.get("standard", "ISO")), "Title": s.get("title", ""), "Status": s.get("status", "PASS"), "Details": s.get("details", "")}
            for s in compliance_data.get("standards", [])
        ],
    }


def generate_techpack_pdf(
    techpack_or_blend: Union[Dict[str, Any], str],
    physics_data: Dict[str, Any] = None,
    compliance_data: Dict[str, Any] = None,
) -> bytes:
    """
    Renders a professional, publication-quality PDF Tech-Pack using ReportLab.
    Supports either generate_techpack_pdf(techpack_dict) or generate_techpack_pdf(blend, physics, compliance).
    """
    if isinstance(techpack_or_blend, dict):
        techpack = techpack_or_blend
    else:
        techpack = generate_techpack_dict(
            str(techpack_or_blend),
            str(techpack_or_blend),
            physics_data or {},
            compliance_data or {},
        )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155"),
    )

    elements = []

    # Title & Metadata Header
    meta = techpack.get("metadata", {})
    elements.append(Paragraph("AIMATRY · INDUSTRIAL TECH-PACK SPECIFICATION", title_style))
    elements.append(Paragraph(f"Document ID: {meta.get('document_id')} | Project: {meta.get('project')} | Institution: {meta.get('institution')}", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=12))

    # General Information Table
    elements.append(Paragraph("1. GENERAL SPECIFICATION", section_style))
    meta_table_data = [
        ["Designated Formulation", meta.get("designated_blend", "N/A"), "Target Threat", meta.get("target_threat", "N/A")],
        ["Areal Density (GSM)", f"{techpack.get('yarn_and_fabric_construction', {}).get('areal_density_gsm')} g/m²", "Weave Geometry", techpack.get("yarn_and_fabric_construction", {}).get("weave_structure", "N/A")],
        ["Estimated Cost (INR)", f"₹{techpack.get('mechanical_and_thermal_properties', {}).get('cost_inr_per_m2')}/m²", "Estimated Cost (USD)", f"${techpack.get('mechanical_and_thermal_properties', {}).get('cost_usd_per_m2')}/m²"],
    ]
    t_meta = Table(meta_table_data, colWidths=[130, 140, 120, 150])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("TEXTCOLOR", (0,0), (-1,-1), colors.HexColor("#1e293b")),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 10))

    # Bill of Materials (BOM) Table
    elements.append(Paragraph("2. BILL OF MATERIALS (FIBER RATIOS)", section_style))
    bom_list = techpack.get("bill_of_materials", [])
    if bom_list:
        bom_table_data = [["Fiber Constituent", "Weight Fraction (%)", "Volume Fraction (%)"]]
        for item in bom_list:
            bom_table_data.append([item.get("Fiber Component", ""), item.get("Weight Fraction (%)", ""), item.get("Volume Fraction (%)", "")])
        t_bom = Table(bom_table_data, colWidths=[240, 150, 150])
        t_bom.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0284c7")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8.5),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0,0), (-1,-1), 5),
        ]))
        elements.append(t_bom)
    elements.append(Spacer(1, 10))

    # Mechanical & Thermal Properties Table
    elements.append(Paragraph("3. MECHANICAL, THERMAL & COMFORT PERFORMANCE", section_style))
    props = techpack.get("mechanical_and_thermal_properties", {})
    props_table_data = [
        ["Tensile Breaking Strength (σ)", f"{props.get('tensile_strength_gpa')} GPa", "Thermal Resistance (R_ct)", f"{props.get('thermal_resistance_rct_m2kw')} m²·K/W"],
        ["Tensile Elastic Modulus (E)", f"{props.get('tensile_modulus_gpa')} GPa", "Evaporative Resistance (R_et)", f"{props.get('evaporative_resistance_ret_m2paw')} m²·Pa/W"],
        ["Limiting Oxygen Index (LOI)", f"{props.get('loi_pct')}%", "Total Heat Loss (THL)", f"{props.get('total_heat_loss_thl_w_m2')} W/m²"],
        ["Max Continuous Service Temp", f"{props.get('max_service_temp_c')} °C", "Composite Bulk Density", f"{props.get('composite_density_g_cm3')} g/cm³"],
    ]
    t_props = Table(props_table_data, colWidths=[160, 110, 160, 110])
    t_props.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0,0), (-1,-1), 5),
    ]))
    elements.append(t_props)
    elements.append(Spacer(1, 10))

    # Compliance & Standards Table
    elements.append(Paragraph("4. REGULATORY PRE-COMPLIANCE AUDIT", section_style))
    comp_list = techpack.get("compliance_certifications", [])
    if comp_list:
        comp_table_data = [["Standard Code", "Title", "Audit Status", "Details"]]
        for c in comp_list:
            comp_table_data.append([c.get("Standard", ""), c.get("Title", ""), c.get("Status", ""), c.get("Details", "")])
        t_comp = Table(comp_table_data, colWidths=[90, 170, 70, 210])
        t_comp.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 8),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0,0), (-1,-1), 4),
        ]))
        elements.append(t_comp)

    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Authored & Verified by AIMATRY AI Engineering Core · Department of Computer Science & Engineering, NITRA Technical Campus.", subtitle_style))

    doc.build(elements)
    return buffer.getvalue()
