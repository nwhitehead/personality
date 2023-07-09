import numpy as np
import pandas as pd

# Read data from csv (semicolon separated)
data = pd.read_csv('data.csv', delimiter='\t')

# Look at some basic stats for A1 question. Exclude people that did not answer or that took < 1 min for entire test.
# data[(data['A1'] > 0) & (data['elapsed'] > 60)]['A1'].describe()

# There are 163 questions in the survey
# Here are the people that filled out all 163 questions (no 0 blank answers)
full = data[(data.T.head(163) != 0).all()][:]

# Compute new column for total attribute (with + and - based on question)
# Data format here is key is name prefix, then value is range tuple (lo, hi).
# 1 through lo is +, lo+1 through hi inclusive is -.
# So for 'A', the formula is A_all = A1 + A2 + A3 + A4 + A5 + A6 + A7 - A8 - A9 - A10
num_positive = {
    'A': (7, 10),
    'B': (8, 13),
    'C': (5, 10),
    'D': (6, 10),
    'E': (6, 10),
    'F': (5, 10),
    'G': (5, 10),
    'H': (6, 10),
    'I': (6, 10),
    'J': (7, 10),
    'K': (5, 10),
    'L': (7, 10),
    'M': (5, 10),
    'N': (7, 10),
    'O': (5, 10),
    'P': (7, 10),
}

# Use table above to add columns for scores
for k in num_positive:
    lo, hi = num_positive[k]
    label = k + '1'
    t = full[label]
    for i in range(2, lo + 1):
        label = k + str(i)
        t += full[label]
    for i in range(lo + 1, hi + 1):
        label = k + str(i)
        t -= full[label]
    label_all = k + '_all'
    full[label_all] = t
    full[f'{k}_z'] = (full[label_all] - full[label_all].median() ) / full[label_all].std()

cov = full[[f'{k}_z' for k in num_positive]].cov()
print(cov)

r = full[[f'{k}_z' for k in num_positive]].to_numpy()
print(r.shape)
# print(np.cov(r.T)) # This matches the .cov() from pandas

c = np.linalg.cholesky(cov)
# print(c)

x = np.random.randn(100000, 16)
y = x @ c.T
print(y.shape)
print(np.cov(y.T))

np.save('cholcov', c.T, allow_pickle=False)

# YES, it matches cov
print(np.cov(y.T) - cov)