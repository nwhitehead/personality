from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time
import fileinput
import numpy

device = "cpu" #  torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")

model.eval()
model.to(device)

label = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
    'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 'joy', 'love', 'nervousness',
    'optimism', 'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral']

for line in fileinput.input():
    tokens_bad = tokenizer(line.rstrip(),
        truncation=True,
        max_length=512,
        return_token_type_ids=False,
        return_tensors="pt",
        return_attention_mask=True)

    #print(len(tokens_bad['input_ids']))
    tokens_bad.to(device)

    t0 = time.perf_counter_ns()
    scores = model(**tokens_bad).logits.cpu().detach().numpy()
    t1 = time.perf_counter_ns()
    dur = (t1 - t0) * 1e-9
    iscores = numpy.argsort(scores)
    sscores = [(label[i], scores[0][i]) for i in reversed(iscores[0])]
    sscores = [x for x in sscores if x[1] > -2]
    print(f'scores: {sscores}\ntime: {dur} s (equiv. {1 / dur} it/s)')
