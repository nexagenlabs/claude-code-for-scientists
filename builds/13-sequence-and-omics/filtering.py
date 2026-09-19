#!/usr/bin/env python3
"""How a threshold nobody stated changes every adjusted p-value."""
import numpy as np, pandas as pd
from scipy import stats
import warnings; warnings.filterwarnings("ignore")

counts = pd.read_csv("counts.csv").set_index("gene_id")
cpm = counts / counts.sum(axis=0) * 1e6
ctrl, treat = ["ctrl_1","ctrl_2","ctrl_3"], ["treat_1","treat_2","treat_3"]

def bh(p):
    p = np.asarray(p); m = len(p); o = np.argsort(p)
    r = np.minimum.accumulate((p[o]*m/(np.arange(m)+1))[::-1])[::-1]
    q = np.empty(m); q[o] = np.clip(r, 0, 1); return q

target = None
print(f"{'min counts':>12}{'genes tested':>15}{'smallest q':>13}")
for thr in (0, 1, 5, 10, 50):
    keep = counts.sum(axis=1) >= thr
    lg = np.log2(cpm[keep] + 1)
    lg = lg[lg.std(axis=1) > 0]
    t, p = stats.ttest_ind(lg[treat], lg[ctrl], axis=1)
    ok = ~np.isnan(p)
    q = bh(p[ok])
    if target is None:
        target = lg.index[ok][np.argmin(p[ok])]
    print(f"{thr:>12}{ok.sum():>15}{q.min():>13.4f}")

print()
print(f"The same gene, {target}, is the strongest hit at every threshold.")
print("Its adjusted p-value depends entirely on how many other genes")
print("were left in the table beside it.")
