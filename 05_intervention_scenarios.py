from pathlib import Path
import pandas as pd

R0, I0, N0, E0, Q0 = 227.1736, 311.6495, 12.3346, 323.9841, 22.21
outdir = Path(__file__).resolve().parents[1] / "outputs"
outdir.mkdir(exist_ok=True)

standalone = []
for p in (0.10, 0.20, 0.30):
    E = E0 - p * I0
    standalone.append({
        "irrigation_pumping_reduction_pct": 100*p,
        "extraction_MCM": E,
        "resource_MCM": R0,
        "extraction_stage_pct": 100*E/R0,
        "extraction_minus_resource_MCM": E-R0,
        "assumption": "non-irrigation extraction and resource unchanged",
    })
for q in (0.50, 0.75, 1.00):
    R = R0 + q*Q0
    standalone.append({
        "irrigation_pumping_reduction_pct": 0,
        "recharge_realisation_pct": 100*q,
        "extraction_MCM": E0,
        "resource_MCM": R,
        "extraction_stage_pct": 100*E0/R,
        "extraction_minus_resource_MCM": E0-R,
        "assumption": "extraction unchanged; additional recharge q*22.21 MCM assumed",
    })
pd.DataFrame(standalone).to_csv(outdir / "standalone_scenarios.csv", index=False)

combined = []
for p in (0.10, 0.20, 0.30):
    E = E0 - p*I0
    for q in (0.50, 0.75, 1.00):
        R = R0 + q*Q0
        combined.append({
            "irrigation_pumping_reduction_pct": 100*p,
            "recharge_realisation_pct": 100*q,
            "extraction_MCM": E,
            "resource_MCM": R,
            "extraction_stage_pct": 100*E/R,
            "extraction_minus_resource_MCM": E-R,
            "assumption": "conditional arithmetic only; not a groundwater model",
        })
pd.DataFrame(combined).to_csv(outdir / "combined_scenarios.csv", index=False)
print("Scenario tables saved. These are assumptions-based calculations, not validated predictions.")
