"""
Generate charts for Module 4 — Winemaking Technology.

Run: python3 scripts/create_charts.py
Output: ../charts/*.png
Requires: matplotlib, pandas, numpy
"""

import os
import warnings

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

BLUE    = "#2c5f8a"
GREEN   = "#4a7c59"
AMBER   = "#d4891a"
RED     = "#a63d2f"
PURPLE  = "#6b4f8a"
GREY    = "#6b7280"
LBLUE   = "#7ab3d4"
LGREEN  = "#93c4a0"
LGREY   = "#d1d5db"


def save(fig, name):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {name}")


# ── Chart 1: Winery zone space requirements (horizontal bar) ─────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "winery_zone_space.csv"))
fig, ax = plt.subplots(figsize=(10, 6))
zones = df["zone"]
y = np.arange(len(zones))
ax.barh(y, df["area_max_m2"] - df["area_min_m2"],
        left=df["area_min_m2"], color=LBLUE, height=0.55, label="Range")
ax.barh(y, df["area_min_m2"], color=BLUE, height=0.55, label="Minimum")
ax.set_yticks(y)
ax.set_yticklabels(zones, fontsize=9)
ax.set_xlabel("Area (m²)")
ax.set_title("Winery Zone Space Requirements (300–400 m² total target)", fontsize=12, fontweight="bold")
ax.axvline(0, color="black", linewidth=0.5)
for i, row in df.iterrows():
    ax.text(row["area_max_m2"] + 1, i, f"{row['area_min_m2']}–{row['area_max_m2']} m²",
            va="center", fontsize=8, color=GREY)
ax.legend(loc="lower right", fontsize=9)
ax.set_xlim(0, 175)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "01_winery_zone_space.png")


# ── Chart 2: Shed conversion cost breakdown (stacked bar) ────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "shed_conversion_costs.csv"))
fig, ax = plt.subplots(figsize=(11, 6))
categories = [c.replace(" (", "\n(") for c in df["work_category"]]
x = np.arange(len(categories))
width = 0.5
ax.bar(x, df["cost_eur_m2_min"], width, color=BLUE, label="Low estimate")
ax.bar(x, df["cost_eur_m2_max"] - df["cost_eur_m2_min"],
       width, bottom=df["cost_eur_m2_min"], color=LBLUE, label="High estimate")
for i, row in df.iterrows():
    ax.text(i, row["cost_eur_m2_max"] + 2, f"€{row['cost_eur_m2_max']}/m²",
            ha="center", fontsize=8, color=GREY)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=7.5, ha="center")
ax.set_ylabel("Cost (€/m²)")
ax.set_title("Shed Conversion Cost by Category (€/m²)\nTotal: €175–405/m² → €60k–140k for 300–400 m²",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "02_shed_conversion_costs.png")


# ── Chart 3: Three-phase CAPEX waterfall ─────────────────────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "capex_by_phase.csv"))
phase_totals = df.groupby("phase")[["cost_low_eur", "cost_high_eur"]].sum()
phase_mid = ((phase_totals["cost_low_eur"] + phase_totals["cost_high_eur"]) / 2).values
phases = ["Phase 1\n(Year 1)", "Phase 2\n(Year 2)", "Phase 3\n(Year 3)"]
colors = [BLUE, GREEN, AMBER]
cumulative = np.cumsum([0] + list(phase_mid[:-1]))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

# Waterfall
for i, (phase, cum, mid) in enumerate(zip(phases, cumulative, phase_mid)):
    ax1.bar(i, mid, bottom=cum, color=colors[i], width=0.5, zorder=3, label=phases[i])
    ax1.text(i, cum + mid / 2, f"€{mid/1000:.0f}k", ha="center", va="center",
             color="white", fontweight="bold", fontsize=10)
    ax1.text(i, cum + mid + 3000, f"Cumulative: €{(cum + mid)/1000:.0f}k",
             ha="center", fontsize=8, color=GREY)

