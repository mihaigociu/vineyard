# Module 5 — Tech & Software Platform

**Vineyard Business Plan — Huși, Vaslui County, Romania**
Last updated: May 2026

---

## 5.1 Overview

This module covers the Python-based monitoring and management platform for the winery operation. The owner's Python background makes a bespoke stack both feasible and financially superior to commercial SaaS alternatives at this scale.

**Platform goals:**
- Monitor fermentation in real time (gravity, temperature, ABV progression)
- Monitor vineyard health via satellite NDVI and in-field IoT sensors
- Support spray decisions with local weather + disease risk models
- Log all production data required for DOC declarations and traceability
- Run on ~€12–18/month operational costs indefinitely

**Architecture philosophy:** local-first, cloud-optional. All critical monitoring works without internet; cloud is used only for off-site backup and remote access.

---

## 5.2 Satellite Remote Sensing (Sentinel-2 / NDVI)

### 5.2.1 Sentinel-2 Mission

- **Spatial resolution:** 10 m for bands B2/B3/B4/B8; 20 m for B5/B6/B7/B8A/B11/B12
- **Revisit time:** 2–3 days over Romania with the 3-satellite constellation (2B + 2C operational as of January 2025)
- **Data level to use:** **Level-2A** (surface reflectance, Sen2Cor corrected)
- **Cost:** Free under the Copernicus Open Data policy

### 5.2.2 Copernicus Data Space Ecosystem (CDSE)

The legacy `scihub.copernicus.eu` is retired. All access is via `https://dataspace.copernicus.eu`.

**Free tier quotas (monthly):**
- Sentinel Hub API requests: 10,000/month
- Processing Units (PU): 10,000/month (300 PU/minute burst)
- openEO credits: 10,000/month
- Rolling 30-day download: 12 TB

For weekly NDVI monitoring of 10 ha, a single AOI tile request costs 10–50 PU. A full growing season (28 acquisitions) uses well under the free quota.

**Authentication:** OAuth2 client credentials (client_id + client_secret). Tokens expire after 10 minutes, refreshable within 60 minutes.

### 5.2.3 Vegetation Indices

| Index | Formula (Sentinel-2 bands) | Resolution | Use for vineyard |
|---|---|---|---|
| **NDVI** | (B8 − B4) / (B8 + B4) | 10 m | Overall canopy vigour; range −1 to +1; healthy mid-season 0.5–0.8 |
| **NDRE** | (B8A − B5) / (B8A + B5) | 20 m | Chlorophyll/nitrogen; more sensitive than NDVI at high leaf area |
| **NDWI/NDMI** | (B8A − B11) / (B8A + B11) | 20 m | Canopy water stress; relevant for Vaslui continental drought conditions |
| **EVI** | 2.5 × (B8−B4) / (B8 + 6×B4 − 7.5×B2 + 1) | 10 m | Reduces soil/atmospheric noise; better for low canopy cover |

### 5.2.4 NDVI Workflow

```python
pip install sentinelhub rasterio geopandas shapely numpy openeo
```

1. Load vineyard blocks as GeoJSON → derive bounding box
2. Query CDSE Sentinel-2 L2A with cloud cover < 20%, past 10 days
3. Compute NDVI per pixel, mask to vineyard AOI using `rasterio.mask.mask()`
4. Aggregate mean NDVI per vineyard block; write timestamped record to TimescaleDB
5. Alert rule: block mean NDVI drops > 15% vs. 30-day rolling average → inspection flag

**Practical limitations at 10 ha:**
- 10 m pixel cannot resolve individual vine rows (~2 m spacing) — only block-level analysis possible
- NE Romania has 50–60% cloudy days in March–May; expect 5–15 usable acquisitions/month in spring
- Always apply the SCL (Scene Classification Layer) cloud/shadow mask before computing indices
- Use a 10–20 m inward buffer per block to avoid boundary mixed pixels

### 5.2.5 Alternatives

- **Planet Labs (PlanetScope):** 3–4 m resolution, daily revisit, enterprise pricing (estimated €2,000–10,000+/year). Not justified at 10 ha.
- **Pessl FieldClimate satellite add-on:** ~€300–600/year combined with iMETOS station.
- **Verdict:** Sentinel-2 via CDSE free tier is the rational choice for this operation.

