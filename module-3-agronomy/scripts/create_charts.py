"""
Create charts for Module 3 — Agronomy & Viticulture.

Reads CSVs from ../data/ and writes PNG charts to ../charts/.

Run: python3 scripts/create_charts.py
Requires: pip install matplotlib pandas numpy
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

PALETTE = ["#2E4057", "#048A81", "#54C6EB", "#EFD3D7", "#8EE3EF", "#A3C4BC"]
ACCENT = "#C0392B"
GOLD = "#D4A017"

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


# ── Chart 1: Monthly climate — temperature and rainfall ──────────────────────
clim = pd.read_csv(os.path.join(DATA_DIR, "husi_monthly_climate.csv"))

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()

months = clim["month"].str[:3]
x = np.arange(len(months))
width = 0.5

# Rainfall bars (background)
bars = ax2.bar(x, clim["precip_mm"], width=width, color="#A3C4BC", alpha=0.5, label="Rainfall (mm)")
# Highlight May-June high-risk months
for i, (m, v) in enumerate(zip(clim["month"], clim["precip_mm"])):
    if m in ["May", "June"]:
        ax2.bar(i, v, width=width, color=ACCENT, alpha=0.7)

# Temperature lines
ax1.fill_between(x, clim["temp_min_c"], clim["temp_max_c"], alpha=0.12, color=PALETTE[0])
ax1.plot(x, clim["temp_mean_c"], color=PALETTE[0], linewidth=2.5, marker="o", markersize=5, label="Mean temp (°C)")
ax1.plot(x, clim["temp_min_c"], color=PALETTE[1], linewidth=1, linestyle="--", label="Min temp (°C)")
ax1.plot(x, clim["temp_max_c"], color=PALETTE[1], linewidth=1, linestyle=":", label="Max temp (°C)")
ax1.axhline(0, color="black", linewidth=0.8, alpha=0.5)
ax1.axhline(10, color=GOLD, linewidth=1, linestyle="--", alpha=0.6, label="10°C growing threshold")

ax1.set_xticks(x)
ax1.set_xticklabels(months)
ax1.set_ylabel("Temperature (°C)", color=PALETTE[0])
ax2.set_ylabel("Precipitation (mm)", color="#666")
ax1.tick_params(axis="y", labelcolor=PALETTE[0])
ax2.tick_params(axis="y", labelcolor="#666")

# Legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
red_patch = mpatches.Patch(color=ACCENT, alpha=0.7, label="May–June (high disease risk)")
ax1.legend(lines1 + lines2 + [red_patch], labels1 + labels2 + ["May–June (high disease risk)"],
           loc="upper left", fontsize=8)

ax1.set_title("Huși/Vaslui — Monthly Climate Profile\nTemperature range and precipitation (source: weatherandclimate.com / OENO One)",
              fontsize=12, fontweight="bold", pad=12)
savefig("01_monthly_climate.png")


# ── Chart 2: Disease risk ranking ────────────────────────────────────────────
disease = pd.read_csv(os.path.join(DATA_DIR, "disease_risk_ranking.csv"))

colors = {5: ACCENT, 4: "#E67E22", 3: GOLD, 2: PALETTE[1], 1: PALETTE[2]}
bar_colors = [colors[s] for s in disease["risk_level_score_1_5"]]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(disease["disease"], disease["risk_level_score_1_5"], color=bar_colors)
for bar, label in zip(bars, disease["risk_label"]):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
            label, va="center", fontsize=9, color="black")
ax.set_xlim(0, 7)
ax.set_xlabel("Risk score (1 = low, 5 = critical)")
ax.set_title("Disease Risk Ranking for Muscat Ottonel — Huși Climate", fontsize=12, fontweight="bold", pad=12)
ax.axvline(4, color="#aaa", linestyle="--", linewidth=1, label="High risk threshold")
ax.legend(fontsize=8)
savefig("02_disease_risk_ranking.png")


# ── Chart 3: Phenological calendar (Gantt-style) ─────────────────────────────
pheno = pd.read_csv(os.path.join(DATA_DIR, "muscat_ottonel_phenology.csv"))

fig, ax = plt.subplots(figsize=(13, 6))
stage_colors = [PALETTE[0]] * len(pheno)
# Highlight critical/risk stages
risk_stages = ["Budburst", "Full flowering", "Harvest (dry/semi-dry)"]
for i, stage in enumerate(pheno["stage"]):
    if stage in risk_stages:
        stage_colors[i] = ACCENT

y_positions = range(len(pheno))
for i, (_, row) in enumerate(pheno.iterrows()):
    start = row["approx_start_month"]
    end = row["approx_end_month"] + 0.8
    ax.barh(i, end - start, left=start - 0.4, color=stage_colors[i], alpha=0.8, height=0.6)

ax.set_yticks(list(y_positions))
ax.set_yticklabels(pheno["stage"], fontsize=9)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                   fontsize=9)
ax.set_xlim(1, 12.5)
ax.set_title("Muscat Ottonel — Phenological Calendar (Huși, ~46.7°N)", fontsize=12, fontweight="bold", pad=12)

# Frost risk overlay
ax.axvspan(3.5, 4.5, alpha=0.12, color=ACCENT, label="Spring frost risk window")
# May-June disease risk
ax.axvspan(4.8, 6.8, alpha=0.08, color="orange", label="High disease pressure (May–Jun)")

normal_patch = mpatches.Patch(color=PALETTE[0], alpha=0.8, label="Growth stage")
critical_patch = mpatches.Patch(color=ACCENT, alpha=0.8, label="Critical/risk stage")
ax.legend(handles=[normal_patch, critical_patch,
                   mpatches.Patch(color=ACCENT, alpha=0.12, label="Spring frost risk"),
                   mpatches.Patch(color="orange", alpha=0.12, label="Disease pressure peak")],
          loc="lower right", fontsize=8)
savefig("03_phenological_calendar.png")


# ── Chart 4: Yield vs quality tradeoff ───────────────────────────────────────
yq = pd.read_csv(os.path.join(DATA_DIR, "yield_quality_benchmarks.csv"))
yq["yield_mid"] = (yq["yield_min_t_ha"] + yq["yield_max_t_ha"]) / 2
yq["yield_range"] = yq["yield_max_t_ha"] - yq["yield_min_t_ha"]

fig, ax = plt.subplots(figsize=(10, 5))
bar_colors = [ACCENT if t else PALETTE[0] for t in yq["target_for_this_operation"]]
bars = ax.barh(yq["quality_level"], yq["yield_mid"], xerr=yq["yield_range"] / 2,
               color=bar_colors, capsize=4, height=0.5)
ax.set_xlabel("Typical yield (tonnes/ha)")
ax.set_title("Muscat Ottonel — Yield Range by Quality Level", fontsize=12, fontweight="bold", pad=12)
target_patch = mpatches.Patch(color=ACCENT, label="Target quality tier for this operation (DOC-CMD)")
ax.legend(handles=[target_patch], fontsize=8)
ax.axvline(6, color=ACCENT, linestyle="--", linewidth=1, alpha=0.6, label="Target yield 6 t/ha")
savefig("04_yield_quality_tradeoff.png")


# ── Chart 5: Vine age vs relative yield and quality ──────────────────────────
age = pd.read_csv(os.path.join(DATA_DIR, "vine_age_vs_yield_quality.csv"))

fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.plot(age["age_midpoint"], age["yield_relative_pct"], color=PALETTE[0], marker="o",
         linewidth=2.5, label="Relative yield (%)")
ax1.fill_between(age["age_midpoint"], age["yield_relative_pct"], alpha=0.1, color=PALETTE[0])
ax2.plot(age["age_midpoint"], age["quality_score_1_5"], color=ACCENT, marker="s",
         linewidth=2.5, linestyle="--", label="Quality score (1–5)")

# Highlight current vine age range
ax1.axvspan(10, 25, alpha=0.1, color=GOLD, label="Estimated current vine age")

ax1.set_xlabel("Vine age (years)")
ax1.set_ylabel("Relative yield (%)", color=PALETTE[0])
ax2.set_ylabel("Quality score (1–5)", color=ACCENT)
ax1.tick_params(axis="y", labelcolor=PALETTE[0])
ax2.tick_params(axis="y", labelcolor=ACCENT)
ax2.set_ylim(0, 6)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="center left", fontsize=8)
ax1.set_title("Muscat Ottonel — Vine Age vs Yield & Quality", fontsize=12, fontweight="bold", pad=12)
savefig("05_vine_age_yield_quality.png")


# ── Chart 6: Treatment costs conventional vs organic ─────────────────────────
costs = pd.read_csv(os.path.join(DATA_DIR, "treatment_costs_conv_vs_organic.csv"))
costs["conv_mid"] = (costs["conventional_eur_ha_yr_min"] + costs["conventional_eur_ha_yr_max"]) / 2
costs["org_mid"] = (costs["organic_eur_ha_yr_min"] + costs["organic_eur_ha_yr_max"]) / 2

total_conv = costs[costs["cost_category"] == "Total direct plant protection"]["conv_mid"].values[0]
total_org = costs[costs["cost_category"] == "Total direct plant protection"]["org_mid"].values[0]

fig, ax = plt.subplots(figsize=(9, 5))
categories = ["Plant protection\nproducts", "Additional\nlabour (organic)"]
conv_values = [
    costs[costs["cost_category"] == "Plant protection products"]["conv_mid"].values[0],
    0,
]
org_values = [
    costs[costs["cost_category"] == "Plant protection products"]["org_mid"].values[0],
    costs[costs["cost_category"] == "Additional labour (organic extra passes)"]["org_mid"].values[0],
]

x = np.arange(len(categories))
width = 0.35
b1 = ax.bar(x - width / 2, conv_values, width, label="Conventional IPM", color=PALETTE[0])
b2 = ax.bar(x + width / 2, org_values, width, label="Organic", color=PALETTE[1])
ax.bar_label(b1, fmt="€%.0f", padding=3, fontsize=8)
ax.bar_label(b2, fmt="€%.0f", padding=3, fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_ylabel("€/ha/year")
ax.set_title(f"Plant Protection Costs — Conventional vs Organic\n(Total: Conv €{int(total_conv)}/ha vs Organic €{int(total_org)}/ha)",
             fontsize=11, fontweight="bold", pad=12)
ax.legend()
ax.text(0.99, 0.97,
        "Note: Organic net income advantage ~€2,000/ha\nif premium market access achieved",
        transform=ax.transAxes, ha="right", va="top", fontsize=8, color="gray",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
savefig("06_treatment_costs_comparison.png")


# ── Chart 7: Complementary varieties radar chart ─────────────────────────────
varieties = pd.read_csv(os.path.join(DATA_DIR, "complementary_varieties.csv"))

# Build a simple comparison bar chart for key attributes
attr_map = {
    "Yield potential": {"Muscat Ottonel (main)": 4, "Zghihara de Husi": 5, "Busuioaca de Bohotin": 4,
                        "Tamaioasa Romaneasca": 3, "Feteasca Alba": 4},
    "Aromatic intensity": {"Muscat Ottonel (main)": 5, "Zghihara de Husi": 1, "Busuioaca de Bohotin": 4,
                           "Tamaioasa Romaneasca": 5, "Feteasca Alba": 2},
    "Acidity": {"Muscat Ottonel (main)": 2, "Zghihara de Husi": 5, "Busuioaca de Bohotin": 3,
                "Tamaioasa Romaneasca": 3, "Feteasca Alba": 4},
    "DM resistance": {"Muscat Ottonel (main)": 2, "Zghihara de Husi": 2, "Busuioaca de Bohotin": 2,
                      "Tamaioasa Romaneasca": 2, "Feteasca Alba": 3},
    "PM resistance": {"Muscat Ottonel (main)": 2, "Zghihara de Husi": 5, "Busuioaca de Bohotin": 2,
                      "Tamaioasa Romaneasca": 2, "Feteasca Alba": 3},
    "Husi authenticity": {"Muscat Ottonel (main)": 4, "Zghihara de Husi": 5, "Busuioaca de Bohotin": 5,
                          "Tamaioasa Romaneasca": 3, "Feteasca Alba": 3},
}

attrs = list(attr_map.keys())
var_names = ["Muscat Ottonel (main)", "Zghihara de Husi", "Busuioaca de Bohotin"]
var_colors = [PALETTE[0], PALETTE[1], ACCENT]

fig, axes = plt.subplots(1, len(var_names), figsize=(14, 5), sharey=True)
for ax, var, color in zip(axes, var_names, var_colors):
    scores = [attr_map[a][var] for a in attrs]
    ax.barh(attrs, scores, color=color, alpha=0.8)
    ax.set_xlim(0, 5.5)
    ax.set_title(var, fontsize=9, fontweight="bold", wrap=True)
    ax.bar_label(ax.containers[0], fmt="%g", padding=2, fontsize=8)
    for i, s in enumerate(scores):
        pass

fig.suptitle("Variety Comparison — Key Agronomic & Commercial Attributes (1–5 scale)", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Score (1=low, 5=high)")
savefig("07_variety_comparison.png")


# ── Chart 8: Grafting vs replanting cost comparison ──────────────────────────
conv = pd.read_csv(os.path.join(DATA_DIR, "variety_conversion_costs.csv"))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Cost range
methods = conv["method"].str.replace(" / ", "\n").str.replace(" (all-in)", "\n(all-in)")
mins = conv["cost_per_ha_min_eur"]
maxs = conv["cost_per_ha_max_eur"]
mids = (mins + maxs) / 2
ranges = maxs - mins

bars = axes[0].bar(methods, mids, yerr=ranges / 2, capsize=6,
                   color=[PALETTE[1], PALETTE[0]], width=0.5)
axes[0].bar_label(bars, fmt="€%.0f avg", padding=6, fontsize=8)
axes[0].set_title("Cost per Hectare (€)", fontsize=10, fontweight="bold")
axes[0].set_ylabel("€/ha")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"€{int(x):,}"))

# Years to commercial crop
bars2 = axes[1].bar(methods, conv["years_to_commercial_crop"],
                    color=[PALETTE[1], PALETTE[0]], width=0.5)
axes[1].bar_label(bars2, fmt="%g years", padding=4, fontsize=8)
axes[1].set_title("Years to Commercial Crop", fontsize=10, fontweight="bold")
axes[1].set_ylabel("Years")

fig.suptitle("Variety Conversion Options — Cost vs Timeline", fontsize=12, fontweight="bold")
savefig("08_variety_conversion_costs.png")


# ── Chart 9: Monthly rainfall with growing season highlighted ────────────────
fig, ax = plt.subplots(figsize=(12, 5))
bar_colors_rain = []
for _, row in clim.iterrows():
    if row["month"] in ["May", "June"]:
        bar_colors_rain.append(ACCENT)
    elif row["month_num"] in range(4, 10):
        bar_colors_rain.append(PALETTE[1])
    else:
        bar_colors_rain.append(PALETTE[0])

bars = ax.bar(months, clim["precip_mm"], color=bar_colors_rain)
ax.bar_label(bars, fmt="%g mm", padding=3, fontsize=8)

ax.set_title("Huși Monthly Rainfall — Disease Risk Context\n(Red = critical DM infection period; green = growing season; blue = dormant season)",
             fontsize=11, fontweight="bold", pad=12)
ax.set_ylabel("Precipitation (mm)")
ax.axhline(clim["precip_mm"].mean(), color="#aaa", linestyle="--",
           label=f"Monthly average ({clim['precip_mm'].mean():.0f} mm)")
ax.legend(fontsize=8)

dm_patch = mpatches.Patch(color=ACCENT, label="May–June: critical downy mildew risk")
gs_patch = mpatches.Patch(color=PALETTE[1], label="Growing season (Apr–Sep)")
ds_patch = mpatches.Patch(color=PALETTE[0], label="Dormant season")
ax.legend(handles=[dm_patch, gs_patch, ds_patch], fontsize=8)
savefig("09_monthly_rainfall_disease_risk.png")

print("\nAll charts written to:", CHARTS_DIR)
