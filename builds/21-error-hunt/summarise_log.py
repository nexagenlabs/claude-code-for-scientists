#!/usr/bin/env python3
"""Summarise the defect log from Chapter 21.

Regenerates the two numbers the chapter reports: the count of defects by
class, and what caught each one. The point of the build is the last row
of the second table.

    python summarise_log.py
"""
import collections
import csv
import sys

rows = list(csv.DictReader(open("error_log.csv", encoding="utf-8")))
if not rows:
    sys.exit("error_log.csv is empty")

chapters = sorted({int(r["chapter"]) for r in rows})
by_class = collections.Counter(r["class"] for r in rows)
by_catch = collections.Counter(r["caught_by"] for r in rows)

print(f"{len(rows)} defects, in {len(chapters)} of the 22 chapters\n")

print("by class")
for name, n in by_class.most_common():
    print(f"  {name:14}{n:3}")

print("\nby what caught it")
for name, n in by_catch.most_common():
    print(f"  {name:16}{n:3}")

reading = by_catch.get("reading", 0)
print(f"\ncaught by rereading the text: {reading}")
