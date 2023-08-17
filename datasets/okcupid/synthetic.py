import numpy as np
import torch

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
        with open('okcupid_onehot.npz', 'rb') as fin:
            data = np.load(fin)
            self.onehot = data['onehot']
            self.anssize = data['anssize']
            self.dataset = data['dataset']
            self.N = self.onehot.shape[0]
            self.Q = self.anssize.shape[0]
            assert sum(self.anssize) == self.onehot.shape[1]
            self.nonzerosizes = np.count_nonzero(self.dataset, axis=1)

    def __len__(self):
        # There is one example per response per question
        return sum(self.nonzerosizes)
    
    def __getitem__(self, idx):
        n, q = split_index(idx, self.nonzerosizes)
        print(f'{idx} / {len(self)} = {n} : {q}')
        # # To get one sample, copy input and output
        # # Then delete the chosen output, create mask for that part
        # C = self.C
        # Q = self.Q
        # x = self.x
        # i = x[n].clone()
        # o = x[n].clone()
        # mask = torch.tensor([0] * (Q * C))
        # i[q * C : q * C + C] = 0
        # mask[q * C : q * C + C] = 1
        # return i, o, mask

dataset = CustomDataset()
for x in dataset:
    pass