---

## 5.3 In-Vineyard IoT Sensors

### 5.3.1 Weather Station

**Davis Instruments Vantage Pro2 (cabled ISS)**
- **Price:** ~€575 (cabled ISS with WeatherLink Console)
- **Measures:** Temperature/RH, barometric pressure, rainfall (tipping bucket), wind speed/direction, solar radiation
- **Linux integration:** `weewx` (open-source Python weather station software); publishes to MQTT, local SQLite/MySQL
- **Leaf wetness add-on:** Davis Leaf & Soil Station ~€90–130; 2 × leaf wetness sensor + soil probes
- **Why it matters:** Leaf wetness hours + temperature are the primary inputs for the Plasmopara viticola (downy mildew) infection model

**Pessl iMETOS LoRAIN (alternative)**
- **Price:** €548–630 special order
- **Advantage:** 4G/GPRS built-in, no separate gateway; FieldClimate web platform with built-in Romanian disease models (Plasmopara, Botrytis, Oidium)
- **FieldClimate API:** REST endpoints for data export; ~€300–600/year subscription

### 5.3.2 Soil Sensors

| Sensor | Price (€) | Technology | Measures | Notes |
|---|---|---|---|---|
| METER EC-5 | €60–100 | FDR capacitance | Volumetric water content | Analog output; needs datalogger |
| METER GS3 | €200–280 | FDR | VWC + EC + temperature | Better for loamy Vaslui soils |
| Sentek Drill & Drop | €400–800 | Multi-depth capacitance | VWC + T at 10 cm intervals | SDI-12; premium |
| **Dragino LSE01** | **€45–65** | Capacitance | VWC + soil T + EC | **LoRaWAN native; best for DIY network** |

**Depth installation:** 30 cm (primary root zone trigger), 60 cm (irrigation front), 90 cm (confirms deep drainage).

### 5.3.3 Disease Warning Models

| Platform | Romania coverage | Cost | Notes |
|---|---|---|---|
| **METOS FieldClimate (Pessl)** | **Yes** | **€300–600/yr** | Best off-the-shelf; REST API; built-in models |
| VitiMeteo | No | Free | Germany/Switzerland/Austria only |
| ISIP | No | Free | German states only |
| Open-Meteo + custom Python | Yes (global) | Free | Build models locally; see Section 5.6 |

### 5.3.4 LoRaWAN Network for 10 ha

At 10 ha (~316 m × 316 m), a single LoRaWAN gateway covers the entire vineyard with margin.

| Protocol | Range | Power draw | Cost | Use case |
|---|---|---|---|---|
| WiFi 2.4 GHz | 50–100 m outdoor | High | €0 | Fermentation sensors inside winery only |
| 4G LTE | Entire plot | 200 mW | €1–5/mo SIM | Single gateway backhaul |
| **LoRaWAN 868 MHz** | **500 m – 2 km** | **10–50 mW** | **€150–400 gateway + €40–100/node** | **Optimal for multi-node 10 ha network** |

**Gateway:** RAK7289CV2 (8-channel outdoor, EU868, with LTE), ~€370. IP67-rated, integrated antennas. Runs ChirpStack v4 (free, open-source LoRaWAN Network Server) on Debian Linux.

**DIY sensor node BOM (per node):**

| Component | Price (€) |
|---|---|
| TTGO LoRa32 T3 V1.6.1 (ESP32 + SX1276 at 868 MHz) | €18–22 |
| DHT22 T/RH sensor (or BME280 for better stability) | €5–8 |
| Capacitive soil moisture sensor | €3–5 |
| DS18B20 waterproof soil temperature | €2–4 |
| 18650 Li-ion 3,000 mAh + TP4056 charger | €5–8 |
| 5V/2W solar panel | €8–15 |
| IP65 ABS enclosure + cables | €8–15 |
| **Total per node** | **€50–75** |

Battery life at 15-minute interval: 4–8 months on 3,000 mAh.

---

## 5.4 Fermentation Monitoring: IoT to Dashboard

### 5.4.1 iSpindel Digital Hydrometer

