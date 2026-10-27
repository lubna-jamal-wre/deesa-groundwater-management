from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent
src = ROOT / "deesa_groundwater_validated_working_dataset.csv"
df = pd.read_csv(src)

def find_col(cands):
    return next((c for c in cands if c in df.columns), None)

well_col = find_col(["Well_ID", "Well_Name", "well_id", "well_name", "Well"])
date_col = find_col(["Observation_Date", "Observation_Month", "observation_date", "date"])
depth_col = find_col(["Depth_to_Water_m_bgl", "Depth_m_bgl", "depth_to_water_m_bgl", "Depth_to_Water"])
if not all([well_col, date_col, depth_col]):
    raise ValueError(f"Required columns not found. Available columns: {list(df.columns)}")

# Parse month/date into a helper field. Preserve original source field.
df["_date"] = pd.to_datetime(df[date_col], errors="coerce")
df["_depth"] = pd.to_numeric(df[depth_col], errors="coerce")
df = df[df["_date"].notna() & df["_depth"].notna()]
df = df[df["_date"].dt.month == 1].copy()

# Exclude flagged records based on documented QC notes; retain them in source CSV.
def qc_exclude(row):
    well = str(row[well_col]).lower()
    date = row["_date"]
    depth = row["_depth"]
    if "aserda" in well:
        return True
    if "deesa" in well and "pz-ii" in well and (
        (date.year == 2018 and depth >= 40) or (date.year == 2024 and depth < 15)
    ):
        return True
    return False

df["_excluded_qc"] = df.apply(qc_exclude, axis=1)
df = df[~df["_excluded_qc"]]

rows = []
for well, g in df.groupby(well_col):
    g = g.sort_values("_date")
    # OLS: depth = intercept + slope * decimal year; slope is m/year.
    if len(g) < 4 or g["_date"].dt.year.nunique() < 3:
        continue
    years = g["_date"].dt.year.to_numpy(dtype=float)
    depths = g["_depth"].to_numpy(dtype=float)
    slope, intercept = np.polyfit(years, depths, 1)
    pred = intercept + slope * years
    ss_res = np.sum((depths - pred) ** 2)
    ss_tot = np.sum((depths - np.mean(depths)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    rows.append({
        "Well": well,
        "n_January_observations": len(g),
        "first_year": int(g["_date"].dt.year.min()),
        "last_year": int(g["_date"].dt.year.max()),
        "first_depth_m_bgl": float(depths[np.argmin(years)]),
        "last_depth_m_bgl": float(depths[np.argmax(years)]),
        "OLS_slope_m_per_year": float(slope),
        "R_squared": float(r2),
        "interpretation": "depth increasing / water level deeper" if slope > 0 else "depth decreasing / water level shallower",
        "caveat": "well-specific screening; interpret with source/QC limitations",
    })

outdir = ROOT / "outputs"
outdir.mkdir(exist_ok=True)
result = pd.DataFrame(rows).sort_values("Well") if rows else pd.DataFrame()
result.to_csv(outdir / "january_ols_trend_screening_reproduced.csv", index=False)
print(result.to_string(index=False) if len(result) else "No well met the minimum data criteria.")
