# Deesa Taluka Groundwater Management — Reproducible Analysis Repository

## Project status and purpose
This repository supports the CE 766 project **“Groundwater Management Strategies under Uncertain Recharge: A Case Study of Deesa Taluka, Banaskantha, Gujarat.”** It contains the working datasets, quality-control records, analysis scripts and scenario outputs used for a site-specific screening assessment. The analysis includes a partial groundwater-resource accounting and matched seasonal groundwater-level comparisons. It is **not** a closed physical water budget, a calibrated groundwater-flow model, or field verification of intervention performance.

## Data and units
- `data/deesa_rainfall_1987_2022_rechecked.csv`: 36 annual rainfall values for 1987–2022, in millimetres (mm). The values were transcribed from the CGWB Aquifer Management Plan, which attributes the series to the WRI State Data Centre, Government of Gujarat. The original station-level file has not been independently retrieved and reconciled.
- `data/deesa_groundwater_validated_working_dataset.csv`: 410 groundwater-monitoring records, spanning 2013–2024. The file contains **30 distinct non-null `Well_Name` labels**. It does not contain a dedicated `Well_ID` field; therefore, 30 is a count of name labels, not an independently verified count of unique physical monitoring installations. Depth to water is in metres below ground level (m bgl). `Observation_Month` is used to preserve source month-level precision.
- `data/deesa_groundwater_validation_exception_log.csv`, `data/deesa_groundwater_validation_final_summary.txt`, and related verification files document known transcription and quality-control limitations.
- `outputs/deesa_seasonal_groundwater_matched_pairs.csv`: matched May–October/November observations, including excluded pairs and QC reasons.
- `outputs/deesa_seasonal_groundwater_summary.csv`: overall and aquifer-group seasonal summaries.
- `outputs/deesa_seasonal_groundwater_unmatched_ambiguous.csv`: well-year groups not paired because seasonal records were non-unique (if any).

Groundwater resource and extraction values are reported in million cubic metres (MCM) after conversion from hectare-metres (ham), using **1 ham = 0.01 MCM**.

## Seasonal groundwater comparison — reproducible method
The script `scripts/07_seasonal_groundwater_pairs.py` pairs observations by the same `Well_Name` and calendar year:
1. May (`Observation_Month` ending in `-05`) is treated as the pre-monsoon observation.
2. October or November (`-10` or `-11`) is treated as the post-monsoon observation.
3. Only unique one-to-one May and October/November records for a well-year are paired. Month-year fields are used; placeholder day values are not treated as exact dates.
4. A pair is excluded from the primary summary if either observation carries the source QC phrase “Large abrupt change”. The original values remain in the matched-pairs output, with an inclusion flag and exclusion reason.
5. Change is calculated as `post-monsoon depth − pre-monsoon depth` in m. A negative value means the post-monsoon depth is shallower.

Reproduce from the repository root (after installing pandas):

```bash
python scripts/07_seasonal_groundwater_pairs.py \
  --input data/deesa_groundwater_validated_working_dataset.csv \
  --outdir outputs
```

### Seasonal comparison results from the current working CSV
- 410 source records.
- 30 distinct non-null well-name labels; no dedicated well-ID field is available.
- 115 unique matched well-year pairs across 25 name labels before QC exclusions.
- Two matched pairs carry the explicit “Large abrupt change” QC flag and are excluded from the primary summary.
- Primary summary: 113 pairs across 25 name labels; 94 show a shallower post-monsoon depth, 18 show a deeper post-monsoon depth, and one is unchanged.
- Mean post-minus-pre depth change in the primary sample: **−1.8154 m**; median: **−2.10 m**.

These are sample-based seasonal depth comparisons. They are not annual storage changes and must not be extrapolated to the full 1,084 km² taluka without a defensible monitoring-network representativeness analysis and aquifer-specific spatial information. Some GWRDC records have month-year-only date precision. Source transcription was checked against the searchable PDF text layer, but not every record was independently image-verified.

