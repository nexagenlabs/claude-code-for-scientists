import pandas as pd
df = pd.read_excel('plate_export_raw.xlsx')
print("columns:", list(df.columns)[:5])
print("shape:", df.shape)
num = pd.to_numeric(df.iloc[:, 4], errors='coerce')
print("rows with a usable reading:", int(num.notna().sum()))
print("mean of whatever survived:", round(float(num.mean()), 4))
