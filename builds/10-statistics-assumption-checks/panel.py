#!/usr/bin/env python3
"""Twelve genes, no real differences, one uncorrected panel."""
import numpy as np, pandas as pd
from scipy import stats

genes = ["DNMT3A","DNMT3B","EZH1","EZH2","pTEN","p53",
         "p21","MGMT","NEAT1","TUSC7","MLH1","MSH3"]
rng = np.random.default_rng(4242)

rows = []
for g in genes:
    ctrl = rng.normal(1.0, 0.25, size=4)      # no true difference anywhere
    treat = rng.normal(1.0, 0.25, size=4)
    p = stats.ttest_ind(ctrl, treat, equal_var=False).pvalue
    rows.append({"gene": g, "p_raw": round(p, 4)})

df = pd.DataFrame(rows).sort_values("p_raw").reset_index(drop=True)
m = len(df)
# Benjamini-Hochberg, computed openly rather than pulled from a library
df["rank"] = df.index + 1
# Benjamini-Hochberg: the running minimum is taken from the largest
# p-value downwards, not from the smallest upwards.
raw_q = df.p_raw * m / df["rank"]
df["bh"] = raw_q[::-1].cummin()[::-1].clip(upper=1).round(4)
print(df.to_string(index=False))
print()
print(f"raw p < 0.05:            {(df.p_raw < 0.05).sum()} of {m} genes")
print(f"after BH correction:     {(df.bh < 0.05).sum()} of {m} genes")
print(f"expected by chance:      {0.05*m:.1f} genes")
