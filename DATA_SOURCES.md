# AIMATRY — Data Sources & Scientific References
## AAK-AI | NITRA Technical Campus

> **Purpose**: This document provides a complete traceability matrix for every data point hardcoded in AIMATRY's `data.py`. All fiber properties, synthesis routes, layer stack designs, and standards references are sourced from manufacturer datasheets, peer-reviewed publications, government specifications, and established research institutions.

---

# 📋 TABLE OF CONTENTS

1. [Fiber Property Sources (FIBER_DATABASE)](#1-fiber-property-sources)
2. [Commercial Benchmark Sources (COMMERCIAL_BENCHMARKS)](#2-commercial-benchmark-sources)
3. [Scenario-Specific Data Sources (SCENARIOS)](#3-scenario-specific-data-sources)
4. [Standards & Compliance Sources (INDIAN_STANDARDS)](#4-standards--compliance-sources)
5. [Synthesis Route Sources](#5-synthesis-route-sources)
6. [Sustainability Data Sources](#6-sustainability-data-sources)
7. [Peer-Reviewed Journal References](#7-peer-reviewed-journal-references)

---

# 1. FIBER PROPERTY SOURCES

## 1.1 Meta-Aramid (Nomex®, Conex®)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 0.5–0.7 GPa | DuPont™ Nomex® Technical Guide |
| Density | 1.38 g/cm³ | DuPont™ Nomex® Technical Guide |
| LOI | 28–32% | DuPont™ Nomex® Technical Guide |
| Max Temp | 370°C | DuPont™ Nomex® Technical Guide |

**Primary Source**: DuPont de Nemours, Inc.  
**Document**: *DuPont™ Nomex® Fiber Technical Guide* (Publication H-52720)  
**URL**: https://www.dupont.com/brands/nomex.html  
**Lab**: DuPont Experimental Station, Wilmington, Delaware, USA  

**Academic Verification**: Hearle, J.W.S. (2001). *High-Performance Fibres*. Woodhead Publishing, Cambridge, UK. Chapter 3: Aramid Fibres. ISBN: 978-1-85573-539-7

---

## 1.2 Para-Aramid (Kevlar®, Twaron®)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 2.9–3.6 GPa | DuPont™ Kevlar® TDS / Teijin Twaron® TDS |
| Density | 1.44 g/cm³ | DuPont™ Kevlar® Technical Guide |
| LOI | 29% | DuPont™ Kevlar® Technical Guide |
| Max Temp | 500°C (decomposition) | DuPont™ Kevlar® Technical Guide |

**Primary Sources**:
- **DuPont**: *Kevlar® Aramid Fiber Technical Guide* (H-77848)  
  URL: https://www.dupont.com/brands/kevlar.html
- **Teijin Aramid**: *Twaron® Product Data Sheets*  
  URL: https://www.teijinaramid.com/products/twaron/  
  **Lab**: Teijin Aramid BV, Arnhem, Netherlands

**Academic Verification**:
- Yang, H.H. (1993). *Kevlar Aramid Fiber*. John Wiley & Sons. ISBN: 978-0-471-93765-4
- Cheng, M. et al. (2005). "Mechanical Properties of Kevlar KM2 Single Fiber." *Journal of Engineering Materials and Technology*, 127(2), 197–203. DOI: 10.1115/1.1857937  
  **Lab**: Purdue University, School of Aeronautics & Astronautics, West Lafayette, Indiana, USA

---

## 1.3 UHMWPE (Dyneema®, Spectra®)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 3.5 GPa | DSM Dyneema® SK75 Product Data Sheet |
| Density | 0.97 g/cm³ | DSM Dyneema® SK75 Product Data Sheet |
| LOI | 17% | Published literature (Hearle 2001) |
| Max Temp | 80°C (softening) | DSM Dyneema® Technical Guide |

**Primary Source**: DSM Dyneema BV (now Avient Corporation)  
**Document**: *Dyneema® SK75 Fiber Product Data Sheet*  
**URL**: https://www.dsm.com/dyneema  
**Lab**: DSM Research, Geleen, Netherlands  

**Academic Verification**:
- Prevorsek, D.C. et al. (1994). "Ultra-high-modulus polyethylene fibres." *Polymer*, 35(18), 3891–3894. DOI: 10.1016/0032-3861(94)90273-9

---

## 1.4 PBO — Zylon® (Poly(p-phenylene-2,6-benzobisoxazole))
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 5.8 GPa | Toyobo Co., Ltd. Zylon® Technical Information |
| Density | 1.56 g/cm³ | Toyobo Zylon® TDS |
| LOI | 68% | Toyobo Zylon® TDS |
| Max Temp | 650°C (decomposition) | Toyobo Zylon® TDS |

**Primary Source**: Toyobo Co., Ltd., Osaka, Japan  
**Document**: *Zylon® (PBO Fiber) Technical Information*  
**URL**: https://www.toyobo-global.com/seihin/dn/zylon/  
**Lab**: Toyobo Research Center, Otsu, Shiga, Japan  

**Academic Verification**:
- Kitagawa, T. et al. (1998). "Molecular packing in poly(p-phenylenebenzobisoxazole) crystal." *Journal of Polymer Science Part B: Polymer Physics*, 36(1), 39–48. DOI: 10.1002/(SICI)1099-0488
- Bourbigot, S. & Flambard, X. (2002). "Heat resistance and flammability of high performance fibres: A review." *Fire and Materials*, 26(4-5), 155–168. DOI: 10.1002/fam.799  
  **Lab**: ENSCL / CNRS, Université de Lille, France

---

## 1.5 Basalt Fiber
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 3.0–4.8 GPa | Mafic SA / Published literature |
| Density | 2.65 g/cm³ | Published literature |
| Max Temp | 700°C (operational) | Mafic / Kamenny Vek datasheets |

**Primary Sources**:
- **Mafic SA**: https://mafic.com/  (Dublin, Ireland / Kells, Ireland plant)
- **Kamenny Vek**: http://www.basfiber.com/  (Moscow, Russia)

**Academic Verification**:
- Fiore, V. et al. (2015). "A review on basalt fibre and its composites." *Composites Part B: Engineering*, 74, 74–94. DOI: 10.1016/j.compositesb.2014.12.034  
  **Lab**: Università degli Studi di Palermo, Department of Civil Engineering, Italy
- Deak, T. & Czigany, T. (2009). "Chemical composition and mechanical properties of basalt and glass fibers: A comparison." *Textile Research Journal*, 79(7), 645–651. DOI: 10.1177/0040517508095597  
  **Lab**: Budapest University of Technology and Economics, Hungary

---

## 1.6 Carbon Fiber (T700)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 4.9 GPa | Toray Industries T700S Data Sheet |
| Density | 1.80 g/cm³ | Toray T700S Data Sheet |
| Max Temp | 2000°C (inert atmosphere) | Published literature |

**Primary Source**: Toray Industries, Inc., Tokyo, Japan  
**Document**: *TORAYCA® T700S Technical Data Sheet No. CFA-005*  
**URL**: https://www.toray.com/products/advanced-composites/  
**Lab**: Toray Composite Materials Research Labs, Nagoya, Japan

---

## 1.7 Polyimide (Kapton®, P84®)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 0.1–0.2 GPa (film) | DuPont Kapton® Technical Data Sheet |
| Density | 1.42 g/cm³ | DuPont Kapton® TDS |
| LOI | 36% | Published literature |
| Max Temp | 400°C | DuPont Kapton® TDS |

**Primary Source**: DuPont de Nemours, Inc.  
**Document**: *Kapton® Polyimide Film Technical Data Sheet* (H-38479-3)  
**URL**: https://www.dupont.com/brands/kapton.html  

**Additional Source for P84®**: Evonik Industries AG, Essen, Germany  
**URL**: https://www.evonik.com/en/products/search/pages/p84-fiber

---

## 1.8 FR Viscose (Lenzing FR®)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 0.2–0.3 GPa | Lenzing AG Technical Documentation |
| Density | 1.52 g/cm³ | Lenzing AG |
| LOI | 28% | Lenzing FR® Product Data Sheet |
| Max Temp | 250°C | Lenzing AG |

**Primary Source**: Lenzing AG, Lenzing, Austria  
**Document**: *Lenzing™ FR Fiber Product Information*  
**URL**: https://www.lenzing.com/products/viscose-fibers  
**Lab**: Lenzing Innovation Center, Lenzing, Austria

---

## 1.9 Milkweed Floss (Asclepias syriaca)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | ~0.03 GPa | Published research |
| Density | 0.90 g/cm³ | Published research |
| Lumen ratio | ~80% | Published research |

**Academic Sources**:
- Crews, P.C. et al. (1991). "The Properties and Potential of Milkweed Floss." *Textile Research Journal*, 61(4), 203–211. DOI: 10.1177/004051759106100403  
  **Lab**: University of Nebraska–Lincoln, Department of Textiles, Clothing & Design, USA
- Sakthivel, J.C. et al. (2005). "Studies on Milkweed Fibres." *Indian Journal of Fibre & Textile Research*, 30, 61–66.  
  **Lab**: Anna University, Department of Textile Technology, Chennai, India
- Karthik, T. & Murugan, R. (2016). "Milkweed — A Potential Sustainable Natural Fibre Crop." *Advances in Natural Polymers*. Springer. DOI: 10.1007/978-3-642-20940-6  
  **Lab**: PSG College of Technology, Coimbatore, India

---

## 1.10 Activated Carbon Fiber (Kynol®, Panox®)
| Property | Value in AIMATRY | Source |
|----------|-----------------|--------|
| Tensile Strength | 0.3–0.5 GPa | Published literature |
| Density | 1.70 g/cm³ | Published literature |
| LOI | 55%+ | Published literature |
| Surface area (SBET) | 1800 m²/g | Published research |

**Primary Sources**:
- **Kynol®**: Kynol Europa GmbH, Hamburg, Germany  
  URL: https://www.kfrp.com/
- **SGL Carbon**: https://www.sglcarbon.com/

**Academic Verification**:
- Suzuki, M. (1994). "Activated carbon fiber: Fundamentals and applications." *Carbon*, 32(4), 577–586. DOI: 10.1016/0008-6223(94)90075-2  
  **Lab**: University of Tokyo, Institute of Industrial Science, Japan
- Economy, J. & Lin, R.Y. (1976). "Adsorption characteristics of activated carbon fibers." *Applied Polymer Symposia*, 29, 199–211.  
  **Lab**: University of Illinois at Urbana-Champaign, USA

---

# 2. COMMERCIAL BENCHMARK SOURCES

| Product | Manufacturer | Data Source |
|---------|-------------|-------------|
| **Kevlar® 29** | DuPont (USA) | DuPont™ Kevlar® Technical Guide (H-77848). URL: https://www.dupont.com/brands/kevlar.html |
| **Kevlar® 49** | DuPont (USA) | DuPont™ Kevlar® Technical Guide (H-77848). URL: https://www.dupont.com/brands/kevlar.html |
| **Nomex® IIIA** | DuPont (USA) | DuPont™ Nomex® Fiber Technical Guide (H-52720). URL: https://www.dupont.com/brands/nomex.html |
| **Twaron® 2000** | Teijin Aramid (Netherlands) | Teijin Aramid Product Data Sheet. URL: https://www.teijinaramid.com/products/twaron/ |
| **Dyneema® SK75** | DSM / Avient (Netherlands) | Dyneema® SK75 Product Data Sheet. URL: https://www.dsm.com/dyneema |
| **Technora® T240** | Teijin (Japan) | Teijin Technora® Technical Handbook. URL: https://www.teijin.com/products/advanced-fibers/technora/ |
| **Zylon® AS** | Toyobo (Japan) | Toyobo Zylon® Technical Information. URL: https://www.toyobo-global.com/seihin/dn/zylon/ |
| **Pyrogel® XT-E** | Aspen Aerogels (USA) | Aspen Aerogels Pyrogel® XT-E Data Sheet. URL: https://www.aerogel.com/products/pyrogel/ |
| **JSLIST Suit** | W.L. Gore / US Army | MIL-PRF-32629 performance specification. US Army NSRDEC, Natick, MA |
| **Basofil® MCF** | BASF (Germany) | BASF Basofil® Melamine Fiber TDS. URL: https://www.basf.com |

---

# 3. SCENARIO-SPECIFIC DATA SOURCES

## 3.1 Arctic Combat — Aerogel Insulation
- **Silica aerogel λ = 0.015–0.018 W/mK**: Aspen Aerogels, Inc. *Pyrogel® XT-E Technical Data Sheet*. URL: https://www.aerogel.com/
- **Academic**: Baetens, R. et al. (2011). "Aerogel insulation for building applications: A state-of-the-art review." *Energy and Buildings*, 43(4), 761–769. DOI: 10.1016/j.enbuild.2010.12.012  
  **Lab**: KU Leuven, Department of Civil Engineering, Belgium

## 3.2 High Ballistic Threat — STF (Shear Thickening Fluid)
- **STF colloidal silica (φ=0.61) in PEG-200**: Lee, Y.S. et al. (2003). "The ballistic impact characteristics of Kevlar woven fabrics impregnated with a colloidal shear thickening fluid." *Journal of Materials Science*, 38(13), 2825–2833. DOI: 10.1023/A:1024424200221  
  **Lab**: University of Delaware, Center for Composite Materials, Newark, Delaware, USA  
  **PI**: Prof. Norman J. Wagner
- **Additional**: Decker, M.J. et al. (2007). "Stab resistance of shear thickening fluid (STF)-treated fabrics." *Composites Science and Technology*, 67(3–4), 565–578. DOI: 10.1016/j.compscitech.2006.08.007  
  **Lab**: University of Delaware, USA

## 3.3 Lunar Environment — Polyimide / Auxetic / Aluminized Mylar
- **Kapton® PI (PMDA-ODA) Tg > 360°C, operational −269°C to +400°C**: DuPont Kapton® TDS (H-38479-3). URL: https://www.dupont.com/brands/kapton.html
- **NASA EMU Spacesuit layup**: Harris, G.L. (2001). *The Origins and Technology of the Advanced Extravehicular Space Suit*. AAS History Series, Vol. 24. American Astronautical Society. ISBN: 978-0877034414  
  **Lab**: NASA Johnson Space Center, Houston, Texas, USA
- **ILC Dover spacesuit construction**: ILC Dover LP, Frederica, Delaware, USA. URL: https://www.ilcdover.com/
- **Auxetic materials (negative Poisson's ratio ν = −0.7)**: Alderson, A. & Alderson, K.L. (2007). "Auxetic materials." *Proceedings of the Institution of Mechanical Engineers, Part G*, 221(4), 565–575. DOI: 10.1243/09544100JAERO185  
  **Lab**: University of Bolton, Institute for Materials Research and Innovation, UK

## 3.4 Deep-Sea — UHMWPE / Graphene Oxide
- **UHMWPE gel spinning (draw ratio 80×)**: Smith, P. & Lemstra, P.J. (1980). "Ultra-high-strength polyethylene filaments by solution spinning/drawing." *Journal of Materials Science*, 15(2), 505–514. DOI: 10.1007/BF00551705  
  **Lab**: DSM Research / Eindhoven University of Technology, Netherlands
- **Graphene oxide barrier (+35% stiffness)**: Hu, K. et al. (2014). "Graphene-polymer nanocomposites for structural and functional applications." *Progress in Polymer Science*, 39(11), 1934–1972. DOI: 10.1016/j.progpolymsci.2014.03.001  
  **Lab**: Columbia University, Department of Mechanical Engineering, New York, USA

## 3.5 CBRN — Activated Carbon / PTFE Membrane
- **ACF SBET = 1800 m²/g, micropore vol = 0.65 cm³/g**: Suzuki, M. (1994) — see Section 1.10 above
- **ePTFE membrane (0.2 μm pore)**: W.L. Gore & Associates, Inc. URL: https://www.gore.com/  
  **Lab**: Gore Creative Technologies, Elkton, Maryland, USA
- **ASZM-TEDA impregnant for CWA neutralization**: US Army DEVCOM Chemical Biological Center (formerly Edgewood Chemical Biological Center), Aberdeen Proving Ground, Maryland, USA  
  **Specification**: MIL-PRF-32629 (JSLIST performance)  
  URL: https://www.cbd.mil/

## 3.6 Volcanic Proximity — Basalt / Zirconia
- **YSZ (ZrO₂-8%Y₂O₃) Tm = 2715°C, IR reflection >85%**: Clarke, D.R. & Levi, C.G. (2003). "Materials design for the next generation thermal barrier coatings." *Annual Review of Materials Research*, 33, 383–417. DOI: 10.1146/annurev.matsci.33.011403.113718  
  **Lab**: University of California Santa Barbara, Materials Department, USA
- **Basalt fiber retains 90% strength at 600°C**: Fiore et al. (2015) — see Section 1.5 above

## 3.7 Hypersonic Re-entry — Carbon-Carbon / PICA Ablative
- **PICA (Phenolic Impregnated Carbon Ablator) ablation rate 0.05 mm/s at 1.5 MW/m²**: Tran, H.K. et al. (1997). *Phenolic Impregnated Carbon Ablators (PICA) as Thermal Protection Systems for Discovery Missions*. NASA Technical Memorandum 110440.  
  **Lab**: NASA Ames Research Center, Moffett Field, California, USA  
  URL: https://ntrs.nasa.gov/citations/19970017394
- **Carbon-carbon composite CVI densification (density 1.75 g/cm³)**: Savage, G. (1993). *Carbon-Carbon Composites*. Chapman & Hall, London. ISBN: 978-0-412-36150-6
- **Space Shuttle nose cone C/C usage**: NASA Marshall Space Flight Center, Huntsville, Alabama  
  URL: https://www.nasa.gov/centers/marshall/

## 3.8 Sustainable Arctic — Milkweed / PCM
- **Milkweed floss (80% lumen ratio, 20–30 μm diameter)**: Crews et al. (1991); Sakthivel et al. (2005) — see Section 1.9
- **Bio-PCM microcapsules (soy wax, ΔH = 180 J/g, Tm = 37°C)**: Sarier, N. & Onder, E. (2012). "Organic phase change materials and their textile applications: An overview." *Thermochimica Acta*, 540, 7–60. DOI: 10.1016/j.tca.2012.04.013  
  **Lab**: Istanbul Technical University, Department of Textile Engineering, Turkey

## 3.9 Wildfire Firefighter — PBO / Aluminized Aramid
- **PBO LOI = 68%, σ = 5.8 GPa**: Toyobo Zylon® TDS — see Section 1.4
- **NFPA 1971 (2018 ed.) requirements**: National Fire Protection Association, Quincy, Massachusetts, USA  
  URL: https://www.nfpa.org/codes-and-standards/nfpa-1971-standard-development/1971
- **MVTR > 1200 g/m²/24h for comfort liners**: Gibson, P.W. (2000). "Effect of temperature on water vapor transport through polymer membrane laminates." *Polymer Testing*, 19(6), 673–691. DOI: 10.1016/S0142-9418(99)00040-6  
  **Lab**: US Army Natick Soldier Research Center, Natick, Massachusetts, USA

## 3.10 Industrial Flash Fire — FR Viscose / Nomex IIIA
- **ATPV = 12.4 cal/cm² per ASTM F1959**: ASTM International Standard F1959/F1959M  
  URL: https://www.astm.org/f1959_f1959m-14.html
- **EN 1149-5 antistatic requirements (surface resistivity < 10⁹ Ω)**: European Committee for Standardization (CEN)  
  URL: https://standards.cen.eu/
- **FR Viscose + Nomex IIIA blend composition**: DuPont™ Nomex® IIIA Technical Guide; Lenzing™ FR Product Information

---

# 4. STANDARDS & COMPLIANCE SOURCES

All standards referenced in AIMATRY are published by their respective standards organizations:

| Standard | Publishing Body | URL |
|----------|----------------|-----|
| **BIS IS 15742** | Bureau of Indian Standards, New Delhi | https://www.bis.gov.in/ |
| **BIS IS 14324** | Bureau of Indian Standards, New Delhi | https://www.bis.gov.in/ |
| **JSS 9500-001** | Directorate of Standardisation (DoS), Ministry of Defence, India | https://ddpdoo.gov.in/ |
| **ISO 11612** | International Organization for Standardization, Geneva | https://www.iso.org/standard/57456.html |
| **ISO 13934-1** | International Organization for Standardization | https://www.iso.org/standard/69853.html |
| **EN ISO 9151** | European Committee for Standardization (CEN) | https://standards.cen.eu/ |
| **EN ISO 11092** | European Committee for Standardization (CEN) | https://standards.cen.eu/ |
| **NFPA 1971** | National Fire Protection Association, USA | https://www.nfpa.org/ |
| **NFPA 2112** | National Fire Protection Association, USA | https://www.nfpa.org/ |
| **MIL-PRF-32629** | US Department of Defense | https://quicksearch.dla.mil/ |
| **NATO STANAG 4294** | NATO Standardization Agency, Brussels | https://nso.nato.int/ |

---

# 5. SYNTHESIS ROUTE SOURCES

| Synthesis Process | Source |
|-------------------|--------|
| **Meta-aramid interfacial polycondensation** | Morgan, P.W. (1965). *Condensation Polymers: By Interfacial and Solution Methods*. Interscience/Wiley. **Lab**: DuPont Central Research, Wilmington, USA |
| **Para-aramid (PPTA) in NMP/CaCl₂** | Kwolek, S.L. et al. (1977). US Patent 4,035,465. DuPont |
| **UHMWPE gel spinning** | Smith, P. & Lemstra, P.J. (1980). *J. Mater. Sci.*, 15, 505–514. **Lab**: Eindhoven UT, Netherlands |
| **PBO synthesis in PPA** | Wolfe, J.F. & Arnold, F.E. (1981). "Rigid-rod polymers." *Macromolecules*, 14(4), 909–915. **Lab**: US Air Force Materials Lab, Wright-Patterson AFB, Ohio |
| **CVI carbon-carbon densification** | Savage, G. (1993). *Carbon-Carbon Composites*. Chapman & Hall |
| **PICA ablative fabrication** | Tran, H.K. et al. (1997). NASA TM-110440. **Lab**: NASA Ames Research Center |
| **PCM microencapsulation (melamine-formaldehyde)** | Zhang, X.X. et al. (2004). "Crystallization and prevention of supercooling of microencapsulated n-alkanes." *J. Colloid Interface Sci.*, 281(2), 299–306. **Lab**: Tianjin Polytechnic University, China |
| **Basalt fiber extrusion at 1450°C** | Mafic SA technical documentation. URL: https://mafic.com/ |

---

# 6. SUSTAINABILITY DATA SOURCES

Sustainability metrics (CO₂ kg/kg, water L/kg, bio-based %) are derived from:

- **Higg Materials Sustainability Index (MSI)**: Sustainable Apparel Coalition  
  URL: https://apparelcoalition.org/the-higg-index/
- **ecoinvent Database v3.9**: Centre for Life Cycle Inventories, Zurich, Switzerland  
  URL: https://ecoinvent.org/
- **GaBi Software / Sphera**: Sphera Solutions GmbH, Leinfelden-Echterdingen, Germany  
  URL: https://sphera.com/
- **Lenzing Sustainability Report 2023**: Bio-based content data for FR Viscose  
  URL: https://www.lenzing.com/sustainability/

---

# 7. PEER-REVIEWED JOURNAL REFERENCES (CONSOLIDATED)

1. Hearle, J.W.S. (2001). *High-Performance Fibres*. Woodhead Publishing. ISBN: 978-1-85573-539-7
2. Bourbigot, S. & Flambard, X. (2002). "Heat resistance and flammability of high performance fibres." *Fire and Materials*, 26(4-5), 155–168. DOI: 10.1002/fam.799
3. Lee, Y.S. et al. (2003). "Ballistic impact characteristics of Kevlar woven fabrics impregnated with a colloidal shear thickening fluid." *J. Mater. Sci.*, 38, 2825–2833. DOI: 10.1023/A:1024424200221
4. Cheng, M. et al. (2005). "Mechanical Properties of Kevlar KM2 Single Fiber." *J. Eng. Mater. Technol.*, 127(2), 197–203. DOI: 10.1115/1.1857937
5. Fiore, V. et al. (2015). "A review on basalt fibre and its composites." *Composites Part B*, 74, 74–94. DOI: 10.1016/j.compositesb.2014.12.034
6. Clarke, D.R. & Levi, C.G. (2003). "Materials design for next generation thermal barrier coatings." *Annu. Rev. Mater. Res.*, 33, 383–417. DOI: 10.1146/annurev.matsci.33.011403.113718
7. Crews, P.C. et al. (1991). "Properties and Potential of Milkweed Floss." *Textile Research Journal*, 61(4), 203–211. DOI: 10.1177/004051759106100403
8. Sakthivel, J.C. et al. (2005). "Studies on Milkweed Fibres." *Indian J. Fibre & Textile Res.*, 30, 61–66.
9. Suzuki, M. (1994). "Activated carbon fiber: Fundamentals and applications." *Carbon*, 32(4), 577–586. DOI: 10.1016/0008-6223(94)90075-2
10. Tran, H.K. et al. (1997). *PICA as TPS for Discovery Missions*. NASA TM-110440.
11. Smith, P. & Lemstra, P.J. (1980). "Ultra-high-strength polyethylene filaments." *J. Mater. Sci.*, 15(2), 505–514. DOI: 10.1007/BF00551705
12. Sarier, N. & Onder, E. (2012). "Organic phase change materials and their textile applications." *Thermochimica Acta*, 540, 7–60. DOI: 10.1016/j.tca.2012.04.013
13. Gibson, P.W. (2000). "Effect of temperature on water vapor transport through polymer membrane laminates." *Polym. Test.*, 19(6), 673–691. DOI: 10.1016/S0142-9418(99)00040-6
14. Alderson, A. & Alderson, K.L. (2007). "Auxetic materials." *Proc. IMechE Part G*, 221(4), 565–575. DOI: 10.1243/09544100JAERO185
15. Hu, K. et al. (2014). "Graphene-polymer nanocomposites." *Prog. Polym. Sci.*, 39(11), 1934–1972. DOI: 10.1016/j.progpolymsci.2014.03.001

---

# 📌 RESEARCH INSTITUTIONS REFERENCED

| Institution | Country | Data Used For |
|-------------|---------|---------------|
| **DuPont Experimental Station** | Wilmington, DE, USA | Kevlar®, Nomex®, Kapton® fiber/film properties |
| **Teijin Aramid BV** | Arnhem, Netherlands | Twaron®, Technora® fiber properties |
| **Toyobo Research Center** | Otsu, Shiga, Japan | Zylon® (PBO) fiber properties |
| **DSM Research** | Geleen, Netherlands | Dyneema® UHMWPE properties |
| **Toray Composite Materials Lab** | Nagoya, Japan | T700 carbon fiber properties |
| **Aspen Aerogels, Inc.** | Northborough, MA, USA | Pyrogel® aerogel data |
| **Lenzing Innovation Center** | Lenzing, Austria | FR Viscose fiber data |
| **NASA Ames Research Center** | Moffett Field, CA, USA | PICA ablative data |
| **NASA Johnson Space Center** | Houston, TX, USA | Spacesuit material layup |
| **University of Delaware** | Newark, DE, USA | Shear Thickening Fluid (STF) research |
| **Purdue University** | West Lafayette, IN, USA | Kevlar KM2 single-fiber testing |
| **University of Nebraska–Lincoln** | Lincoln, NE, USA | Milkweed floss fiber properties |
| **Anna University** | Chennai, India | Milkweed fiber studies |
| **PSG College of Technology** | Coimbatore, India | Milkweed sustainable fiber research |
| **Istanbul Technical University** | Istanbul, Turkey | PCM microcapsule textile applications |
| **Università di Palermo** | Palermo, Italy | Basalt fiber composites review |
| **Budapest University of Technology** | Budapest, Hungary | Basalt fiber mechanical properties |
| **KU Leuven** | Leuven, Belgium | Aerogel insulation for buildings |
| **UCSB Materials Department** | Santa Barbara, CA, USA | YSZ thermal barrier coatings |
| **Columbia University** | New York, NY, USA | Graphene-polymer nanocomposites |
| **University of Tokyo** | Tokyo, Japan | Activated carbon fiber fundamentals |
| **UIUC** | Urbana-Champaign, IL, USA | Activated carbon fiber adsorption |
| **Université de Lille / CNRS** | Lille, France | High-performance fiber flammability |
| **Eindhoven University of Technology** | Eindhoven, Netherlands | UHMWPE gel spinning process |
| **US Army Natick Soldier Center** | Natick, MA, USA | Moisture vapor transport, CBRN suits |
| **US Army DEVCOM CBC** | Aberdeen, MD, USA | ASZM-TEDA CWA neutralization |
| **W.L. Gore & Associates** | Elkton, MD, USA | ePTFE membrane technology |

---

# 👥 AAK-AI TEAM

## Team Members

| Name | Role | Contact |
|------|------|---------|
| **Ayush Singh** | Team Lead & Developer | 📞 9672626676 |
| **Vansh Mishra** | Core Member | 📞 6399324181 |
| **Nikhil Kumar Yadav** | Core Member | 📞 9140504848 |

## Under the Guidance of

| Name | Designation | Department |
|------|------------|------------|
| | | |

> **Institute**: NITRA Technical Campus (Academic Wing of NITRA), Ghaziabad, Uttar Pradesh, India

---

*Document prepared by AAK-AI, NITRA Technical Campus.*  
*All data points are traceable to manufacturer datasheets (primary) or peer-reviewed publications (secondary).*  
*Last updated: April 2026*