The iSpindel is a floating ESP8266 cylinder containing an MPU-6050 accelerometer and DS18B20 temperature sensor. As fermentation consumes sugar, liquid density drops and the cylinder's tilt angle changes. Tilt angle is converted to specific gravity via a user-calibrated polynomial (calibrated with 4–6 sugar-water reference solutions).

- **Accuracy:** ±0.002 SG after calibration
- **Battery life:** 4–6 weeks at 15-minute interval; up to 3 months at 30-minute interval
- **Cost:** €40–55 DIY kit; €75–95 pre-assembled (Tindie, eBay)
- **Connectivity:** WiFi 2.4 GHz; HTTP POST or MQTT
- **Key advantage over Tilt Hydrometer:** WiFi penetrates thin stainless steel better than BLE; Tilt Hydrometer's Bluetooth is unreliable inside stainless tanks

### 5.4.2 MQTT Broker

**Recommended:** Eclipse Mosquitto (self-hosted, `sudo apt install mosquitto`, <50 MB RAM).

**Topic naming convention:**
```
winery/fermentation/tank_01/gravity       → 1.045
winery/fermentation/tank_01/temperature   → 18.2
winery/fermentation/tank_01/battery       → 4.1
winery/vineyard/sensor_row03/temperature  → 22.4
winery/vineyard/sensor_row03/soil_vwc     → 0.32
winery/power/status                       → "mains" | "on_battery"
```

**QoS:** Level 0 for routine sensor readings; Level 1 for alerts and power events.

### 5.4.3 Time-Series Stack

**TimescaleDB (recommended over pure InfluxDB):**
- PostgreSQL extension: relational + time-series in one database
- Enables SQL JOINs between sensor data and vineyard records (e.g. "average soil moisture in block 3 during high disease pressure weeks")
- Grafana PostgreSQL data source works natively
- ARM64 Docker image available; adequate performance on a mini-PC

```sql
-- Hypertable for sensor readings
CREATE TABLE sensor_readings (
    time        TIMESTAMPTZ NOT NULL,
    node_id     TEXT NOT NULL,
    temperature DOUBLE PRECISION,
    soil_vwc    DOUBLE PRECISION
);
SELECT create_hypertable('sensor_readings', 'time');

-- Join with block metadata
SELECT s.time, s.temperature, vb.block_name
FROM sensor_readings s
JOIN sensor_nodes n ON s.node_id = n.id
JOIN vineyard_blocks vb ON n.block_id = vb.id
WHERE s.time > NOW() - INTERVAL '7 days';
```

**InfluxDB:** Simpler for pure time-series at high ingestion rate; can be used as an ingest buffer feeding TimescaleDB if sensor volume grows.

### 5.4.4 Grafana Dashboards

**Fermentation monitoring panels:**
1. Gravity vs. time (fermentation curve: OG ~1.080–1.110 → FG ~0.990–0.998 for dry wine)
2. Temperature vs. time — alert if > 28°C or < 12°C for > 2 hours
3. Fermentation rate (dSG/dt) — flat line after 48 h and SG > 1.010 = stuck fermentation
4. Estimated ABV: `ABV% ≈ (OG − FG) × 131.25` — Calculate Field transform
5. Tank status table: current gravity, temperature, status per tank

**Alert rules (Grafana Alerting → Telegram bot contact point):**
- Stuck fermentation: Δgravity < 0.001 in 48 hours AND SG > 1.010
- Temperature excursion: > 28°C for ≥ 2 consecutive hours
- Low battery: iSpindel voltage < 3.6 V
- Power event: `winery/power/status = "on_battery"`

**Grafana OSS:** All features free, self-hosted. No licence cost.

---

## 5.5 Python Tech Stack Architecture

### 5.5.1 Full Stack

