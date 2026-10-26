# Deesa Taluka Groundwater Management — Reproducible Code Bundle

## Important honesty note
# Deesa Groundwater Management Project

This repository contains the data and Python scripts used for the preliminary analysis of groundwater-resource availability and management scenarios in Deesa Taluka, Banaskantha, Gujarat.

## Contents
- `data/` — Rainfall, groundwater-level and groundwater-resource datasets, with supporting files.
- `scripts/` — Python scripts for data processing, statistical analysis, groundwater-balance calculations and intervention scenarios.
- `outputs/` — Generated tables, results and figures.
- `requirements.txt` — Python package requirements.

**Note:** The analysis is preliminary. Scenario results depend on stated assumptions.

## Folder structure
- `data/`: working CSVs and the available validation bundle.
- `scripts/01_sort_and_qc_groundwater.py`: reads the 410-record working groundwater CSV, sorts by well/month, reports missingness and flags known issues without silently modifying source values.
- `scripts/02_rainfall_statistics.py`: calculates annual rainfall descriptive statistics.
- `scripts/03_january_trend_screening.py`: performs well-specific OLS trend screening for January observations where possible, retaining caveats and source-flag exclusions.
- `scripts/04_groundwater_balance.py`: calculates the 2023 CGWB baseline balance and extraction stage.
- `scripts/05_intervention_scenarios.py`: calculates standalone and combined scenario sensitivities.
- `scripts/06_make_baseline_figure.py`: generates a baseline groundwater resource/extraction chart.
- `outputs/`: generated result tables and figure.
- `requirements.txt`: Python package requirements.

## Main source data and units
1. CGWB, *Aquifer Management Plan of Deesa Taluka, Banaskantha District, Gujarat (NAQUIM 2.0), 2024*: https://cgwb.gov.in/cgwbpnm/public/publication-detail/1647
2. CGWB, *Gujarat Ground Water Year Book 2023–24*: https://gwdata.cgwb.gov.in/download/Yearbook/Gujarat_GWYB%202023-24.pdf
3. GGRC, taluka-wise micro-irrigation achievements: https://www.ggrc.co.in/documents/Achievements.pdf

Rainfall is in millimetres (mm). Groundwater depth is in metres below ground level (m bgl). Groundwater-resource and extraction volumes are expressed in million cubic metres (MCM) after conversion from hectare-metres (ham), using 1 ham = 0.01 MCM.

## Methods implemented in these scripts
- Sort monitoring records by well identifier/name and observation month/date.
- Report duplicate keys, missing values, and flagged observations; do not silently correct source values.
- Compute rainfall mean, median, minimum, maximum, population standard deviation and sample standard deviation.
- Fit ordinary least-squares (OLS) trend lines to January depth-to-water observations per well, with minimum-observation criteria. A positive slope means depth to water is increasing (water level is becoming deeper). Trend estimates are site-specific and not a taluka-wide estimate.
- Calculate extraction stage = total extraction / annual extractable groundwater resource × 100.
- Calculate scenarios using fixed 2023 baseline values. Irrigation-pumping reduction p is applied to irrigation extraction only, holding domestic/industrial extraction constant. Additional recharge fraction q is applied to the CGWB-reported 22.21 MCM estimate.

## Critical limitations
- The working groundwater dataset contains 410 records from 31 named wells, but not all rows have been image-by-image verified against the source PDF. Numeric text-layer checks are not independent station verification.
- Month-only observation dates must not be treated as exact day-level dates.
- Aserda Pz coordinates and some Deesa Pz-II readings are flagged for independent confirmation; Fagudara Pz readings have unusual within-year changes. Check validation logs before interpreting trend outputs.
- The 2022 resource-assessment table appears to have inconsistent/mislabelled extraction categories; scripts do not silently correct it.
- CGWB micro-irrigation/recharge figures are planning estimates, not measured realised savings or verified recharge performance.
- Scenario arithmetic is not a dynamic groundwater model and does not simulate aquifer storage or groundwater-level response.
- This package does not include a calibrated groundwater-flow model.

## Run
From this folder, install dependencies with:
`python -m pip install -r requirements.txt`

Run scripts in order:
`python scripts/01_sort_and_qc_groundwater.py`
`python scripts/02_rainfall_statistics.py`
`python scripts/03_january_trend_screening.py`
`python scripts/04_groundwater_balance.py`
`python scripts/05_intervention_scenarios.py`
`python scripts/06_make_baseline_figure.py`

Scripts write generated tables/figures to `outputs/`.

## Baseline constants used
- Extractable groundwater resource R0 = 227.1736 MCM
- Irrigation extraction I0 = 311.6495 MCM
- Domestic + industrial extraction N0 = 12.3346 MCM
- Total extraction E0 = 323.9841 MCM
- CGWB-reported additional-recharge estimate Q0 = 22.21 MCM

## Citation
Prepared for the CE 766 preliminary project, IIT Bombay (2026). Original external datasets remain attributable to the agencies listed above.
