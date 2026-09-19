#!/usr/bin/env python3
"""Kaplan-Meier by hand, and what happens when most animals are alive."""
import numpy as np, pandas as pd

rng = np.random.default_rng(1212)
n = 20
# A treatment that works: most animals are still alive when the study ends.
time_to_event = rng.exponential(140, size=n)
study_end = 60
observed = time_to_event <= study_end
t = np.minimum(time_to_event, study_end).round(1)

df = pd.DataFrame({"time": t, "event": observed.astype(int)}).sort_values("time")

surv, at_risk, curve = 1.0, n, []
for row in df.itertuples():
    if row.event:
        surv *= (1 - 1 / at_risk)
    curve.append((row.time, surv, at_risk))
    at_risk -= 1

lowest = min(s for _, s, _ in curve)
median = next((tt for tt, s, _ in curve if s <= 0.5), None)

print(f"{n} animals, study ended at day {study_end}")
print(f"events observed      {int(df.event.sum())}")
print(f"censored             {int((1 - df.event).sum())}")
print(f"lowest survival estimate reached  {lowest:.2f}")
print(f"median survival      {median if median is not None else 'NOT REACHED'}")
