#!/usr/bin/env python3
"""What out-of-order execution does. Three notebook cells, two histories."""
import pandas as pd

def cell1(): return pd.read_csv("plate_clean.csv")      # load the plate
def cell2(df): return df[df.treatment != "blank"]       # drop the blanks
def cell3(df): return round(df.od595.mean(), 4)         # take the mean

# The order the notebook file implies, read top to bottom.
df = cell1()
df = cell2(df)
print(f"as written   (1, 2, 3): {cell3(df)} on {len(df)} wells")

# What actually happened: cell 3 was written and run first. Cell 2 was
# inserted above it afterwards, and cell 3 was never run again.
df = cell1()
print(f"as executed  (1, 3):    {cell3(df)} on {len(df)} wells")
print()
print("The notebook on disk is identical in both cases. The number that")
print("reached the figure is the second one.")
