import time
import torch
from transformers import pipeline
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f'device={device}')
summarizer = pipeline("summarization", model="philschmid/bart-large-cnn-samsum", device=device, min_length=10, max_length=100)

conversation = '''
Ashani: *You are both sitting in a coffee shop after lunch. Ashani sips her coffee.* What's on your mind?

User: Why are people such morons?

Ashani: *Ashani puts her coffee cup down and looks at User with a sympathetic expression, her soft brown eyes filled with understanding.* It can be disheartening sometimes, witnessing the shortcomings of others. But I believe that everyone has their own struggles and flaws. Perhaps their actions are a result of their own fears or insecurities. It's essential to remember that we all make mistakes and have room to grow. Instead of labeling them as morons, maybe we can try to understand their perspective or offer a helping hand if they're open to it. Is there a specific situation that prompted this question?

User: My boss was being a jerk today. He cancelled a meeting right before it started. I worked all week to make the presentation, all useless.
'''

conversation='''
Ashani is a 35 year old Indian American living in San Francisco. She went to college in the USA and immigrated when she was 12 years old. Ashani is people focused, feeling oriented, giving and caring, qualitative over quantitative, calm, patient and accepting, level-headed, competitive, intense and passionate, serious and withdrawn, positive outlook toward authority, comfortable alone, tender and forgiving, assumes honesty, direct in speech, and emotionally expressive.
'''

conversation='''
Pam: *Pam and I are lounging in the hallway between class, talking about our plans for the weekend and holding hands with fingers entwined. Our faces are turned towards each other as we lean separately against the lockers. Pam looks at me with bright eyes.*
So You, what do you want to do Friday night?
*Nearby, the class clown has knocked over a trashcan accidentally, and is being chased by the janitor.*

Nathan: Maybe we can bake some brownies together.

Pam: Yeah! That sounds great! We could make them while watching a movie after dinner, then take a walk afterwards.
*The bell rings for 5th period, ending our conversation before I have time to ask anything else. As we part ways in the hallway, the crowd of students begin leaving school. Pam looks back at me with a smile as she walks away.*

Nathan: See you tonight!

Pam: *waves goodbye!*
*As soon as class is over, Pam and I meet up outside my house. She's carrying two bags full of ingredients that will be used to bake brownies together. We enter into her kitchen, then head towards the oven to preheat it.
She turns on the oven while talking about our plans for the night.*

Nathan: Are your parents going to be home tonight?

Pam: Yeah, they usually are, but they go out late at night sometimes though so we can stay up later than usual. It won't be a problem if they come back in late. They always trust us when we say we're safe with each other! *smiles and giggles*
'''

summary = summarizer("Nathan: What is the meaning of life?\n\nAssistant: 42, of course.\n")
print(summary)
print('start')
t0 = time.perf_counter_ns()
n = 1
for i in range(n):
    summary = summarizer(conversation)
t1 = time.perf_counter_ns()
dur = (t1 - t0) * 1e-9
print(f'Summary:{summary}\nTime: {dur / n} sec/it, or {n / dur} it/sec')
