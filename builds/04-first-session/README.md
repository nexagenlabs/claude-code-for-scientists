# 04-first-session

Turns a messy plate-reader export into a tidy, versioned dataset.

Chapter 4, Your First Session: A Messy Export to a Versioned Dataset.

## What this build does

Takes a messy plate-reader export and turns it into a tidy, versioned
dataset.

`make_fixture.py` builds the export, carrying the defects real
instrument exports carry. `naive_read.py` shows what you get if you open
it and start averaging. `clean_plate.py` does the work properly: every
row that leaves the dataset is written to `plate_excluded.csv` with a
reason attached, so nothing is dropped silently. The gate then checks
the result.

## What it needs

Python, and these packages: `openpyxl`, `pandas`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `plate_clean.csv`
- `plate_excluded.csv`
- `plate_export_raw.xlsx`

## How to run it

Run it from this directory, in this order.

```
python make_fixture.py
python naive_read.py
python clean_plate.py
python tests/gate_plate.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
