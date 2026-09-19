#!/usr/bin/env python3
"""Turn absorbances into percent viability. Writes plate_viability.csv."""
import sys
import pandas as pd

def main(inp="plate_clean.csv", out="plate_viability.csv", bug=False):
    df = pd.read_csv(inp)
    blank = df.loc[df.treatment == "blank", "od595"].mean()
    dmso = df.loc[df.treatment == "DMSO", "od595"].mean()
    denom = dmso if bug else dmso - blank          # the seeded fault
    df["viability_pct"] = 100 * (df.od595 - blank) / denom
    df.to_csv(out, index=False)
    print(f"wrote {out}, blank {blank:.4f}, denominator {denom:.4f}")

if __name__ == "__main__":
    main(bug="--bug" in sys.argv)
