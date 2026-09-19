# 15-image-and-plate-reader

Three kinds of plate and image data, each with a known answer.

Chapter 15, Image and Plate-Reader Data: Counts, MTT and qPCR.

## What this build does

Three kinds of plate and image data, each with a known answer.

`threshold.py` segments a synthetic field of cells at several thresholds
against a known count. `illumination.py` counts the same field by region
under uneven lighting, then corrects it. `edge_effect.py` shows what
evaporation from the outer ring does to an IC50. `qpcr.py` shows what
the ddCt method assumes and what it costs when the assumption fails.

## What it needs

Python, and these packages: `numpy`, `pandas`, `scipy`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `RUN_ORDER.txt`
- `field.npy`
- `plate96.csv`

## How to run it

The order matters. One script writes what the next one reads, and
`RUN_ORDER.txt` records the dependency.

```
python threshold.py
python illumination.py
python qpcr.py
python edge_effect.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
