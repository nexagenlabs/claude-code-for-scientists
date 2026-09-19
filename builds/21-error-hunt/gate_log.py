#!/usr/bin/env python3
"""The gate for the Chapter 21 build.

Checks the log is internally consistent. Chapter 21 reports counts from
it, so the counts and the file must not drift apart.
"""
import collections
import csv
import sys

EXPECTED_CLASSES = {"arithmetic", "incomplete", "unverified", "silent",
                    "tautology", "overclaim", "false_alarm"}
# Chapter 21 prints this count. If the file shrinks, the printed number
# and the file behind it have drifted, which is the whole subject of the
# chapter. Without this the gate passed on a truncated log.
EXPECTED_ROWS = 23

rows = list(csv.DictReader(open("error_log.csv", encoding="utf-8")))
fails = []

if len(rows) != EXPECTED_ROWS:
    fails.append(f"Chapter 21 reports {EXPECTED_ROWS} defects, "
                 f"the log holds {len(rows)}")

# Every row is complete.
for i, r in enumerate(rows, start=2):
    for field in ("chapter", "class", "description", "caught_by"):
        if not r.get(field, "").strip():
            fails.append(f"row {i}: {field} is empty")

# Chapters are real ones.
for i, r in enumerate(rows, start=2):
    try:
        ch = int(r["chapter"])
    except ValueError:
        fails.append(f"row {i}: chapter '{r['chapter']}' is not a number")
        continue
    if not 0 <= ch <= 22:
        fails.append(f"row {i}: chapter {ch} does not exist")

# No class appears that the chapter does not describe.
seen = {r["class"] for r in rows}
for extra in sorted(seen - EXPECTED_CLASSES):
    fails.append(f"class '{extra}' is not one of the seven in Chapter 21")

# The chapter's headline claim, checked against the file.
by_catch = collections.Counter(r["caught_by"] for r in rows)
if by_catch.get("reading", 0) != 0:
    fails.append("Chapter 21 says no defect was caught by rereading, "
                 f"but the log has {by_catch['reading']}")

# The class counts must sum to the total.
if sum(collections.Counter(r["class"] for r in rows).values()) != len(rows):
    fails.append("class counts do not sum to the number of rows")

for f in fails:
    print(f"  [log] {f}")
print(f"\n{len(fails)} problem(s) across {len(rows)} logged defects.")
sys.exit(1 if fails else 0)
