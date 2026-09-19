# 02-what-an-agent-does

Two readings of the same two files, one gated by an assertion.

Chapter 2, What an AI Coding Agent Actually Does, and What It Cannot.

## What this build does

Two readings of the same two files. `naive.py` concatenates both runs
and reports a mean per compound. `gated.py` does the same thing with one
assertion in front of it, and that assertion stops the run.

The two files record IC50 in different units. The mean `naive.py` prints
is arithmetically correct and scientifically meaningless. That is the
whole build.

## What it needs

Python, and these packages: `pandas`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `run_a.csv`
- `run_b.csv`

## How to run it

Run it from this directory, in this order.

```
python naive.py
python gated.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.

`gated.py` exits 1. It is supposed to. The assertion is the point.
