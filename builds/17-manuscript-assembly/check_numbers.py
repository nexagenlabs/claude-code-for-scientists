#!/usr/bin/env python3
"""Check every number in the prose against the results file.

The manuscript is the claim. results.csv is the evidence. This compares
them and refuses to be reassured by fluent writing.
"""
import re, sys
import pandas as pd

res = pd.read_csv("results.csv").set_index("key")["value"].to_dict()
text = open("manuscript.md").read()

# Prose wraps, so every gap in a pattern must tolerate a line break.
CLAIMS = [
    (r"IC50 of ([\d.]+)\s+uM",                        "ic50_tmz"),
    (r"95% CI ([\d.]+)\s+to\s+([\d.]+)\s+uM",         ("ic50_tmz_ci_low",
                                                        "ic50_tmz_ci_high")),
    (r"viability\s+fell\s+to\s+([\d.]+)\s+per\s+cent",  "viability_tmz50"),
    (r"n\s*=\s*(\d+)\s+independent\s+plates",         "n_experiments"),
    (r"across\s+([\d,]+)\s+genes",                    "genes_tested"),
    (r"identified\s+(\d+)\s+genes",                   "genes_significant"),
]

fails = []
for pattern, keys in CLAIMS:
    m = re.search(pattern, text)
    if not m:
        fails.append(f"[missing]  no claim matching: {pattern}")
        continue
    keys = keys if isinstance(keys, tuple) else (keys,)
    for got, key in zip(m.groups(), keys):
        stated = float(got.replace(",", ""))
        actual = float(res[key])
        status = "ok" if abs(stated - actual) < 1e-9 else "MISMATCH"
        line = (f"  {key:22} manuscript {stated:>12,g}"
                f"   results {actual:>12,g}   {status}")
        print(line)
        if status != "ok":
            fails.append(f"[number]   {key}: manuscript says {stated:g}, "
                         f"results file says {actual:g}")

print()
if fails:
    for f in fails: print(f)
    sys.exit(1)
print("Every number in the prose matches the results file.")
