#!/usr/bin/env python3
"""One column of dates, read by three people in three countries."""
import pandas as pd, io

raw = "sample,collected\nS1,03/04/2026\nS2,11/03/2026\nS3,07/08/2026\n"

print("the column as deposited:")
for line in raw.strip().splitlines()[1:]:
    print("   " + line)
print()

for label, dayfirst in (("read as day/month (most of the world)", True),
                        ("read as month/day (United States)", False)):
    d = pd.read_csv(io.StringIO(raw))
    d["parsed"] = pd.to_datetime(d.collected, dayfirst=dayfirst, format="mixed")
    print(f"{label}")
    for r in d.itertuples():
        print(f"   {r.sample}  {r.collected}  ->  {r.parsed:%d %B %Y}")
    print()

print("Every one of those parses without an error. Three of the six")
print("readings are wrong, and nothing in the file says which.")
print()
print("The same column written the one unambiguous way:")
for s, iso in (("S1", "2026-04-03"), ("S2", "2026-03-11"), ("S3", "2026-08-07")):
    print(f"   {s},{iso}")
