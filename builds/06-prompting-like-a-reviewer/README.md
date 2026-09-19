# 06-prompting-like-a-reviewer

Normalises one plate to its controls two different ways.

Chapter 6, Prompting Like a Reviewer: Inputs, Outputs, Units, Failure.

## What this build does

Normalises one plate to its controls two different ways. Both are
readings a competent analyst might choose, and the numbers differ.

The instruction did not say which normalisation was wanted, so the agent
picked one. This is what an underspecified prompt costs, measured.

## What it needs

Python, and these packages: `pandas`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `plate_clean.csv`

## How to run it

Run it from this directory, in this order.

```
python normalise_two_ways.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
