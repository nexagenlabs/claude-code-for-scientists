#!/usr/bin/env python3
"""Resolve every DOI in the bibliography. Nothing is taken on trust.

Needs network. The cached responses in crossref_cache.json let the
demonstration run offline; delete it to hit the live API.
"""
import json, os, sys, urllib.request

CACHE = "crossref_cache.json"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def resolve(doi):
    if doi in cache:
        return cache[doi]
    url = f"https://api.crossref.org/works/{doi}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            m = json.load(r)["message"]
            return {"found": True,
                    "title": (m.get("title") or [""])[0],
                    "journal": (m.get("container-title") or [""])[0],
                    "year": m["issued"]["date-parts"][0][0]}
    except Exception:
        return {"found": False}

bib = json.load(open("bibliography.json"))
bad = 0
for entry in bib:
    r = resolve(entry["doi"])
    if not r["found"]:
        print(f"  UNRESOLVED  {entry['doi']}")
        print(f"              cited as: {entry['cited_as']}")
        bad += 1
        continue
    year_ok = str(r["year"]) == str(entry["year"])
    print(f"  {'ok      ' if year_ok else 'YEAR    '}    {entry['doi']}")
    print(f"              {r['journal']} {r['year']}")
    if not year_ok:
        print(f"              cited as {entry['year']}")
        bad += 1

print()
print(f"{len(bib)} references, {bad} problem(s).")
sys.exit(1 if bad else 0)
