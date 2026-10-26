from pathlib import Path
import pandas as pd

R0 = 227.1736  # MCM annual extractable groundwater resource
I0 = 311.6495  # MCM irrigation extraction
N0 = 12.3346   # MCM domestic + industrial extraction
E0 = 323.9841  # MCM total extraction
stage = 100 * E0 / R0
rows = [
    ("Annual extractable groundwater resource", R0),
    ("Irrigation extraction", I0),
    ("Domestic + industrial extraction", N0),
    ("Total groundwater extraction", E0),
    ("Extraction stage (%)", stage),
    ("Extraction minus extractable resource (MCM)", E0 - R0),
]
outdir = Path(__file__).resolve().parents[1] / "outputs"
outdir.mkdir(exist_ok=True)
pd.DataFrame(rows, columns=["Parameter", "Value"]).to_csv(outdir / "groundwater_balance_2023.csv", index=False)
print(f"Extraction stage = (E0/R0)*100 = ({E0:.4f}/{R0:.4f})*100 = {stage:.2f}%")
print(f"Extraction minus resource = {E0-R0:.4f} MCM (screening indicator, not measured storage deficit)")
