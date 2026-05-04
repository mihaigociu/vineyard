"""
Build CSV data files for Module 3 — Agronomy & Viticulture.

Sources: OENO One viticultural zones study, weatherandclimate.com, Plantgrape.fr,
MDPI, PMC, EUR-Lex, Romanian Journal of Horticulture.
See module-3-agronomy.md for full citations.

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


# ── 1. Monthly climate data ───────────────────────────────────────────────────
write_csv(
    "husi_monthly_climate.csv",
    ["month", "month_num", "temp_min_c", "temp_mean_c", "temp_max_c", "precip_mm"],
    [
        ["January",   1,  -6.0,  -2.5,  -0.1,  60],
        ["February",  2,  -3.8,   0.3,   2.9,  64],
        ["March",     3,   1.2,   6.7,   9.9,  56],
        ["April",     4,   5.8,  13.5,  16.8,  76],
        ["May",       5,  10.5,  19.2,  22.4, 133],
        ["June",      6,  14.6,  23.3,  26.4, 146],
        ["July",      7,  15.8,  25.3,  28.8,  91],
        ["August",    8,  15.7,  25.6,  29.7,  38],
        ["September", 9,  11.9,  20.1,  24.1,  53],
        ["October",  10,   6.9,  12.3,  15.8,  84],
        ["November", 11,   2.9,   6.6,   9.8,  48],
        ["December", 12,  -2.4,   0.9,   3.4,  54],
    ],
)

# ── 2. Muscat Ottonel phenological calendar ───────────────────────────────────
write_csv(
    "muscat_ottonel_phenology.csv",
    ["stage", "approx_start_month", "approx_end_month", "timing_description", "notes"],
    [
        ["Sap bleeding",          2,  3,  "Late Feb – early Mar",       "Soil temp >5°C trigger"],
        ["Budburst",              3,  4,  "Late Mar – early Apr",       "FROST RISK OVERLAP — last frost mid-late April"],
        ["Shoot 10cm",            4,  4,  "Mid-April",                  "First fungicide application"],
        ["Pre-flowering",         5,  5,  "Late May",                   "Inflorescence visible; spray programme intensifies"],
        ["Full flowering",        6,  6,  "Early to mid-June",          "CRITICAL disease window; coulure risk"],
        ["Berry set",             6,  6,  "Late June",                  ""],
        ["Veraison",              7,  7,  "Mid to late July",           "Hail risk peaks; reduce nitrogen"],
        ["Harvest (dry/semi-dry)",8,  9,  "Late Aug – mid-Sep",         "Target 6-8 t/ha; manual harvest"],
        ["Harvest (late harvest)",9, 10,  "Sep – early Oct",            "DOC-CT style; 3-5 t/ha"],
    ],
)

# ── 3. Disease risk ranking ───────────────────────────────────────────────────
write_csv(
    "disease_risk_ranking.csv",
    ["rank", "disease", "pathogen", "risk_level_score_1_5", "risk_label", "key_driver", "management"],
    [
        [1, "Downy mildew",          "Plasmopara viticola",   5, "CRITICAL",          "May-June rainfall peak + susceptible variety",         "12-15 fungicide treatments/season; DSS recommended"],
        [2, "Grey rot / Botrytis",   "Botrytis cinerea",      4, "HIGH",              "Thin-skinned compact clusters; warm humid flowering",  "Leaf removal; fungicides at bloom + pre-harvest; harvest timing"],
        [3, "Powdery mildew",        "Erysiphe necator",      3, "MODERATE",          "Warm dry July-August; susceptible variety",            "Sulphur programme; standard management"],
        [4, "Esca trunk disease",    "Phaeomoniella spp.",    3, "MODERATE LONG-TERM","Vine age 10-25 yr = prime expression window",          "No curative treatment; wound sealants at pruning; visual survey urgently needed"],
    ],
)

# ── 4. Spray programme calendar ───────────────────────────────────────────────
write_csv(
    "spray_programme_calendar.csv",
    ["treatment_num", "phenological_stage", "target_diseases", "conventional_products", "organic_alternatives", "is_critical"],
    [
        [1,    "Dormancy/pre-budburst",              "Excoriosis, anthracnose",           "Copper + oil (TMTD alternatives)",          "Copper + vegetable oil",        False],
        ["2-3","Shoot growth 5-15 cm",               "Downy mildew, powdery mildew",      "Mancozeb/folpet; sulphur",                  "Copper; sulphur",               False],
        ["4-5","Shoot growth 15-30 cm",              "Downy mildew, powdery mildew",      "Systemic DM (cymoxanil); sulphur",          "Copper; sulphur; potassium bicarb", False],
        ["6-7","Pre-bloom / inflorescence",          "DM, PM, early botrytis",            "Contact+systemic combo; switch/rovral",     "Copper; sulphur; Bacillus subtilis", True],
        ["8-9","Full bloom / post-bloom",            "DM, PM, botrytis on inflorescences","Copper; fenhexamid or cyprodinil; sulphur", "Copper (within 4kg limit); Bacillus subtilis; sulphur", True],
        ["10-11","Berry growth (pea-size to closure)","DM, PM, botrytis",                 "Alternating chemistry (resistance mgmt)",   "Copper; sulphur; Trichoderma",  False],
        ["12-13","Bunch closure to veraison",        "DM, botrytis (pre-harvest)",        "Respect PHI; reduce systemics",             "Copper; potassium bicarb",      False],
        [14,   "Veraison (optional)",                "Late botrytis",                     "Biostimulants preferred",                   "Bacillus subtilis; kaolin",     False],
    ],
)

# ── 5. Yield benchmarks by quality level ─────────────────────────────────────
write_csv(
    "yield_quality_benchmarks.csv",
    ["quality_level", "yield_min_t_ha", "yield_max_t_ha", "wine_style", "target_for_this_operation"],
    [
        ["DOC-CIB (noble rot)",     1,  3,  "Dessert; botrytised sweet",         False],
        ["DOC-CT (late harvest)",   3,  5,  "Semi-sweet; demi-dulce",            False],
        ["DOC-CMD (full maturity)", 5,  8,  "Dry; off-dry; demi-sec",            True],
        ["IG varietal",             8, 12,  "Commercial/industrial quality",     False],
        ["Non-DOC / maximum",      12, 15,  "Table wine; unacceptable for premium", False],
    ],
)

# ── 6. Vine age vs yield and quality ─────────────────────────────────────────
write_csv(
    "vine_age_vs_yield_quality.csv",
    ["age_range_years", "age_midpoint", "yield_relative_pct", "quality_score_1_5", "notes"],
    [
        ["1-5",   3,   0,  0, "Establishment; no commercial crop"],
        ["5-10",  7,  75,  3, "Rapidly increasing; may overproduce; yield management critical"],
        ["10-15", 12, 100,  4, "At/near peak yield; good quality if managed"],
        ["15-25", 20,  95,  5, "Stable; sweet spot for aromatic whites; lower natural vigour"],
        ["25-35", 30,  80,  5, "Declining output; increasing concentration"],
        ["35+",   40,  65,  5, "Old-vine complexity; consistency variable; disease risk rises"],
    ],
)

# ── 7. Treatment costs conventional vs organic ────────────────────────────────
write_csv(
    "treatment_costs_conv_vs_organic.csv",
    ["cost_category", "conventional_eur_ha_yr_min", "conventional_eur_ha_yr_max",
     "organic_eur_ha_yr_min", "organic_eur_ha_yr_max"],
    [
        ["Plant protection products",            250, 400, 300, 500],
        ["Additional labour (organic extra passes)", 0,   0, 100, 150],
        ["Total direct plant protection",        250, 450, 400, 650],
    ],
)

# ── 8. Complementary varieties comparison ────────────────────────────────────
write_csv(
    "complementary_varieties.csv",
    ["variety", "ripening", "yield_t_ha_typical", "acidity", "aromatics",
     "dm_resistance", "pm_resistance", "botrytis_risk", "husi_authenticity",
     "recommendation", "notes"],
    [
        ["Muscat Ottonel (main)",     "Early (Aug-Sep)",      "6-8",   "Low",      "Very high (floral/musky)",   "Susceptible",  "Susceptible",  "High",     "Yes (DOC)",         "Keep as flagship",                "Current main variety"],
        ["Zghihara de Husi",          "Late (Sep-Oct)",       "15-17", "Very high","None (fresh/green)",         "Susceptible",  "Resistant",    "Moderate", "Yes (DOC, iconic)", "Strongly recommend 15-25% rows",  "Natural complement to Muscat Ottonel; blending + standalone"],
        ["Busuioaca de Bohotin",      "Mid-late (Sep)",       "10-14", "Moderate", "High (rose/basil)",          "Susceptible",  "Susceptible",  "High",     "Yes (DOC, 226ha in Vaslui)", "Strongly recommend 1-2 ha", "Historically authentic to Husi; rosé/pink wine potential"],
        ["Tamaioasa Romaneasca",      "Mid (Sep)",            "6-9",   "Moderate", "Very high (rose/jasmine)",   "Susceptible",  "Susceptible",  "High",     "Feasible (Cotnari nearby)", "Secondary consideration",    "Premium aromatic tier; botrytis-sensitive"],
        ["Feteasca Alba",             "Early-mid (Aug-Sep)",  "8-12",  "High",     "Moderate (neutral aromatic)","Moderate",     "Moderate",     "Moderate", "Yes (DOC)",         "Optional for volume blend",       "Reliable workhorse; good blending complement"],
    ],
)

# ── 9. Grafting vs replanting costs ──────────────────────────────────────────
write_csv(
    "variety_conversion_costs.csv",
    ["method", "cost_per_ha_min_eur", "cost_per_ha_max_eur",
     "years_to_commercial_crop", "success_rate_pct", "best_suited_for"],
    [
        ["Top-working / field grafting",  500,  2500,  3, 75, "Capital-constrained Year 1-2; partial variety introduction"],
        ["Grub out and replant (all-in)", 12000, 21000, 5, 90, "Full reset; trunk disease pressure; trellis/density change; AFIR grant available"],
    ],
)

# ── 10. Rootstock comparison for Husi soils ───────────────────────────────────
write_csv(
    "rootstock_recommendations.csv",
    ["rootstock", "lime_tolerance_pct_active", "vigour", "recommended_for_husi",
     "priority", "notes"],
    [
        ["SO4",              17, "Moderate",      True,  "Primary",   "Best general adaptability; widely available in Romania; suits both chernozem and sandy-clay"],
        ["420A Berlandieri", 20, "Low-moderate",  True,  "Quality",   "Reduces vigour; improves aromatic concentration; use on upper-slope quality blocks"],
        ["5BB Kober",        20, "High",          "Conditional", "Poor soils only", "Risk of excess vigour on high-fertility chernozems"],
        ["41B Millardet",    40, "Moderate-low",  False, "Specialist","Only if high active lime confirmed by soil test"],
        ["125AA",            20, "High",          "Conditional", "Drought soils", "Good drought tolerance; not first choice for chernozems"],
    ],
)

print("\nAll CSV files written to:", DATA_DIR)
