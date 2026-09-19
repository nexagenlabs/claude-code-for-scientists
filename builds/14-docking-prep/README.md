# 14-docking-prep

Builds a receptor file with the defects real PDB entries carry.

Chapter 14, Structure and Docking Prep: PDB Cleaning and Batch Runs.

## What this build does

Builds a receptor file carrying the defects real PDB entries carry, then
inspects it before anything touches it.

The defects are a second chain, a missing loop, an alternate
conformation, ordered waters, a metal and a co-crystallised ligand.
`box_and_rmsd.py` runs two controls that cost nothing: does the box
contain the site, and does redocking put the ligand back.
`enrichment.py` is the negative control.

## What it needs

Python, and these packages: `numpy`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `receptor_raw.pdb`

## How to run it

Run it from this directory, in this order.

```
python make_pdb.py
python inspect_pdb.py
python box_and_rmsd.py
python enrichment.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
