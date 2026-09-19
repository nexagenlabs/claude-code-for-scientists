#!/usr/bin/env python3
"""Two controls that cost nothing: does the box contain the site, and
does redocking put the ligand back where it was?"""
import numpy as np

def load(fname, resname):
    pts = []
    for line in open(fname):
        if line.startswith(("ATOM", "HETATM")) and line[17:20].strip() == resname:
            pts.append([float(line[30+8*i:38+8*i]) for i in range(3)])
    return np.array(pts)

lig = load("receptor_raw.pdb", "LIG")
centre_true = lig.mean(axis=0)
print(f"co-crystallised ligand centre  "
      f"{centre_true[0]:.1f}, {centre_true[1]:.1f}, {centre_true[2]:.1f}")
print()

def box_check(name, centre, size):
    c, s = np.array(centre), np.array(size)
    lo, hi = c - s/2, c + s/2
    inside = ((lig >= lo) & (lig <= hi)).all(axis=1)
    print(f"{name:26} contains {inside.sum()}/{len(lig)} ligand atoms"
          f"   {'ok' if inside.all() else 'THE SITE IS NOT IN THE BOX'}")

prot = []
for line in open("receptor_raw.pdb"):
    if line.startswith("ATOM"):
        prot.append([float(line[30+8*i:38+8*i]) for i in range(3)])
centroid = np.array(prot).mean(axis=0)
print(f"protein centroid               "
      f"{centroid[0]:.1f}, {centroid[1]:.1f}, {centroid[2]:.1f}")
print()
box_check("centred on the ligand", centre_true, [20, 20, 20])
box_check("centred on the protein", centroid, [20, 20, 20])
box_check("centred on the protein, 40 A", centroid, [40, 40, 40])
print()

def rmsd(a, b):
    return float(np.sqrt(((a - b) ** 2).sum(axis=1).mean()))

rng = np.random.default_rng(77)
good = lig + rng.normal(0, 0.45, lig.shape)          # a near-native pose
flipped = lig[::-1] + rng.normal(0, 0.45, lig.shape)  # right place, wrong pose
far = lig + np.array([6.0, 2.0, 1.0])                 # a different pocket

print("REDOCKING CONTROL, heavy-atom RMSD to the crystal pose")
for name, pose in (("near-native", good), ("atoms reversed", flipped),
                   ("displaced 6 A", far)):
    r = rmsd(pose, lig)
    print(f"  {name:16} {r:5.2f} A   "
          f"{'passes the usual 2.0 A criterion' if r <= 2.0 else 'fails'}")
