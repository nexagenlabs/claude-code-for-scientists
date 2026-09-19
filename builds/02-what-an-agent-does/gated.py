import pandas as pd
a = pd.read_csv('run_a.csv'); b = pd.read_csv('run_b.csv')
both = pd.concat([a, b])
assert both['unit'].nunique() == 1, f"mixed units: {sorted(both['unit'].unique())}"
print(both.groupby('compound')['ic50'].mean().round(1).to_string())
