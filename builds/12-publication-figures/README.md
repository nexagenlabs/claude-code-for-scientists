# 12-publication-figures

Regenerates a figure from its data rather than editing it by hand.

Chapter 12, Publication Figures That Regenerate on Demand.

## What this build does

Regenerates a figure from its data rather than editing it by hand, then
checks it against the journal's stated requirements.

`errorbars.py` draws the same four experiments with three kinds of error
bar, which are three different claims. `colourcheck.py` asks whether two
colours would still be two colours to a red-green reader, using the
Machado, Oliveira and Fernandes (2009) severity 1.0 deuteranopia matrix.

## What it needs

Python, and these packages: `matplotlib`, `numpy`, `pandas`, `pillow`, `scipy`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `RUN_ORDER.txt`
- `figure_2a.png`
- `mtt.csv`

## How to run it

The order matters. One script writes what the next one reads, and
`RUN_ORDER.txt` records the dependency.

```
python make_figure.py
python tests/gate_figure.py
python errorbars.py
python colourcheck.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.

`make_figure.py` overwrites `figure_2a.png`. The copy in the
repository was produced by the matplotlib version recorded in
TOOLING.md, so your bytes may differ while the figure matches.
