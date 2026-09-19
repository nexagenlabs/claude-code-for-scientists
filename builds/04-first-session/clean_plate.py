#!/usr/bin/env python3
"""Turn the SpectraCount export into a tidy, versioned dataset.

Input :  plate_export_raw.xlsx, sheet 'Plate Export'
Output:  plate_clean.csv        one row per well, no aggregation
         plate_excluded.csv     every row not carried through, with a reason

Nothing is dropped silently. A row leaves the dataset only into the
exclusions file, with a reason attached.
"""
import re
import pandas as pd

RAW = "plate_export_raw.xlsx"
HEADER_ROW = 5          # zero-based: the row holding Well, Sample ID, ...
UNIT_ROW = 1            # the first row after the header holds units, not data
EXPECTED_WELLS = 32

raw = pd.read_excel(RAW, sheet_name="Plate Export", header=HEADER_ROW)
raw = raw.iloc[UNIT_ROW:].reset_index(drop=True)

# Trailing notes look like data. A real well has a well ID of a letter
# followed by digits; anything else is a footer.
is_well = raw["Well"].astype(str).str.fullmatch(r"[A-H]\d{1,2}")
footer = raw[~is_well.fillna(False)]
df = raw[is_well.fillna(False)].copy()

# Sample identifiers were typed three different ways. Normalise to one.
def canon_id(value):
    text = str(value).strip().upper()
    match = re.fullmatch(r"U87[\s_\-]?(\d+)", text)
    return f"U87_{match.group(1)}" if match else None

df["sample_id"] = df["Sample ID"].map(canon_id)

# Readings arrive as numbers, as text, and as two instrument sentinels.
def parse_reading(value):
    text = str(value).strip()
    if text.upper() == "OVER":
        return pd.NA, "above instrument range"
    if text.startswith("<"):
        return pd.NA, "below instrument range"
    try:
        return float(text), None
    except ValueError:
        return pd.NA, "unparseable reading"

parsed = df["Reading"].map(parse_reading)
df["od595"] = [p[0] for p in parsed]
df["flag"] = [p[1] for p in parsed]

df["time_h"] = df["Time"].astype(str).str.extract(r"(\d+)").astype(int)
df = df.rename(columns={"Well": "well", "Treatment": "treatment", "Conc": "conc_uM"})
tidy = df[["well", "sample_id", "treatment", "conc_uM", "od595", "flag", "time_h"]]

kept = tidy[tidy["flag"].isna()].drop(columns="flag")
excluded = tidy[tidy["flag"].notna()]

kept.to_csv("plate_clean.csv", index=False)
excluded.to_csv("plate_excluded.csv", index=False)

print(f"raw rows read            {len(raw)}")
print(f"footer rows removed      {len(footer)}")
print(f"wells found              {len(tidy)}")
print(f"carried through          {len(kept)}")
print(f"excluded with a reason   {len(excluded)}")
