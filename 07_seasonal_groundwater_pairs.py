#!/usr/bin/env python3
"""Reproduce Deesa Taluka matched seasonal groundwater-level analysis.

Input: deesa_groundwater_validated_working_dataset.csv
Rules:
- Pre-monsoon: Observation_Month ending in -05 (May).
- Post-monsoon: Observation_Month ending in -10 or -11 (October/November).
- Match within the same Well_Name and calendar year.
- Retain only unique one-to-one May and October/November records per well-year.
- Exclude a matched pair from the primary summary if either record's QC_Flag
  contains 'Large abrupt change'. Source values are retained unchanged in the
  matched-pairs output, with an inclusion flag and exclusion reason.
- Observation_Month is used, not placeholder day values in exact dates.

This is seasonal depth-to-water comparison, not an aquifer-wide storage estimate.
"""
from pathlib import Path
import argparse
import re
import pandas as pd


def aquifer_group(value: object) -> str:
    s = str(value).lower()
    # Order matters: distinguish Semi-Confined and Confined-II/I before generic Confined.
    if "semi-confined" in s:
        return "Semi-Confined"
    if "confined-ii" in s:
        return "Confined-II"
    if "confined-i" in s:
        return "Confined-I"
    if "unconfined" in s:
        return "Unconfined"
    if "confined" in s:
        return "Confined (unspecified)"
    return "Unclassified"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to working groundwater CSV")
    ap.add_argument("--outdir", default="outputs", help="Output directory")
    args = ap.parse_args()

    src = pd.read_csv(args.input)
    required = {
        "Source_Row", "Well_Name", "Observation_Month", "Depth_to_Water_m_bgl",
        "Aquifer_Type_source", "Owner_source", "Date_Precision", "QC_Flag"
    }
    missing = required - set(src.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {sorted(missing)}")

    src["Observation_Month"] = src["Observation_Month"].astype("string")
    src["Year"] = pd.to_numeric(src["Observation_Month"].str.slice(0, 4), errors="coerce")
    src["Month"] = pd.to_numeric(src["Observation_Month"].str.slice(5, 7), errors="coerce")
    src["Depth_to_Water_m_bgl"] = pd.to_numeric(src["Depth_to_Water_m_bgl"], errors="coerce")
    src["QC_Flag"] = src["QC_Flag"].fillna("").astype(str)

    pre = src[src["Month"].eq(5)]
    post = src[src["Month"].isin([10, 11])]
    rows = []
    ambiguous = []

    for (well, year), g_pre in pre.groupby(["Well_Name", "Year"], dropna=False):
        g_post = post[(post["Well_Name"] == well) & (post["Year"] == year)]
        if len(g_pre) == 1 and len(g_post) == 1:
            a, b = g_pre.iloc[0], g_post.iloc[0]
            delta = b["Depth_to_Water_m_bgl"] - a["Depth_to_Water_m_bgl"]
            flags = " | ".join(x for x in [a["QC_Flag"], b["QC_Flag"]] if x)
            exclude = bool(re.search(r"Large abrupt change", flags, flags=re.I))
            rows.append({
                "Well_Name": well,
                "Year": int(year),
                "Pre_Month": a["Observation_Month"],
                "Post_Month": b["Observation_Month"],
                "Pre_Depth_m_bgl": a["Depth_to_Water_m_bgl"],
                "Post_Depth_m_bgl": b["Depth_to_Water_m_bgl"],
                "Delta_Post_minus_Pre_m": delta,
                "Aquifer_Group": aquifer_group(a["Aquifer_Type_source"]),
                "Aquifer_Pre_raw": a["Aquifer_Type_source"],
                "Aquifer_Post_raw": b["Aquifer_Type_source"],
                "Pre_Source": a["Owner_source"],
                "Post_Source": b["Owner_source"],
                "Pre_Source_Row": a["Source_Row"],
                "Post_Source_Row": b["Source_Row"],
                "Pre_Date_Precision": a["Date_Precision"],
                "Post_Date_Precision": b["Date_Precision"],
                "QC_Flag": flags,
                "Included_in_primary_summary": not exclude,
                "Exclusion_reason": "Large abrupt change flagged in source QC" if exclude else ""
            })
        elif len(g_pre) > 1 or len(g_post) > 1:
            ambiguous.append({"Well_Name": well, "Year": year,
                              "May_records": len(g_pre), "OctNov_records": len(g_post),
                              "Status": "Not paired: non-unique seasonal record"})

    pairs = pd.DataFrame(rows).sort_values(["Well_Name", "Year"]).reset_index(drop=True)
    included = pairs[pairs["Included_in_primary_summary"]].copy()
    if len(pairs) == 0:
        raise ValueError("No unique matched seasonal pairs found; inspect input date fields.")

    def summary_row(label: str, d: pd.DataFrame) -> dict:
        delta = d["Delta_Post_minus_Pre_m"]
        return {
            "Group": label,
            "Matched_pairs": len(d),
            "Distinct_well_name_labels": d["Well_Name"].nunique(),
            "Post_monsoon_depth_shallower_n": int((delta < 0).sum()),
            "Post_monsoon_depth_deeper_n": int((delta > 0).sum()),
            "No_change_n": int((delta == 0).sum()),
            "Mean_delta_post_minus_pre_m": delta.mean(),
            "Median_delta_post_minus_pre_m": delta.median(),
            "Interpretation": "Negative delta means post-monsoon depth is shallower."
        }

    summary = [summary_row("All unique matched pairs (before QC exclusions)", pairs),
               summary_row("Primary analysis (large-abrupt-change pairs excluded)", included)]
    for group, d in included.groupby("Aquifer_Group", dropna=False):
        summary.append(summary_row(f"Aquifer: {group}", d))

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    pairs.to_csv(outdir / "deesa_seasonal_groundwater_matched_pairs.csv", index=False)
    pd.DataFrame(summary).to_csv(outdir / "deesa_seasonal_groundwater_summary.csv", index=False)
    pd.DataFrame(ambiguous, columns=["Well_Name", "Year", "May_records", "OctNov_records", "Status"]).to_csv(
        outdir / "deesa_seasonal_groundwater_unmatched_ambiguous.csv", index=False)

    print(f"Input records: {len(src)}")
    print(f"Distinct non-null Well_Name labels: {src['Well_Name'].nunique()}")
    print("No Well_ID field is present; distinct labels are not independently verified physical-well IDs.")
    print(f"Unique matched pairs before QC exclusions: {len(pairs)}")
    print(f"Distinct labels in matched sample: {pairs['Well_Name'].nunique()}")
    print(f"Pairs excluded by large-abrupt-change QC flag: {len(pairs) - len(included)}")
    print(f"Primary matched pairs: {len(included)}")
    if len(included):
        d = included["Delta_Post_minus_Pre_m"]
        print(f"Primary direction counts (shallower/deeper/unchanged): {(d<0).sum()}/{(d>0).sum()}/{(d==0).sum()}")
        print(f"Primary mean delta (m): {d.mean():.6f}")
    print(f"Ambiguous well-year groups not paired: {len(ambiguous)}")
    print(f"Outputs written to: {outdir.resolve()}")

if __name__ == "__main__":
    main()
