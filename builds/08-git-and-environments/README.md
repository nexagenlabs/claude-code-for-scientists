# 08-git-and-environments

Two things that make a result hard to reproduce.

Chapter 8, Git, Environments and Notebooks Without Becoming an Engineer.

## What this build does

Two things that make a result hard to reproduce.

`bootstrap_ci.py` draws a bootstrap confidence interval. The seed is
optional, so you can watch the interval move when it is left out.
`hidden_state.py` shows what out-of-order execution does to a notebook:
three cells, two histories, two different answers.

## What it needs

Python, and these packages: `numpy`, `pandas`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `plate_clean.csv`
- `tmz_ci.csv`

## How to run it

Run it from this directory, in this order.

```
python bootstrap_ci.py --seed
python hidden_state.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.

Run `bootstrap_ci.py` with `--seed` to reproduce the recorded output.
Without the flag the interval differs on every run, which is the
lesson rather than a defect. `tmz_ci.csv` is overwritten each time.
