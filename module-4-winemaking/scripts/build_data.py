"""
Build CSV data files for Module 4 — Winemaking Technology.

Sources: Bucher Vaslin, Letina, Enartis, Lallemand, Laffort, AFIR, PMC/MDPI,
Wine Business Analytics, Freedom of the Press, North Slope Chillers.
See module-4-winemaking.md for full citations.

Run: python3 scripts/build_data.py
Output: ../data/*.csv
"""

import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def write_csv(filename, headers, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"  Written: {filename} ({len(rows)} rows)")


# ── 1. Winery zone space requirements ────────────────────────────────────────
write_csv(
    "winery_zone_space.csv",
    ["zone", "area_min_m2", "area_max_m2", "notes"],
    [
        ["Reception / crush pad",       40,  60,  "Covered canopy; forklift access essential"],
        ["Press room",                  25,  40,  "Press body + juice trough + hose routing"],
        ["Fermentation room",           80, 150,  "Dominant zone; glycol-jacketed tanks require aisle clearance"],
        ["Aging / storage cellar",      60, 100,  "Tank storage; barrel program if any"],
        ["Bottling area",               20,  40,  "Can share with storage when not in use"],
        ["Laboratory",                   8,  15,  "Bench + water + ventilation"],
        ["Cleaning / utility room",     10,  20,  "CIP, chemical storage, compressed air"],
        ["Cold stabilisation room",      0,  30,  "Integrated into ferm room if jackets reach -5°C"],
    ],
)

# ── 2. Shed conversion cost breakdown ────────────────────────────────────────
write_csv(
    "shed_conversion_costs.csv",
    ["work_category", "cost_eur_m2_min", "cost_eur_m2_max", "notes"],
    [
        ["Structural shell / insulation",           50, 150, "Roof upgrade, wall insulation for temp control"],
        ["Polyurethane mortar flooring",            40,  80, "Including existing concrete prep; food-safe standard"],
        ["Internal walls / zone partitioning",      30,  60, "Fermentation vs. storage vs. lab"],
        ["Electrical (3-phase, IP-rated wet zones)", 15,  30, "Including earthing"],
        ["Plumbing (hot/cold water + trench drains)", 20,  40, "ACO-type stainless trench drains"],
        ["Ventilation (CO2 extraction)",            10,  25, "Critical safety item for CO2 during fermentation"],
        ["ANSVSA-compliant finishes",               10,  20, "Ceiling coatings, door seals, pest screens"],
    ],
)

