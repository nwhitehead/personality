import torch
import numpy as np
import sys

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
            print(f'{idx} / {len(self)} = {n} : {maskq} : {maskqq}')
            # To get one sample, copy input and output
            # Then delete the chosen output, create mask for that part
            # Expand integers into one hot for one response
            t = np.zeros((self.sz,), dtype=int)
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
            i = torch.tensor(t)
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
print(len(dataset))

train_dataloader = torch.utils.data.DataLoader(dataset, batch_size=4, shuffle=True)

for x in train_dataloader:
    pass
    #print(x)
print('well we got here')