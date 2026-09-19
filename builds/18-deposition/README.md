# 18-deposition

What a deposit needs before a stranger can use it.

Chapter 18, Supplementary Data, Availability Statements and Deposition.

## What this build does

What a deposit needs before a stranger can use it.

`dates.py` shows what one column of dates does when three people in
three countries read it. The gate checks the things that make a deposit
reusable rather than merely present. Run it before you upload, not after
a reviewer asks.

## What it needs

Python, and these packages: `pandas`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `deposit/MANIFEST.sha256`
- `deposit/data_dictionary.csv`
- `deposit/plate_clean.csv`

## How to run it

Run it from this directory, in this order.

```
python dates.py
python tests/deposit_check.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
