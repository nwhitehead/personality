import torch.nn.functional as F

from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import time

def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


# Each input text should start with "query: " or "passage: ".
# For tasks other than retrieval, you can simply use the "query: " prefix.
BS = 1
N = 3
input_texts = ['query: how much protein should a female eat'] * BS

tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-large-v2')
model = AutoModel.from_pretrained('intfloat/e5-large-v2')

time0 = time.perf_counter()

for i in range(N):
    # Tokenize the input texts
    batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

    outputs = model(**batch_dict)
    embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])

time1 = time.perf_counter()
delta = time1 - time0

print(f'Batch time: {delta / N}s ({N / delta} per sec)')
print(f'Individual time: {delta / N / BS}s ({N * BS / delta} per sec)')

# (Optionally) normalize embeddings
embeddings = F.normalize(embeddings, p=2, dim=1)
print(embeddings)
