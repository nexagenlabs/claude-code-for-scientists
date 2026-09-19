#!/usr/bin/env python3
"""An append-only log that notices when somebody edits the past."""
import hashlib, json, sys

def link(prev, entry):
    payload = json.dumps(entry, sort_keys=True) + prev
    return hashlib.sha256(payload.encode()).hexdigest()

def build(entries):
    chain, prev = [], "0" * 64
    for e in entries:
        h = link(prev, e)
        chain.append({**e, "prev": prev[:8], "hash": h[:8], "_full": h})
        prev = h
    return chain

def verify(chain):
    prev = "0" * 64
    for i, row in enumerate(chain):
        entry = {k: v for k, v in row.items()
                 if k not in ("prev", "hash", "_full")}
        if link(prev, entry) != row["_full"]:
            return i
        prev = row["_full"]
    return None

entries = [
    {"when": "2026-03-11 09:14", "who": "ST", "what": "plate P1 seeded, U87MG p12"},
    {"when": "2026-03-11 09:40", "who": "ST", "what": "TMZ dilution series prepared, 50 and 100 uM"},
    {"when": "2026-03-13 10:02", "who": "ST", "what": "MTT read at 48 h, plate P1"},
    {"when": "2026-03-13 10:20", "who": "RK", "what": "well B4 flagged saturated, excluded"},
    {"when": "2026-03-14 16:31", "who": "ST", "what": "analysis v1 committed, gate passed"},
]
chain = build(entries)

print(f"{'when':18}{'who':5}{'prev':10}{'hash':10}what")
for r in chain:
    print(f"{r['when']:18}{r['who']:5}{r['prev']:10}{r['hash']:10}{r['what']}")
print(f"\nverify: {'intact' if verify(chain) is None else 'BROKEN'}")

# Somebody decides entry 4 read better a different way.
chain[3]["what"] = "well B4 excluded, low signal"
chain[3]["_full"] = link(chain[3]["prev"] + "0"*56, {})   # a plausible-looking hash
bad = verify(chain)
print(f"\nafter editing entry {bad+1 if bad is not None else '?'} in place:")
print(f"verify: {'intact' if bad is None else f'BROKEN at entry {bad+1}'}")
print("Every later entry's hash was computed from the original text,")
print("so changing one line invalidates everything after it.")
