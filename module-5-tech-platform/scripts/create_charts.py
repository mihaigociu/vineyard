"""
Generate charts for Module 5 — Tech & Software Platform.

Run: python3 scripts/create_charts.py
Output: ../charts/*.png
Requires: matplotlib, pandas, numpy
"""

import os
import warnings

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "..", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

BLUE   = "#2c5f8a"
GREEN  = "#4a7c59"
AMBER  = "#d4891a"
RED    = "#a63d2f"
PURPLE = "#6b4f8a"
GREY   = "#6b7280"
LBLUE  = "#7ab3d4"
LGREEN = "#93c4a0"
LGREY  = "#d1d5db"


def save(fig, name):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {name}")


# ── Chart 1: System architecture diagram (block diagram) ─────────────────────
fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")
ax.set_facecolor("#f8fafc")
fig.patch.set_facecolor("#f8fafc")

def box(ax, x, y, w, h, label, sublabel="", color=BLUE, fontsize=9):
    rect = mpatches.FancyBboxPatch((x, y), w, h,
        boxstyle="round,pad=0.1", facecolor=color, edgecolor="white",
        linewidth=1.5, alpha=0.9, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2 + (0.12 if sublabel else 0), label,
            ha="center", va="center", fontsize=fontsize,
            color="white", fontweight="bold", zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.22, sublabel,
                ha="center", va="center", fontsize=7, color="white", alpha=0.9, zorder=4)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3),
                zorder=2)

# Layer labels
for y, label, col in [(7.5, "FIELD LAYER", BLUE), (4.8, "EDGE LAYER (winery mini-PC)", GREEN),
                       (2.0, "CLOUD LAYER", PURPLE), (0.35, "SATELLITE", AMBER)]:
    ax.text(0.2, y, label, fontsize=8, color=col, fontweight="bold", alpha=0.7)
    ax.axhline(y - 0.08, color=col, linewidth=0.6, alpha=0.3, xmin=0.01, xmax=0.99)

# Field sensors
box(ax, 0.3, 6.1, 2.2, 1.0, "ESP32+LoRa Nodes", "×5 rows, 15-min interval", BLUE)
box(ax, 2.8, 6.1, 2.2, 1.0, "Dragino LSE01", "Soil VWC+T+EC, LoRaWAN", BLUE)
box(ax, 5.3, 6.1, 2.2, 1.0, "Davis VP2 Station", "T/RH/rain/wind/leaf wet", BLUE)
box(ax, 7.8, 6.1, 2.2, 1.0, "iSpindel × tanks", "Gravity+T, WiFi MQTT", BLUE)
box(ax, 10.3, 6.1, 2.2, 1.0, "RAK7289CV2 Gateway", "LoRaWAN → 4G MQTT", GREEN, fontsize=8)

# Arrows field → gateway / broker
arrow(ax, 1.4, 6.1, 10.9, 7.1)
arrow(ax, 3.9, 6.1, 10.9, 7.1)
arrow(ax, 6.4, 6.1, 10.9, 7.1)
arrow(ax, 8.9, 6.1, 10.0, 5.6)
arrow(ax, 11.4, 6.1, 11.4, 5.6)

# Edge layer
box(ax, 0.3, 4.0, 2.5, 1.1, "Mosquitto MQTT", "Broker; all feeds", GREEN)
box(ax, 3.1, 4.0, 2.5, 1.1, "Telegraf", "MQTT → TimescaleDB", GREEN)
box(ax, 5.9, 4.0, 2.8, 1.1, "TimescaleDB", "sensor + vineyard records", GREEN)
box(ax, 9.0, 4.0, 2.0, 1.1, "Grafana", "Dashboards + alerts", AMBER)
box(ax, 11.3, 4.0, 2.2, 1.1, "FastAPI\nStreamlit", "API + owner dashboard", PURPLE)

arrow(ax, 2.8, 4.55, 3.1, 4.55)
arrow(ax, 5.6, 4.55, 5.9, 4.55)
arrow(ax, 8.7, 4.55, 9.0, 4.55)
arrow(ax, 10.85, 4.55, 11.3, 4.55)

# Cloud layer
box(ax, 2.5, 1.2, 2.5, 1.1, "Hetzner CX22", "Off-site backup\n€3.49/mo", PURPLE, fontsize=8)
box(ax, 5.5, 1.2, 2.5, 1.1, "Tailscale", "Mesh VPN; remote access\nFree tier", PURPLE, fontsize=8)
box(ax, 8.5, 1.2, 2.5, 1.1, "Telegram Bot", "Alerts to phone\nFree", PURPLE, fontsize=8)

