#!/usr/bin/env python3
"""Would these two colours still be two colours to a red-green reader?

Uses the Machado, Oliveira and Fernandes (2009) severity-1.0 deuteranopia
matrix, applied in linear RGB, then reports CIE76 distance in Lab.
"""
import numpy as np

DEUT = np.array([[0.367322, 0.860646, -0.227968],
                 [0.280085, 0.672501,  0.047413],
                 [-0.011820, 0.042940, 0.968881]])

def srgb_to_linear(c): return np.where(c <= 0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
def linear_to_srgb(c): return np.where(c <= 0.0031308, c*12.92, 1.055*c**(1/2.4)-0.055)

def simulate(hexcol):
    rgb = np.array([int(hexcol[i:i+2], 16)/255 for i in (1, 3, 5)])
    return np.clip(linear_to_srgb(DEUT @ srgb_to_linear(rgb)), 0, 1)

def to_lab(rgb):
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = M @ srgb_to_linear(np.asarray(rgb, dtype=float))
    xyz = xyz / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, xyz ** (1/3), 7.787 * xyz + 16/116)
    return np.array([116*f[1]-16, 500*(f[0]-f[1]), 200*(f[1]-f[2])])

def report(name, a, b):
    da = to_lab([int(a[i:i+2],16)/255 for i in (1,3,5)])
    db = to_lab([int(b[i:i+2],16)/255 for i in (1,3,5)])
    sa, sb = to_lab(simulate(a)), to_lab(simulate(b))
    print(f"{name:26} normal vision {np.linalg.norm(da-db):6.1f}"
          f"   red-green vision {np.linalg.norm(sa-sb):6.1f}")

print("CIE76 colour distance. Below about 20, two colours read as one.\n")
report("red and green", "#D62728", "#2CA02C")
report("blue and orange", "#1F77B4", "#FF7F0E")
report("blue and grey", "#1F77B4", "#7F7F7F")
