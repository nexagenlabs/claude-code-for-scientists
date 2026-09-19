#!/usr/bin/env python3
"""Screen every record against a versioned criteria file.

One record at a time. Every record leaves with a verdict and a reason,
or is written to the failures file. Nothing is dropped.
"""
import sys, yaml
import pandas as pd

def screen_one(rec, crit, strict_mechanism=True):
    text = f"{rec.title} {rec.abstract}".lower()
    hits = {}
    for field, terms in crit["include_all_of"].items():
        hits[field] = any(t.lower() in text for t in terms)
    for terms in crit["exclude_if_any_of"].values():
        if any(t.lower() in text for t in terms):
            return 0, "excluded population"
    if not strict_mechanism:
        hits.pop("mechanism_stated", None)
    missing = [f for f, ok in hits.items() if not ok]
    if missing:
        return 0, "missing: " + ", ".join(missing)
    return 1, "all criteria met"

def main(criteria="criteria_v1.yaml", out="screened.csv", strict=True):
    crit = yaml.safe_load(open(criteria))
    df = pd.read_csv("corpus.csv")
    verdicts, reasons, failures = [], [], []
    for rec in df.itertuples():
        try:
            v, r = screen_one(rec, crit, strict)
        except Exception as exc:                      # never lose a record
            failures.append({"pmid": rec.pmid, "error": str(exc)})
            v, r = None, "screening failed"
        verdicts.append(v); reasons.append(r)
    df["verdict"], df["reason"] = verdicts, reasons
    df.to_csv(out, index=False)
    pd.DataFrame(failures).to_csv("screen_failures.csv", index=False)
    print(f"{len(df)} records in, {int(df.verdict.sum())} included, "
          f"{len(failures)} failures")

if __name__ == "__main__":
    main(strict="--loose" not in sys.argv,
         out="screened_loose.csv" if "--loose" in sys.argv else "screened.csv")