arrow(ax, 5.9, 4.0, 3.75, 2.3)
arrow(ax, 5.9, 4.0, 6.75, 2.3)
arrow(ax, 9.0, 4.0, 9.75, 2.3)

# Satellite
box(ax, 0.3, 0.2, 3.5, 0.95, "CDSE Sentinel-2 (weekly batch)", "NDVI per block → TimescaleDB", AMBER, fontsize=8)
arrow(ax, 2.05, 1.15, 5.9, 4.0)

ax.set_title("Vineyard Tech Platform — System Architecture",
             fontsize=13, fontweight="bold", pad=10, color="#1f2937")
plt.tight_layout()
save(fig, "01_system_architecture.png")


# ── Chart 2: Hardware budget tier 1 vs tier 2 ────────────────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "hardware_budget.csv"))
fig, axes = plt.subplots(1, 2, figsize=(13, 6))

for ax, tier in zip(axes, [1, 2]):
    sub = df[df["tier"] == tier].copy()
    sub = sub.sort_values("total_eur", ascending=True)
    colors = [GREEN if p == "Critical" else BLUE if p == "High" else GREY
              for p in sub["priority"]]
    bars = ax.barh(range(len(sub)), sub["total_eur"], color=colors, height=0.65)
    for i, (_, row) in enumerate(sub.iterrows()):
        ax.text(row["total_eur"] + 5, i, f"€{row['total_eur']:.0f}",
                va="center", fontsize=8, color=GREY)
    ax.set_yticks(range(len(sub)))
    labels = [t[:38] + "…" if len(t) > 38 else t for t in sub["item"]]
    ax.set_yticklabels(labels, fontsize=8)
    total = sub["total_eur"].sum()
    ax.set_title(f"Tier {tier} Hardware (Year {tier})\nTotal: €{total:,.0f}",
                 fontsize=11, fontweight="bold")
    ax.set_xlabel("Cost (€)")
    ax.set_xlim(0, sub["total_eur"].max() * 1.3)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

crit_p = mpatches.Patch(color=GREEN, label="Critical")
high_p = mpatches.Patch(color=BLUE, label="High")
med_p  = mpatches.Patch(color=GREY, label="Medium / Low")
axes[1].legend(handles=[crit_p, high_p, med_p], fontsize=8, loc="lower right")
plt.tight_layout()
save(fig, "02_hardware_budget.png")


# ── Chart 3: Monthly operational costs breakdown ──────────────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "monthly_operational_costs.csv"))
df["mid"] = (df["monthly_cost_eur_min"] + df["monthly_cost_eur_max"]) / 2
fig, ax = plt.subplots(figsize=(10, 5))
paid = df[df["mid"] > 0].copy()
free = df[df["mid"] == 0].copy()

colors = [BLUE, GREEN, PURPLE]
ax.barh(range(len(paid)), paid["mid"], color=colors[:len(paid)], height=0.55)
for i, row in enumerate(paid.itertuples()):
    ax.text(row.mid + 0.1, i, f"€{row.monthly_cost_eur_min:.2f}–€{row.monthly_cost_eur_max:.2f}/mo",
            va="center", fontsize=9, color=GREY)
ax.set_yticks(range(len(paid)))
ax.set_yticklabels([t[:45] for t in paid["item"]], fontsize=9)

total_min = df["monthly_cost_eur_min"].sum()
total_max = df["monthly_cost_eur_max"].sum()
ax.axvline(total_max, color=RED, linestyle="--", linewidth=1.2)
ax.text(total_max + 0.1, len(paid) - 0.5,
        f"Total max: €{total_max:.2f}/mo\n(€{total_max*12:.0f}/yr)",
        color=RED, fontsize=9)

free_items = ", ".join(free["item"].tolist())
ax.text(0.5, -0.9, f"Free (€0): {free_items}",
        ha="left", fontsize=7.5, color=GREY,
        transform=ax.get_yaxis_transform())

ax.set_xlabel("Monthly Cost (€)")
ax.set_title("Monthly Operational Costs (Platform)\nPaid items only; grey = free tier",
             fontsize=11, fontweight="bold")
ax.set_xlim(0, total_max * 1.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "03_monthly_operational_costs.png")


# ── Chart 4: Simulated fermentation curve (iSpindel output) ──────────────────
np.random.seed(42)
days = np.linspace(0, 14, 200)
og = 1.095
fg = 0.994
k = 0.55  # fermentation rate constant
sg = fg + (og - fg) * np.exp(-k * days)
sg += np.random.normal(0, 0.0005, len(days))
temp = 15.5 + 1.5 * np.sin(days * 0.8) + np.random.normal(0, 0.2, len(days))
abv = (og - sg) * 131.25

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

