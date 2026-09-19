#!/usr/bin/env python3
"""Regenerate the viability figure from the data. Never edited by hand."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from scipy import stats

MM = 1 / 25.4
WIDTH_MM, HEIGHT_MM, DPI, MIN_PT = 89, 65, 300, 7

df = pd.read_csv("mtt.csv")
pm = df.groupby(["treatment", "plate"]).viability_pct.mean().reset_index()
order = ["DMSO", "TMZ_50", "TMZ_100"]

means, halves = [], []
for t in order:
    v = pm[pm.treatment == t].viability_pct
    means.append(v.mean())
    halves.append(stats.t.ppf(0.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v)))

plt.rcParams.update({"font.size": MIN_PT, "font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(WIDTH_MM * MM, HEIGHT_MM * MM))
ax.bar(order, means, yerr=halves, capsize=3,
       color=["#1F77B4", "#FF7F0E", "#7F7F7F"], edgecolor="black", linewidth=0.6)
for i, t in enumerate(order):                      # every point, not just the bar
    v = pm[pm.treatment == t].viability_pct
    ax.plot(np.full(len(v), i), v, "o", color="black", markersize=2.5, zorder=3)
ax.set_ylabel("Viability (% of DMSO)")
ax.set_xlabel("Treatment")
ax.set_ylim(0, 120)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(pad=0.3)
fig.savefig("figure_2a.png", dpi=DPI)
print(f"wrote figure_2a.png at {WIDTH_MM} x {HEIGHT_MM} mm, {DPI} dpi, "
      f"error bars are 95 per cent CI on n = 4 experiments")
