# 11-survival-and-dose-response

Fits a four-parameter logistic, and a Kaplan-Meier by hand.

Chapter 11, Survival, Dose-Response and Growth: Fitting What You Measured.

## What this build does

Fits a four-parameter logistic to a dose-response series and reports
what the fit is entitled to claim.

`fit.py` fits the full series, then a short one, and shows the
confidence interval widen and the bottom drift below zero. `survival.py`
builds a Kaplan-Meier estimate by hand and shows what it looks like when
most animals are still alive at the end of the study.

## What it needs

Python, and these packages: `numpy`, `pandas`, `scipy`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `dose.csv`

## How to run it

Run it from this directory, in this order.

```
python make_dose.py
python fit.py
python survival.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
