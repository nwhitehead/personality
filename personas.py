from datasets import load_dataset
import random

# load dataset
dataset = load_dataset("bavard/personachat_truecased")

# access training split
train_data = dataset["train"]

# get personality descriptions as a list
personality_descriptions = train_data["personality"]
personality_descriptions

# sample 50 of the descriptions
random.seed(42)
personality_descriptions_sampled = random.sample(personality_descriptions, k=50)

for x in personality_descriptions_sampled:
    print(x)
