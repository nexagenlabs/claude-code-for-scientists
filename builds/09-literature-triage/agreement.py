#!/usr/bin/env python3
"""Performance against the gold set, and agreement between two screens."""
import pandas as pd

strict = pd.read_csv("screened.csv")
loose = pd.read_csv("screened_loose.csv")
gold = strict["gold"]

def perf(name, v):
    tp = int(((v == 1) & (gold == 1)).sum()); fn = int(((v == 0) & (gold == 1)).sum())
    fp = int(((v == 1) & (gold == 0)).sum()); tn = int(((v == 0) & (gold == 0)).sum())
    sens = tp / (tp + fn); spec = tn / (tn + fp)
    print(f"{name:18} sensitivity {sens:.3f}   specificity {spec:.3f}   "
          f"missed {fn}   extra to read {fp}")

def kappa(a, b):
    n = len(a)
    po = (a == b).mean()
    pe = ((a == 1).mean() * (b == 1).mean()) + ((a == 0).mean() * (b == 0).mean())
    k = (po - pe) / (1 - pe)
    both1 = ((a == 1) & (b == 1)).mean(); both0 = ((a == 0) & (b == 0)).mean()
    prev_index = abs(both1 - both0)
    pabak = 2 * po - 1
    return po, k, prev_index, pabak

print("Against the gold set")
perf("strict criteria", strict.verdict)
perf("loose criteria", loose.verdict)
print()
po, k, pi, pabak = kappa(strict.verdict, loose.verdict)
print("Between the two screens")
print(f"  raw agreement      {po:.3f}")
print(f"  Cohen's kappa      {k:.3f}")
print(f"  prevalence index   {pi:.3f}")
print(f"  PABAK              {pabak:.3f}")

# The paradox, as arithmetic rather than as data. Hold raw agreement at
# 96 per cent and vary how rare the included class is.
print()
print("Same raw agreement, three prevalences")
print("  prevalence   raw agreement   Cohen's kappa")
import numpy as np
N = 500
for prev in (0.30, 0.11, 0.02):
    n_inc = int(round(N * prev))
    n_dis = int(round(N * 0.04))              # 4 per cent disagreement
    a = np.zeros(N, dtype=int); a[:n_inc] = 1
    b = a.copy()
    b[n_inc - n_dis // 2 : n_inc] = 0         # half the disagreements
    b[n_inc : n_inc + (n_dis - n_dis // 2)] = 1
    po = (a == b).mean()
    pe = (a.mean() * b.mean()) + ((1 - a.mean()) * (1 - b.mean()))
    print(f"  {prev:9.0%}   {po:13.3f}   {(po - pe) / (1 - pe):13.3f}")
