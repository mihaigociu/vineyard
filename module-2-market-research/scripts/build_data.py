"""
Build CSV data files for Module 2 — Romanian Wine Market Research.

Data sourced from: OIV, ONVV, Revistaprogresiv.ro, ZF.ro, Wines of Romania,
IndexBox, Statista, Revistabiz.ro (see module-2-market-research.md for full citations).

Run: python scripts/build_data.py
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


# ── 1. Romanian wine production (million hl) ──────────────────────────────────
write_csv(
    "ro_wine_production.csv",
    ["year", "production_mhl", "notes"],
    [
        [2018, 5.1, "Normal year"],
        [2019, 4.9, "Slight decline"],
        [2020, 3.3, "Frost + drought"],
        [2021, 4.5, "Strong recovery"],
        [2022, 3.8, "Drought impact"],
        [2023, 4.4, "+15% vs 2022; 6th in Europe"],
        [2024, 3.1, "-20%; severe drought"],
        [2025, 4.1, "Estimate; +29% recovery (OIV)"],
    ],
)

# ── 2. Romanian wine domestic consumption (million hl) ────────────────────────
write_csv(
    "ro_wine_consumption.csv",
    ["year", "consumption_mhl", "yoy_pct_change", "notes"],
    [
        [2018, 4.1, None, "Baseline"],
        [2019, 4.0, -2.4, ""],
        [2020, 3.9, -2.5, "Pandemic; HoReCa closed"],
        [2021, 4.1, 5.1, "Rebound"],
        [2022, 3.7, -9.8, "Inflation squeeze"],
        [2023, 3.0, -18.9, "Drought-reduced supply"],
        [2024, 2.7, -11.4, "Continued consumer spending squeeze (OIV)"],
    ],
)

# ── 3. Romanian wine market value (EUR million) ───────────────────────────────
write_csv(
    "ro_wine_market_value.csv",
    ["year", "market_value_eur_million", "source", "notes"],
    [
        [2019, 380, "Estimate", "Pre-pandemic baseline"],
        [2020, 370, "Estimate", "Pandemic disruption"],
        [2021, 430, "KEYSFIN/Bursa.ro", "Peak; RON 2.1bn commercial market"],
        [2022, 450, "Revistabiz.ro", "Internal market value"],
        [2023, 470, "Estimate extrapolated", "Premiumisation continues"],
        [2024, 700, "Statista (total incl imports)", "Total market revenue"],
    ],
)

# ── 4. Per capita wine consumption comparison ─────────────────────────────────
write_csv(
    "per_capita_consumption_comparison.csv",
    ["country", "litres_per_capita_2023_2024", "source"],
    [
        ["Portugal", 61.1, "Visual Capitalist 2025"],
        ["Italy", 42.7, "Visual Capitalist 2025"],
        ["France", 41.5, "Visual Capitalist 2025"],
        ["Austria", 28.6, "Visual Capitalist 2025"],
        ["EU Average", 28.7, "Visual Capitalist 2025"],
        ["Germany", 24.5, "Visual Capitalist 2025"],
        ["Netherlands", 20.7, "Visual Capitalist 2025"],
        ["Romania", 18.7, "Visual Capitalist 2025 / Revistaprogresiv"],
        ["Bulgaria", 17.2, "Visual Capitalist 2025"],
        ["Poland", 6.4, "Visual Capitalist 2025"],
    ],
)

# ── 5. Wine category split (production, viticultural year 2022/23) ────────────
write_csv(
    "ro_wine_category_split.csv",
    ["category", "production_hl", "yoy_change_pct", "trend", "notes"],
    [
        ["Table/bulk (no GI)", 2240000, -33.0, "Declining sharply", "~70% of total; structural retreat"],
        ["PDO (DOC)", 800524, -5.0, "Stable/slight decline", "Controlled designation"],
        ["PGI (IG)", 359000, 21.8, "Growing", "Only category with volume growth"],
    ],
)

# ── 6. Price tier breakdown (estimated) ──────────────────────────────────────
write_csv(
    "ro_wine_price_tiers.csv",
    ["tier", "price_range_ron", "price_range_eur", "volume_share_pct_est", "value_share_pct_est"],
    [
        ["Entry", "<20", "<4", 67, 37],
        ["Mid-range", "20-60", "4-12", 26, 43],
        ["Premium", ">60", ">12", 7, 20],
    ],
)

# ── 7. Romanian wine exports ──────────────────────────────────────────────────
write_csv(
    "ro_wine_exports.csv",
    ["year", "volume_tonnes", "value_eur_million", "avg_price_eur_per_litre"],
    [
        [2014, 34000, 22, 0.65],
        [2019, 38000, 60, 1.58],
        [2021, 38000, 69, 1.82],
        [2022, 36300, 71.6, 1.97],
        [2023, 34400, 72.5, 2.09],
        [2024, 18000, 38, 2.11],  # estimated from USD 42m figure
    ],
)

# ── 8. Top export destinations ────────────────────────────────────────────────
write_csv(
    "ro_wine_export_destinations.csv",
    ["rank", "country", "share_of_export_value_pct_approx", "2024_growth_pct", "notes"],
    [
        [1, "Netherlands", 25, None, "Re-export hub"],
        [2, "Germany", 20, 23.6, "Largest consumer-end market by volume"],
        [3, "United Kingdom", 16, 506.5, "Highest growth; post-Brexit stabilisation"],
        [4, "Bulgaria", 8, None, ""],
        [5, "USA", 7, None, ""],
        [6, "Czech Republic", 5, None, ""],
        [7, "Poland", 4, None, ""],
        [8, "Norway", 3, None, ""],
        [9, "Italy/Spain", 3, None, "Diaspora market"],
        [10, "Other", 9, None, ""],
    ],
)

# ── 9. Competitive landscape summary ─────────────────────────────────────────
write_csv(
    "husi_region_competitors.csv",
    ["producer", "location", "vineyard_ha", "annual_litres_est", "muscat_ottonel", "organic", "key_varieties"],
    [
        ["Casa de Vinuri Husi", "Husi, Vaslui", 600, 9000000, "No", "No", "Zghihara de Husi, Busuioaca, Feteasca Neagra"],
        ["Domeniile Averesti", "Averesti, Vaslui", 650, 6000000, "Yes (not flagship)", "No", "Busuioaca de Bohotin, Muscat Ottonel, Zghihara de Husi"],
        ["Vincon Vrancea", "Husi + Vrancea", 1500, 25000000, "Yes (premium tier)", "No", "Muscat Ottonel (Oenoteca), Feteasca Neagra, Cab Sauv"],
        ["Cotnari SA", "Cotnari, Iasi", 1600, 10000000, "No", "No", "Grasa de Cotnari, Francusa, Feteasca Alba, Tamaioasa"],
        ["ViaHusi", "Husi, Vaslui", None, None, "Unknown", "Unknown", "Unknown - boutique"],
        ["Target vineyard (Husi)", "Husi, Vaslui", 10, 35000, "Yes (flagship)", "Target", "Muscat Ottonel"],
    ],
)

# ── 10. Muscat Ottonel global market ─────────────────────────────────────────
write_csv(
    "muscat_ottonel_global_market.csv",
    ["year", "global_muscat_wine_market_usd_billion", "notes"],
    [
        [2024, 2.14, "Actual; DataIntelo"],
        [2025, 2.24, "Projected"],
        [2026, 2.35, "Projected"],
        [2027, 2.46, "Projected"],
        [2028, 2.58, "Projected"],
        [2029, 2.71, "Projected"],
        [2030, 2.84, "Projected"],
        [2031, 2.97, "Projected"],
        [2032, 3.10, "Projected"],
        [2033, 3.23, "Projected (CAGR 4.7%)"],
    ],
)

print("\nAll CSV files written to:", DATA_DIR)
