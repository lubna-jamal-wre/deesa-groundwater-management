from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
src = ROOT / "deesa_rainfall_1987_2022_rechecked.csv"
df = pd.read_csv(src)
print("Columns:", list(df.columns))

year_col = next((c for c in df.columns if "year" in c.lower()), None)
rain_col = next((c for c in df.columns if "rain" in c.lower() or "precip" in c.lower()), None)
if not year_col or not rain_col:
    raise ValueError("Could not identify year/rainfall columns. Inspect CSV headers and update candidates.")
df[rain_col] = pd.to_numeric(df[rain_col], errors="coerce")
x = df[rain_col].dropna()
summary = pd.DataFrame([{
    "n": int(x.count()),
    "mean_mm": x.mean(),
    "median_mm": x.median(),
    "minimum_mm": x.min(),
    "minimum_year": int(df.loc[df[rain_col].idxmin(), year_col]),
    "maximum_mm": x.max(),
    "maximum_year": int(df.loc[df[rain_col].idxmax(), year_col]),
    "population_sd_mm": x.std(ddof=0),
    "sample_sd_mm": x.std(ddof=1),
}])
outdir = ROOT / "outputs"
outdir.mkdir(exist_ok=True)
summary.to_csv(outdir / "rainfall_summary_statistics.csv", index=False)
print(summary.to_string(index=False))
