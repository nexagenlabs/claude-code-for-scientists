# 09-literature-triage

Screens a corpus at two strictnesses, then measures both screens.

Chapter 9, Literature Triage: Screening That Survives Peer Review.

## What this build does

Screens a corpus against a versioned criteria file at two strictnesses,
then measures both screens against the gold set and against each other.

Every record leaves the screen with a verdict and a reason, or goes to
the failures file. Nothing is dropped. The corpus is generated rather
than real, because real abstracts are copyrighted and cannot be
redistributed in a public repository.

## What it needs

Python, and these packages: `numpy`, `pandas`, `pyyaml`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `corpus.csv`
- `criteria_v1.yaml`
- `screen_failures.csv`
- `screened.csv`
- `screened_loose.csv`

## How to run it

Run it from this directory, in this order.

```
python make_corpus.py
python screen.py
python screen.py --loose
python agreement.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
