#!/usr/bin/env python3
"""A small receptor file carrying the defects real PDB entries carry:
a second chain, a missing loop, an alternate conformation, ordered
waters, a metal, and a co-crystallised ligand.
"""
import numpy as np
rng = np.random.default_rng(1414)

lines, serial = [], 1
def atom(rec, name, alt, res, chain, seq, xyz, occ, elem):
    global serial
    lines.append(f"{rec:<6}{serial:>5} {name:^4}{alt:1}{res:>3} {chain:1}"
                 f"{seq:>4}    {xyz[0]:8.3f}{xyz[1]:8.3f}{xyz[2]:8.3f}"
                 f"{occ:6.2f}{20.0:6.2f}          {elem:>2}")
    serial += 1

# Chain A: residues 10 to 40, with 21 to 24 missing (a disordered loop).
present = [r for r in range(10, 41) if not (21 <= r <= 24)]
for i, r in enumerate(present):
    centre = np.array([12.0 + 0.9*i, 8.0 + 0.5*np.sin(i), 15.0 + 0.4*np.cos(i)])
    for name, elem in (("N","N"), ("CA","C"), ("C","C"), ("O","O")):
        atom("ATOM", name, " ", "ALA", "A", r, centre + rng.normal(0, 0.4, 3), 1.00, elem)

# Residue 33 has two conformations at partial occupancy.
for altloc, occ, shift in (("A", 0.6, 0.0), ("B", 0.4, 1.8)):
    atom("ATOM", "CB", altloc, "SER", "A", 33,
         np.array([32.5 + shift, 9.0, 16.0]), occ, "C")

# Chain B: a crystallographic copy nobody asked for.
for i, r in enumerate(range(10, 25)):
    centre = np.array([12.0 + 0.9*i, 38.0, 15.0])
    for name, elem in (("N","N"), ("CA","C"), ("C","C"), ("O","O")):
        atom("ATOM", name, " ", "ALA", "B", r, centre + rng.normal(0, 0.4, 3), 1.00, elem)

# Waters, a magnesium, and the ligand that marks the site.
for k in range(7):
    atom("HETATM", "O", " ", "HOH", "A", 200+k,
         np.array([20.0+2*k, 10.0, 14.0]) + rng.normal(0, 0.5, 3), 1.00, "O")
atom("HETATM", "MG", " ", " MG", "A", 300, np.array([26.4, 9.2, 15.6]), 1.00, "MG")
for k, nm in enumerate(["C1","C2","N1","O1","O2","C3"]):
    atom("HETATM", nm, " ", "LIG", "A", 400,
         np.array([27.0, 9.0, 15.5]) + rng.normal(0, 1.2, 3), 1.00, nm[0])

open("receptor_raw.pdb", "w").write("\n".join(lines) + "\nEND\n")
print(f"wrote receptor_raw.pdb with {serial-1} atoms")
