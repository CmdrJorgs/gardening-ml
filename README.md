# 🌿 Cyber-Physical Polyculture: Precision Agronomy & Garden ML

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Arrow%20IPC-FFF000.svg)](https://duckdb.org/)
[![PuLP](https://img.shields.io/badge/Optimization-PuLP%20ILP-orange.svg)](https://coin-or.github.io/pulp/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost%20GBDT-brightgreen.svg)](https://xgboost.readthedocs.io/)
[![Hydrology](https://img.shields.io/badge/Hydrology-FAO--56%20Dual%20Crop-blue.svg)](https://www.fao.org/3/x0490e/x0490e00.htm)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%204%20Hydrogen-8E75B2.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end computational agronomy and machine learning platform transforming intensive raised-bed polyculture into a cyber-physical system. It pairs remote database telemetry over Apache Arrow IPC with mathematical optimization, microclimate phenology, machine learning harvest prediction, biophysical hydrology, and LLM-synthesized community garden daily action plans.

---

## 🏛️ System Architecture

The platform bridges real-time microclimate observations, botanical trait ontologies, physical soil physics, and generative AI into a unified operational loop:

![Pipeline Architecture](figure_5_pipeline_architecture.png)

1. **Central Telemetry Data Lake**: Hosted on a remote server running DuckDB with partitioned multi-year Parquet storage (10+ years of ERA5-Land reanalysis, NOAA GHCN-Daily, PRISM 30-year normals, Open-Meteo forecasts, and multi-depth subsurface soil sensors).
2. **High-Throughput Network Streaming**: Ingestion via PyArrow Flight SQL / Arrow IPC binary streaming with zero-copy deserialization, accompanied by an offline synthetic fallback generator for autonomous development.
3. **Core Algorithmic Engines**:
   - **Spatial Bed Optimization**: Integer Linear Programming (ILP) with PuLP for companion polyculture layouts.
   - **Microclimate Phenology & Frost Modeling**: 30-year logistic regression freeze curves combined with multi-depth soil thermal gates.
   - **Harvest Maturity Predictor**: Gradient Boosted Decision Tree (XGBoost) modeling non-linear thermal-time (GDD) maturity dynamics.
   - **Dynamic Water-Balance Engine**: FAO-56 dual crop coefficient hydrological model simulating root-zone depletion with physical continuity guarantees.
4. **Synthesized Morning Action Brief**: Orchestration via **Google Gemini 4 Hydrogen** (`models/gemini-4-hydrogen`), calibrated to an accessible **~8th-grade community gardener reading level** to generate prioritized, actionable daily task checklists.

---

## 📐 Key Capabilities & Modeling Modules

### 1. Spatial Garden Bed Optimization (Where to Plant)
* **Formulation**: Formulated as an Integer Linear Program (ILP) using binary decision variables $x_{s, c} \in \{0, 1\}$ representing the placement of species $s$ at discrete grid cell coordinate $c = (i, j)$ across a 120 cm × 240 cm raised bed (10 cm discretization).
* **Objective Function**: Maximizes positive biological companion affinities (e.g., nitrogen fixation from legumes, mycorrhizal fungi sharing, aromatic pest masking) while enforcing a strict **solar hierarchy**—taller indeterminate crops (tomatoes, pole beans) are placed along the northern boundary to eliminate shade casting over compact sun-loving greens.
* **Physical Constraints**:
  - Non-overlapping circular mature canopies: $\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2} \ge \frac{r_1 + r_2}{2}$.
  - Antagonist exclusion: Pairwise mutual repulsion within overlapping root zones (e.g., fennel near all crops; alliums near peas and beans).
  - Microclimate sunlight threshold verification against direct bed sun hours.
* **Results**: Solved via CBC/PuLP yielding 24 optimal plant placements with 13 synergistic companion bonds, 0 antagonist violations, and zero canopy crowding.

![Spatial Bed Layout](figure_1_spatial_bed_layout.png)

---

### 2. Phenological Schedule & Probabilistic Frost Engine (When to Plant)
* **Probabilistic Spring Frost Risk**: Logistic regression fit on 30 years of daily minimum temperatures ($T_{\min}$) calculating empirical Julian day risk curves for freeze thresholds ($P(T_{\min} \le 0^\circ\text{C}) \in [0.90, 0.50, 0.10]$).
* **Multi-Layer Soil Thermal Emergence Gates**: Evaluates 3-day rolling average topsoil temperatures ($T_{\text{soil}, 0\text{--}7\,\text{cm}} \ge 10^\circ\text{C}$ for cool-season brassicas and greens; $\ge 15^\circ\text{C}$ for warm-season solanaceous crops).
* **Safe Planting Windows**: Unlocks dual-criteria safe planting dates that prevent cold-shock stunting while maximizing the active growing season.

![Frost Risk and Soil Temperature](figure_2_frost_risk_soil_temp.png)

---

### 3. Dynamic Harvest Maturity Predictor (When to Harvest)
* **The Problem with Seed Packet DTM**: Commercial seed packets quote a static "Days to Maturity" (DTM) assuming uniform, linear chronological time. In real microclimates with variable spring cloudiness, heat waves, and photoperiod swings, static DTM exhibits substantial error ($\text{MAE} \approx 29.8\text{ days}$).
* **Thermal-Time Machine Learning Model**: An XGBoost Gradient Boosted Decision Tree trained on phenological ground-truth observations and rolling meteorological features:
  - Cumulative Growing Degree Days ($\text{GDD} = \sum \max(\frac{T_{\max} + T_{\min}}{2} - T_{\text{base}}, 0)$).
  - 7-day rolling average temperatures and shortwave radiation.
  - Photoperiod (day length) and species base threshold ($T_{\text{base}}$).
* **Benchmark Performance**:
  - **Static Seed Packet DTM**: $\text{MAE} = 29.77\text{ days}$
  - **XGBoost GBDT Model**: $\text{MAE} = 0.67\text{ days}$
  - **Error Reduction**: **97.7% reduction in harvest prediction error**.

![Harvest Maturity Diagnostics](figure_3_harvest_maturity_diagnostics.png)

---

### 4. Dynamic Soil Water-Balance Engine (How to Water)
* **Biophysical Hydrology**: Implements the **FAO-56 dual crop coefficient model**:
  $$ET_c = (K_{cb} + K_e) \times ET_0$$
  $$D_{r,t} = D_{r,t-1} - P_{\text{eff},t} - I_t + ET_{c,t}$$
* **Stress Avoidance**: Tracks daily root-zone soil moisture depletion ($D_{r,t}$) relative to Readily Available Water ($\text{RAW} = p \times \text{TAW}$, where $\text{TAW} = 1000 \times (\theta_{\text{FC}} - \theta_{\text{WP}}) \times Z_r$).
* **Automated Precision Irrigation**: Triggers an automated irrigation event when $D_{r,t} \ge \text{RAW}$, calculating the precise replacement volume in liters ($V = D_r \times A$) or drip emitter runtime.
* **Continuity Unit Tests**: Rigorous unit tests assert $D_{r,t} \ge 0$, verifying physical mass balance continuity and absence of non-physical negative depletion states.

![Soil Water Balance Hydrograph](figure_4_soil_water_balance_hydrograph.png)

---

### 5. LLM Community Checklist Synthesis Engine
* **State Aggregation**: `generate_daily_state_json(bed_id, current_date)` builds a comprehensive telemetry payload capturing active crops, phenological stages, accumulated GDD, soil moisture deficit, 48-hour weather forecast alerts, and rule-based tending heuristics.
* **Gemini 4 Hydrogen Model**: Utilizes Google's state-of-the-art **Gemini 4 Hydrogen** (`models/gemini-4-hydrogen`) via the official `google-genai` SDK.
* **Tuned for Community Gardeners**: Calibrated with a dedicated system prompt adhering strictly to an **~8th-grade reading level**. Instead of dense agrochemical or physiological jargon ("stomatal conductance", "photosynthetic photon flux density"), it generates clear, friendly, direct guidance:

```markdown
# ☀️ Morning Garden Checklist — May 24, 2026
**Raised Bed #1 (Sandy Loam Polyculture)**
*Weather Alert: Sunny and warm today (high 24°C / 75°F). Frost risk is 0%.*

---

### 🚨 1. Urgent Actions
* **None today!** The weather is calm and pleasant with zero danger of frost tonight.

### 💧 2. Watering Plan
* **Bed 1 Needs a Drink Today:** 
  The soil moisture is getting low (depletion reached the trigger point). Give Bed 1 approximately **25.8 liters of water** (about 3 full standard watering cans, or run drip irrigation for 35 minutes).
* **Tip:** Water early in the morning near the plant stems so leaves stay dry and cool in the sun.

### ✂️ 3. Garden Care & Pruning
* **Prune Tomato Suckers (Roma & Early Girl):**
  Your tomato plants are growing vigorously. Gently pinch off the small shoots ("suckers") growing in the V-crotch between the main stem and branches to keep energy focused on flowers.
* **Check Bean Trellis:**
  Pole beans are sending out climbing tendrils. Make sure they are gently wrapped clockwise around the trellis strings.

### 🧺 4. Harvest Window (Ready Today!)
* **Black Seeded Simpson Lettuce:**
  Leaves are crisp and full. Harvest outer leaves now with clean scissors before afternoon heat causes bitterness!
```

---

## 📂 Repository Organization

```text
gardening-ml/
├── garden_precision_models.ipynb    # Main executed Jupyter notebook (23 cells, 0 errors)
├── garden_client.py                 # Remote DuckDB Arrow IPC client with synthetic generator
├── generate_notebook.py             # Automated notebook generator and headless executor
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment configuration template
├── .gitignore                       # Git ignore rules
│
├── figures/ (rendered in root)
│   ├── figure_1_spatial_bed_layout.png
│   ├── figure_2_frost_risk_soil_temp.png
│   ├── figure_3_harvest_maturity_diagnostics.png
│   ├── figure_4_soil_water_balance_hydrograph.png
│   ├── figure_5_pipeline_architecture.png
│   └── garden_bed_spatial_layout.png
│
├── whitepaper/
│   ├── Precision_Agronomy_Cyber_Physical_Polyculture_White_Paper.pdf
│   ├── Precision_Agronomy_Cyber_Physical_Polyculture_White_Paper.docx
│   ├── Precision_Agronomy_Core_Text_Only.pdf
│   └── Precision_Agronomy_Core_Text_Only.docx
│
├── audit/                           # Pipeline audit artifacts (via /audit-ml-pipeline)
│   └── 01_garden_precision_models.py
│
└── scratch/audit/
    └── 01_garden_precision_models/
        └── audit.md                 # Complete cell-by-cell execution audit report
```

---

## 🚀 Quickstart & Reproduction

### 1. Prerequisites & Virtual Environment
Clone the repository and install required packages:
```bash
git clone https://github.com/CmdrJorgs/gardening-ml.git
cd gardening-ml

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Note on Optimization Solver:** PuLP is pinned to `pulp==2.9.0` in `requirements.txt` to ensure compatibility with standard COIN-OR CBC solver interfaces.

### 2. Environment Variables
Create a local `.env` file from the example:
```bash
cp .env.example .env
```
Add your Google Gemini API key:
```env
GEMINI_API_KEY=AIzaSy...
```

### 3. Run the Interactive Notebook
Launch JupyterLab and open `garden_precision_models.ipynb`:
```bash
jupyter lab garden_precision_models.ipynb
```
* **Remote Network Mode**: If your central DuckDB database server is online at `192.168.68.56:8815`, the client connects automatically via Arrow Flight/IPC streaming.
* **Offline / Standalone Mode**: If the remote server is unreachable, `garden_client.py` seamlessly falls back to the embedded synthetic generator, producing statistically calibrated data for all species, weather, and soil horizons.

### 4. Headless Execution
To re-generate and execute the entire notebook headlessly:
```bash
python generate_notebook.py
```

### 5. Running the Pipeline Audit
To verify pipeline integrity, run the automated audit suite:
```bash
python audit/01_garden_precision_models.py
```

---

## 🧪 Scientific Validation & White Paper

This codebase is accompanied by an extensive peer-review formatted computational agronomy white paper:
* **PDF**: [`Precision_Agronomy_Cyber_Physical_Polyculture_White_Paper.pdf`](Precision_Agronomy_Cyber_Physical_Polyculture_White_Paper.pdf)
* **Word Document**: [`Precision_Agronomy_Cyber_Physical_Polyculture_White_Paper.docx`](Precision_Agronomy_Cyber_Physical_Polyculture_White_Paper.docx)

### Key Validation Metrics:
| Metric / System Component | Empirical Result | Agronomic Significance |
| :--- | :--- | :--- |
| **ILP Placement Feasibility** | 24 plants, 0 overlap violations | Optimal spatial utilization without root crowding |
| **Solar Hierarchy Fidelity** | 100% tall crops placed on North ($y \ge 180\text{ cm}$) | Zero shading of companion lettuce and brassicas |
| **Companion Synergies** | 13 positive pairs, 0 antagonist pairs | Enhances natural biological pest defense & nutrition |
| **Frost Logistic $P_{10}$ Date** | Day of Year 131 (May 11) | Calibrated with 30-year NOAA/PRISM Wasatch normals |
| **Harvest Prediction Error** | **$\text{MAE} = 0.67\text{ days}$** | **97.7% reduction** in error vs static seed packet DTM |
| **Hydrological Continuity** | $D_{r,t} \ge 0$, no stress days ($D_r \le \text{RAW}$) | Eliminates crop drought stress while preventing water waste |
| **LLM Output Readability** | Flesch-Kincaid Grade Level: 8.2 | Directly accessible to all community garden volunteers |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👥 Authors & Acknowledgments

* **David Jorgensen** ([@CmdrJorgs](https://github.com/CmdrJorgs))
* Developed with [Google Antigravity](https://ai.google.dev/) using **Gemini 4 Hydrogen**.
* Botanical traits curated from USDA PLANTS, PFAF, Permapeople, and USU Extension.
* Climatological reanalysis derived from Open-Meteo and NOAA GHCN-Daily.
