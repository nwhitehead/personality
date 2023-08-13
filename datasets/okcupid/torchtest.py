
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
        self.question_choices = torch.randint(Q, (1, samples))

    def __len__(self):
        return self.samples
    
    def __getitem__(self, idx):
        # To get one sample, copy input and output
        # Then delete the chosen output, create mask for that part
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
data = CustomDataset(10000, 10, 4, 0.3, 10000)

train_dataloader = torch.utils.data.DataLoader(data, batch_size=4, shuffle=True)
test_dataloader = torch.utils.data.DataLoader(data, batch_size=4, shuffle=True)

# Define model
import torch.nn as nn
class NeuralNetwork(nn.Module):
    def __init__(self, Q, C, SZ):
        super().__init__()
        self.Q = Q
        self.C = C
        self.SZ = SZ
        self.ops = nn.Sequential(
            nn.Linear(Q * C, SZ),
            nn.ReLU(),
            nn.Linear(SZ, SZ),
            nn.ReLU(),
            nn.Linear(SZ, Q * C)
        )

    def forward(self, x):
        return self.ops(x)

model = NeuralNetwork(10, 4, 40).to(device)

# Loss function that is only computed over nonzero mask area
mseloss = torch.nn.MSELoss()
def loss_fn(predicted, target, mask):
    return mseloss(predicted * mask, target * mask)

optimizer = torch.optim.AdamW(model.parameters())

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y, m) in enumerate(dataloader):
        X, y, m = X.to(device), y.to(device), m.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y, m)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y, m in dataloader:
            X, y, m = X.to(device), y.to(device), m.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y, m).item()
            guess = (pred * m).argmax(1)
            right = (y * m).argmax(1)
            correct += (guess == right).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


## Let's do this
epochs = 50
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)
print("Done!")
