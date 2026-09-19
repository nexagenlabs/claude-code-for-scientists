# 10-statistics-assumption-checks

Four demonstrations of counting the wrong thing.

Chapter 10, Statistics with Assumption Checks and Honest Effect Sizes.

## What this build does

Four demonstrations of counting the wrong thing.

Technical wells treated as independent experiments, a twelve-gene panel
with no correction, and a false positive rate measured on a design where
the true effect is exactly zero. Only the plate-to-plate offset is
real, and that is enough to produce results.

## What it needs

Python, and these packages: `numpy`, `pandas`, `scipy`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `mtt.csv`

## How to run it

Run it from this directory, in this order.

```
python make_mtt.py
python panel.py
python pseudorep.py
python false_positive_rate.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