total_line = sum(phase_mid)
ax1.axhline(total_line, color=RED, linestyle="--", linewidth=1.5, zorder=4)
ax1.text(2.4, total_line + 2000, f"Total ~€{total_line/1000:.0f}k", color=RED, fontsize=9)
ax1.set_xticks(range(3))
ax1.set_xticklabels(phases)
ax1.set_ylabel("Cumulative Investment (€)")
ax1.set_title("3-Year CAPEX Waterfall\n(Mid-range estimates)", fontsize=11, fontweight="bold")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Phase breakdown horizontal bars
phase_data = df.groupby("phase").apply(
    lambda g: (g["cost_low_eur"].sum(), g["cost_high_eur"].sum())
).reset_index()
phase_labels = ["Phase 1", "Phase 2", "Phase 3"]
lows = [phase_data.iloc[i][0][0] for i in range(3)]
highs = [phase_data.iloc[i][0][1] for i in range(3)]
y = np.arange(3)
ax2.barh(y, [h - l for h, l in zip(highs, lows)], left=lows,
         color=[c + "80" for c in [BLUE, GREEN, AMBER]], height=0.5)
ax2.barh(y, lows, color=[BLUE, GREEN, AMBER], height=0.5)
for i, (lo, hi) in enumerate(zip(lows, highs)):
    ax2.text(hi + 1500, i, f"€{lo/1000:.0f}k – €{hi/1000:.0f}k",
             va="center", fontsize=9, color=GREY)
ax2.set_yticks(y)
ax2.set_yticklabels(phase_labels)
ax2.set_xlabel("Investment (€)")
ax2.set_title("Phase Spend Range\n(Low–High estimates)", fontsize=11, fontweight="bold")
ax2.set_xlim(0, max(highs) * 1.35)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "03_capex_three_phase.png")


# ── Chart 4: Top equipment capex breakdown (Phase 1 + 2 key items) ───────────
df = pd.read_csv(os.path.join(DATA_DIR, "capex_by_phase.csv"))
key_items = df[df["phase"].isin([1, 2])].copy()
key_items["mid"] = (key_items["cost_low_eur"] + key_items["cost_high_eur"]) / 2
key_items = key_items.sort_values("mid", ascending=True).tail(12)
fig, ax = plt.subplots(figsize=(12, 7))
colors_map = {1: BLUE, 2: GREEN}
bar_colors = [colors_map[p] for p in key_items["phase"]]
bars = ax.barh(range(len(key_items)), key_items["mid"], color=bar_colors, height=0.65)
for i, row in enumerate(key_items.itertuples()):
    ax.text(row.mid + 500, i,
            f"€{row.cost_low_eur/1000:.0f}k–€{row.cost_high_eur/1000:.0f}k",
            va="center", fontsize=8, color=GREY)
