"""Two defensible readings of 'normalise the plate to controls'.

Same input, same wells, both methods are ones a competent analyst might
choose. The instruction did not say which, so the agent picked one.
"""
import pandas as pd

df = pd.read_csv("plate_clean.csv")
blank_mean = df.loc[df.treatment == "blank", "od595"].mean()
dmso_raw = df.loc[df.treatment == "DMSO", "od595"].mean()
dmso_corrected = dmso_raw - blank_mean

treated = df[~df.treatment.isin(["blank", "DMSO"])].copy()

# A: ratio to the untreated control, no blank subtraction.
treated["viability_A"] = 100 * treated.od595 / dmso_raw

# B: blank subtracted from both numerator and denominator.
treated["viability_B"] = 100 * (treated.od595 - blank_mean) / dmso_corrected

out = (treated.groupby(["treatment", "conc_uM"])[["viability_A", "viability_B"]]
       .mean().round(1).reset_index())
out["difference"] = (out.viability_A - out.viability_B).round(1)

print(f"mean blank OD      {blank_mean:.4f}")
print(f"mean DMSO OD       {dmso_raw:.4f}   (blank corrected {dmso_corrected:.4f})")
print()
print(out.to_string(index=False))

# The two methods agreed closely above because the blank was small.
# Nanaomycin A is a pyranonaphthoquinone, and quinones absorb in the
# visible range, so a compound-containing blank is not always small.
print()
for blank in (0.0612, 0.20, 0.35):
    corrected = dmso_raw - blank
    a = 100 * treated.od595 / dmso_raw
    b = 100 * (treated.od595 - blank) / corrected
    spread = (a - b).abs().max()
    print(f"blank OD {blank:.4f}   largest disagreement between methods:"
          f" {spread:5.1f} percentage points")