## Principal original sources
1. Central Ground Water Board (CGWB), *Aquifer Management Plan of Deesa Taluka, Banaskantha District, Gujarat (NAQUIM 2.0), 2024*: https://cgwb.gov.in/cgwbpnm/public/publication-detail/1647
2. CGWB, *Gujarat Ground Water Year Book 2023–24*: https://gwdata.cgwb.gov.in/download/Yearbook/Gujarat_GWYB%202023-24.pdf
3. Gujarat Green Revolution Company (GGRC), taluka-wise micro-irrigation achievements: https://www.ggrc.co.in/documents/Achievements.pdf

## 2023 baseline accounting and scenarios
The detailed CGWB 2023 resource-assessment table is used as the scenario baseline:
- Annual extractable groundwater resource `R0` = 227.1736 MCM.
- Irrigation extraction `I0` = 311.6495 MCM.
- Domestic plus industrial extraction `N0` = 12.3346 MCM.
- Total extraction `E0` = 323.9841 MCM.
- Baseline extraction stage = `(E0 / R0) × 100` = approximately 142.62%.
- Extraction less annual extractable resource = 96.8105 MCM. This is an accounting difference, **not a direct measurement of aquifer-storage depletion**.

The agreed intervention framework is:
1. Irrigation-pumping reductions of 10%, 20% and 30%.
2. Micro-irrigation using 97.576 MCM as a potential crop-water-saving planning estimate only. It is not automatically treated as groundwater-pumping savings.
3. Artificial recharge at 50%, 75% and 100% realisation of the assumed 22.21 MCM additional-recharge estimate.
4. Combined irrigation-pumping reduction and artificial recharge.

For pumping reduction fraction `p` and additional-recharge realisation fraction `q`:

```text
Ep = E0 - p * I0
Rq = R0 + q * 22.21
ES = (Ep / Rq) * 100
```

`R0` is the **net annual extractable resource**, not gross recharge. These are conditional arithmetic scenarios, not calibrated predictions of aquifer recovery. The micro-irrigation planning estimate is kept separate to avoid double-counting potential crop-water savings as pumping reductions.

## Important CGWB source discrepancy
The CGWB management-plan narrative prints total annual recharge as 2,524.15 ham, while the detailed resource accounting reports natural discharge of 2,524.15 ham and annual extractable resource of 22,717.36 ham. Adding the latter two values implies gross recharge of 25,241.51 ham, but that implied value is **not treated as a verified reported recharge measurement**. The discrepancy is retained transparently; scenario calculations use the directly reported net annual extractable resource as `R0`.

## Other limitations and quality-control notes
- Rainfall volume calculated from mean rainfall and area is gross precipitation, not groundwater recharge.
- Rainfall series, monitoring observations and the 2023 resource assessment have different temporal coverage and are not a continuous calibrated time series.
- The working groundwater dataset has 30 name labels, not a verified physical-well ID count. Name variants and station identity need source-level reconciliation.
- Aserda Pz coordinates, Deesa Pzii observations and other flagged changes require independent source-image or field confirmation.
- Month-year-only dates must not be interpreted as exact day-level dates.
- The 22.21 MCM recharge value and its realisation fractions are planning assumptions; realised recharge has not been field-verified.
- The 97.576 MCM micro-irrigation figure is potential crop-water savings. The groundwater-sourced share and actual pumping response are unknown.
- Independent rainfall-derived recharge, all other recharge components, natural discharge, boundary inflows/outflows and taluka-wide annual storage change are not fully quantified. The available accounting is therefore partial and must not be described as a closed water budget.

## Suggested citation
Jamal, L. (2026). *Deesa Taluka Groundwater Management: Reproducible Analysis and Quality-Control Files*. CE 766 project repository. Cite the original CGWB and GGRC sources above for source-derived data.
