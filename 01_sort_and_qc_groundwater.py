from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
src = ROOT / "deesa_groundwater_validated_working_dataset.csv"
outdir = ROOT / "outputs"
outdir.mkdir(exist_ok=True)

df = pd.read_csv(src)
print("Rows:", len(df))
print("Columns:", list(df.columns))
print("\nMissing values by column:\n", df.isna().sum().to_string())

# Use available source fields rather than assuming a single exact schema.
def first_existing(candidates):
    return next((c for c in candidates if c in df.columns), None)

well_col = first_existing(["Well_ID", "Well_Name", "well_id", "well_name", "Well"])
date_col = first_existing(["Observation_Date", "Observation_Month", "observation_date", "date"])
depth_col = first_existing(["Depth_to_Water_m_bgl", "Depth_m_bgl", "depth_to_water_m_bgl", "Depth_to_Water"])

if well_col is None:
    raise ValueError("Could not identify well ID/name column. Inspect CSV headers and update candidates.")
sort_cols = [well_col]
if date_col:
    # Keep source values; parse a helper key without overwriting the original date.
    df["_sort_date"] = pd.to_datetime(df[date_col], errors="coerce")
    sort_cols.append("_sort_date")
df_sorted = df.sort_values(sort_cols, kind="stable", na_position="last")
if "_sort_date" in df_sorted:
    df_sorted = df_sorted.drop(columns=["_sort_date"])
df_sorted.to_csv(outdir / "groundwater_sorted_by_well_date.csv", index=False)

if well_col and date_col:
    dup = df.duplicated([well_col, date_col], keep=False)
    df.loc[dup].sort_values([well_col, date_col]).to_csv(outdir / "groundwater_duplicate_well_date_keys.csv", index=False)

# Flag known issues transparently; do not delete or correct records.
flags = []
for i, row in df.iterrows():
    reasons = []
    well = str(row.get(well_col, "")).lower() if well_col else ""
    date = str(row.get(date_col, "")) if date_col else ""
    try:
        depth = float(row[depth_col]) if depth_col and pd.notna(row[depth_col]) else None
    except (TypeError, ValueError):
        depth = None
    if "aserda" in well:
        reasons.append("Aserda Pz coordinates require independent confirmation")
    if "deesa" in well and "pz-ii" in well and depth is not None and (depth >= 40 or (date.startswith("2024") and depth < 15)):
        reasons.append("Deesa Pz-II source-reported value flagged in project QC notes")
    if reasons:
        item = row.to_dict()
        item["QC_flag"] = "; ".join(reasons)
        flags.append(item)
if flags:
    pd.DataFrame(flags).to_csv(outdir / "groundwater_known_issue_flags.csv", index=False)

print(f"Sorted dataset written to {outdir / 'groundwater_sorted_by_well_date.csv'}")
print("Source values are preserved; flags are review prompts, not automatic corrections.")
