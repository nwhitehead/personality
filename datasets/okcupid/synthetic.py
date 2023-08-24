import torch
import random
import numpy as np
import sys

# Fixed seed for testing purposes
random.seed(5)
torch.manual_seed(5)

# Setup where things are stored
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def split_index(idx, sizes):
    '''
    Split a linear index into question and category fields

    idx: number from 0 to sum of sizes (exclusive)
    returns: tuple of index to sizes, and offset from that size
    '''
    sm = 0
    for index, sz in enumerate(sizes):
        x = sm + sz
        if idx < x:
            return (index, idx - sm)
        sm = x
    raise RuntimeError('could not split, index too large')

class CustomDataset(torch.utils.data.Dataset):
    """Custom synthetic testing dataset"""
    def __init__(self):
        with open('okcupid.npz', 'rb') as fin:
            data = np.load(fin)
            # Remove one because we interpret 0 entries as no data (not a category itself for one shot encoding)
            self.anssize = np.array([x - 1 for x in data['anssize']])
            self.dataset = data['dataset'].T
            self.N = self.dataset.shape[0]
            self.Q = self.anssize.shape[0]
            self.sz = sum(self.anssize)
            assert self.anssize.shape[0] == self.dataset.shape[1]
            self.nonzerosizes = np.count_nonzero(self.dataset, axis=1)

    def __len__(self):
        # There is one example per response per question
        return sum(self.nonzerosizes)
    
    def __getitem__(self, idx):
        try:
            n, maskq = split_index(idx, self.nonzerosizes)
            # maskq is an index into nonzero choices on the row n in the dataset
            # Find the actual question number for the maskq-th nonzero choice
            nz = [i for i in range(self.Q) if self.dataset[n, i] > 0]
            maskqq = nz[maskq]
            #print(f'{idx} / {len(self)} = {n} : {maskq} : {maskqq}')
            # To get one sample, copy input and output
            # Then delete the chosen output, create mask for that part
            # Expand integers into one hot for one response
            t = torch.tensor(np.zeros((self.sz,)), dtype=torch.float)
            pos = 0
            for q in range(self.Q):
                cmax = self.anssize[q]
                c = int(self.dataset[n, q])
                # if c is 0, there is no 1 to place
                if c > 0:
                    assert 0 < c <= cmax
                    # subtract 1 because c is in range 1..cmax, offset is 0..cmax-1
                    t[pos + c - 1] = 1
                pos += self.anssize[q]
            # Now t has one hot encoding of entire answer row
            # Clone into i for input
            i = t.clone().detach()
            # Create mask
            mask = torch.tensor([0] * self.sz)
            maskpos = sum(self.anssize[:maskqq])
            masksz = self.anssize[maskqq]
            mask[maskpos : maskpos + masksz] = 1
            # Clear input so we don't give away the answer
            i[maskpos : maskpos + masksz] = 0
            return i, t, mask
        except:
            print('exception')
            raise RuntimeError()

dataset = CustomDataset()

BS = 16
train_dataset, test_dataset, _unused_data = torch.utils.data.random_split(dataset, [0.0001, 0.00001, 0.99989])
train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=BS, shuffle=True)
test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=BS, shuffle=True)

# Define model
import torch.nn as nn
class NeuralNetwork(nn.Module):
    def __init__(self, L, SZ):
        super().__init__()
        self.L = L
        self.SZ = SZ
        self.ops = nn.Sequential(
            nn.Linear(L, SZ),
            nn.ReLU(),
            nn.Linear(SZ, SZ),
            nn.ReLU(),
            nn.Linear(SZ, L)
        )

    def forward(self, x):
        return self.ops(x)

model = NeuralNetwork(4073, 1024).to(device)

# Loss function that is only computed over nonzero mask area
mseloss = torch.nn.MSELoss()
def loss_fn(predicted, target, mask):
    return mseloss(predicted * mask, target * mask)

optimizer = torch.optim.AdamW(model.parameters())

def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader) * BS
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
    size = len(dataloader) * BS
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
epochs = 5
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)
    test(test_dataloader, model, loss_fn)
print("Done!")