```
FIELD LAYER
──────────────────────────────────────────────────────────
[ESP32+LoRa nodes]    ─ LoRa 868 MHz ─► [RAK7289CV2 gateway]
[Dragino LSE01 soil]  ─ LoRa 868 MHz ─►         │
[Davis VP2 station]   ─ 4G / WiFi ───►           │ 4G LTE + MQTT
[iSpindel × tanks]    ─ WiFi 2.4 GHz ─► [Winery WiFi AP]
                                                  │
EDGE LAYER (Beelink EQ12 mini-PC, on-premise at winery)
──────────────────────────────────────────────────────────
  Mosquitto MQTT Broker  ◄── all sensor feeds
         ↓
  Telegraf  (MQTT input → TimescaleDB line protocol)
         ↓
  TimescaleDB (PostgreSQL 16)
  ├── sensor_readings (hypertable)
  ├── vineyard_blocks, spray_log, harvest_records
  └── fermentation_log, ndvi_observations
         ↓
  FastAPI  (port 8000)  ←── REST endpoints for mobile + reports
  Streamlit (port 8501) ←── owner-operator daily dashboard
  Grafana  (port 3000)  ←── real-time monitoring + alerts
         ↓ sync when internet available
CLOUD: Hetzner CX22 VPS €3.49/mo — off-site backup + remote relay

SATELLITE (weekly batch job)
  CDSE → sentinelhub → NDVI per block → TimescaleDB
```

### 5.5.2 Hardware

| Option | Price | Notes |
|---|---|---|
| **Beelink EQ12 (N100, 16 GB, 500 GB NVMe)** | **~€150–170** | **Recommended** — x86_64, broader Docker support, lower power draw (~8–15W), more headroom |
| Raspberry Pi 5 (8 GB) + NVMe SSD | ~€185–200 | ARM64; Pi 5 prices elevated in 2025 due to DRAM shortage |

**Important:** Use NVMe SSD, not microSD — microSD fails under continuous database write load.

### 5.5.3 Docker Compose

```yaml
version: "3.9"
services:
  postgres:
    image: timescale/timescaledb:2.14.2-pg16
    environment:
      POSTGRES_PASSWORD: "${DB_PASSWORD}"
      POSTGRES_DB: vineyard
    volumes: [pgdata:/var/lib/postgresql/data]
  mosquitto:
    image: eclipse-mosquitto:2.0
    ports: ["1883:1883"]
  telegraf:
    image: telegraf:1.30
    volumes: [./telegraf/telegraf.conf:/etc/telegraf/telegraf.conf]
  grafana:
    image: grafana/grafana:10.4.0
    ports: ["3000:3000"]
    volumes: [grafana_data:/var/lib/grafana]
  fastapi:
    build: ./api
    ports: ["8000:8000"]
  streamlit:
    build: ./dashboard
    ports: ["8501:8501"]
volumes:
  pgdata: {}
  grafana_data: {}
```

### 5.5.4 FastAPI Endpoints

```
GET  /api/v1/sensors/latest              → last reading per node
GET  /api/v1/sensors/{node}/history      → time-series with date range
GET  /api/v1/fermentation/{tank}         → current gravity, temp, ABV
GET  /api/v1/ndvi/latest                 → NDVI per vineyard block
POST /api/v1/harvest/records             → submit harvest record
POST /api/v1/spray/log                   → submit spray application
GET  /api/v1/reports/onvpv/harvest       → generate XLSX declaration
GET  /api/v1/gdd/current_season          → cumulative GDD from April 1
```

### 5.5.5 Cloud Hosting

| Provider | Plan | €/month | Notes |
|---|---|---|---|
| **Hetzner** | CX22: 2 vCPU, 4 GB, 40 GB | **€3.49** | Germany; full GDPR compliance; recommended |
| Hetzner | CX32: 4 vCPU, 8 GB, 80 GB | €6.49 | If full stack in cloud |
| Fly.io | shared-cpu-1x | ~€1.80 | Frankfurt EU datacenter; good for FastAPI only |

**Remote access:** Tailscale (free tier, 100 devices, 3 users). Works behind NAT/CGNAT — critical for Romanian mobile networks. No port forwarding needed.

### 5.5.6 ONVPV Declaration Export

ONVPV SNIIV has no public REST API (as of 2026) — declarations require manual portal entry. Python can generate the pre-filled XLSX:

