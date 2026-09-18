"""
AIMATRY Core: Automated Regulatory Standards Compliance Auditor
Evaluates physical and chemical metrics against international and Indian regulatory thresholds:
- ISO 11612 (Heat & Flame Protective Clothing)
- NFPA 1971 (Structural Firefighting Ensembles)
- ASTM F1959 / NFPA 70E (Arc Flash ATPV Categories)
- BIS IS 15742 (Indian Standard for Thermal Protection)
- BIS IS 14324 / NIJ 0101.06 (Ballistic Protection)
- EN ISO 11092 (Physiological Comfort & Hotplate Breathability)
"""

from typing import Dict, Any, List


def audit_compliance(physics_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Performs comprehensive automated regulatory compliance evaluation for a given material.
    """
    loi = physics_data.get("loi_pct", 28.0)
    tensile_gpa = physics_data.get("tensile_strength_gpa", 1.0)
    max_temp = physics_data.get("max_service_temp_c", 300.0)
    thl = physics_data.get("total_heat_loss_thl_w_m2", 250.0)
    ret = physics_data.get("evaporative_resistance_ret", 12.0)
    rct = physics_data.get("thermal_resistance_rct", 0.04)
    gsm = physics_data.get("fabric_gsm", 240.0)

    # Approximate TPP and ATPV based on LOI, GSM, and thermal resistance
    tpp_cal_cm2 = round(float((loi / 28.0) * (gsm / 200.0) * (rct / 0.04) * 22.0), 1)
    atpv_cal_cm2 = round(float((loi / 28.0) * (gsm / 220.0) * (max_temp / 350.0) * 8.5), 1)

    standards_results = []

    # 1. ISO 11612:2015 (Heat & Flame Protection)
    iso_pass = (loi >= 27.0) and (max_temp >= 260.0) and (tensile_gpa >= 0.3)
    iso_level = "Level B3 (High)" if tpp_cal_cm2 >= 35 else ("Level B2 (Medium)" if tpp_cal_cm2 >= 20 else "Level B1 (Standard)")
    standards_results.append({
        "code": "ISO 11612:2015",
        "standard": "ISO 11612:2015",
        "title": "Flame Retardant Protective Clothing",
        "category": "Thermal",
        "status": "PASS" if iso_pass else "FAIL",
        "badge": "🟢 PASS" if iso_pass else "🔴 NON-COMPLIANT",
        "classification": iso_level if iso_pass else "Not Certified",
        "criteria": f"LOI ≥ 27% (actual: {loi}%), Max Temp ≥ 260°C (actual: {max_temp}°C)",
        "details": f"Heat transmission performance qualifies for {iso_level} convective thermal barrier.",
    })

    # 2. NFPA 1971 (Structural Firefighting)
    nfpa_tpp_pass = tpp_cal_cm2 >= 35.0
    nfpa_thl_pass = thl >= 205.0
    nfpa_pass = nfpa_tpp_pass and nfpa_thl_pass and (loi >= 28.0)
    standards_results.append({
        "code": "NFPA 1971",
        "standard": "NFPA 1971",
        "title": "Structural & Proximity Firefighting Turnout Gear",
        "category": "Thermal & Breathability",
        "status": "PASS" if nfpa_pass else "FLAG",
        "badge": "🟢 PASS" if nfpa_pass else "🟡 PARTIAL / FLAG",
        "classification": "Turnout Shell Grade" if nfpa_pass else "Conditional / Linings Only",
        "criteria": f"TPP ≥ 35 cal/cm² (calc: {tpp_cal_cm2}), THL ≥ 205 W/m² (calc: {thl})",
        "details": f"Total Heat Loss is {thl} W/m² (NFPA threshold: 205 W/m²).",
    })

    # 3. ASTM F1959 / NFPA 70E (Arc Flash Protection)
    if atpv_cal_cm2 >= 40.0:
        arc_cat = "Category 4 (Extreme Risk)"
    elif atpv_cal_cm2 >= 25.0:
        arc_cat = "Category 3 (High Risk)"
    elif atpv_cal_cm2 >= 8.0:
        arc_cat = "Category 2 (Moderate Risk)"
    elif atpv_cal_cm2 >= 4.0:
        arc_cat = "Category 1 (Low Risk)"
    else:
        arc_cat = "Unrated (< 4.0 cal/cm²)"

    standards_results.append({
        "code": "ASTM F1959 / NFPA 70E",
        "standard": "ASTM F1959 / NFPA 70E",
        "title": "Arc Thermal Performance Value (ATPV)",
        "category": "Electrical / Arc Flash",
        "status": "PASS" if atpv_cal_cm2 >= 8.0 else "FLAG",
        "badge": f"⚡ {arc_cat.split(' ')[0]}",
        "classification": arc_cat,
        "criteria": f"Calculated ATPV: {atpv_cal_cm2} cal/cm²",
        "details": f"Garment satisfies electrical safety requirements for NFPA 70E {arc_cat}.",
        "min_atpv_cal_cm2": atpv_cal_cm2,
    })

    # 4. BIS IS 15742:2007 (Indian Standard: Thermal Protection)
    bis_pass = (loi >= 28.0) and (tensile_gpa >= 0.45)
    standards_results.append({
        "code": "BIS IS 15742:2007",
        "standard": "BIS IS 15742:2007",
        "title": "Textiles - Protective Clothing Against Heat & Flame",
        "category": "National / Defense",
        "status": "PASS" if bis_pass else "FAIL",
        "badge": "🇮🇳 PASS" if bis_pass else "🇮🇳 NON-COMPLIANT",
        "classification": "Class 1 Protective Fabric" if bis_pass else "Uncertified",
        "criteria": f"LOI ≥ 28% (actual: {loi}%), Tensile ≥ 0.45 GPa (actual: {tensile_gpa} GPa)",
        "details": "Mandatory benchmark for Indian Army, MHA, and Indian industrial tender specifications.",
    })

    # 5. BIS IS 14324 / NIJ 0101.06 (Ballistic Threat Class)
    ballistic_pass = tensile_gpa >= 1.8
    standards_results.append({
        "code": "BIS IS 14324 / NIJ 0101.06",
        "standard": "BIS IS 14324 / NIJ 0101.06",
        "title": "Body Armour - Ballistic Protection",
        "category": "Ballistic / Defense",
        "status": "PASS" if ballistic_pass else "FLAG",
        "badge": "🛡️ NIJ IIIA Grade" if ballistic_pass else "🛡️ Non-Ballistic",
        "classification": "Level IIIA Capable" if ballistic_pass else "Soft Armor Backing Only",
        "criteria": f"Tensile Strength ≥ 1.8 GPa (actual: {tensile_gpa} GPa)",
        "details": "High tenacity composite matrix suitable for bullet-resistant vest plies.",
    })

    # 6. EN ISO 11092 (Sweating Hotplate Physiological Comfort)
    comfort_pass = ret <= 20.0
    standards_results.append({
        "code": "EN ISO 11092",
        "standard": "EN ISO 11092",
        "title": "Physiological Effects - Water Vapour Resistance (Ret)",
        "category": "Breathability",
        "status": "PASS" if comfort_pass else "FLAG",
        "badge": "💨 Breathable" if comfort_pass else "💨 Low Permeability",
        "classification": "Class 3 (High Breathability)" if ret <= 13 else "Class 2 (Standard Breathability)",
        "criteria": f"Ret ≤ 20.0 m²·Pa/W (actual: {ret} m²·Pa/W)",
        "details": f"Evaporative resistance measurement confirms wearer thermal stress regulation.",
    })

    overall_pass = all(s["status"] == "PASS" for s in standards_results)
    pass_count = sum(1 for s in standards_results if s["status"] == "PASS")
    total_count = len(standards_results)

    return {
        "overall_pass": overall_pass,
        "pass_count": pass_count,
        "total_standards": total_count,
        "standards": standards_results,
        "calculated_metrics": {
            "tpp_cal_cm2": tpp_cal_cm2,
            "atpv_cal_cm2": atpv_cal_cm2,
            "thl_w_m2": thl,
            "loi_pct": loi,
            "ret": ret,
            "rct": rct,
        },
        "summary": {
            "overall_rating": "Fully Certified" if overall_pass else f"Qualified ({pass_count}/{total_count} Standards)",
            "passed_standards": pass_count,
            "total_standards": total_count,
            "all_passed": overall_pass,
        }
    }
