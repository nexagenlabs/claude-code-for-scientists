#!/usr/bin/env python3
"""Evaporation from the outer ring, and what it does to an IC50."""
import numpy as np, pandas as pd
from scipy.optimize import curve_fit

rng = np.random.default_rng(1616)
TRUE_IC50 = 42.0
doses = np.array([0.5, 1.5, 5, 15, 45, 135, 400, 1200])

def hill(x, bottom, top, ic50, slope):
    return bottom + (top - bottom) / (1 + (x / ic50) ** slope)

def viability(d): return hill(d, 8.0, 100.0, TRUE_IC50, 1.3)

# A 96-well plate: rows A to H, columns 1 to 12. The dose series runs
# across the columns, and the outer ring loses volume to evaporation.
rows = []
for ri, row in enumerate("ABCDEFGH"):
    for ci in range(12):
        col = ci + 1
        edge = row in "AH" or col in (1, 12)
        d = doses[ci % 8]
        v = viability(d) + rng.normal(0, 2.0)
        if edge:
            v *= 1.18            # concentrated medium reads higher
        rows.append({"row": row, "col": col, "edge": edge,
                     "dose_uM": d, "viability_pct": v})
df = pd.DataFrame(rows)
df.to_csv("plate96.csv", index=False)

def fit(sub, label):
    x, y = sub.dose_uM.to_numpy(), sub.viability_pct.to_numpy()
    p, _ = curve_fit(hill, x, y, p0=[0, 100, 30, 1.0],
                     bounds=([0, 50, 1e-3, 0.1], [40, 160, 1e5, 10]), maxfev=20000)
    print(f"{label:34} IC50 {p[2]:6.1f} uM   top {p[1]:6.1f}")

ctrl_edge = df[(df.dose_uM == doses[0]) & df.edge].viability_pct.mean()
ctrl_in = df[(df.dose_uM == doses[0]) & ~df.edge].viability_pct.mean()
print(f"lowest-dose wells: edge {ctrl_edge:.1f} per cent, "
      f"interior {ctrl_in:.1f} per cent, "
      f"difference {ctrl_edge-ctrl_in:+.1f}\n")
print(f"true IC50 is {TRUE_IC50} uM")
fit(df, "all wells, edge included")
fit(df[~df.edge], "interior wells only")

# Layout B: one dose per row, which is how many people set a plate up.
rows_b = []
for ri, row in enumerate("ABCDEFGH"):
    for ci in range(12):
        col = ci + 1
        edge = row in "AH" or col in (1, 12)
        d = doses[ri]                      # the dose is the row
        v = viability(d) + rng.normal(0, 2.0)
        if edge:
            v *= 1.18
        rows_b.append({"row": row, "dose_uM": d, "edge": edge,
                       "viability_pct": v})
b = pd.DataFrame(rows_b)
print()
print("Layout B: one dose per row, so the lowest and highest doses")
print("sit entirely on the edge rows.")
fit(b, "all wells, edge included")
fit(b[~b.edge], "interior wells only")
