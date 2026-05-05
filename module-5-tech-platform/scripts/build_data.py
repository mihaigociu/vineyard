"""
Build CSV data files for Module 5 — Tech & Software Platform.

Sources: CDSE/Copernicus, Davis Instruments, Pessl/Metos, RAK Wireless,
Dragino, iSpindel, Grafana, Hetzner, Open-Meteo, Tailscale.
See module-5-tech-platform.md for full citations.

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


# ── 1. Sentinel-2 vegetation indices ─────────────────────────────────────────
write_csv(
    "sentinel2_indices.csv",
    ["index", "formula", "bands", "resolution_m", "primary_use", "healthy_range"],
    [
        ["NDVI",  "(B8-B4)/(B8+B4)",                      "B8 (NIR 842nm), B4 (Red 665nm)",               10, "Overall canopy vigour",                    "0.5–0.8 healthy mid-season"],
        ["NDRE",  "(B8A-B5)/(B8A+B5)",                    "B8A (865nm), B5 (705nm)",                      20, "Chlorophyll and nitrogen status",          "0.2–0.5 healthy"],
        ["NDWI",  "(B8A-B11)/(B8A+B11)",                  "B8A (865nm), B11 (SWIR1 1610nm)",              20, "Canopy water stress",                       "0.1–0.4 no stress"],
        ["EVI",   "2.5*(B8-B4)/(B8+6*B4-7.5*B2+1)",      "B8, B4, B2 (Blue 490nm)",                     10, "Vigour; reduces soil/atmospheric noise",    "0.2–0.6 healthy"],
    ],
)

# ── 2. IoT sensor comparison ──────────────────────────────────────────────────
write_csv(
    "iot_sensor_comparison.csv",
    ["sensor", "manufacturer", "price_eur_min", "price_eur_max",
     "connectivity", "measures", "recommended", "notes"],
    [
        ["Vantage Pro2 cabled ISS",  "Davis Instruments",  540,  610, "USB/WiFi", "T/RH/pressure/rain/wind/solar radiation",    True,  "Add Leaf&Soil Station for leaf wetness; use weewx for MQTT"],
        ["iMETOS LoRAIN",            "Pessl/METOS",        548,  630, "4G GPRS",  "T/RH/rain/wind/leaf wetness/soil",           True,  "4G built-in; FieldClimate platform with Romanian disease models"],
        ["HOBO MX2301A",             "Onset",               80,  110, "BLE",      "T/RH only",                                  False, "Supplemental micro-climate sensor; BLE download only"],
        ["GS3 soil sensor",          "METER",              200,  280, "SDI-12",   "VWC + EC + soil temperature",                False, "Premium; good for loamy Vaslui soils; needs datalogger"],
        ["LSE01 soil/VWC node",      "Dragino",             45,   65, "LoRaWAN",  "VWC + soil temperature + EC",                True,  "Best DIY option; LoRaWAN native; plug into ChirpStack gateway"],
        ["DIY ESP32+LoRa node",      "DIY (BOM ~€60)",      50,   75, "LoRaWAN",  "T/RH + soil VWC + soil temperature",        True,  "TTGO LoRa32 + DHT22 + capacitive soil sensor; 4-8mo battery"],
    ],
)

# ── 3. Connectivity comparison ────────────────────────────────────────────────
write_csv(
    "connectivity_options.csv",
    ["protocol", "range_m_min", "range_m_max", "power_draw",
     "gateway_cost_eur", "monthly_cost_eur", "use_case", "recommended_for"],
    [
        ["WiFi 2.4 GHz",    50,    100, "High (100-300mW)",   0,   0,    "Fermentation sensors inside winery building",              "iSpindel tanks; indoor only"],
        ["4G LTE",       1000,  50000, "Medium (200mW TX)",  0,   5,    "Single gateway 4G backhaul to cloud",                     "LoRa gateway uplink; weather station"],
        ["LoRaWAN 868", 500,   2000,   "Very low (10-50mW)", 370, 1,    "Multi-node 10 ha outdoor sensor network",                  "All outdoor vineyard sensors; main field network"],
        ["Ethernet LAN",    100, 100,  "None (passive)",     50,  0,    "Wired connection inside winery building",                  "Mini-PC, NAS, critical devices"],
    ],
)

# ── 4. LoRaWAN gateway comparison ─────────────────────────────────────────────
write_csv(
    "lorawan_gateway_comparison.csv",
    ["gateway", "manufacturer", "price_eur", "channels",
     "backhaul", "ip_rating", "os", "recommended"],
    [
        ["RAK7289CV2",   "RAK Wireless", 370, 8,  "4G LTE + Ethernet",   "IP67", "Debian Linux + ChirpStack",    True],
        ["DLOS8N",       "Dragino",      437, 8,  "4G LTE + Ethernet",   "IP65", "OpenWrt + ChirpStack",         False],
        ["RAK5146 PiHAT","RAK Wireless", 100, 8,  "Via Raspberry Pi",    "None", "ChirpStack on Pi (DIY)",       False],
    ],
)

# ── 5. iSpindel vs Tilt Hydrometer ────────────────────────────────────────────
write_csv(
    "fermentation_monitor_comparison.csv",
    ["device", "price_eur_min", "price_eur_max", "connectivity",
     "sg_accuracy", "battery_weeks", "stainless_tank_ok",
     "mqtt_native", "recommended"],
    [
        ["iSpindel DIY",          40,  55, "WiFi 2.4 GHz", "±0.002 SG", "4–6 (15min interval)",  True,  True,  True],
        ["iSpindel pre-assembled",75,  95, "WiFi 2.4 GHz", "±0.002 SG", "4–6 (15min interval)",  True,  True,  True],
        ["Tilt Hydrometer",      110, 130, "BLE only",     "±0.002 SG", "~3 months (Tilt Pro)",  False, False, False],
        ["Tilt Pro",             140, 155, "BLE only",     "±0.001 SG", "~3 months",             False, False, False],
    ],
)

# ── 6. Software stack components ──────────────────────────────────────────────
write_csv(
    "software_stack.csv",
    ["component", "software", "licence", "monthly_cost_eur",
     "role", "docker_arm64", "recommended"],
    [
        ["MQTT broker",         "Eclipse Mosquitto 2.0",              "EPL/EDL (free)",   0,    "Receives all sensor MQTT feeds",                                          True,  True],
        ["Time-series DB",      "TimescaleDB 2.14 (PostgreSQL 16)",   "Apache 2 (free)",  0,    "Stores sensor readings + vineyard records in same DB",                    True,  True],
        ["Metrics ingest",      "Telegraf 1.30",                      "MIT (free)",       0,    "MQTT input plugin → TimescaleDB/InfluxDB write",                          True,  True],
        ["Dashboard",           "Grafana OSS 10.4",                   "AGPL (free)",      0,    "Real-time monitoring dashboards + alerting",                              True,  True],
        ["App dashboard",       "Streamlit",                          "Apache 2 (free)",  0,    "Owner-operator daily use; vineyard records, reports",                     True,  True],
        ["API backend",         "FastAPI + uvicorn",                   "MIT (free)",       0,    "REST endpoints; ONVPV export; mobile access",                             True,  True],
        ["Alt time-series DB",  "InfluxDB v2 OSS",                    "MIT (free)",       0,    "Alternative to TimescaleDB; pure time-series only",                       True,  False],
        ["Remote access",       "Tailscale",                          "Free (up to 100)", 0,    "Secure mesh VPN; works behind NAT/CGNAT",                                 True,  True],
    ],
)

# ── 7. Cloud hosting comparison ───────────────────────────────────────────────
write_csv(
    "cloud_hosting_comparison.csv",
    ["provider", "plan", "vcpu", "ram_gb", "storage_gb",
     "monthly_eur", "region", "gdpr", "recommended"],
    [
        ["Hetzner",  "CX22",              2, 4,  40,  3.49,  "Germany (nbg1/hel1)",  True,  True],
        ["Hetzner",  "CX32",              4, 8,  80,  6.49,  "Germany (nbg1/hel1)",  True,  False],
        ["Fly.io",   "shared-cpu-1x",     1, 0.256, 3, 1.80, "Frankfurt (fra)",       True,  False],
        ["Render",   "Starter",           1, 0.512, 0, 7.00,  "Frankfurt",             True,  False],
    ],
)

# ── 8. Phenology GDD thresholds ───────────────────────────────────────────────
write_csv(
    "phenology_gdd_thresholds.csv",
    ["stage", "cgdd_min", "cgdd_max", "typical_date_start",
     "typical_date_end", "notes"],
    [
        ["Budburst",              150, 200, "Mar 25", "Apr 05", "Base 10°C; accumulated from April 1"],
        ["Shoot 10 cm",           200, 250, "Apr 05", "Apr 15", "First spray window"],
        ["Inflorescence visible", 280, 350, "May 10", "May 20", "Disease pressure intensifies"],
        ["Flowering",             350, 450, "May 20", "Jun 10", "Critical disease window; coulure risk"],
        ["Berry set",             450, 550, "Jun 10", "Jun 20", ""],
        ["Veraison",              900, 1100,"Jul 20", "Aug 05", "Hail risk peak; colour change"],
        ["Harvest (still wine)",  1300, 1530,"Aug 25", "Sep 15", "20-22 Brix target; manual harvest"],
    ],
)

# ── 9. Weather API comparison ─────────────────────────────────────────────────
write_csv(
    "weather_api_comparison.csv",
    ["api", "free_calls_per_day", "commercial_cost",
     "romania_coverage", "historical_data", "agro_variables", "recommended"],
    [
        ["Open-Meteo",      "10,000/day",      "API key required for commercial use",     True,  "40yr ERA5",    "GDD, soil moisture, ET0, leaf wetness",  True],
        ["VisualCrossing",  "1,000 records/day","$0.0001/record",                         True,  "1970-present", "Standard; good historical",              False],
        ["MeteoBlue",       "5,000 calls/year", "Credit-based",                           True,  "Yes",          "Limited agro variables on free",         False],
        ["Meteomatics",     "None",             "Enterprise only",                        True,  "Yes",          "Full agro suite",                        False],
        ["METOS FieldClimate","REST API",       "€300-600/yr (with station subscription)",True, "Yes",          "Full disease models built-in",           False],
    ],
)

# ── 10. Hardware budget ───────────────────────────────────────────────────────
write_csv(
    "hardware_budget.csv",
    ["item", "qty", "unit_price_eur", "total_eur", "tier", "year", "priority"],
    [
        ["Davis Vantage Pro2 cabled ISS",          1, 575, 575,  1, 1, "High"],
        ["Davis Leaf & Soil Station",              1, 110, 110,  1, 1, "High"],
        ["iSpindel DIY kit (per fermentation tank)",2,  50, 100,  1, 1, "Critical"],
        ["Beelink EQ12 mini-PC (16GB, 500GB NVMe)",1, 165, 165,  1, 1, "Critical"],
        ["RAK7289CV2 outdoor LoRaWAN gateway",     1, 370, 370,  1, 1, "High"],
        ["Dragino LSE01 soil/VWC nodes",           3,  55, 165,  1, 1, "High"],
        ["APC Back-UPS 650 UPS",                   1, 100, 100,  1, 1, "High"],
        ["Network switch + cables",                1,  50,  50,  1, 1, "Medium"],
        ["Annual IoT SIM + Hetzner VPS (annualised)",1,57,  57,  1, 1, "Low"],
        ["Pessl iMETOS LoRAIN weather station",    1, 590, 590,  2, 2, "Medium"],
        ["Pessl FieldClimate subscription (annual)",1,400, 400,  2, 2, "Medium"],
        ["DIY LoRa sensor nodes (additional x5)",  5,  70, 350,  2, 2, "Medium"],
        ["iSpindel kits for remaining tanks (x4)", 4,  50, 200,  2, 2, "High"],
    ],
)

# ── 11. Monthly operational costs ────────────────────────────────────────────
write_csv(
    "monthly_operational_costs.csv",
    ["item", "monthly_cost_eur_min", "monthly_cost_eur_max", "notes"],
    [
        ["Digi fixed broadband (winery)",        8.00, 12.00, "100-500 Mbps cable/4G home broadband"],
        ["Digi IoT SIM (LoRa gateway 4G uplink)",0.50,  2.00, "~150 MB/month sensor traffic"],
        ["Hetzner CX22 VPS",                     3.49,  3.49, "Germany; GDPR; off-site backup + remote relay"],
        ["Tailscale (remote access)",             0.00,  0.00, "Free tier: 100 devices, 3 users"],
        ["Open-Meteo weather data",               0.00,  0.00, "Free: 10,000 calls/day"],
        ["CDSE Sentinel-2 satellite",             0.00,  0.00, "Free: 10,000 PU/month"],
        ["Grafana OSS + Streamlit (self-hosted)", 0.00,  0.00, "Free open-source licences"],
    ],
)

print("\nAll CSV files written to:", DATA_DIR)
