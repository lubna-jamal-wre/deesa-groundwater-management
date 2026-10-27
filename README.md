# Deesa Taluka Groundwater Management — Reproducible Code Bundle

This repository contains the data, Python scripts and generated outputs used for the preliminary analysis of groundwater-resource availability and management scenarios in Deesa Taluka, Banaskantha, Gujarat, prepared for the CE 766 preliminary project at IIT Bombay.

**Important limitation:** This is a preliminary analysis. Intervention scenarios are assumption-based sensitivity calculations, not predictions from a calibrated groundwater-flow model.

## Contents

- Root directory: input CSV files, six Python scripts, `README.md` and `requirements.txt`.
- `outputs/`: processed groundwater data, quality-control reports, rainfall statistics, trend-screening results, groundwater-balance calculations, intervention scenario tables and figures.


## Repository structure

- Root directory: Python scripts, input CSV files, `README.md` and `requirements.txt`.
- `outputs/`: generated data-quality reports, processed groundwater records, rainfall statistics, January trend-screening results, groundwater-balance tables, intervention scenario tables and the baseline figure.

The six Python scripts are:

- `01_sort_and_qc_groundwater.py` — sorts groundwater records and generates data-quality checks.
- `02_rainfall_statistics.py` — calculates descriptive rainfall statistics.
- `03_january_trend_screening.py` — performs well-specific January groundwater-depth trend screening.
- `04_groundwater_balance.py` — calculates the 2023 baseline groundwater balance.
- `05_intervention_scenarios.py` — calculates standalone and combined intervention sensitivities.
- `06_make_baseline_figure.py` — generates the baseline groundwater-resource and extraction figure.


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

Run these commands from the repository root directory.

First, install the required packages:

`python -m pip install -r requirements.txt`

Then run the scripts in order:

`python 01_sort_and_qc_groundwater.py`

`python 02_rainfall_statistics.py`

`python 03_january_trend_screening.py`

`python 04_groundwater_balance.py`

`python 05_intervention_scenarios.py`

`python 06_make_baseline_figure.py`

Generated tables and figures are written to `outputs/`.

## Baseline constants used
- Extractable groundwater resource R0 = 227.1736 MCM
- Irrigation extraction I0 = 311.6495 MCM
- Domestic + industrial extraction N0 = 12.3346 MCM
- Total extraction E0 = 323.9841 MCM
- CGWB-reported additional-recharge estimate Q0 = 22.21 MCM

## Citation
Prepared for the CE 766 preliminary project, IIT Bombay (2026). Original external datasets remain attributable to the agencies listed above.
