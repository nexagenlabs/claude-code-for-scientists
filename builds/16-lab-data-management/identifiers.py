#!/usr/bin/env python3
"""Two things an identifier has to survive: collision and transcription."""
import numpy as np
from itertools import product

# 1. COLLISION. Short human-chosen identifiers repeat sooner than people expect.
def collision_prob(space, n):
    p = 1.0
    for k in range(n):
        p *= (space - k) / space
    return 1 - p

print("Chance that two samples share an identifier")
print(f"{'scheme':>34}{'space':>12}{'at 500':>9}{'at 5000':>9}")
schemes = [("initials + date, e.g. ST-1103", 26*26*365),
           ("three digits, e.g. 047", 1000),
           ("four letters, e.g. QKZM", 26**4),
           ("eight hex, e.g. 3f9a17c2", 16**8)]
for name, space in schemes:
    print(f"{name:>34}{space:>13,}"
          f"{collision_prob(space,500):>9.1%}{collision_prob(space,5000):>9.1%}")

# 2. TRANSCRIPTION. A check digit catches the errors people actually make.
def luhn_digit(num):
    total, alt = 0, True
    for d in reversed(num):
        v = int(d) * (2 if alt else 1)
        total += v - 9 if v > 9 else v
        alt = not alt
    return str((10 - total % 10) % 10)

def valid(code):
    return code[-1] == luhn_digit(code[:-1])

rng = np.random.default_rng(16)
base = ["".join(str(d) for d in rng.integers(0, 10, 7)) for _ in range(4000)]
codes = [b + luhn_digit(b) for b in base]

single, transpose = 0, 0
for c in codes:
    i = int(rng.integers(0, 7))
    wrong = list(c); wrong[i] = str((int(wrong[i]) + int(rng.integers(1, 10))) % 10)
    if not valid("".join(wrong)): single += 1
    j = int(rng.integers(0, 6))
    if c[j] != c[j+1]:
        sw = list(c); sw[j], sw[j+1] = sw[j+1], sw[j]
        if not valid("".join(sw)): transpose += 1

print()
print("A check digit on a seven-digit identifier catches")
print(f"  single wrong digit      {100*single/len(codes):5.1f} per cent of the time")
print(f"  two digits swapped      {100*transpose/len(codes):5.1f} per cent of the time")
