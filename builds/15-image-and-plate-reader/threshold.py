#!/usr/bin/env python3
"""A field of cells with a known count, segmented at several thresholds."""
import numpy as np
from scipy import ndimage

rng = np.random.default_rng(1515)
H = W = 512
TRUE_N = 80

img = np.zeros((H, W), dtype=float)
centres = rng.uniform(20, H-20, size=(TRUE_N, 2))
yy, xx = np.mgrid[0:H, 0:W]
for cy, cx in centres:
    r = rng.uniform(5, 7)
    bright = rng.uniform(0.55, 1.0)          # cells are not equally bright
    img += bright * np.exp(-(((yy-cy)**2 + (xx-cx)**2) / (2*r**2)))

img += rng.normal(0.04, 0.025, img.shape)    # camera noise and background
img = np.clip(img, 0, None)
np.save("field.npy", img)

print(f"true cell count: {TRUE_N}\n")
print(f"{'threshold':>10}{'objects found':>16}{'error':>10}")
for t in (0.15, 0.25, 0.35, 0.45, 0.55, 0.70, 0.85):
    mask = img > t
    mask = ndimage.binary_opening(mask, structure=np.ones((3, 3)))
    n = ndimage.label(mask)[1]
    print(f"{t:>10.2f}{n:>16}{n-TRUE_N:>+10}")