```python
import openpyxl
from io import BytesIO

def generate_harvest_declaration(db_session, year: int) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Parcela", "Soi", "Suprafata (ha)", "Data recoltei",
               "Cantitate (kg)", "Brix"])
    records = db_session.execute(
        "SELECT parcel_id, variety, surface_ha, harvest_date, weight_kg, brix "
        "FROM harvest_records WHERE EXTRACT(YEAR FROM harvest_date) = :yr",
        {"yr": year}
    ).fetchall()
    for r in records:
        ws.append(list(r))
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()
```

---

## 5.6 Precision Viticulture: Decision Support

### 5.6.1 Disease Risk Model (Python, Open-Meteo)

Open-Meteo provides free weather data for any location globally, including Huși (46.67°N, 27.98°E), with 7-day forecast and 40-year ERA5 historical data.

```python
import requests
import pandas as pd
import numpy as np

def get_weather_husi(past_days=7, forecast_days=7):
    r = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": 46.67, "longitude": 27.98,
        "hourly": "temperature_2m,relativehumidity_2m,precipitation",
        "past_days": past_days,
        "forecast_days": forecast_days,
        "timezone": "Europe/Bucharest"
    })
    df = pd.DataFrame(r.json()["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    return df

def plasmopara_daily_risk(df):
    df = df.copy()
    df["wet"] = (df["relativehumidity_2m"] >= 95) | (df["precipitation"] > 0.1)
    df["infectable"] = df["wet"] & df["temperature_2m"].between(10, 30)
    daily = df.groupby(df["time"].dt.date).agg(
        rain_mm=("precipitation", "sum"),
        infectable_hours=("infectable", "sum")
    )
    daily["risk"] = np.select(
        [daily["rain_mm"] > 2.0,
         (daily["rain_mm"] > 0.5) & (daily["infectable_hours"] >= 4),
         daily["rain_mm"] > 0],
        [4, 3, 1], default=0
    )
    return daily
```

**VitiMeteo** (free, Strasbourg university) does **not** cover Romania. METOS FieldClimate (~€300–600/year) is the best off-the-shelf option with Romanian coverage and a REST API for data export.

### 5.6.2 Growing Degree Days for Phenology Prediction

```python
def calculate_gdd(df, t_base=10.0):
    df = df.copy()
    df["t_avg"] = (df["tmax"] + df["tmin"]) / 2
    df["gdd"] = (df["t_avg"] - t_base).clip(lower=0)
    df["cgdd"] = df["gdd"].cumsum()
    return df
```

**Muscat Ottonel phenology thresholds at Huși** (base 10°C, accumulated from 1 April):

| Stage | Cumulative GDD | Typical calendar date |
|---|---|---|
| Budburst | 150–200 | Late March – early April |
| Flowering | 350–450 | Late May – early June |
| Véraison | 900–1,100 | Late July – early August |
| **Harvest** | **1,300–1,530** | **Late August – mid September** |

### 5.6.3 Harvest Timing — Multi-Signal Decision

| Signal | Tool | Target for Muscat Ottonel |
|---|---|---|
| °Brix | Handheld refractometer (€30–80) | 20–22 °Brix (still wine); 24–26 (late harvest) |
| pH | Pocket pH meter (€20–50) | 3.1–3.4 |
| TA | Titration kit (€30) | 5.5–7.5 g/L tartaric |
| Berry tasting | Free | Brown seeds, easy pulp release, strong Muscat aroma |
| NDVI trend | Sentinel-2 (free) | Plateau then initial decline = approaching senescence |
| Cumulative GDD | Open-Meteo + Python | ≥ 1,300 from April 1 |

### 5.6.4 Weather API Comparison

| API | Free tier | Romania | Notes |
|---|---|---|---|
| **Open-Meteo** | **10,000 calls/day** | **Yes, full coverage** | **Primary source** — includes GDD, soil moisture, ET₀ |
| VisualCrossing | 1,000 records/day | Yes | Good historical; commercial-grade |
| MeteoBlue | 5,000 calls/year | Yes | Occasional high-res event forecasts |
| Meteomatics | No free tier | Yes | Enterprise only; not recommended |

---

## 5.7 Vineyard Management Software

### 5.7.1 Commercial Options Assessment

All major commercial VMS platforms (Vintrace, Ekos, OenOS, Wineware) are priced at €200–800/month and designed for Australian, US, or French compliance. **None natively integrate with ONVPV/SNIIV** Romanian declarations.

