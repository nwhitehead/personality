import torch

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
for n in range(N):
    for q in range(Q):
        if torch.rand(1, 1) < similarity:
            x[n][q] = x[n][0]
# Convert to one-hot, flatten questions together
x = torch.flatten(torch.nn.functional.one_hot(x), 1)
print(x)

# Let's try deleting one answer, train to get answer back
