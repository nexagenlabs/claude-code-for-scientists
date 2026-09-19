# 07-verification-gates

Four families of verification gate, and a fault injector to test them.

Chapter 7, Verification Gates: Never Trust a Number You Did Not Reproduce.

## What this build does

Four families of verification gate over a plate pipeline, and a fault
injector that seeds one problem at a time to see which family notices.

`inject.py` seeds four faults in turn: wells silently dropped, readings
in the wrong unit, a blank handled inconsistently, and two plates'
labels swapped. Watch which gate catches which.

## What it needs

Python, and these packages: `pandas`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `RUN_ORDER.txt`
- `plate_clean.csv`
- `plate_excluded.csv`
- `plate_viability.csv`
- `sample_sheet.csv`

## How to run it

The order matters. One script writes what the next one reads, and
`RUN_ORDER.txt` records the dependency.

```
python normalise.py
python gates.py
python inject.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.

`gates.py` stays at the build root rather than moving into `tests/`,
because `inject.py` invokes it by that path. Moving it would break the
chapter's own demonstration.
