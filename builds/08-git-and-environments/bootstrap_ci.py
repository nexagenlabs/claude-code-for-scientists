#!/usr/bin/env python3
"""A bootstrap confidence interval for mean viability. Seed optional."""
import sys, hashlib
import numpy as np, pandas as pd

seeded = "--seed" in sys.argv
rng = np.random.default_rng(20260311) if seeded else np.random.default_rng()

df = pd.read_csv("plate_clean.csv")
vals = df.loc[df.treatment == "TMZ", "od595"].to_numpy()
boot = np.array([rng.choice(vals, size=len(vals), replace=True).mean()
                 for _ in range(2000)])
lo, hi = np.percentile(boot, [2.5, 97.5])

out = pd.DataFrame({"statistic": ["mean_od595"], "estimate": [vals.mean()],
                    "ci_low": [lo], "ci_high": [hi]}).round(4)
out.to_csv("tmz_ci.csv", index=False)
digest = hashlib.sha256(open("tmz_ci.csv", "rb").read()).hexdigest()[:16]
print(f"{'seeded  ' if seeded else 'unseeded'}  "
      f"CI {lo:.4f} to {hi:.4f}   sha256 {digest}")
