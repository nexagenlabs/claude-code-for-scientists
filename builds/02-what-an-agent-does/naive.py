import pandas as pd
a = pd.read_csv('run_a.csv'); b = pd.read_csv('run_b.csv')
both = pd.concat([a, b])
print("means the agent reported:")
print(both.groupby('compound')['ic50'].mean().round(1).to_string())
