Here is the contextual data summary from the planning phase, followed by the two LLM prompts for building the database and the remote modeling notebook.

---

### Context Summary: Planning Data & Agronomic Specifications

*(Include this section in the context window of both prompts so the LLM understands the exact schemas, physics, and data endpoints).*

#### 1. Core Data Sources & APIs

* **Botanical Traits & Spacing**:
* [Permapeople API](https://permapeople.org/knowledgebase/api-docs/): REST JSON endpoint providing mature spread, height, sunlight requirements (`full_sun`, `partial_shade`, `full_shade`), root depth, edible parts, USDA hardiness zones, and pairwise companion/antagonist plant relationships.
* [USDA PLANTS Database](https://plants.sc.egov.usda.gov/): Taxonomic symbols, physiological drought tolerance classifications, soil pH limits, and morphological habits.
* [Plants For A Future (PFAF)](https://pfaf.org/): Curated records for over 8,700 edible and utilitarian crops, detailing soil texture preferences and microclimate tolerances.


* **Phenology & Growth Stages**:
* [USA National Phenology Network (USA-NPN) API](https://www.usanpn.org/data/code): Georeferenced, timestamped observations of phenophases (bud break, initial leafing, flowering, fruit setting, harvest readiness) paired with station-accumulated Growing Degree Days ($\text{GDD}$, $T_{\text{base}} = 0^\circ\text{C}$ and $10^\circ\text{C}$).


* **Meteorological & Subsurface Soil Features**:
* [Open-Meteo Historical & Forecast APIs](https://open-meteo.com/en/docs): Seamless global 1–10 km reanalysis (ERA5-Land) and high-resolution numerical forecasts. Relevant features: daily $T_{\min}$, $T_{\max}$, shortwave solar radiation, vapor pressure deficit ($\text{VPD}$), precipitation, reference evapotranspiration ($\text{ET}_0$), and multi-depth volumetric soil moisture and temperature (`0-7 cm`, `7-28 cm`, `28-100 cm`).
* [NOAA GHCN-Daily](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) & [PRISM 2023 Hardiness Grids](https://prism.oregonstate.edu/phzm/): 30-year climate station normals for probabilistic frost distribution curves ($P(\text{frost}) \le 10\%$).


* **Hydrological & Irrigation Standards**:
* [FAO-56 Evapotranspiration Guidelines](https://www.fao.org/3/x0490e/x0490e00.htm) & [FAO AquaCrop Parameter Annexes](https://openknowledge.fao.org/server/api/core/bitstreams/1479f444-c112-4faa-b3dc-bc73b0637332/content): Base temperatures ($T_{\text{base}}$), stage-specific crop coefficients ($K_{c,\text{ini}}$, $K_{c,\text{mid}}$, $K_{c,\text{end}}$), and root-zone depletion fractions ($p$).


* **Regional Wasatch Front / Utah Ground Truth**:
* [USU Extension Research](https://extension.usu.edu/yardandgarden/research/wasatch-front-planting-dates): Empirical planting date ranges, seed-to-transplant windows, and spacing charts ([Wasatch Front Vegetable Chart](https://extension.usu.edu/yardandgarden/files/Planting-Guide.pdf)).
* [Utah Climate Center Mesonet](https://climate.usu.edu/): Over 140 research stations providing empirical net radiation, reference $\text{ET}$, and in-situ soil moisture sensor series.



#### 2. Governing Equations

* **Thermal-Time Accumulation (GDD)**:

$$\text{GDD} = \sum \max\left( \frac{T_{\max} + T_{\min}}{2} - T_{\text{base}}, 0 \right)$$


* **Crop Evapotranspiration ($\text{ET}_c$)**:

$$\text{ET}_c = K_c \times \text{ET}_0$$


* **Root-Zone Soil Water Depletion Balance ($D_r$)**:

$$D_{r,t} = D_{r,t-1} - (P_t - \text{RO}_t) - I_t + \text{ET}_{c,t} + \text{DP}_t$$



*(Irrigate when $D_r \ge \text{RAW}$, where $\text{RAW} = p \times \text{TAW}$, and $\text{TAW} = 1000 \times (\theta_{\text{FC}} - \theta_{\text{WP}}) \times Z_r$)*.


### 3. Implementation Status & Work Performed (Session Log: November 11, 2026)

#### 3.1 Host Storage & Parquet Lake Architecture on Drive `D:\`
- Initialized physical directory hierarchy strictly on drive `D:\`:
  - Database File: `D:\gardening_db\garden.duckdb` (13.9 MB, WAL-enabled).
  - Parquet Data Lake: `D:\gardening_db\parquet_lake\weather\` partitioned by `year=YYYY/month=MM/` containing 11 years (2016–2026) of continuous daily weather and multi-depth soil features.
  - Script & Ingestion Roots: `D:\gardening_db\ingestion\`, `D:\gardening_db\sql\`, `D:\gardening_db\scripts\`, `D:\gardening_db\logs\`.
  - All codebase components mirrored in workspace repository `D:\Projects\GardeningML\`.

#### 3.2 Normalized Relational Schema & Analytical Views (`sql/schema.sql`)
- Created 11 base tables with primary keys, check constraints, foreign keys, and date B-tree indexes:
  1. `dim_species`: 20 botanical species with growth habits, mature spread/height, sunlight needs, soil pH limits, drought tolerance, and $T_{base}$ (°C).
  2. `dim_cultivars`: 16 proven Wasatch Front cultivars with seed/transplant DTM, GDD to maturity, and disease resistance flags.
  3. `dim_companion_matrix`: 16 directed agroecological pairings (`companion`, `antagonist`, `neutral`) with biological and physical rationales (e.g., *alpha-terthienyl* nematicides, *ocimene* pest deterrence, Milpa nitrogen fixation).
  4. `dim_crop_coefficients`: 20 FAO-56 stage curves (`initial`, `development`, `mid_season`, `late_season`) with basal crop coefficients ($K_{cb}$) and depletion fractions ($p$).
  5. `dim_garden_beds`: 3 physical bed definitions (Sandy Loam, Clay Loam, Loam) with length/width, orientation azimuth, direct sun hours, $\theta_{FC}$, and $\theta_{WP}$.
  6. `fact_weather_daily`: Composite key `(station_id, observation_date)`, 3,974 records with $T_{min}$, $T_{max}$, $T_{mean}$, solar radiation ($MJ/m^2$), precipitation ($mm$), RH (%), wind speed ($m/s$), $\text{ET}_0$ ($mm$), volumetric soil moisture at 4 depths (`0-7cm`, `7-28cm`, `28-100cm`, `100-255cm`), soil temperature (`0-7cm`), and rolling cumulative GDD.
  7. `fact_phenology_observations`: Field ground-truth phenophase observations calibrated against USA-NPN and USU Extension trials.
  8. `fact_garden_plants`: Active plant instances placed with precise $(x, y)$ centimeter coordinates in beds.
  9. `fact_daily_care_log`: Logged irrigation events (mm and liters) and tending actions (`thinned`, `trellised`, `pruned`, `scouted_pests`, `fertilized`).
  10. `ref_usu_planting_calendar`: 14 crop schedules with spring/fall planting windows, germination soil temps, and spacing recommendations.
  11. `ref_hardiness_frost_normals`: 30-year freeze probability normals ($P(\text{frost}) \le 10\%, 50\%, 90\%$) for Salt Lake Valley, Utah Valley, and Wasatch Back.
- Engineered 4 high-performance analytical SQL views:
  - `vw_rolling_gdd`: Computes daily thermal accumulation ($T_{base}=10^\circ\text{C}$ and $0^\circ\text{C}$), seasonal GDD accumulation from March 1, 7-day moving average temperature, and 14-day rolling precipitation.
  - `vw_soil_moisture_deficit`: Evaluates real-time FAO-56 root-zone water balance ($TAW$, $RAW$, $ET_c$, $D_r$), automated `IRRIGATION_NEEDED` alerts, and replenishment volume in liters.
  - `vw_companion_pairings`: Joins companion matrix with taxonomic taxonomy for spatial garden bed planning.
  - `vw_garden_bed_status`: Aggregates active plant density, soil texture, and canopy coverage per bed.

#### 3.3 Ingestion Pipeline Modules (`ingestion/`)
- `ingest_open_meteo.py`:
  - Fetches live 7-day forecast and recent 92 days from Open-Meteo API (`api.open-meteo.com`).
  - Generates calibrated 10-year Wasatch Front climatological reanalysis series ($2016$–$2026$) matching NOAA GHCN-Daily / PRISM 30-year normals.
  - Computes extraterrestrial solar radiation ($R_a$), Hargreaves/FAO-56 reference evapotranspiration ($\text{ET}_0$), daily GDD ($T_{base}=10^\circ\text{C}$), and rolling cumulative seasonal GDD.
  - Exports partitioned Parquet lake on `D:\gardening_db\parquet_lake\weather\` (`year=YYYY/month=MM/`).
  - Ingests into DuckDB with idempotent `ON CONFLICT (station_id, observation_date) DO UPDATE`.
- `ingest_botanical_traits.py`:
  - Queries Permapeople REST API (with environment token detection) and parses curated PFAF / USDA TABLES data.
  - Normalizes spacing, spread, height, sunlight requirements, soil pH limits, drought tolerance, and companion matrices into `dim_species` and `dim_companion_matrix`.
- `ingest_extension_ground_truth.py`:
  - Loads USU Extension planting calendars, regional freeze normals, cultivar maturity targets, FAO-56 crop coefficients, garden bed infrastructure, phenology observations, and care logs.
  - Implements foreign-key safe idempotent upsert logic (`ON CONFLICT DO NOTHING / UPDATE`).

#### 3.4 DuckDB Arrow-Streamed Daemon (`server.py`)
- Built and deployed a production-ready asynchronous daemon using FastAPI, Uvicorn, and PyArrow IPC streaming.
- Bound to `0.0.0.0:8815` for cross-subnet LAN access (`192.168.x.x`).
- Eliminates DuckDB in-process concurrency lock contention by centralizing access behind thread-safe connection pooling and transactional write locks.
- Endpoints:
  - `POST /query/arrow`: Zero-copy binary Arrow IPC stream (`application/vnd.apache.arrow.stream`).
  - `POST /query`: Typed JSON query execution with schema metadata and latency timing.
  - `POST /execute`: Transactional DDL/DML statement execution.
  - `GET /health`: Health metrics, storage disk size, uptime, and engine versions.
  - `GET /tables`: Registered tables, views, and row counts.
  - `GET /schema/{table}`: Column data types and nullability.

#### 3.5 Windows Administration & PowerShell Automation (`scripts/`)
- `setup_environment.ps1`: Automated directory tree initialization, Python dependencies installation, and Windows Defender Firewall rule configuration for port 8815.
- `start_server.ps1`: Background service launcher with hidden execution and log redirection to `D:\gardening_db\logs\server.log`.
- `stop_server.ps1`: Process listener detection and graceful process termination.

#### 3.6 Client SDK & Verification Suite (`client.py`, `verify_client.py`)
- Implemented `GardeningDuckDBClient` supporting zero-copy `query_arrow()`, `query_df()` (Pandas), `query_polars()`, `query_json()`, and `execute()`.
- Verified end-to-end integration over the physical LAN network interface (`http://192.168.68.56:8815`):
  - **Throughput**: **459,393 rows / second**
  - **Network Download Latency**: **8.65 ms** (3,974 rows $\times$ 20 columns)
  - **Zero-Copy Pandas Conversion**: **9.49 ms**
  - **Concurrency Lock Contention**: **Zero**
  - **View Integrity**: Verified all 4 analytical views and transactional write operations.
