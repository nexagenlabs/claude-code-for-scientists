# verify_plate.py, runs after every analysis and fails loudly
import pandas as pd

raw = pd.read_csv('data/plate_raw.csv')
clean = pd.read_csv('data/plate_2026_03_11_clean.csv')

# Gate 1: the plate arrived complete
assert len(raw) == 96, f'expected 96 wells, found {len(raw)}'

# Gate 2: every well is accounted for, either kept or deliberately dropped
n_blank = (raw['condition'] == 'blank').sum()
assert len(clean) == 96 - n_blank, f'{96 - n_blank - len(clean)} wells went missing'

# Gate 3: the blanks were removed, not merely hidden from view
assert (clean['condition'] != 'blank').all(), 'blank wells still present'

# Gate 4: the absorbances are physically possible
assert clean['od595'].between(0, 4).all(), 'OD outside instrument range'

print('All gates passed for', clean['plate_id'].iloc[0])
