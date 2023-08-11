
import torch
import random

# Fixed seed for testing purposes
random.seed(5)
torch.manual_seed(5)

# Setup where things are stored
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class CustomDataset(torch.utils.data.Dataset):
    """Custom synthetic testing dataset"""
    def __init__(self, N, Q, C, similarity, samples):
        """
        N: number of simulated user responses
        Q: number of questions
        C: number of categories per question
        similarity: chance any later answers copy first answer
        samples: number of generated samples
        """
        self.N = N
        self.Q = Q
        self.C = C
        self.similarity = similarity
        self.samples = samples
        # Actually generate the choices here
        self.x = torch.randint(C, (N, Q))
        # Now fill in same choices based on similarity (before we one-hot encode for simplicity)
        for n in range(N):
            for q in range(Q):
                if torch.rand(1, 1) < similarity:
                    self.x[n][q] = self.x[n][0]
        # Convert to one-hot, flatten questions together
        # Make numerically floating point
        self.x = torch.flatten(torch.nn.functional.one_hot(self.x), 1) * 1.0
        # Now fill in sample choices
        self.sample_choices = torch.randint(N, (1, samples))
        self.question_choices = torch.randint(C, (1, samples))

    def __len__(self):
        return self.samples
    
    def __getitem__(self, idx):
        C = self.C
        Q = self.Q
        x = self.x
        n = self.sample_choices[0][idx]
        q = self.question_choices[0][idx]
        i = x[n].clone()
        o = x[n].clone()
        mask = torch.tensor([0] * (Q * C))
        i[q * C : q * C + C] = 0
        mask[q * C : q * C + C] = 1
        return i, o, mask

# Generate some random data
data = CustomDataset(10, 3, 4, 0.5, 20)
for i in data:
    print(i)

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

# for (i, mask, o) in samples():
#     print((i, mask, o, criterion(i, o, mask)))