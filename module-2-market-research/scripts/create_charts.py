"""
Create charts for Module 2 — Romanian Wine Market Research.

Reads CSV files from ../data/ and writes PNG charts to ../charts/.

Run: python scripts/create_charts.py
Requires: pip install matplotlib pandas
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EFD3D7", "#8EE3EF", "#A3C4BC"]
ACCENT = "#C0392B"

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 150,
})


def savefig(name):
    path = os.path.join(CHARTS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {name}")


# ── Chart 1: Wine production vs consumption trend ────────────────────────────
prod = pd.read_csv(os.path.join(DATA_DIR, "ro_wine_production.csv"))
cons = pd.read_csv(os.path.join(DATA_DIR, "ro_wine_consumption.csv"))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(prod["year"], prod["production_mhl"], marker="o", color=PALETTE[0], linewidth=2, label="Production (m hl)")
ax.plot(cons["year"], cons["consumption_mhl"], marker="s", color=PALETTE[1], linewidth=2, label="Consumption (m hl)")
# align on common years before fill
merged = pd.merge(prod[["year", "production_mhl"]], cons[["year", "consumption_mhl"]], on="year")
ax.fill_between(merged["year"], merged["production_mhl"], merged["consumption_mhl"], alpha=0.08, color=PALETTE[0])
ax.axvline(2025, color=ACCENT, linestyle="--", linewidth=1, alpha=0.6, label="2025 estimate")
ax.set_title("Romania — Wine Production vs Domestic Consumption (2018–2025)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("Million hectolitres")
ax.legend()
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
savefig("01_production_vs_consumption.png")


# ── Chart 2: Market value trend ───────────────────────────────────────────────
val = pd.read_csv(os.path.join(DATA_DIR, "ro_wine_market_value.csv"))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(val["year"].astype(str), val["market_value_eur_million"], color=PALETTE[0], width=0.6)
ax.bar_label(bars, fmt="€%g m", padding=4, fontsize=9)
ax.set_title("Romanian Wine Market Value (EUR million)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("EUR million")
ax.set_ylim(0, val["market_value_eur_million"].max() * 1.2)
savefig("02_market_value_trend.png")


# ── Chart 3: Per capita consumption comparison ────────────────────────────────
pc = pd.read_csv(os.path.join(DATA_DIR, "per_capita_consumption_comparison.csv"))
pc = pc.sort_values("litres_per_capita_2023_2024", ascending=True)

colors = [ACCENT if c == "Romania" else ("#888" if c == "EU Average" else PALETTE[0]) for c in pc["country"]]
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(pc["country"], pc["litres_per_capita_2023_2024"], color=colors)
ax.bar_label(bars, fmt="%.1f L", padding=4, fontsize=9)
eu_val = pc.loc[pc["country"] == "EU Average", "litres_per_capita_2023_2024"].values[0]
ax.axvline(eu_val, color="#888", linestyle="--", linewidth=1.2, label=f"EU Average ({eu_val} L)")
ax.set_title("Wine Consumption per Capita — Romania vs Selected Countries (2023–2024)", fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("Litres per person per year")
ax.legend()
savefig("03_per_capita_comparison.png")


# ── Chart 4: Wine category split (production volume) ─────────────────────────
cat = pd.read_csv(os.path.join(DATA_DIR, "ro_wine_category_split.csv"))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Pie chart
wedges, texts, autotexts = axes[0].pie(
    cat["production_hl"],
    labels=cat["category"],
    autopct="%1.0f%%",
    colors=PALETTE[:3],
    startangle=140,
    pctdistance=0.7,
)
axes[0].set_title("Production Share by Category\n(Viticultural year 2022/23)", fontsize=11, fontweight="bold")

# YoY change bar
bar_colors = [ACCENT if v < 0 else PALETTE[1] for v in cat["yoy_change_pct"]]
bars = axes[1].bar(cat["category"], cat["yoy_change_pct"], color=bar_colors)
axes[1].bar_label(bars, fmt="%.1f%%", padding=4, fontsize=9)
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].set_title("YoY Volume Change by Category (%)", fontsize=11, fontweight="bold")
axes[1].set_ylabel("Change (%)")
axes[1].tick_params(axis="x", labelsize=9)
plt.setp(axes[1].get_xticklabels(), rotation=15, ha="right")

fig.suptitle("Romanian Wine Market — Category Breakdown (2022/23)", fontsize=13, fontweight="bold", y=1.02)
savefig("04_wine_category_split.png")


# ── Chart 5: Price tier breakdown ─────────────────────────────────────────────
tiers = pd.read_csv(os.path.join(DATA_DIR, "ro_wine_price_tiers.csv"))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, col, title in [
    (axes[0], "volume_share_pct_est", "Volume Share (%)"),
    (axes[1], "value_share_pct_est", "Value Share (%)"),
]:
    wedges, texts, autotexts = ax.pie(
        tiers[col],
        labels=[f"{r['tier']}\n({r['price_range_ron']} RON)" for _, r in tiers.iterrows()],
        autopct="%1.0f%%",
        colors=PALETTE[:3],
        startangle=90,
        pctdistance=0.75,
    )
    ax.set_title(title, fontsize=11, fontweight="bold")

fig.suptitle("Romanian Wine Market — Price Tier Split (estimated)", fontsize=13, fontweight="bold", y=1.02)
fig.text(0.5, -0.04, "Note: estimates synthesised from public data; no single source provides confirmed tier split",
         ha="center", fontsize=8, color="gray")
savefig("05_price_tier_split.png")


# ── Chart 6: Export value vs volume trend ────────────────────────────────────
exp = pd.read_csv(os.path.join(DATA_DIR, "ro_wine_exports.csv"))

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.bar(exp["year"].astype(str), exp["volume_tonnes"] / 1000, color=PALETTE[0], alpha=0.7, label="Volume (000 tonnes)")
ax2.plot(exp["year"].astype(str), exp["value_eur_million"], color=ACCENT, marker="o", linewidth=2, label="Value (EUR million)")
ax1.set_title("Romanian Wine Exports — Volume vs Value (2014–2024)", fontsize=13, fontweight="bold", pad=12)
ax1.set_xlabel("Year")
ax1.set_ylabel("Volume (000 tonnes)", color=PALETTE[0])
ax2.set_ylabel("Value (EUR million)", color=ACCENT)
ax1.tick_params(axis="y", labelcolor=PALETTE[0])
ax2.tick_params(axis="y", labelcolor=ACCENT)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
savefig("06_export_volume_vs_value.png")


# ── Chart 7: Top export destinations ─────────────────────────────────────────
dest = pd.read_csv(os.path.join(DATA_DIR, "ro_wine_export_destinations.csv"))
dest = dest.sort_values("share_of_export_value_pct_approx", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
bar_colors = [ACCENT if c == "United Kingdom" else PALETTE[0] for c in dest["country"]]
bars = ax.barh(dest["country"], dest["share_of_export_value_pct_approx"], color=bar_colors)
ax.bar_label(bars, fmt="%g%%", padding=4, fontsize=9)
ax.set_title("Romanian Wine Export Destinations by Value Share (2022–2024 avg)", fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("Approx. share of export value (%)")
ax.text(16, dest[dest["country"] == "United Kingdom"].index[0] - dest.index[0],
        "+506% in 2024", fontsize=8, color=ACCENT, va="center")
savefig("07_export_destinations.png")


# ── Chart 8: Competitive landscape — vineyard size ───────────────────────────
comp = pd.read_csv(os.path.join(DATA_DIR, "husi_region_competitors.csv"))
comp = comp.dropna(subset=["vineyard_ha"])
comp = comp.sort_values("vineyard_ha")

bar_colors = [ACCENT if p == "Target vineyard (Husi)" else PALETTE[0] for p in comp["producer"]]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(comp["producer"], comp["vineyard_ha"], color=bar_colors)
ax.bar_label(bars, fmt="%g ha", padding=4, fontsize=9)
ax.set_title("Husi Region Competitors — Vineyard Area (ha)", fontsize=13, fontweight="bold", pad=12)
ax.set_xlabel("Vineyard area (ha)")
ax.set_xscale("log")
ax.set_xlabel("Vineyard area, ha (log scale)")
savefig("08_competitor_vineyard_size.png")


# ── Chart 9: Muscat Ottonel global market projection ─────────────────────────
mo = pd.read_csv(os.path.join(DATA_DIR, "muscat_ottonel_global_market.csv"))
actuals = mo[mo["notes"].str.startswith("Actual")]
projections = mo[mo["notes"].str.startswith("Projected")]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(actuals["year"], actuals["global_muscat_wine_market_usd_billion"],
        color=PALETTE[0], marker="o", linewidth=2.5, label="Actual")
ax.plot(projections["year"], projections["global_muscat_wine_market_usd_billion"],
        color=PALETTE[1], marker="o", linewidth=2, linestyle="--", label="Projected (CAGR 4.7%)")
ax.axvline(2024.5, color="#aaa", linestyle=":", linewidth=1)
ax.set_title("Global Muscat Wine Market — Size & Projection (USD billion)", fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("Year")
ax.set_ylabel("USD billion")
ax.legend()
ax.text(0.02, 0.95, "Source: DataIntelo Muscat Wine Market Report",
        transform=ax.transAxes, fontsize=7, color="gray", va="top")
savefig("09_muscat_global_market.png")

print("\nAll charts written to:", CHARTS_DIR)
