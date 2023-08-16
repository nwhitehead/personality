import numpy as np
import torch

with open('okcupid.npz', 'rb') as fin:
    data = np.load(fin)
    # How many questions to consider?
    Q = data['dataset'].shape[0]
    # How many responses to consider?
    N = data['dataset'].shape[1]
    dataset = data['dataset'][:Q, :N]
    anssize = data['anssize'][:Q]
    cols = sum(anssize)
    res = np.zeros((N, cols))
    for q in range(Q):
        print(f'{q} / {Q}')
        # Where are we in res cols (one hot pieces are concatenated along column dimension)
        pos = sum(anssize[:q])
        # Number of classes for one hot
        C = anssize[q]
        # Expand integers into one hot for one response
        t = torch.tensor(dataset[q], dtype=torch.long)
        q0 = torch.nn.functional.one_hot(t, num_classes=C)
        # Put one hot values into right position of result matrix
        res[:, pos : pos + C] = q0
    # Now save it
    with open('okcupid_onehot.npz', 'wb') as fout:
        np.savez_compressed(fout, onehot=res, anssize=anssize, dataset=dataset.T)
