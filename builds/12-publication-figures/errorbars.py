#!/usr/bin/env python3
"""The same four experiments, three kinds of error bar."""
import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv("mtt.csv")
plate_means = df.groupby(["treatment", "plate"]).viability_pct.mean().reset_index()

print(f"{'treatment':10}{'mean':>8}{'SD':>8}{'SEM':>8}{'95% CI half':>13}")
for t, g in plate_means.groupby("treatment"):
    v = g.viability_pct
    n = len(v)
    sd = v.std(ddof=1)
    sem = sd / np.sqrt(n)
    half = stats.t.ppf(0.975, n - 1) * sem
    print(f"{t:10}{v.mean():8.2f}{sd:8.2f}{sem:8.2f}{half:13.2f}")

print()
print("n = 4 independent experiments per condition")
print("The three bars differ by a factor of "
      f"{(stats.t.ppf(0.975, 3) / 1.0):.2f} between SEM and CI alone.")
