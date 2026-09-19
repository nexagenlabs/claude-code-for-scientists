#!/usr/bin/env python3
"""A dose-response experiment, laid out the way people actually run one."""
import numpy as np, pandas as pd

rng = np.random.default_rng(1111)
TRUE_IC50, TRUE_HILL, TRUE_BOTTOM, TRUE_TOP = 42.0, 1.3, 8.0, 100.0

def curve(x, ic50=TRUE_IC50, hill=TRUE_HILL, bottom=TRUE_BOTTOM, top=TRUE_TOP):
    return bottom + (top - bottom) / (1 + (x / ic50) ** hill)

# The full series somebody would run if they had the plate space.
full_doses = np.array([0.5, 1.5, 5, 15, 45, 135, 400, 1200])
# What most people actually run: a narrower series, stopping too early.
short_doses = np.array([1, 3, 10, 30, 100])

rows = []
for name, doses in (("full", full_doses), ("short", short_doses)):
    for plate in ["P1", "P2", "P3"]:
        for d in doses:
            v = curve(d) + rng.normal(0, 3.0)
            rows.append({"series": name, "plate": plate,
                         "dose_uM": float(d), "viability_pct": round(v, 2)})

pd.DataFrame(rows).to_csv("dose.csv", index=False)
print(f"true IC50 {TRUE_IC50} uM, Hill slope {TRUE_HILL}, "
      f"bottom {TRUE_BOTTOM}, top {TRUE_TOP}")
print(f"full series  {full_doses.min()} to {full_doses.max()} uM")
print(f"short series {short_doses.min()} to {short_doses.max()} uM")
