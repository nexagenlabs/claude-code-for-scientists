#!/usr/bin/env python3
"""Two checks on a draft: is every claim evidenced, and is it hedged
to match the evidence behind it?"""
import csv, json, os, re, sys

# Verbs that assert more than an observation. The strength you may use
# depends on what kind of evidence sits behind the sentence.
STRONG = r"demonstrat\w+|prov\w+|establish\w+|confirm\w+|shows? that|will\b"
ALLOWED = {"measured": True, "cited": True, "inferred": False, "proposed": False}

# Resolve pointers rather than merely checking that one was recorded.
results = {r["key"] for r in csv.DictReader(open("results.csv"))} \
          if os.path.exists("results.csv") else set()
dois = {e["doi"] for e in json.load(open("bibliography.json"))} \
       if os.path.exists("bibliography.json") else set()

def resolves(ev):
    if ev.startswith("results.csv:"):
        return ev.split(":", 1)[1] in results
    return ev in dois

claims = list(csv.DictReader(open("claims.csv")))
text = open("draft.md").read()
fails = []

print(f"{'id':4}{'evidence':11}{'language':10}claim")
for c in claims:
    et = c["evidence_type"]
    # locate the sentence carrying this claim by its distinctive words
    # Match on word stems, so "reduces" in the ledger still finds
    # "reduced" in the draft. Inflection is not divergence.
    key = [w[:5].lower() for w in re.findall(r"[a-zA-Z]{6,}", c["claim"])][:4]
    sentence = ""
    for s in re.split(r"(?<=[.])\s+", text.replace("\n", " ")):
        if sum(k in s.lower() for k in key) >= 2:
            sentence = s; break
    strong = bool(re.search(STRONG, sentence, re.I)) if sentence else False
    lang = "strong" if strong else "hedged"
    print(f"{c['claim_id']:4}{et:11}{lang:10}{c['claim'][:44]}")

    if et in ("measured", "cited"):
        if not c["evidence"]:
            fails.append(f"{c['claim_id']}: says {et} but no evidence is recorded")
        elif not resolves(c["evidence"]):
            fails.append(f"{c['claim_id']}: evidence '{c['evidence']}' "
                         f"does not resolve to anything")
    if not sentence:
        fails.append(f"{c['claim_id']}: claim does not appear in the draft")
    elif strong and not ALLOWED[et]:
        fails.append(f"{c['claim_id']}: {et} evidence, but the sentence "
                     f"asserts it. Rewrite:\n        \"{sentence.strip()[:96]}\"")

print()
for f in fails:
    print("  [claim] " + f)
print(f"\n{len(fails)} problem(s) across {len(claims)} claims.")
sys.exit(1 if fails else 0)
