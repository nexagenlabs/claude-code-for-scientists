#!/usr/bin/env python3
"""Reads in must equal reads accounted for, per sample, at every step."""
import sys
import pandas as pd

df = pd.read_csv("read_summary.csv")
fails = []
for r in df.itertuples():
    downstream = (r.assigned + r.no_feature + r.ambiguous
                  + r.multimapping + r.unaligned + r.trimmed_away)
    if downstream != r.raw_reads:
        fails.append(f"[accounting] {r.sample}: {r.raw_reads:,} raw, "
                     f"{downstream:,} accounted for, "
                     f"{r.raw_reads - downstream:,} unexplained")
    rate = r.assigned / r.raw_reads
    if rate < 0.50:
        fails.append(f"[qc] {r.sample}: only {100*rate:.1f} per cent of reads "
                     f"assigned to a feature")

print(f"{'sample':10}{'raw':>12}{'assigned':>12}{'rate':>8}")
for r in df.itertuples():
    print(f"{r.sample:10}{r.raw_reads:>12,}{r.assigned:>12,}"
          f"{100*r.assigned/r.raw_reads:>7.1f}%")
print()
if fails:
    for f in fails: print(f)
    sys.exit(1)
print("All accounting gates passed.")
