#!/usr/bin/env python3
"""How often does each analysis cry wolf when nothing is happening?

Between-plate design: two plates get control, two get treatment, three
technical wells each. The treatment effect is exactly zero. Only the
plate-to-plate offset is real.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(2026)
N_SIM = 4000
plate_sd, well_sd = 6.0, 1.6

wells_hits = plates_hits = 0
for _ in range(N_SIM):
    ctrl, treat = [], []
    for group, store in ((0, ctrl), (1, treat)):
        for _plate in range(2):
            offset = rng.normal(0, plate_sd)       # real, and not the treatment
            store.append(offset + rng.normal(0, well_sd, size=3))
    c_w = np.concatenate(ctrl); t_w = np.concatenate(treat)
    c_p = np.array([x.mean() for x in ctrl]); t_p = np.array([x.mean() for x in treat])
    if stats.ttest_ind(c_w, t_w, equal_var=False).pvalue < 0.05:
        wells_hits += 1
    if stats.ttest_ind(c_p, t_p, equal_var=False).pvalue < 0.05:
        plates_hits += 1

print(f"{N_SIM} simulated experiments with no real treatment effect")
print(f"  wells counted as n   significant at p < 0.05 in "
      f"{100*wells_hits/N_SIM:5.1f} per cent")
print(f"  plates counted as n  significant at p < 0.05 in "
      f"{100*plates_hits/N_SIM:5.1f} per cent")
