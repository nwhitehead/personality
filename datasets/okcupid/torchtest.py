import torch
import random

# Setup where things are stored
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Fixed seed for testing purposes
random.seed(5)

# Generate some random data
# N: number of samples
N = 10
# Q: number of questions
Q = 3
# C: number of categories per question
C = 4
# Generate integers for which answer picked
x = torch.randint(C, (N, Q))
# Now make later answers sometimes match first answer
similarity = 0.5
# How many samples to have in full dataset
SAMPLES = N
for n in range(N):
    for q in range(Q):
        if torch.rand(1, 1) < similarity:
            x[n][q] = x[n][0]
# Convert to one-hot, flatten questions together
# Make numerically floating point
x = torch.flatten(torch.nn.functional.one_hot(x), 1) * 1.0

# Let's try deleting one answer, train to get answer back
def samples():
    for index in range(SAMPLES):
        n = random.randint(0, N - 1)
        q = random.randint(0, Q - 1)
        i = x[n].clone()
        o = x[n].clone()
        mask = torch.tensor([0] * (Q * C))
        i[q * C : q * C + C] = 0
        mask[q * C : q * C + C] = 1
        yield (i, mask, o)

# Loss function that is only computed over nonzero mask area
mseloss = torch.nn.MSELoss()
def criterion(predicted, target, mask):
    print(target * mask, predicted * mask)
    return mseloss(predicted * mask, target * mask)

for (i, mask, o) in samples():
    print((i, mask, o, criterion(i, o, mask)))
