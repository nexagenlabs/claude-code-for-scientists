#!/usr/bin/env python3
"""The Chapter 4 gate. Run after clean_plate.py, every time."""
import pandas as pd

EXPECTED_WELLS = 32
EXPECTED_TREATMENTS = {"blank", "DMSO", "TMZ", "NanA", "TMZ+NanA"}

kept = pd.read_csv("plate_clean.csv")
excluded = pd.read_csv("plate_excluded.csv")

# Gate 1: every well is accounted for, kept or excluded with a reason.
total = len(kept) + len(excluded)
assert total == EXPECTED_WELLS, f'{EXPECTED_WELLS} != {total}'

# Gate 2: no well appears twice.
assert kept["well"].is_unique, "duplicate wells in the clean file"

# Gate 3: every sample identifier was recognised.
assert kept["sample_id"].notna().all(), "unrecognised sample identifiers survived"

# Gate 4: every excluded row carries a reason.
assert excluded["flag"].notna().all(), "a row was excluded without a reason"

# Gate 5: absorbances are physically possible.
assert kept["od595"].between(0, 4).all(), "OD outside instrument range"

# Gate 6: no treatment appeared that we did not plan for.
unexpected = set(kept["treatment"]) - EXPECTED_TREATMENTS
assert not unexpected, f"unplanned treatment in the data: {unexpected}"

# Gate 7: one time point, as the protocol says.
assert kept["time_h"].nunique() == 1, f"mixed time points: {sorted(kept['time_h'].unique())}"

print(f"All 7 gates passed. {len(kept)} wells clean, {len(excluded)} excluded with reasons.")
