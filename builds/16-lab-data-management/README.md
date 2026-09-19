# 16-lab-data-management

Three mechanisms for knowing that data has not quietly changed.

Chapter 16, Lab Data Management: Sample Tracking and Audit Trails.

## What this build does

Three mechanisms for knowing that data has not quietly changed.

`manifest.py` builds a checksum manifest over a raw data directory and
checks it. `audit_log.py` is an append-only log that notices when
somebody edits the past. `identifiers.py` covers two things an
identifier has to survive: collision and transcription.

## What it needs

Python, and these packages: `numpy`.
Versions are pinned in the repository's `requirements.lock.txt`.

These files ship with the build:

- `MANIFEST.sha256`
- `data_raw/plate_P1.csv`
- `data_raw/plate_P2.csv`

## How to run it

Run it from this directory, in this order.

```
python manifest.py
python manifest.py --check
python identifiers.py
python audit_log.py
```

## What correct output looks like

`expected_output.txt` holds the output these commands produced on the
machine that assembled this repository. It was captured by running them,
not copied from the book.