# ── 3. Equipment capex by phase ───────────────────────────────────────────────
write_csv(
    "capex_by_phase.csv",
    ["phase", "year", "item", "cost_low_eur", "cost_high_eur", "priority", "notes"],
    [
        [1, 1, "Stainless tanks (6-8 units, variable cap, glycol jacket)",  15000, 28000, "Critical",  "2x50hl + 2x30hl + 2x20hl; used from Letina/Marchisio dealer"],
        [1, 1, "Glycol chiller (5-ton, used or entry-level new)",            5000, 12000, "Critical",  "Used EU brand preferred"],
        [1, 1, "Glycol piping + control valves",                             2000,  5000, "Critical",  "Materials + installation"],
        [1, 1, "Eccentric screw pump",                                       1500,  4000, "High",      "Used Ragazzini or SRAML"],
        [1, 1, "Crusher-destemmer",                                          1500,  3000, "High",      "New entry-level roller type"],
        [1, 1, "Lab equipment (refractometer, pH, SO2 titrator, TA kit)",    1500,  3500, "High",      "Hanna HI84500 + pH meter + basics"],
        [1, 1, "Oenological inputs Year 1",                                  1500,  3000, "Critical",  "Yeast, enzymes, nutrients, SO2, fining agents"],
        [1, 1, "Hoses, fittings, CIP equipment",                             1000,  2500, "High",      "Essential plumbing"],
        [1, 1, "Press (cooperative pressing Year 1; own press Year 2)",         0, 12000, "Medium",    "Defer to Year 2 to free capital"],
        [1, 1, "Contingency (10%)",                                          2900,  7200, "—",         ""],
        [2, 2, "Shed conversion (200-300 m2)",                              35000, 70000, "Critical",  "ANSVSA registration; floor, drainage, electrics, ventilation"],
        [2, 2, "Pneumatic press (20-25 hl, used)",                           8000, 20000, "High",      "Bucher/Pera/Enoveneta via Arsilac or Vinimat"],
        [2, 2, "Grape reception hopper + screw conveyor",                    2000,  5000, "Medium",    "New entry-level"],
        [2, 2, "Vibrating sorting table",                                    2000,  5000, "Medium",    "Vibrating preferred for DOC quality signal"],
        [2, 2, "Additional tanks (reach 450-500 hl total)",                  5000, 15000, "High",      "3-4 additional units"],
        [2, 2, "Semi-automatic bottling line (used filler+corker+labeller)", 6000, 15000, "Medium",    "Used from Vinimat/Enotools; or contract Year 2 buy Year 3"],
        [2, 2, "ANSVSA compliance docs + HACCP plan",                        1000,  3000, "Critical",  "Technical documentation and inspection fees"],
        [3, 3, "Pad filter + sterile membrane cartridge",                    2000,  5000, "High",      "Complete pre-bottling filtration"],
        [3, 3, "Lab upgrade (Hanna HI901W wine titrator)",                   1500,  4500, "Medium",    "pH, TA, VA, SO2, RS in one instrument"],
        [3, 3, "Bottling line upgrade (new integrated semi-auto)",          12000, 25000, "Medium",    "If not purchased Year 2"],
        [3, 3, "4-6 used neutral oak tonneaux (500 L) for Zgihara/reserve", 1200,  2700, "Low",       "Used/neutral; Zghihara and reserve blend experiments only"],
        [3, 3, "Tasting room / direct sales setup",                          5000, 15000, "Medium",    "High-margin channel"],
        [3, 3, "Branding, label design, website",                            3000,  8000, "High",      "One-time professional investment"],
        [3, 3, "Working capital (inputs + packaging 35,000 bottles)",       15000, 25000, "Critical",  "Bottles, corks, labels, capsules, cartons"],
    ],
)

# ── 4. Tank configuration and pricing ────────────────────────────────────────
write_csv(
    "tank_configuration.csv",
    ["capacity_hl", "capacity_l", "quantity", "total_hl", "price_new_min_eur",
     "price_new_max_eur", "price_per_hl_min", "price_per_hl_max", "purpose"],
    [
        [10,  1000, 2,  20,  1500,  3000, 150, 300, "Trial batches, blending tests"],
        [20,  2000, 2,  40,  2500,  4500, 125, 225, "Reserve / late harvest selections"],
        [30,  3000, 3,  90,  3500,  6000, 117, 200, "Press fractions, special lots"],
        [50,  5000, 4, 200,  5000,  9000, 100, 180, "Main fermentation / bulk storage"],
        [100, 10000, 1, 100, 8000, 14000,  80, 140, "Large-batch storage (Phase 2+)"],
    ],
)

# ── 5. Glycol chiller sizing ──────────────────────────────────────────────────
write_csv(
    "glycol_chiller_sizing.csv",
    ["chiller_size_tons", "chiller_kw", "new_price_min_eur", "new_price_max_eur",
     "used_price_min_eur", "used_price_max_eur", "suitable_for", "recommended_phase"],
    [
        [ 5,  18,  8000, 15000,  4000,  8000, "Year 1 bridging; 2-3 simultaneous tanks",    1],
        [10,  35, 18000, 30000,  6000, 12000, "Main operation; 5-6 simultaneous tanks",      2],
        [15,  53, 28000, 45000, 10000, 18000, "Full capacity + cold stab simultaneously",    2],
    ],
)