ax1.plot(days, sg, color=BLUE, linewidth=2, label="Specific Gravity (iSpindel)")
ax1.axhline(fg + 0.005, color=RED, linestyle="--", linewidth=1, alpha=0.7, label="Target FG ≈ 0.994 (dry wine)")
ax1.axhline(1.010, color=AMBER, linestyle=":", linewidth=1, label="SG 1.010 — stuck ferment alert threshold")
ax1.set_ylabel("Specific Gravity")
ax1.set_ylim(0.985, 1.105)
ax1.legend(fontsize=8, loc="upper right")
ax1.set_title("Simulated Fermentation Monitoring — iSpindel Output\n(Muscat Ottonel, OG ~1.095, dry style)",
              fontsize=11, fontweight="bold")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax2_twin = ax2.twinx()
ax2.plot(days, temp, color=GREEN, linewidth=1.5, label="Temperature (°C)")
ax2.axhline(14, color=LBLUE, linestyle="--", linewidth=1, alpha=0.7)
ax2.axhline(16, color=LBLUE, linestyle="--", linewidth=1, alpha=0.7)
ax2.fill_between(days, 14, 16, alpha=0.1, color=LBLUE, label="14–16°C optimal range")
ax2_twin.plot(days, abv, color=AMBER, linewidth=1.5, linestyle="--", label="Est. ABV (%)")
ax2.set_ylabel("Temperature (°C)", color=GREEN)
ax2_twin.set_ylabel("Estimated ABV (%)", color=AMBER)
ax2.set_xlabel("Days since inoculation")
ax2.set_ylim(12, 22)
ax2_twin.set_ylim(0, 15)
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="center right")
ax2.spines["top"].set_visible(False)

ax1.axvline(13, color=RED, linestyle=":", alpha=0.5)
ax2.axvline(13, color=RED, linestyle=":", alpha=0.5)
ax1.text(13.1, 1.015, "Fermentation\ncomplete", fontsize=7.5, color=RED, alpha=0.8)
plt.tight_layout()
save(fig, "04_fermentation_simulation.png")


# ── Chart 5: GDD phenology calendar ──────────────────────────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "phenology_gdd_thresholds.csv"))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))

# GDD ranges
y = np.arange(len(df))
colors = [BLUE, BLUE, GREEN, GREEN, GREEN, AMBER, RED]
for i, row in df.iterrows():
    ax1.barh(i, row["cgdd_max"] - row["cgdd_min"],
             left=row["cgdd_min"], color=colors[i], height=0.55, alpha=0.85)
    ax1.text(row["cgdd_max"] + 10, i,
             f"{row['cgdd_min']}–{row['cgdd_max']} GDD",
             va="center", fontsize=8, color=GREY)
ax1.set_yticks(y)
ax1.set_yticklabels(df["stage"], fontsize=9)
ax1.set_xlabel("Cumulative Growing Degree Days (base 10°C, from April 1)")
ax1.set_title("Muscat Ottonel Phenology\nvs. Growing Degree Days at Huși",
              fontsize=11, fontweight="bold")
ax1.set_xlim(0, 1800)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Simulated GDD accumulation curve
month_days = np.linspace(0, 180, 180)  # April 1 to Sep 27
daily_gdd = np.clip(
    18 + 4 * np.sin(month_days / 180 * np.pi) + np.random.normal(0, 1.5, 180),
    0, None
)
cgdd = np.cumsum(daily_gdd)
ax2.plot(month_days, cgdd, color=BLUE, linewidth=2.5)

months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
month_ticks = [0, 30, 61, 91, 122, 153]
ax2.set_xticks(month_ticks)
ax2.set_xticklabels(months)

stage_colors = [BLUE, BLUE, GREEN, GREEN, GREEN, AMBER, RED]
for i, row in df.iterrows():
    mid_gdd = (row["cgdd_min"] + row["cgdd_max"]) / 2
    close = np.argmin(np.abs(cgdd - mid_gdd))
    ax2.axhline(mid_gdd, color=stage_colors[i], linestyle="--", alpha=0.4, linewidth=0.8)
    ax2.text(close, mid_gdd + 10, row["stage"].split("(")[0].strip(),
             fontsize=7, color=stage_colors[i], alpha=0.85)

