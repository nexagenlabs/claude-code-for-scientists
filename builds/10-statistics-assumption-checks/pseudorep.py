#!/usr/bin/env python3
"""The same comparison, counted two ways."""
import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv("mtt.csv")
a = df[df.treatment == "DMSO"]
b = df[df.treatment == "TMZ_50"]

# Wrong: every well treated as an independent observation.
t1, p1 = stats.ttest_ind(a.viability_pct, b.viability_pct, equal_var=False)
print(f"wells as n      n = {len(a)} vs {len(b)}   "
      f"t = {t1:6.3f}   p = {p1:.4f}")

# Right: each plate contributes one number.
am = a.groupby("plate").viability_pct.mean()
bm = b.groupby("plate").viability_pct.mean()
t2, p2 = stats.ttest_rel(am, bm)           # same plates, so paired
print(f"plates as n     n = {len(am)} vs {len(bm)}   "
      f"t = {t2:6.3f}   p = {p2:.4f}")

diff = (am - bm)
mean_d = diff.mean()
sem = diff.std(ddof=1) / np.sqrt(len(diff))
crit = stats.t.ppf(0.975, len(diff) - 1)
print()
print(f"effect: {mean_d:.2f} percentage points lower with TMZ 50 uM, "
      f"95% CI {mean_d - crit*sem:.2f} to {mean_d + crit*sem:.2f}")
