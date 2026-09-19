#!/usr/bin/env python3
"""The join that silently loses half your genes."""
import pandas as pd

counts = pd.read_csv("counts.csv")[["gene_id"]].head(2000).copy()
# The quantifier wrote versioned identifiers, as most of them do.
counts["gene_id"] = counts.gene_id + "." + ((counts.index % 9) + 1).astype(str)

# The annotation file was downloaded from a different source, unversioned.
annot = pd.DataFrame({"gene_id": pd.read_csv("counts.csv").gene_id.head(2000),
                      "symbol": [f"SYM{i}" for i in range(2000)]})

naive = counts.merge(annot, on="gene_id", how="inner")
print(f"counts rows        {len(counts)}")
print(f"annotation rows    {len(annot)}")
print(f"after the join     {len(naive)}")
print()

# The repair, and the gate that should have been there first.
counts["gene_base"] = counts.gene_id.str.split(".").str[0]
fixed = counts.merge(annot, left_on="gene_base", right_on="gene_id", how="left")
matched = fixed.symbol.notna().sum()
print(f"after stripping the version suffix   {matched} of {len(counts)} matched")
print()
print("Gate: a join must not lose rows unless you said it could.")
print(f"  rows in {len(counts)}, rows out {len(naive)}, "
      f"lost {len(counts) - len(naive)}")
