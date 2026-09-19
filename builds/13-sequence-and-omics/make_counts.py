#!/usr/bin/env python3
"""A count matrix with a known answer, and two seeded design problems.

20,000 genes, six libraries, three per group. 200 genes are genuinely
differentially expressed. Library sizes differ the way they really do,
and the batches are laid out badly on purpose.
"""
import numpy as np, pandas as pd

rng = np.random.default_rng(1313)
N_GENES, N_PER = 20000, 3
TRUE_DE = 200

base = rng.lognormal(mean=4.0, sigma=1.6, size=N_GENES)          # gene abundance
de_idx = rng.choice(N_GENES, size=TRUE_DE, replace=False)
lfc = np.zeros(N_GENES)
lfc[de_idx] = rng.choice([-1, 1], size=TRUE_DE) * rng.uniform(1.0, 2.5, size=TRUE_DE)

# Library sizes vary threefold, which is ordinary.
depth = np.array([1.0, 0.9, 1.15, 2.8, 1.05, 0.95])
samples = ["ctrl_1", "ctrl_2", "ctrl_3", "treat_1", "treat_2", "treat_3"]
group = np.array([0, 0, 0, 1, 1, 1])
# Batch is perfectly confounded with group: controls run first, treated later.
batch = np.array([0, 0, 0, 1, 1, 1])
batch_shift = rng.normal(0, 0.35, size=N_GENES)

mat = np.zeros((N_GENES, len(samples)), dtype=int)
for j, s in enumerate(samples):
    mu = base * depth[j] * np.exp(lfc * group[j]) * np.exp(batch_shift * batch[j])
    mat[:, j] = rng.negative_binomial(n=1 / 0.15, p=(1 / 0.15) / ((1 / 0.15) + mu))

df = pd.DataFrame(mat, columns=samples)
df.insert(0, "gene_id", [f"ENSG{i:08d}" for i in range(N_GENES)])
df.to_csv("counts.csv", index=False)

pd.DataFrame({"sample": samples, "group": ["control"]*3 + ["treated"]*3,
              "batch": ["run1"]*3 + ["run2"]*3,
              "library_size": mat.sum(axis=0)}).to_csv("samples.csv", index=False)
pd.DataFrame({"gene_id": df.gene_id[de_idx], "true_lfc": lfc[de_idx].round(3)}
             ).to_csv("truth.csv", index=False)

print(f"{N_GENES} genes, {len(samples)} libraries, {TRUE_DE} truly changed")
print("library sizes (millions):",
      ", ".join(f"{v/1e6:.1f}" for v in mat.sum(axis=0)))