ax2.set_xlabel("Month (approximate)")
ax2.set_ylabel("Cumulative GDD (base 10°C)")
ax2.set_title("Simulated GDD Accumulation\n(Huși typical season)",
              fontsize=11, fontweight="bold")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "05_phenology_gdd_calendar.png")


# ── Chart 6: Disease risk model output (simulated) ───────────────────────────
np.random.seed(7)
n = 120  # days May–Aug
dates = pd.date_range("2026-05-01", periods=n)
rain = np.where(np.random.random(n) < 0.3, np.random.exponential(8, n), 0)
risk = np.where(rain > 2.0, 4,
       np.where((rain > 0.5) & (np.random.random(n) > 0.4), 3,
       np.where(rain > 0, 1, 0)))
risk = np.convolve(risk, [0.2, 0.6, 0.2], mode="same").clip(0, 4)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
ax1.bar(dates, rain, color=BLUE, alpha=0.7, width=0.9, label="Rainfall (mm)")
ax1.set_ylabel("Rainfall (mm/day)")
ax1.legend(fontsize=9)
ax1.set_title("Simulated Disease Risk Model Output — Plasmopara Viticola (Downy Mildew)\nHuși, May–August (Python model on Open-Meteo data)",
              fontsize=11, fontweight="bold")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

risk_colors = {0: LGREEN, 1: LBLUE, 2: AMBER, 3: RED, 4: PURPLE}
for i, (d, r) in enumerate(zip(dates, risk)):
    c = risk_colors[min(int(r), 4)]
    ax2.bar(d, r, color=c, width=0.9, alpha=0.85)
ax2.axhline(3, color=RED, linestyle="--", linewidth=1.2, label="Spray threshold (risk ≥ 3)")
ax2.set_ylim(0, 5)
ax2.set_yticks([0, 1, 2, 3, 4])
ax2.set_yticklabels(["0 None", "1 Low", "2 Moderate", "3 High", "4 Critical"])
ax2.set_ylabel("Disease Pressure (0–4)")
ax2.legend(fontsize=9)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# Add legend patches
for val, label, col in [(0, "0 None", LGREEN), (1, "1 Low", LBLUE),
                         (2, "2 Moderate", AMBER), (3, "3 High", RED),
                         (4, "4 Critical", PURPLE)]:
    pass  # already on y axis
plt.tight_layout()
save(fig, "06_disease_risk_model.png")


# ── Chart 7: IoT connectivity comparison (radar / bar) ───────────────────────
df = pd.read_csv(os.path.join(DATA_DIR, "connectivity_options.csv"))
fig, ax = plt.subplots(figsize=(10, 5))
labels = df["protocol"]
x = np.arange(len(labels))
width = 0.25

# Normalised scores: range (log scale), power efficiency, cost efficiency
range_score = np.log10(df["range_m_max"]) / np.log10(50000) * 5
power_map = {"High (100-300mW)": 1, "Medium (200mW TX)": 2,
             "Very low (10-50mW)": 5, "None (passive)": 5}
power_score = [power_map[p] for p in df["power_draw"]]
cost_score = [5, 2, 5, 5]  # WiFi free, 4G costs, LoRa gateway low monthly, Ethernet free

bars1 = ax.bar(x - width, range_score, width, color=BLUE, label="Range (normalised)")
bars2 = ax.bar(x, power_score, width, color=GREEN, label="Power efficiency (1=high, 5=low)")
bars3 = ax.bar(x + width, cost_score, width, color=AMBER, label="Cost efficiency (5=cheapest)")

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("Score (0–5)")
ax.set_ylim(0, 6.5)
ax.set_title("Connectivity Options: Range / Power / Cost Comparison\n(LoRaWAN 868 optimal for outdoor 10 ha multi-node network)",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.axvline(1.5, color=LGREY, linewidth=1.5)
ax.text(2.0, 6.0, "← Winery only | Field network →", ha="center", fontsize=8.5, color=GREY)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "07_connectivity_comparison.png")


# ── Chart 8: NDVI simulated vineyard block map ───────────────────────────────
np.random.seed(12)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Simulated NDVI grid for 10 ha vineyard
grid = np.random.uniform(0.45, 0.80, (20, 20))
# Add a stressed zone (e.g. block 3 bottom-left with drought or disease)
grid[13:18, 2:7] = np.random.uniform(0.22, 0.40, (5, 5))
# Add a very healthy zone
grid[2:7, 12:17] = np.random.uniform(0.72, 0.82, (5, 5))

im = axes[0].imshow(grid, cmap="RdYlGn", vmin=0.2, vmax=0.85, aspect="equal")
axes[0].set_title("Simulated Sentinel-2 NDVI Map\n10 ha Vineyard at Huși (single acquisition)",
                  fontsize=10, fontweight="bold")
