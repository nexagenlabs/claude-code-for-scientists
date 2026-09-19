import pandas as pd
kept = pd.read_csv("plate_clean.csv")

print("1. the whole table          ", kept.shape)
print("2. one column of it        ", kept["od595"].head(3).tolist())
print("3. a yes or no for each row", kept["od595"].between(0, 4).head(3).tolist())
print("4. were they all yes?      ", kept["od595"].between(0, 4).all())
print()
print("a row selection:", len(kept[kept.treatment != "blank"]), "of", len(kept), "rows")
print()
n = 30
print(f"an f-string: 'expected 32 wells, found {n}'")
print()
try:
    assert len(kept) == 32, f"expected 32 wells, found {len(kept)}"
except AssertionError as e:
    print("what a failed assert prints:", e)
