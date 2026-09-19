# 17-manuscript-assembly

Checks a manuscript against its own evidence.

Chapter 17, Manuscript Assembly with Verified Citations.

## What this build does

Checks a manuscript against its own evidence.

`check_numbers.py` compares every number in the prose against the
results file and refuses to be reassured by fluent writing.
`citations.py` resolves every DOI in the bibliography.

Both scripts find real problems in the shipped fixture and exit 1. That
is the demonstration, not a fault in the build.

## What it needs

Python, and these packages: `pandas`, `urllib`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `bibliography.json`
- `crossref_cache.json`
- `manuscript.md`
- `results.csv`

## How to run it

Run it from this directory, in this order.

```
python check_numbers.py
python citations.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.

`citations.py` needs network access. The cached responses in
`crossref_cache.json` let it run offline. Delete that file to hit the
live API instead.

Both scripts exit 1 on the shipped fixture.
