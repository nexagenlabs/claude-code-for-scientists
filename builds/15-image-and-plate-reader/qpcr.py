#!/usr/bin/env python3
"""What the ddCt method assumes, and what it costs when the assumption fails."""
import numpy as np

# A real experiment: target and reference, control and treated.
ct = {"target_ctrl": 24.10, "ref_ctrl": 18.40,
      "target_treat": 22.35, "ref_treat": 18.55}
d_ctrl = ct["target_ctrl"] - ct["ref_ctrl"]
d_treat = ct["target_treat"] - ct["ref_treat"]
ddct = d_treat - d_ctrl

print(f"delta Ct control {d_ctrl:6.2f}   delta Ct treated {d_treat:6.2f}"
      f"   delta delta Ct {ddct:+6.2f}\n")

print(f"{'assumed efficiency':>20}{'fold change':>14}{'error vs 100%':>16}")
ref = 2.0 ** (-ddct)
for eff in (1.00, 0.95, 0.90, 0.85):
    fold = (1 + eff) ** (-ddct)
    print(f"{eff:>19.0%}{fold:>14.2f}{100*(fold-ref)/ref:>15.1f}%")

print()
print("The 100 per cent row is what 2^-ddCt gives you. Every other row")
print("is the same Ct values read with a primer pair that amplifies")
print("slightly less than perfectly, which is the normal case.")
print()
print("Standard curve slopes and the efficiency they imply:")
for slope in (-3.10, -3.32, -3.58, -3.90):
    e = 10 ** (-1/slope) - 1
    print(f"  slope {slope:5.2f}   efficiency {e:5.1%}"
          f"   {'acceptable' if 0.90 <= e <= 1.10 else 'OUT OF RANGE'}")
