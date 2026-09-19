#!/usr/bin/env python3
"""The same field, unevenly lit, counted by region, then corrected."""
import numpy as np
from scipy import ndimage

rng = np.random.default_rng(99)
img = np.load("field.npy")
H, W = img.shape
yy, xx = np.mgrid[0:H, 0:W]

# Illumination falls off towards the edges of the field of view.
r = np.sqrt((yy - H/2)**2 + (xx - W/2)**2) / (H/2)
vignette = 1.0 - 0.55 * r**2
lit = img * vignette

# A flat-field image: the same optics, an empty well, averaged.
blank = vignette * 1.0 + rng.normal(0, 0.004, img.shape)
corrected = lit / np.maximum(blank, 1e-3)

def count(a, t=0.55):
    m = ndimage.binary_opening(a > t, structure=np.ones((3, 3)))
    return ndimage.label(m)[1]

centre = (slice(H//4, 3*H//4), slice(W//4, 3*W//4))
print("one fixed threshold of 0.55, true count 80\n")
print(f"{'':22}{'evenly lit':>12}{'vignetted':>11}{'corrected':>11}")
print(f"{'whole field':22}{count(img):>12}{count(lit):>11}{count(corrected):>11}")
print(f"{'centre of the field':22}{count(img[centre]):>12}"
      f"{count(lit[centre]):>11}{count(corrected[centre]):>11}")
print()
print("The centre barely moves. The whole field halves. A cell that")
print("sits near the edge of the image is simply not counted.")
