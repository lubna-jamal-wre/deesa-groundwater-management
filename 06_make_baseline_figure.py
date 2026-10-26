from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
outdir = ROOT / "outputs"
outdir.mkdir(exist_ok=True)

labels = [
    "Extractable groundwater resource",
    "Irrigation extraction",
    "Domestic + industrial extraction",
    "Total groundwater extraction",
]
values = [227.1736, 311.6495, 12.3346, 323.9841]
fig, ax = plt.subplots(figsize=(9, 4.8))
bars = ax.barh(labels, values)
ax.invert_yaxis()
ax.set_xlabel("Annual volume (MCM)")
ax.set_title("Deesa Taluka: Groundwater Resource and Extraction, 2023")
ax.grid(axis="x", linestyle="--", linewidth=0.6)
ax.set_axisbelow(True)
ax.bar_label(bars, labels=[f"{v:.2f}" for v in values], padding=4, fontsize=9)
ax.set_xlim(0, 370)
fig.text(0.01, 0.01,
         "Note: Total extraction includes irrigation, domestic and industrial uses.",
         ha="left", fontsize=8)
fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig(outdir / "Deesa_Groundwater_Balance_2023.png", dpi=300, bbox_inches="tight")
print(outdir / "Deesa_Groundwater_Balance_2023.png")