### 5.7.2 Open-Source Options

**Odoo 17 Community Edition (recommended if full ERP needed):**
- Licence: LGPL (free, self-hosted)
- Manufacturing (MRP) module: free in Community; BOM, work orders, lot/batch tracking — directly applicable to winemaking batches
- Implementation effort: medium
- Hosting: Hetzner VPS €6.49/month or Frappe Cloud ~$25/month

**ERPNext v15 (Frappe):**
- Agriculture module: github.com/frappe/agriculture — crop management, spray tracking, harvest records
- Implementation effort: high (2–4 months)

### 5.7.3 Minimum Viable Feature Set (Custom FastAPI Build)

The owner's Python background makes a custom build viable and optimal — particularly because ONVPV compliance requires custom work in any case.

**Priority 1 (Must have at launch):**
- Vineyard block register (parcel ID, cadastral ref, variety, surface ha, rootstock, planting year)
- Spray log (date, product, dose/ha, PHI, target disease, operator — required for GAP and organic certification)
- Harvest record (block, date, weight kg, Brix, pH, TA)
- Tank/wine batch log (inputs, yeast additions, racking dates, analyses)
- DOC declaration export (pre-filled XLSX for ONVPV portal entry)

**Priority 2:** Phenological observation log, chemical analysis log, work orders, stock inventory

**Priority 3:** Cost-per-litre analysis, invoicing, label batch tracking

**Build vs. buy decision:** Build the custom FastAPI backend for IoT + vineyard records. Add Odoo Community only if broader accounting/invoicing/HR is needed. Do not pay €200–500/month SaaS for a 10 ha boutique operation where ONVPV compliance requires custom work regardless.

---

## 5.8 Connectivity & Infrastructure

### 5.8.1 Mobile Data Coverage at Huși

Huși is a city of ~28,000 — standard Romanian urban 4G coverage is available.

| Operator | 4G coverage | Notes |
|---|---|---|
| Orange Romania | Excellent (>99% population) | Widest coverage; 30–80 Mbps typical |
| Vodafone Romania | Good | Absorbed Telekom Romania postpaid customers (Sept 2025) |
| **Digi Mobil** | **Good (98%+ claimed)** | **Cheapest data rates; recommended for IoT SIM** |

Verify at vineyard coordinates (46.67°N, 27.98°E) at nperf.com.

### 5.8.2 Fixed Broadband

- **Digi/RCS&RDS:** €8–12/month for 100–500 Mbps cable or 4G home broadband (dominant ISP in Romania)
- **Orange FTTH (where available):** €15–20/month
- Sufficient for all proposed stack requirements

### 5.8.3 Power Reliability and UPS

NE Romania (E.ON distribution in Vaslui): 4–12 power interruptions/year, typically < 4 hours. A UPS is essential for always-on database + MQTT broker.

**APC Back-UPS 650 (BX650I-GR, European Schuko):** €80–120 at Romanian retailers (Altex.ro, PCGarage.ro, eMAG.ro). At ~27 W load (mini-PC + router + gateway): 12–18 minutes runtime.

For longer runtime: APC Smart-UPS 1500 (~€300–400) gives 40+ minutes, or add a 12V 18 Ah sealed lead-acid battery (~€40) for 2–4 hours.

```bash
# apcupsd + MQTT power notifications
ONBATTERY   → publish winery/power/status = "on_battery" → Telegram alert
BATTERY < 20% → trigger graceful Docker Compose stop
POWERRESTORED → publish winery/power/status = "mains"
```

### 5.8.4 IoT SIM Data Costs in Romania

| Provider | Monthly cost | Notes |
|---|---|---|
| **Digi prepaid** | **< €1** (~150 MB/month) | Best value; top up €5 for 10 GB every 6–12 months |
| Orange consumer SIM | €10–12 (20 GB) | Overkill for IoT use |
| Thingsmobile (EU IoT SIM) | €2–5/month | One contract across EU; useful for future scaling |

A LoRaWAN gateway sending 14,400 readings/day at 50 bytes ≈ 22 MB/month sensor traffic. Total with overhead: ~100–150 MB/month.

### 5.8.5 Local-First Design

