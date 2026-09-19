# 00-reading-code

Prints one small table five ways, then lets an assertion fail.

Chapter 0, Reading Code You Did Not Write.

## What this build does

Prints one small table five ways, so you can see what each line of
pandas actually returns. It ends by letting an assertion fail on
purpose, so that you have seen what a failed check prints before you
meet one in your own work.

## What it needs

Python, and these packages: `pandas`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `plate_clean.csv`

## How to run it

Run it from this directory, in this order.

```
python read_along.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
