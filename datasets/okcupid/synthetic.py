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
            self.N = self.onehot.shape[0]
            self.Q = self.anssize.shape[0]
            assert sum(self.anssize) == self.onehot.shape[1]
    def __len__(self):
        # There is one example per response per question
        return self.N * self.Q
    
    def __getitem__(self, idx):
        index, offset = split_index(idx, self.anssize)
        print(idx, index, offset)
        # # To get one sample, copy input and output
        # # Then delete the chosen output, create mask for that part
        # C = self.C
        # Q = self.Q
        # x = self.x
        # n = self.sample_choices[0][idx]
        # q = self.question_choices[0][idx]
        # i = x[n].clone()
        # o = x[n].clone()
        # mask = torch.tensor([0] * (Q * C))
        # i[q * C : q * C + C] = 0
        # mask[q * C : q * C + C] = 1
        # return i, o, mask

dataset = CustomDataset()
for x in dataset:
    pass