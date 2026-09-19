#!/usr/bin/env python3
"""The negative control: can the scoring function tell actives from decoys?

Fifty known actives against one thousand property-matched decoys, with
scores drawn to give a scoring function of realistic, modest quality.
"""
import numpy as np

rng = np.random.default_rng(1515)
N_ACT, N_DEC = 50, 1000

# More negative is better, as docking scores conventionally are.
actives = rng.normal(-8.4, 1.1, N_ACT)
decoys = rng.normal(-7.6, 1.2, N_DEC)

scores = np.concatenate([actives, decoys])
label = np.concatenate([np.ones(N_ACT), np.zeros(N_DEC)])
order = np.argsort(scores)                    # best first
label = label[order]

# Area under the ROC curve, computed from ranks.
auc = (np.sum([np.sum(a < decoys) + 0.5*np.sum(a == decoys) for a in actives])
       / (N_ACT * N_DEC))

def enrichment(frac):
    n = int(round(frac * len(label)))
    hits = label[:n].sum()
    return hits, (hits / n) / (N_ACT / len(label))

print(f"{N_ACT} actives, {N_DEC} decoys")
print(f"AUC                     {auc:.3f}   (0.5 is random)")
for frac in (0.01, 0.05, 0.10):
    hits, ef = enrichment(frac)
    print(f"top {frac:>5.0%}   {int(hits):3} actives found   "
          f"enrichment factor {ef:5.2f}")
print()
print("A random scoring function gives AUC 0.5 and enrichment 1.0.")
print("Report both, or a reader cannot tell your ranking from a shuffle.")
