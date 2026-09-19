#!/usr/bin/env python3
"""Does the figure meet the journal's stated requirements?"""
import sys
from PIL import Image

REQ_MM, REQ_DPI, TOL_MM = 89.0, 300, 0.5
fails = []
im = Image.open("figure_2a.png")
dpi_x, dpi_y = im.info.get("dpi", (0, 0))
width_mm = im.width / dpi_x * 25.4 if dpi_x else 0

if round(dpi_x) < REQ_DPI:
    fails.append(f"resolution {dpi_x:.0f} dpi, journal requires {REQ_DPI}")
if abs(width_mm - REQ_MM) > TOL_MM:
    fails.append(f"width {width_mm:.1f} mm, journal single column is {REQ_MM}")
if im.mode not in ("RGB", "RGBA", "L"):
    fails.append(f"colour mode {im.mode} is not a submittable mode")

print(f"figure_2a.png   {im.width} x {im.height} px   {dpi_x:.0f} dpi   "
      f"{width_mm:.1f} mm wide")
if fails:
    for f in fails:
        print("  [figure] " + f)
    sys.exit(1)
print("All figure gates passed.")
