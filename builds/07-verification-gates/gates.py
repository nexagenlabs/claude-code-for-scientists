#!/usr/bin/env python3
"""Four families of verification gate over the plate pipeline."""
import sys
import pandas as pd

EXPECTED_WELLS = 32
OD_MIN, OD_MAX = 0.0, 4.0

def run(clean="plate_clean.csv", excluded="plate_excluded.csv",
        sheet="sample_sheet.csv", viability="plate_viability.csv"):
    kept = pd.read_csv(clean)
    excl = pd.read_csv(excluded)
    ss = pd.read_csv(sheet)
    failures = []

    def gate(family, claim, message):
        if not claim:
            failures.append(f"[{family}] {message}")

    # 1. CONSERVATION: nothing appears or disappears without being counted.
    total = len(kept) + len(excl)
    gate("conservation", total == EXPECTED_WELLS,
         f"{EXPECTED_WELLS} wells expected, {total} accounted for")
    gate("conservation", kept["well"].is_unique, "a well appears twice")

    # 2. RANGE: every value is physically possible for the instrument.
    gate("range", kept["od595"].between(OD_MIN, OD_MAX).all(),
         f"OD outside {OD_MIN} to {OD_MAX}: "
         f"max seen {kept['od595'].max():.4g}")
    gate("range", (kept["conc_uM"] >= 0).all(), "negative concentration")

    # 3. INVARIANT: a quantity whose value we know before looking.
    #    Checked against what the pipeline wrote, never recomputed here.
    via = pd.read_csv(viability)
    dmso_via = via.loc[via.treatment == "DMSO", "viability_pct"].mean()
    gate("invariant", abs(dmso_via - 100) < 0.01,
         f"DMSO should normalise to 100 by construction, pipeline gave "
         f"{dmso_via:.2f}")

    # 4. PROVENANCE: the data matches what the bench said was on the plate.
    merged = ss.merge(kept, on="well", how="inner", suffixes=("_sheet", "_data"))
    mismatch = merged[(merged.treatment_sheet != merged.treatment_data) |
                      (merged.sample_id_sheet != merged.sample_id_data)]
    gate("provenance", len(mismatch) == 0,
         f"{len(mismatch)} well(s) disagree with the sample sheet: "
         f"{list(mismatch.well)[:4]}")

    if failures:
        for f in failures:
            print(f)
        return 1
    print("All gates passed.")
    return 0

if __name__ == "__main__":
    sys.exit(run(*sys.argv[1:]))
