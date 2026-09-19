#!/usr/bin/env python3
"""Would a stranger be able to use this deposit?

Checks the things that make a deposit reusable rather than merely
present. Run it before you upload, not after a reviewer asks.
"""
import csv, hashlib, os, re, sys

D = "deposit"
fails, warns = [], []

def has(name): return os.path.exists(os.path.join(D, name))

# 1. Can a stranger tell what this is?
if not has("README.md"):
    fails.append("no README.md: nobody can tell what this deposit is")
else:
    txt = open(os.path.join(D, "README.md")).read().lower()
    for need in ("what this is", "how to regenerate", "licen"):
        if need not in txt:
            warns.append(f"README does not mention: {need}")

# 2. Is every file accounted for?
if not has("MANIFEST.sha256"):
    fails.append("no MANIFEST.sha256: a reader cannot verify what they got")
else:
    listed = {l.split(None, 2)[2].strip()
              for l in open(os.path.join(D, "MANIFEST.sha256"))}
    present = {f for f in os.listdir(D) if f != "MANIFEST.sha256"}
    for missing in sorted(listed - present):
        fails.append(f"manifest lists {missing}, which is not here")
    for extra in sorted(present - listed):
        fails.append(f"{extra} is present but not in the manifest")

# 3. Does every data column have a stated meaning and unit?
if not has("data_dictionary.csv"):
    fails.append("no data_dictionary.csv: column names are not units")
else:
    documented = {r["column"] for r in
                  csv.DictReader(open(os.path.join(D, "data_dictionary.csv")))}
    for f in sorted(os.listdir(D)):
        if f.endswith(".csv") and f != "data_dictionary.csv":
            cols = next(csv.reader(open(os.path.join(D, f))))
            for c in cols:
                if c not in documented:
                    fails.append(f"{f}: column '{c}' is not in the dictionary")

# 4. Things that must never be in a public deposit.
# No word boundary before a slash: \\b cannot match there, so an
# absolute path would have slipped through the first version of this.
PII = re.compile(r"\b(NHS|MRN|DOB|patient_name)\b"
                 r"|/Users/[A-Za-z0-9._-]+"
                 r"|/home/[A-Za-z0-9._-]+", re.I)
for f in sorted(os.listdir(D)):
    p = os.path.join(D, f)
    if not os.path.isfile(p): continue
    try: txt = open(p, encoding="utf-8", errors="ignore").read()
    except OSError: continue
    for m in sorted({x.group(0) for x in PII.finditer(txt)}):
        fails.append(f"{f}: contains '{m}', which should not be public")

# 5. Ambiguous dates.
for f in sorted(os.listdir(D)):
    if f.endswith(".csv"):
        txt = open(os.path.join(D, f), encoding="utf-8", errors="ignore").read()
        if re.search(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", txt):
            warns.append(f"{f}: slash-separated dates are ambiguous, use ISO")

for w in warns: print(f"  [warn] {w}")
for f in fails: print(f"  [fail] {f}")
print()
print(f"{len(fails)} failure(s), {len(warns)} warning(s).")
sys.exit(1 if fails else 0)