# ── 6. Press comparison ───────────────────────────────────────────────────────
write_csv(
    "press_comparison.csv",
    ["brand", "model", "capacity_hl", "new_price_min_eur", "new_price_max_eur",
     "inert_gas", "notes"],
    [
        ["Bucher Vaslin",       "XPro 20 hl",         20, 18000, 28000, False, "Standard commercial entry; widely distributed"],
        ["Bucher Vaslin",       "Inertys XPro 40 hl", 40, 35000, 55000, True,  "Premium inert-gas pressing; best for aromatics"],
        ["Della Toffola / Pera","Smart Press 20 hl",  20, 15000, 25000, False, "Competitive pricing; Italian"],
        ["Enoveneta",           "PPC 20",             20, 12000, 20000, False, "Closed cage; reliable; Eastern European distribution"],
        ["Speidel",             "Water bladder 20 hl",20,  8000, 15000, False, "German; proven; no inert gas option"],
        ["Used (any brand)",    "10-25 hl",           20,  4000, 12000, False, "Via Arsilac, Vinimat, Agriaffaires; 40-60% of new"],
    ],
)

# ── 7. Packaging cost per bottle ──────────────────────────────────────────────
write_csv(
    "packaging_cost_per_bottle.csv",
    ["item", "cost_min_eur", "cost_max_eur", "notes"],
    [
        ["Glass bottle (750 mL)",    0.30, 0.45, "Romanian supplier (VitroPack, Dunarea Glass); palette order"],
        ["DIAM 3 technical cork",    0.30, 0.50, "Recommended closure; virtually TCA-free"],
        ["Tin capsule / foil",       0.05, 0.10, "Standard coloured foil"],
        ["Front + back labels",      0.10, 0.30, "Digital print, runs of 2,000-5,000; premium adds €0.10-0.15"],
        ["Cardboard case (6 or 12)", 0.15, 0.25, "Per bottle share of case cost"],
    ],
)

# ── 8. Closure comparison ─────────────────────────────────────────────────────
write_csv(
    "closure_comparison.csv",
    ["closure_type", "cost_per_unit_min_eur", "cost_per_unit_max_eur",
     "oxygen_transmission", "best_for", "risk", "recommended"],
    [
        ["DIAM 3 technical cork",  0.30, 0.50, "Low-moderate; controlled",  "Main dry aromatic white; 2-5yr shelf life",    "Virtually TCA-free",                True],
        ["Screwcap (Stelvin)",     0.08, 0.20, "Near-zero (ROPP)",          "Off-dry / demi-sec; fresh young wines",        "Market acceptance developing in RO", False],
        ["Natural cork",           0.40, 1.20, "Low-moderate; variable",    "Late-harvest / noble rot premium tier",        "TCA taint risk without DIAM",       False],
        ["Glass stopper (Vinolok)",0.40, 0.80, "Near-zero",                 "Premium aromatic; high visual impact",         "Higher cost; special bottling head", False],
        ["Synthetic cork (Nomacorc)",0.10,0.25,"Low; controlled",           "Fresh whites for immediate consumption",       "Perceived quality barrier",         False],
    ],
)

# ── 9. Yeast comparison ───────────────────────────────────────────────────────
write_csv(
    "yeast_comparison.csv",
    ["strain", "supplier", "beta_glucosidase", "temp_range_min_c", "temp_range_max_c",
     "nitrogen_needs", "key_notes", "recommended"],
    [
        ["LALVIN QA23",    "Lallemand", "High",        10, 28, "Low",    "Top choice; widely available in Romania; ferments to dryness at 10°C; excellent for fresh aromatic whites",         True],
        ["Zymaflore VL1",  "Laffort",   "High",        16, 20, "High",   "Specifically recommended for Muscat, Riesling, Gewurztraminer; low VA production; premium aromatic expression",    True],
        ["LALVIN ICV D47", "Lallemand", "High",        15, 20, "Low",    "High glycerol and polysaccharides for body; citrus and floral notes; good secondary choice",                       False],
        ["SafOeno HD T18", "Fermentis", "High",        14, 20, "Medium", "Positioned specifically for terpenic white wines",                                                                 False],
        ["EnartisFerm Q9", "Enartis",   "Medium-High", 14, 22, "Medium", "Good for aromatic whites; lower risk of SO2 production",                                                           False],
    ],
)

