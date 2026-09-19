#!/usr/bin/env python3
"""What is actually in this structure file, before anything touches it."""
import sys
from collections import Counter, defaultdict

chains, waters, hetero, altlocs = Counter(), 0, Counter(), Counter()
resnums = defaultdict(set)
for line in open("receptor_raw.pdb"):
    if line.startswith(("ATOM", "HETATM")):
        res, chain, seq = line[17:20].strip(), line[21], int(line[22:26])
        alt = line[16]
        if res == "HOH":
            waters += 1
        elif line.startswith("HETATM"):
            hetero[res] += 1
        else:
            chains[chain] += 1
            resnums[chain].add(seq)
        if alt != " ":
            altlocs[f"{chain}{seq}"] += 1

print("STRUCTURE INVENTORY")
for c, n in sorted(chains.items()):
    lo, hi = min(resnums[c]), max(resnums[c])
    gaps = sorted(set(range(lo, hi + 1)) - resnums[c])
    print(f"  chain {c}   {n:4} atoms   residues {lo} to {hi}"
          f"   missing {gaps if gaps else 'none'}")
print(f"  waters           {waters}")
for h, n in hetero.items():
    print(f"  hetero {h:5}     {n} atoms")
print(f"  alternate conformations at {list(altlocs) if altlocs else 'none'}")

print()
decisions = []
if len(chains) > 1:
    decisions.append("Two chains. Which one is the receptor?")
if any(sorted(set(range(min(v), max(v)+1)) - v) for v in resnums.values()):
    decisions.append("A gap in the backbone. Is it near the site?")
if waters:
    decisions.append(f"{waters} waters. Which, if any, are kept?")
if hetero:
    decisions.append(f"Hetero groups {list(hetero)}. Metal kept? Ligand removed?")
if altlocs:
    decisions.append("An alternate conformation. Which one is docked?")
print("DECISIONS THIS FILE REQUIRES OF YOU")
for d in decisions:
    print("  " + d)
print()
print(f"{len(decisions)} decisions. A preparation script that reports none")
print("of them has made all of them on your behalf.")
