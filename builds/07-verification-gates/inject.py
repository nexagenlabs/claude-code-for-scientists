#!/usr/bin/env python3
"""Seed one fault at a time and see which family of gate notices."""
import subprocess, sys
import pandas as pd

def fresh():
    return pd.read_csv("plate_clean.csv")

def faults():
    # A: two wells vanish during a filtering step
    a = fresh().iloc[:-2]
    yield "A  two wells silently dropped", a

    # B: readings arrive in milli-absorbance units from a second reader
    b = fresh(); b["od595"] = b["od595"] * 1000
    yield "B  readings in the wrong unit", b

    # C: the blank subtracted from the numerator only
    c = fresh()
    blank = c.loc[c.treatment == "blank", "od595"].mean()
    c.loc[c.treatment == "DMSO", "od595"] = c.loc[c.treatment == "DMSO", "od595"] + blank
    yield "C  blank handled inconsistently", c

    # D: two plates' sample labels swapped, data otherwise intact
    d = fresh()
    swap = {"U87_2": "U87_3", "U87_3": "U87_2"}
    d["sample_id"] = d["sample_id"].replace(swap)
    yield "D  two plates' labels swapped", d

for label, frame in faults():
    frame.to_csv("_tmp_clean.csv", index=False)
    out = subprocess.run([sys.executable, "gates.py", "_tmp_clean.csv"],
                         capture_output=True, text=True)
    print(f"{label}")
    for line in out.stdout.strip().splitlines():
        print(f"      {line}")
    print()