# ── 10. Filtration options comparison ────────────────────────────────────────
write_csv(
    "filtration_options.csv",
    ["method", "aroma_stripping", "capex_min_eur", "capex_max_eur",
     "suitable_for_this_scale", "recommended", "notes"],
    [
        ["Cold static settling (debourbage)",        "None",    0,      0,      True,  True,  "Post-pressing gross clarification; no equipment beyond cold tank"],
        ["Plate-and-frame pad filter",               "Low",     1500,   4000,   True,  True,  "Rough/polishing pre-bottling; 50-100 hl per pad change"],
        ["0.45 micron sterile membrane cartridge",   "Minimal", 200,    500,    True,  True,  "Inline before bottling valve; €50-150 per cartridge run"],
        ["Diatomaceous earth (DE) leaf filter",      "Low",     3000,   8000,   True,  False, "Economic but creates DE waste stream; not necessary at this scale"],
        ["Cross-flow membrane filtration",           "Minimal", 20000,  40000,  False, False, "Justified above 1,000 hl/year; not warranted at this scale"],
    ],
)

# ── 11. Grant eligibility overview ────────────────────────────────────────────
write_csv(
    "grant_eligibility.csv",
    ["programme", "administering_body", "grant_rate_pct", "max_support_eur",
     "eligible_investments", "application_timing", "notes"],
    [
        ["IS-V-02 Wine Sector Support",  "APIA/AFIR",  50, 400000,
         "Tanks, presses, chillers, filters, bottling lines, lab, tasting room, consulting",
         "Year 2-3 once operational",
         "Most directly relevant grant; requires ONVPV registration"],
        ["IS-V-07 Wine Sector Support",  "APIA/AFIR",  50, 250000,
         "Same as IS-V-02 (different sub-measure)",
         "Year 2-3 once operational",
         "Alternative sub-measure; same eligibility conditions"],
        ["DR-23 Agricultural Processing","AFIR (CAP)", 65, 3000000,
         "Agricultural processing equipment; wine processing if NACE 1102 confirmed",
         "Dec 2025 - Feb 2026 call (verify next call dates)",
         "CRITICAL: verify wine/NACE 1102 eligibility with AFIR before applying"],
    ],
)

# ── 12. Lab equipment setup ───────────────────────────────────────────────────
write_csv(
    "lab_equipment.csv",
    ["equipment", "in_house_or_outsource", "cost_min_eur", "cost_max_eur",
     "use_case", "when_needed"],
    [
        ["Handheld digital refractometer",           "In-house",  50,   200, "Brix at harvest and pre-ferment",                  "Daily during harvest"],
        ["Benchtop pH meter (Hanna HI5521)",         "In-house", 200,   600, "pH at all stages",                                 "Throughout season"],
        ["SO2 mini-titrator (Hanna HI84500)",        "In-house", 200,  1100, "Free and total SO2",                               "Post-ferment and pre-bottling"],
        ["TA titration kit (NaOH, manual)",          "In-house",  50,   600, "Titratable acidity in must and wine",              "Throughout season"],
        ["Glass hydrometer set",                     "In-house",  20,   500, "Residual sugar during fermentation",               "Daily during ferment"],
        ["Calibrated thermometer",                   "In-house",  30,   100, "Tank temperatures",                                "Throughout season"],
        ["Lab glass (burettes, flasks, pipettes)",   "In-house", 200,   500, "All analyses",                                     "Throughout season"],
        ["Basic microscope (optional)",              "In-house", 200,   600, "Yeast cell counts, brett screening",               "During ferment"],
        ["YAN analysis (NOPA/SOPA enzymatic)",       "Outsource", 50,   150, "Yeast assimilable nitrogen per block",             "Pre-harvest"],
        ["Alcohol by volume (distillation method)",  "Outsource", 30,    80, "Label accuracy requirement",                       "Pre-bottling each lot"],
        ["Complete microbiological screen",          "Outsource", 80,   200, "Total bacteria, LAB, brett",                       "Pre-bottling each lot"],
        ["Nutritional declaration (EU label)",       "Outsource", 100,  300, "EU 2021/2117 label requirement",                   "Once per wine style/vintage"],
        ["Pesticide residue screen",                 "Outsource", 200,  500, "Annual requirement for DOC certificate",           "Annual"],
    ],
)

print("\nAll CSV files written to:", DATA_DIR)