axes[0].set_xlabel("← West    East →")
axes[0].set_ylabel("← South    North →")
axes[0].set_xticks([0, 5, 10, 15, 19])
axes[0].set_xticklabels(["0m", "50m", "100m", "150m", "190m"], fontsize=8)
axes[0].set_yticks([0, 5, 10, 15, 19])
axes[0].set_yticklabels(["0m", "50m", "100m", "150m", "190m"], fontsize=8)
cbar = plt.colorbar(im, ax=axes[0], shrink=0.85)
cbar.set_label("NDVI", fontsize=9)

# Annotate stressed zone
axes[0].add_patch(mpatches.Rectangle((1.5, 12.5), 5, 5, fill=False,
                                      edgecolor=RED, linewidth=2, linestyle="--"))
axes[0].text(4, 18.3, "⚠ Low NDVI block\n→ inspection flag", ha="center",
             fontsize=7.5, color=RED, fontweight="bold")

# NDVI trend over season for 3 blocks
days2 = np.linspace(0, 200, 50)
block_a = 0.15 + 0.65 * np.sin(np.pi * days2 / 200) ** 0.5 + np.random.normal(0, 0.02, 50)
block_b = 0.10 + 0.55 * np.sin(np.pi * days2 / 200) ** 0.5 + np.random.normal(0, 0.02, 50)
block_c = 0.12 + 0.70 * np.sin(np.pi * days2 / 200) ** 0.5 + np.random.normal(0, 0.02, 50)
# Simulate stress event in block B from day 100
block_b[25:] -= np.linspace(0, 0.22, 25)
block_b[25:] = block_b[25:].clip(0.1)

axes[1].plot(days2, block_a, color=GREEN, linewidth=2, label="Block A (healthy)")
axes[1].plot(days2, block_b, color=RED, linewidth=2, label="Block B (stress event ~day 100)")
axes[1].plot(days2, block_c, color=BLUE, linewidth=2, label="Block C (healthy)")
axes[1].axhline(0.30, color=AMBER, linestyle="--", linewidth=1.2, label="Alert threshold (NDVI < 0.30)")
axes[1].axvline(100, color=RED, linestyle=":", alpha=0.6)
axes[1].text(102, 0.15, "Stress\ndetected", color=RED, fontsize=8)
axes[1].set_xlabel("Day of year from April 1")
axes[1].set_ylabel("Block mean NDVI")
axes[1].set_title("NDVI Trend by Vineyard Block\n(Weekly Sentinel-2 acquisitions)",
                  fontsize=10, fontweight="bold")
axes[1].legend(fontsize=8)
axes[1].set_ylim(0, 0.9)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "08_ndvi_vineyard_map.png")


# ── Chart 9: Software stack cost comparison (custom vs SaaS) ─────────────────
options = ["Custom\nFastAPI stack\n(this plan)", "Odoo Community\n(ERP add-on)", "Vintrace\n(SaaS)", "Ekos\n(SaaS)"]
capex  = [3250, 500, 0, 0]     # hardware + setup
opex_y = [215, 100, 3000, 5400]  # annual operational
colors_cap  = [BLUE, GREEN, GREY, GREY]
colors_op   = [LBLUE, LGREEN, "#c9b0b0", "#c9b0b0"]

fig, ax = plt.subplots(figsize=(11, 6))
x = np.arange(len(options))
width = 0.38
ax.bar(x - width/2, capex, width, color=colors_cap, label="Upfront hardware / setup cost (€)")
ax.bar(x + width/2, opex_y, width, color=colors_op, label="Annual operational cost (€/yr)")

for i, (c, o) in enumerate(zip(capex, opex_y)):
    if c > 0:
        ax.text(i - width/2, c + 30, f"€{c:,}", ha="center", fontsize=8.5, color=GREY)
    else:
        ax.text(i - width/2, 50, "€0", ha="center", fontsize=8.5, color=GREY)
    ax.text(i + width/2, o + 30, f"€{o:,}/yr", ha="center", fontsize=8.5, color=GREY)

ax.set_xticks(x)
ax.set_xticklabels(options, fontsize=9)
ax.set_ylabel("Cost (€)")
ax.set_title("Tech Platform: Custom Build vs. SaaS\n(5-year cost of ownership favours custom build by €15k–25k)",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
save(fig, "09_build_vs_buy_comparison.png")


print(f"\nAll charts written to: {CHARTS_DIR}")
