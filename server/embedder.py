import torch.nn.functional
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import numpy as np

def _average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

class Embedder:
    '''
    Embed text into vectors 

    Instantiation loads the model into memory. The `embed` method does the work.

    '''
    def __init__(self, model):
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.model = AutoModel.from_pretrained(model)

    def embed(self, input_texts, prefix='', max_length=512):
        # Tokenize the input texts
        inputs = [prefix + text for text in input_texts]
        print(inputs)
        batch_dict = self.tokenizer(inputs, max_length=max_length, padding=True, truncation=True, return_tensors='pt')
        # Run the model
        outputs = self.model(**batch_dict)
        embeddings = _average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        # Normalize embeddings
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings

def score(passages, queries):
    ''' 
    Score lists of embeddings
    
    passages is a list of embeddings for the content (M vectors of appropriate size for the model)
    queries is the list of query embeddings (N vectors of appropriate size for the model)

    Result is an M x N matrix of scores. Each element (r, c) of the matrix
    measures how close the r passage is to the c query.

    '''
    return (np.array(passages) @ np.array(queries).T)