labels = [t[:45] + "…" if len(t) > 45 else t for t in key_items["item"]]
ax.set_yticks(range(len(key_items)))
ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("Mid-range Estimate (€)")
ax.set_title("Key Equipment Items — Phase 1 & 2\n(sorted by estimated cost)", fontsize=11, fontweight="bold")
p1_patch = mpatches.Patch(color=BLUE, label="Phase 1 (Year 1)")
p2_patch = mpatches.Patch(color=GREEN, label="Phase 2 (Year 2)")
ax.legend(handles=[p1_patch, p2_patch], fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(0, key_items["mid"].max() * 1.35)
plt.tight_layout()
save(fig, "04_equipment_cost_breakdown.png")


# ── Chart 5: Packaging cost per bottle (stacked bar) ─────────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "packaging_cost_per_bottle.csv"))
fig, ax = plt.subplots(figsize=(9, 6))
items = df["item"]
mids = (df["cost_min_eur"] + df["cost_max_eur"]) / 2
bar_colors = [BLUE, GREEN, AMBER, PURPLE, GREY]
bottom = 0
for i, (item, mid) in enumerate(zip(items, mids)):
    ax.bar(0, mid, bottom=bottom, color=bar_colors[i], width=0.4, label=item)
    if mid > 0.02:
        ax.text(0, bottom + mid / 2, f"€{mid:.2f}", ha="center", va="center",
                color="white", fontsize=10, fontweight="bold")
    bottom += mid

total_mid = mids.sum()
ax.text(0, total_mid + 0.03, f"Total: €{total_mid:.2f}/bottle", ha="center",
        fontsize=11, fontweight="bold", color="black")

# Add range annotation
total_min = df["cost_min_eur"].sum()
total_max = df["cost_max_eur"].sum()
ax.text(0, -0.12, f"Range: €{total_min:.2f} – €{total_max:.2f}/bottle",
        ha="center", fontsize=9, color=GREY)

ax.set_xlim(-0.5, 0.7)
ax.set_ylim(-0.2, total_mid + 0.25)
ax.set_xticks([])
ax.set_ylabel("Cost per Bottle (€)")
ax.set_title("Packaging Cost per Bottle\n(Mid-range breakdown)", fontsize=12, fontweight="bold")
ax.legend(loc="upper right", fontsize=8, bbox_to_anchor=(1.45, 1.0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
plt.tight_layout()
save(fig, "05_packaging_cost_per_bottle.png")


# ── Chart 6: Tank configuration — total HL by size ───────────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "tank_configuration.csv"))
fig, axes = plt.subplots(1, 2, figsize=(13, 6))

# Pie: total HL by tank size
ax = axes[0]
labels = [f"{row['capacity_hl']} hl × {row['quantity']}" for _, row in df.iterrows()]
values = df["total_hl"]
explode = [0.05] * len(values)
wedge_colors = [BLUE, GREEN, AMBER, PURPLE, GREY][:len(values)]
wedges, texts, autotexts = ax.pie(
    values, labels=labels, autopct="%1.0f%%", colors=wedge_colors,
    explode=explode, startangle=90
)
for t in autotexts:
    t.set_fontsize(9)
ax.set_title("Tank Configuration\n(% of total 450 hl working capacity)", fontsize=11, fontweight="bold")

# Bar: price range by tank capacity
ax2 = axes[1]
x = np.arange(len(df))
width = 0.4
ax2.bar(x - width/2, df["price_new_min_eur"], width, color=BLUE, label="New (min)")
ax2.bar(x + width/2, df["price_new_max_eur"], width, color=LBLUE, label="New (max)")
used_mid = ((df["price_new_min_eur"] + df["price_new_max_eur"]) / 2 * 0.40)
ax2.bar(x, used_mid, width * 0.6, color=GREEN, alpha=0.8, label="Used (~40% of new)")
ax2.set_xticks(x)
ax2.set_xticklabels([f"{c} hl" for c in df["capacity_hl"]])
ax2.set_ylabel("Price per Tank (€)")
ax2.set_title("Tank Price Range by Capacity\n(new vs. used estimate)", fontsize=11, fontweight="bold")
ax2.legend(fontsize=9)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "06_tank_configuration.png")


# ── Chart 7: Grant leverage scenarios ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
scenarios = ["No grant\n(self-funded)", "IS-V-02\n(50% grant)", "DR-23\n(65% grant)"]
total_investment = 170000
grant_rates = [0, 0.50, 0.65]
eligible_fraction = 0.70  # ~70% of total investment is grant-eligible (equipment+conversion)

eligible = total_investment * eligible_fraction
own_cash = [total_investment - (eligible * r) for r in grant_rates]
grant_amounts = [eligible * r for r in grant_rates]

x = np.arange(len(scenarios))
bars_own = ax.bar(x, own_cash, color=BLUE, width=0.5, label="Own investment (€)")
bars_grant = ax.bar(x, grant_amounts, bottom=own_cash, color=GREEN, width=0.5, label="Grant received (€)")

for i, (own, grant) in enumerate(zip(own_cash, grant_amounts)):
    ax.text(i, own / 2, f"€{own/1000:.0f}k", ha="center", va="center",
            color="white", fontweight="bold", fontsize=10)
    if grant > 0:
        ax.text(i, own + grant / 2, f"€{grant/1000:.0f}k grant",
                ha="center", va="center", color="white", fontweight="bold", fontsize=10)
    ax.text(i, total_investment + 3000, f"Net own: €{own/1000:.0f}k",
            ha="center", fontsize=9, color=GREY)

ax.axhline(total_investment, color=RED, linestyle="--", linewidth=1.2)
ax.text(2.4, total_investment + 1500, f"Total project: €{total_investment/1000:.0f}k", color=RED, fontsize=9)
ax.set_xticks(x)
ax.set_xticklabels(scenarios, fontsize=10)
ax.set_ylabel("Investment (€)")
ax.set_title(
    "Grant Leverage: Own Investment Required by Scenario\n(€170k total mid-range; 70% eligible for grant)",
    fontsize=11, fontweight="bold"
)
ax.legend(fontsize=9)
ax.set_ylim(0, total_investment * 1.15)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "07_grant_leverage_scenarios.png")


# ── Chart 8: Filtration options — capex vs. aroma impact ─────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "filtration_options.csv"))
df = df[df["capex_max_eur"] > 0].copy()  # exclude cold settling (no equipment)
aroma_impact = {"None": 0, "Minimal": 1, "Low": 2, "Medium": 3, "High": 4}
df["aroma_score"] = df["aroma_stripping"].map(aroma_impact)
df["capex_mid"] = (df["capex_min_eur"] + df["capex_max_eur"]) / 2

fig, ax = plt.subplots(figsize=(10, 6))
colors_rec = [GREEN if r else GREY for r in df["recommended"]]
scatter = ax.scatter(df["aroma_score"], df["capex_mid"], c=colors_rec,
                     s=200, zorder=5, edgecolors="white", linewidths=1.5)

for _, row in df.iterrows():
    ax.annotate(row["method"],
                xy=(row["aroma_score"], row["capex_mid"]),
                xytext=(8, 0), textcoords="offset points",
                fontsize=8, va="center")

ax.set_xticks([0, 1, 2, 3, 4])
ax.set_xticklabels(["None", "Minimal", "Low", "Medium", "High"])
ax.set_xlabel("Aroma Stripping Risk")
ax.set_ylabel("Capital Cost (€)")
ax.set_title("Filtration Options: Aroma Impact vs. Capital Cost\n(green = recommended at this scale)",
             fontsize=11, fontweight="bold")
rec_patch = mpatches.Patch(color=GREEN, label="Recommended")
not_patch = mpatches.Patch(color=GREY, label="Not recommended at this scale")
ax.legend(handles=[rec_patch, not_patch], fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "08_filtration_options.png")


# ── Chart 9: Winemaking temperature zones ────────────────────────────────────
zones = [
    ("Cold stabilisation\n(−4 to −1°C)", -4, -1),
    ("Post-ferment cold settling\n(4–8°C)", 4, 8),
    ("White wine fermentation\n(14–16°C optimal)", 12, 18),
    ("Storage tanks\n(12–15°C)", 12, 15),
    ("Bottle storage\n(12–15°C)", 12, 15),
]
fig, ax = plt.subplots(figsize=(11, 6))
y_pos = list(range(len(zones)))
zone_colors = [PURPLE, LBLUE, GREEN, BLUE, AMBER]
for i, (label, lo, hi) in enumerate(zones):
    ax.barh(i, hi - lo, left=lo, color=zone_colors[i], height=0.55, alpha=0.85)
    mid = (lo + hi) / 2
    ax.text(hi + 0.3, i, f"{lo}°C – {hi}°C", va="center", fontsize=9, color=GREY)

ax.axvline(14, color=RED, linestyle="--", linewidth=1.5, label="14°C — lower Muscat Ottonel ferment target")
ax.axvline(16, color=AMBER, linestyle="--", linewidth=1.5, label="16°C — upper Muscat Ottonel ferment target")

ax.set_yticks(y_pos)
ax.set_yticklabels([z[0] for z in zones], fontsize=9)
ax.set_xlabel("Temperature (°C)")
ax.set_title("Winery Temperature Zones for Muscat Ottonel\n(14–16°C fermentation critical for terpene preservation)",
             fontsize=11, fontweight="bold")
ax.legend(loc="lower right", fontsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "09_temperature_zones.png")


print(f"\nAll charts written to: {CHARTS_DIR}")
