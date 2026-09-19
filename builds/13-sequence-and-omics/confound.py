#!/usr/bin/env python3
"""What a confounded design finds when there is nothing to find.

Same six libraries, same batch structure, and this time the treatment
does absolutely nothing. Every gene is unchanged by design.
"""
import numpy as np, pandas as pd
from scipy import stats
import warnings; warnings.filterwarnings("ignore")

rng = np.random.default_rng(1414)
N = 20000
base = rng.lognormal(4.0, 1.6, size=N)
depth = np.array([1.0, 0.9, 1.15, 1.1, 1.05, 0.95])
batch = np.array([0, 0, 0, 1, 1, 1])          # still confounded with group
batch_shift = rng.normal(0, 0.35, size=N)     # a real batch effect
mat = np.zeros((N, 6), dtype=int)
for j in range(6):
    mu = base * depth[j] * np.exp(batch_shift * batch[j])
    mat[:, j] = rng.negative_binomial(n=1/0.15, p=(1/0.15)/((1/0.15)+mu))

cols = ["ctrl_1","ctrl_2","ctrl_3","treat_1","treat_2","treat_3"]
df = pd.DataFrame(mat, columns=cols)
cpm = df / df.sum(axis=0) * 1e6
lg = np.log2(cpm + 1); lg = lg[lg.std(axis=1) > 0]

t, p = stats.ttest_ind(lg[["treat_1","treat_2","treat_3"]],
                       lg[["ctrl_1","ctrl_2","ctrl_3"]], axis=1)
p = p[~np.isnan(p)]
m = len(p); order = np.argsort(p)
q = np.empty(m); q[order] = np.clip(
    np.minimum.accumulate((p[order]*m/(np.arange(m)+1))[::-1])[::-1], 0, 1)

print("The treatment does nothing in this dataset. Not one gene was changed.")
print(f"  genes tested          {m:6}")
print(f"  raw p < 0.05          {(p < 0.05).sum():6}")
print(f"  after BH correction   {(q < 0.05).sum():6}")
print()
print("Every one of those is the batch. The design cannot tell the")
print("difference, because every control was run on day one and every")
print("treated sample on day two.")
