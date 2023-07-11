import numpy as np
import json

# A   warmth
# B   reasoning
# C   emotional stability
# D   dominance
# E   liveliness
# F   rule consciousness
# G   social boldness
# H   sensitivity
# I   vigilance
# J   abstractedness
# K   privateness
# L   apprehension
# M   openness to change
# N   self reliance
# O   perfectionism
# P   tension


# Number of samples
N = 100000
# Dimensionality for each sample
D = 16

# Actual covariances from real data (of z scores)
cov = np.load('cov.npy')

# Cholesky decomp of cov matrix for generating same covariances from iid draws
c = np.load('cholcov.npy')

# Start with independent normal draws
np.random.seed(1234)
x = np.random.randn(N, D)
# Give them the right covariance
y = x @ c.T

print(c)
# print(y[0])

diff = np.abs(np.cov(y.T) - cov)
print(np.max(diff), np.mean(diff))

# Now export cholcov to JS format
with open('cholcov.json', 'wt') as fout:
    fout.write(json.dumps(c.T.tolist()))

