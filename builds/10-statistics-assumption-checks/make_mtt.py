#!/usr/bin/env python3
"""Four independent MTT experiments, three technical wells per condition.

Each plate carries a small batch offset, which is what makes technical
wells within a plate correlated and is the whole reason the distinction
between a well and an experiment matters.
"""
import numpy as np, pandas as pd

rng = np.random.default_rng(1010)
plates = ["P1", "P2", "P3", "P4"]
conds = {"DMSO": 100.0, "TMZ_50": 92.0, "TMZ_100": 86.0}

rows = []
for p in plates:
    plate_offset = rng.normal(0, 6.0)        # the batch effect, per plate
    for cond, true_mean in conds.items():
        for well in range(3):                # technical wells
            value = true_mean + plate_offset + rng.normal(0, 1.6)
            rows.append({"plate": p, "treatment": cond,
                         "well": f"{p}_{cond}_{well+1}",
                         "viability_pct": round(value, 2)})

df = pd.DataFrame(rows)
df.to_csv("mtt.csv", index=False)
print(f"{len(df)} wells, {df.plate.nunique()} plates, "
      f"{df.treatment.nunique()} conditions")
print(df.groupby(["treatment"]).viability_pct.agg(["mean", "std"]).round(2))
