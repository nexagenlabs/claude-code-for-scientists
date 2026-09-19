#!/usr/bin/env python3
"""A synthetic screening corpus.

Real abstracts are copyrighted and cannot be redistributed in a public
repository, so this fixture is generated. Its structure mirrors a PubMed
export: an identifier, a title, an abstract, a year and a journal.
The ground truth column exists only because this is a teaching fixture.
"""
import numpy as np, pandas as pd

rng = np.random.default_rng(9091)
N = 500

drug_on   = ["ivermectin", "avermectin B1", "selamectin", "moxidectin"]
drug_off  = ["albendazole", "praziquantel", "metformin", "chloroquine",
             "doxycycline", "niclosamide"]
model_on  = ["HepG2 cells", "Huh7 hepatocellular carcinoma cells",
             "U87MG glioblastoma cells", "MCF-7 breast cancer cells"]
model_off = ["Onchocerca volvulus", "Anopheles gambiae", "murine scabies",
             "healthy volunteers", "Caenorhabditis elegans"]
mech      = ["protein kinase C activation", "WNT signalling inhibition",
             "mitochondrial depolarisation", "PAK1 downregulation"]
other     = ["pharmacokinetics", "mass drug administration",
             "resistance surveillance", "formulation stability"]

rows = []
for i in range(N):
    # A record is relevant if it studies an avermectin, in a cancer model,
    # with a stated mechanism. All three, or it is out.
    is_drug  = rng.random() < 0.42
    is_model = rng.random() < 0.38
    is_mech  = rng.random() < 0.55
    drug  = rng.choice(drug_on if is_drug else drug_off)
    model = rng.choice(model_on if is_model else model_off)
    tail  = rng.choice(mech if is_mech else other)
    relevant = int(is_drug and is_model and is_mech)
    # Real corpora are not tidy. Some relevant papers describe the
    # mechanism in words no criteria list anticipates, and some
    # irrelevant ones mention a cancer line in a background sentence.
    odd_mech = relevant and rng.random() < 0.22
    if odd_mech:
        tail = rng.choice(["apoptosis induction", "cell cycle arrest",
                           "autophagic flux"])
    background = (not relevant) and rng.random() < 0.10
    extra = (" Previous work in HepG2 cells reported inhibition of growth."
             if background else "")
    rows.append({
        "pmid": 30000000 + i,
        "title": f"Effect of {drug} on {model}: a study of {tail}",
        "abstract": (f"We investigated {drug} in {model}. "
                     f"The work focuses on {tail}. "
                     f"Results are reported with appropriate controls." + extra),
        "year": int(rng.integers(2015, 2027)),
        "journal": rng.choice(["J Pharm Sci", "Oncol Rep", "Parasitology",
                               "Br J Cancer", "PLOS ONE"]),
        "gold": relevant,
    })

df = pd.DataFrame(rows)
df.to_csv("corpus.csv", index=False)
print(f"{len(df)} records, {df.gold.sum()} relevant "
      f"({100*df.gold.mean():.1f} per cent prevalence)")
