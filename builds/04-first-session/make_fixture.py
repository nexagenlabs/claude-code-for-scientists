"""Build the messy plate-reader export used as the Chapter 4 fixture.

Every defect here is one I have seen in a real instrument export or in a
sheet a collaborator sent me. Nothing is exaggerated for effect.
"""
from openpyxl import Workbook
from openpyxl.styles import Font
import random

wb = Workbook()
ws = wb.active
ws.title = "Plate Export"

# 1. Instrument preamble above the real header. Four rows of it.
ws["A1"] = "SpectraCount MX-200 :: Endpoint Absorbance"
ws["A1"].font = Font(bold=True)
ws["A2"] = "Exported: 11/03/2026 14:22"
ws["A3"] = "Operator: ST      Protocol: MTT_48h_v2"
ws["A4"] = "Wavelength: 595 nm"
# row 5 blank

# 2. Two header rows, the second holding the units.
headers = ["Well", "Sample ID", "Treatment", "Conc", "Reading", "Time", "Notes"]
units   = ["",     "",          "",          "uM",   "OD",      "h",    ""]
for c, (h, u) in enumerate(zip(headers, units), start=1):
    ws.cell(row=6, column=c, value=h).font = Font(bold=True)
    ws.cell(row=7, column=c, value=u)

random.seed(11)
conds = [("blank", 0), ("DMSO", 0), ("TMZ", 50), ("TMZ", 100),
         ("NanA", 1), ("NanA", 5), ("TMZ+NanA", 50), ("TMZ+NanA", 100)]

# 3. Sample IDs written three different ways by three different people.
id_styles = ["U87_{}", "u87-{}", "U87 {}"]

row = 8
for rep in range(1, 5):                       # four replicate blocks
    for i, (treat, conc) in enumerate(conds):
        well = f"{chr(65 + rep - 1)}{i + 1}"
        sid = id_styles[(rep + i) % 3].format(rep)
        if treat == "blank":
            od = round(random.uniform(0.04, 0.09), 4)
        else:
            od = round(random.uniform(0.35, 1.85), 4)
        ws.cell(row=row, column=1, value=well)
        ws.cell(row=row, column=2, value=sid)
        ws.cell(row=row, column=3, value=treat)
        ws.cell(row=row, column=4, value=conc)
        # 4. Some readings stored as text, one saturated, one below range.
        if rep == 2 and i == 3:
            ws.cell(row=row, column=5, value="OVER")
        elif rep == 3 and i == 0:
            ws.cell(row=row, column=5, value="<0.010")
        elif rep == 4:
            ws.cell(row=row, column=5, value=str(od))      # text, not number
        else:
            ws.cell(row=row, column=5, value=od)
        # 5. Two date/time formats in one column.
        ws.cell(row=row, column=6, value=48 if rep % 2 else "48h")
        row += 1

# 6. A blank spacer row, then trailing notes rows that look like data.
row += 1
ws.cell(row=row, column=1, value="Mean of blanks")
ws.cell(row=row, column=5, value="=AVERAGE(E8,E16,E24,E32)")
row += 1
ws.cell(row=row, column=1, value="NB: plate 3 re-read after lamp warm-up")

# 7. A second sheet nobody mentions, holding a duplicate partial export.
ws2 = wb.create_sheet("Sheet2")
ws2["A1"] = "old export, do not use"

wb.save("plate_export_raw.xlsx")
print("fixture written: plate_export_raw.xlsx")
print("data rows written:", 32)
