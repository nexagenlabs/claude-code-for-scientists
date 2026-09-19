#!/usr/bin/env python3
"""Fit a four-parameter logistic, and report what it is entitled to claim."""
import numpy as np, pandas as pd
from scipy.optimize import curve_fit

def hill(x, bottom, top, ic50, slope):
    return bottom + (top - bottom) / (1 + (x / ic50) ** slope)

def fit_series(df, label, free_bottom=True):
    x = df.dose_uM.to_numpy(); y = df.viability_pct.to_numpy()
    p0 = [min(y), max(y), np.median(x), 1.0]
    lower = [-50 if free_bottom else 0, 50, 1e-3, 0.1]
    upper = [50 if free_bottom else 1e-9 + 0, 150, 1e5, 10]
    popt, pcov = curve_fit(hill, x, y, p0=p0, bounds=(lower, upper), maxfev=20000)
    se = np.sqrt(np.diag(pcov))
    bottom, top, ic50, slope = popt
    lo, hi = ic50 - 1.96 * se[2], ic50 + 1.96 * se[2]
    spans = (x.min() <= ic50 <= x.max())
    print(f"{label:22} IC50 {ic50:8.1f}   95% CI {lo:8.1f} to {hi:8.1f}"
          f"   bottom {bottom:6.1f}   {'' if spans else 'EXTRAPOLATED'}")
    return ic50, (lo, hi), spans

df = pd.read_csv("dose.csv")
print("true IC50 is 42.0 uM\n")
fit_series(df[df.series == "full"], "full series")
fit_series(df[df.series == "short"], "short series")

# Constraining the plateau to something physically possible.
short = df[df.series == "short"]
x, y = short.dose_uM.to_numpy(), short.viability_pct.to_numpy()
popt, pcov = curve_fit(hill, x, y, p0=[0, 100, 30, 1.0],
                       bounds=([0, 50, 1e-3, 0.1], [30, 150, 1e5, 10]),
                       maxfev=20000)
se = np.sqrt(np.diag(pcov))
print(f"short, bottom >= 0     IC50 {popt[2]:8.1f}   "
      f"95% CI {popt[2]-1.96*se[2]:8.1f} to {popt[2]+1.96*se[2]:8.1f}"
      f"   bottom {popt[0]:6.1f}")
