# 19-grant-and-thesis-drafting

Two checks on a draft: are claims evidenced, is the language hedged.

Chapter 19, Grant and Thesis Drafting: Structure First, Facts Checked.

## What this build does

Two checks on a draft: is every claim evidenced, and is the language
hedged to match the evidence behind it.

The shipped draft carries three problems on purpose. One claim cites
evidence that does not resolve, and two assert more than their evidence
supports. The script exits 1 on all three.

## What it needs

Python and the standard library. Nothing else.

These files ship with the build:

- `bibliography.json`
- `claims.csv`
- `draft.md`
- `results.csv`

## How to run it

Run it from this directory, in this order.

```
python claim_check.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.

`claim_check.py` exits 1 on the shipped draft. That is the point.
