# 21 Error Hunt

Summarises the defect log, and gates it against the chapter's claims.

Chapter 21, Catching AI Errors: An Evaluator's Checklist.

## What this build does

Regenerates the counts Chapter 21 reports from `error_log.csv`, then
gates them.

This build has no science in it. It exists because Chapter 21 reports counts
from `error_log.csv`, and a chapter that reports counts from a file should
have something that checks the counts still match the file.

## What it needs

Python 3.9 or later. No packages.

These files ship with the build:

- `error_log.csv`

## How to run it

Run it from this directory, in this order.

```
python summarise_log.py     # the two tables Chapter 21 prints
python gate_log.py          # the gate
```

## What correct output looks like

`summarise_log.py` reports 23 defects in 16 of the 22 chapters, seven classes
led by arithmetic at 7, and five ways they were caught led by an audit script
at 10. The last line reads zero.

`gate_log.py` reports no problems across 23 logged defects and exits 0.

`expected_output.txt` holds the output `summarise_log.py` produced on the
machine that assembled this repository. It was captured by running it, not
copied from the book.

## The gate

Five checks. Every row is complete, every chapter number exists, no class
appears outside the seven the chapter describes, the class counts sum to the
row count, and no defect is recorded as having been caught by rereading.

That last one is the chapter's headline claim. Add a row to the log saying a
defect was found by reading and the gate fails, which is the intended
behaviour: the claim in print and the file behind it cannot drift apart
silently.