The platform is designed to function fully without internet:

**Works offline:**
- All sensor data collection (local LoRa + MQTT + TimescaleDB)
- Fermentation monitoring (local WiFi + MQTT)
- All dashboards on the local network
- Disease model calculations (runs on cached weather data)
- Spray log entry, harvest records, all production tracking

**Requires internet (periodic):**
- Sentinel-2 NDVI download (weekly, ~5 min)
- Open-Meteo weather forecast refresh (daily, ~1 min)
- Remote access via Tailscale
- Off-site backup sync (nightly pg_dump → Hetzner VPS)

---

## 5.9 Hardware Budget

### Tier 1 — Minimum Viable (Year 1)

| Item | Qty | Unit Price (€) | Total (€) |
|---|---|---|---|
| Davis Vantage Pro2 cabled ISS | 1 | 575 | 575 |
| Davis Leaf & Soil Station (2× leaf wetness + soil probes) | 1 | 110 | 110 |
| iSpindel DIY kit (per fermentation tank) | 2 | 50 | 100 |
| Beelink EQ12 mini-PC (N100, 16 GB, 500 GB NVMe) | 1 | 165 | 165 |
| RAK7289CV2 outdoor LoRaWAN gateway (EU868 + LTE) | 1 | 370 | 370 |
| Dragino LSE01 soil/VWC nodes | 3 | 55 | 165 |
| APC Back-UPS 650 UPS | 1 | 100 | 100 |
| Network switch + cables | 1 | 50 | 50 |
| Annual IoT SIM + Hetzner VPS | — | 57 | 57 |
| **Tier 1 Total** | | | **~€1,692** |

### Tier 2 — Expanded (Year 2, additional)

| Item | Price (€) |
|---|---|
| Pessl iMETOS LoRAIN weather station | 590 |
| FieldClimate subscription (disease models, REST API) | 400/yr |
| Additional DIY LoRa sensor nodes (×5) | 350 |
| iSpindel per remaining tanks (×4) | 200 |
| **Tier 2 Total** | **~€1,540** |

**2-year hardware total: ~€3,250**. Annual operational costs: ~€150–215/year. Well within the project's budget envelope.

---

## 5.10 Monthly Operational Cost Summary

| Item | Monthly (€) |
|---|---|
| Digi fixed broadband (winery) | 8–12 |
| Digi IoT SIM (LoRa gateway 4G backhaul) | 0.50–2 |
| Hetzner CX22 VPS (backup + remote relay) | 3.49 |
| Tailscale (remote access) | 0 (free tier) |
| Open-Meteo weather data | 0 (free tier) |
| CDSE Sentinel-2 satellite data | 0 (free tier) |
| Grafana + Streamlit (self-hosted) | 0 |
| **Total** | **~€12–18/month** |

**Annual operational cost: ~€150–215/year**, excluding hardware depreciation.

---

## Key Sources

- Copernicus Data Space Ecosystem: dataspace.copernicus.eu
- CDSE quotas: documentation.dataspace.copernicus.eu/Quotas.html
- sentinelhub Python: github.com/sentinel-hub/sentinelhub-py
- Davis Vantage Pro2: davisinstruments.com
- Pessl iMETOS LoRAIN: metos.global/en/lorain/
- Dragino LSE01: dragino.com/products/lora-lorawan-end-node/item/159-lse01.html
- RAK7289CV2 gateway: store.rakwireless.com
- iSpindel: ispindel.de/docs/README_en.html
- InfluxDB v2: docs.influxdata.com
- Grafana free tier: grafana.com/products/cloud/free-tier/
- TimescaleDB: timescale.com
- ONVPV RPV Online: onvpv.ro/en/content/rpv-online
- Odoo winery session 2025: odoo.com/event/odoo-experience-2025
- ERPNext agriculture module: github.com/frappe/agriculture
- Hetzner Cloud pricing: hetzner.com/cloud
- Open-Meteo API: open-meteo.com/en/docs
- Tailscale: tailscale.com
- Digi Romania coverage: digi.ro/asistenta/acoperire-servicii-portabilitate
- Romanian Journal of Horticulture 2020 (Huși GDD data): romanianjournalofhorticulture.ro
