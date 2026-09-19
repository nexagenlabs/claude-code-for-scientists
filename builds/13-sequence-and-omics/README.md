# 13-sequence-and-omics

A count matrix with a known answer and two seeded design problems.

Chapter 13, Sequence and Omics: FASTQ to Differential Expression.

## What this build does

A count matrix with a known answer and two seeded design problems.

20,000 genes and six libraries, of which 200 genes are genuinely
differentially expressed. The scripts then show a join that silently
loses half the genes, a filtering threshold nobody stated that moves
every adjusted p-value, and a confounded design that finds structure
where none was put.

## What it needs

Python, and these packages: `numpy`, `pandas`, `scipy`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `RUN_ORDER.txt`
- `counts.csv`
- `counts.csv.gz`
- `read_summary.csv`
- `samples.csv`
- `truth.csv`

## How to run it

The order matters. One script writes what the next one reads, and
`RUN_ORDER.txt` records the dependency.

```
python make_counts.py
python de.py
python filtering.py
python annotation.py
python confound.py
python read_accounting.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.

`read_accounting.py` exits 1. One sample has only 35.5 per cent of its
reads assigned to a feature, and the gate is right to say so.
