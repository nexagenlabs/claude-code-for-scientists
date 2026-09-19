#!/usr/bin/env python3
"""Three things a count matrix will teach you if you ask it."""
import numpy as np, pandas as pd
from scipy import stats
import warnings; warnings.filterwarnings("ignore")

counts = pd.read_csv("counts.csv").set_index("gene_id")
truth = set(pd.read_csv("truth.csv").gene_id)
ctrl, treat = ["ctrl_1","ctrl_2","ctrl_3"], ["treat_1","treat_2","treat_3"]

def bh(p):
    p = np.asarray(p); m = len(p); order = np.argsort(p)
    ranked = np.minimum.accumulate((p[order]*m/(np.arange(m)+1))[::-1])[::-1]
    q = np.empty(m); q[order] = np.clip(ranked, 0, 1); return q

def de(mat):
    lg = np.log2(mat + 1)
    keep = lg.std(axis=1) > 0
    lg = lg[keep]
    t, p = stats.ttest_ind(lg[treat], lg[ctrl], axis=1)
    r = pd.DataFrame({"gene_id": lg.index,
                      "lfc": lg[treat].mean(axis=1) - lg[ctrl].mean(axis=1),
                      "p": p}).dropna()
    r["q"] = bh(r.p.values)
    return r

cpm = counts / counts.sum(axis=0) * 1e6

print("1. THE INVARIANT: most genes did not change, so the median")
print("   log fold change across all genes should be about zero.\n")
for label, mat in (("raw counts", counts), ("counts per million", cpm)):
    r = de(mat)
    print(f"   {label:22} median LFC {r.lfc.median():+.3f}")

print("\n2. THE SCALE: 20,000 tests at once.\n")
r = de(cpm)
raw_hits = (r.p < 0.05).sum()
q_hits = (r.q < 0.05).sum()
tp = len(set(r.loc[r.q < 0.05, "gene_id"]) & truth)
print(f"   genes tested                {len(r):6}")
print(f"   raw p < 0.05                {raw_hits:6}   expected by chance {0.05*len(r):.0f}")
print(f"   after BH correction         {q_hits:6}")
print(f"   of which genuinely changed  {tp:6}   out of {len(truth)} that were")
