import torch.nn.functional as F

from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import time

MODEL = 'intfloat/e5-base-v2'

def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


# Each input text should start with "query: " or "passage: ".
# For tasks other than retrieval, you can simply use the "query: " prefix.
input_texts = [
    'passage: Suzy sells seashells by the seashore',
    'passage: The number 6 is a perfect number. That means the sum of its prime factors including 1 is equal to the number.',
    'passage: This is a red herring. A herring is a type of fish, and the fact that it is red makes it surprising and novel.',
    'query: Who sells seashells?',
    'query: Where does Suzy sell?',
    'query: Is 8 a perfect number?',
]

print('Tokenizing')
tokenizer = AutoTokenizer.from_pretrained(MODEL)
t_load0 = time.perf_counter()
print('Loading model')
model = AutoModel.from_pretrained(MODEL)
t_load1 = time.perf_counter()
print(f'Time to load mode: {t_load1 - t_load0} s')

time0 = time.perf_counter()

# Tokenize the input texts
batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

outputs = model(**batch_dict)
embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])

time1 = time.perf_counter()
delta = time1 - time0

BS = len(input_texts)
print(f'Time: {delta / BS}s ({BS / delta} per sec)')

# (Optionally) normalize embeddings
embeddings = F.normalize(embeddings, p=2, dim=1)
print(embeddings)

scores = (embeddings[:3] @ embeddings[3:].T) * 100
print(scores.tolist())
