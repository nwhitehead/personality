# AI Personality

A service for creating AI personalities.

* Create custom AIs, define your own personality and persona by answering quiz questions.
* Interact long-term with a persistent AI.
* Publish your AIs to the world for others.

Features:
* Comes with set of pictures for avatars (initially just Ashani)
* Tools for easily tweaking and creating new personas (no typing needed)
* Quiz questions determine base personality and description, filled in with automatic details.
* AI can update avatar image to express emotions
* Persistent long-term memory of important details, chat history.

## Name ideas

ShimmerAI

## Tech Ideas

Use ChatGPT-3.5 turbo for main API backend. Tried Pygmalion and open source alternatives, not good enough I think.

Context needs to be limited on the input side. Maybe 512 tokens for persona info and permanent memory, then 1024 tokens
for rolling chat history. Then 512 tokens for chat recall, memory recall. Chat recall is lines of chat, based on embedding
similarity to current line. Memory recall is recalling specific memories that are created and stored on server by bot.
ChatGPT uses JSON "function calls" to store memories, change emotion expressed, change "permanent" memory.

Use [Spacy](https://spacy.io/) for splitting sentences for chunking.

We can do summarization with:
[BART Large CNN Samsum](https://huggingface.co/philschmid/bart-large-cnn-samsum)

Embedding can use Sentence Transformers, or Instruct.
[InstructOR paper](https://arxiv.org/abs/2212.09741)


## Testers

Need alpha testers to try chats, see if things are working or not. Test each aspect of the model, each aspect of interaction.

Plan: put up signup page, with catchy graphics, some text describing how it works.

## Competitors

* replika
* [CharStar](https://charstar.ai/)
* [kuki](https://www.kuki.ai/about)
* hoomano
* koko

CharStar is scary. I don't want to be in that world. Interface is nice (but doesn't stream).

Tried kuki, not impressed. It told me about AIML, claimed to have written an essay, then had no idea what I was talking about when I asked if there was a link to it.

In general: Pygmalion-6B is not adequate. ChatGPT-3.5 can be annoyingly prudish for "friend chats". Needs jailbreak to be at all non-professional. But with
reasonable system prompt can be intelligent and actually friendly. For local models, my favorites are:
* WizardLM-13B-V1.1-GPTQ
* Pygmalion-13B-SuperHOT-8K-GPTQ


## Quiz

Quiz should be PF16, that is more interesting than big 5 style. Found good resources at:
[OpenPsychometrics/data](https://openpsychometrics.org/_rawdata/)
They also have interesting stuff with movie/book recommendations, "Which Character", and other stuff.

Wikipedia on PF16 has descriptors for low and high for each factor:
https://en.wikipedia.org/wiki/16PF_Questionnaire

Best Big-5 one:
[OpenPsychometrics big-5](https://openpsychometrics.org/printable/big-five-personality-test.pdf)

Hobbies:
[Personality Database](https://www.personality-database.com/profile?pid=3&cid=30&sub_cat_id=31569)

OkCupid had good quizzes back in the day. Some are available for psychological research.
[OkCupid Dataset paper](https://openpsych.net/paper/46/)

## Fun

One thing that might be fun is quiz questions for you and for the AI persona. The quiz question
asks what they think they other person would answer. Basically a quiz to see how well you know
the other person. The quiz questions for this game can also be used to generate the AI persona
(e.g. generating answers to them is the thing generating the persona).

Example questions:
[BGR couple's quiz](https://www.mindbodygreen.com/articles/couples-quiz)

[Women's Health Magazine quiz](https://www.womenshealthmag.com/sex-and-love/a32160810/couples-quiz-questions/)

[Pyschology Today](https://www.psychologytoday.com/us/blog/in-practice/201607/21-questions-test-how-well-you-really-know-your-partner)

Some issues:
* How does scoring work? These types of questions aren't easy to say "yes" or "no" to an answer. Need to ask ChatGPT how good
an answer it is with explanation maybe.
* Need to make sure quiz answers are consistent. They overlap in many ways. Maybe start with factual family history, then personality,
then preferences and thoughts about things. Build up with existing answers in context each time.



## Costs

Back of envelope:

Context:
* 250 tokens for system prompt
* 250 tokens for basic character description
* 500 "memory" retrieved tokens from past conversation (or just linear
conversation if not rolling off yet)
* 1000 linear history tokens

Each conversation round maybe takes 150 tokens in history. So 1000 tokens is
maybe 7 rounds of more "full" text, or maybe 15 rounds of short replies.

Output is maybe: 100 tokens for character, 100 tokens for 4 suggestions (they are
usually short). So maybe budget 250 tokens for everything.

Total is input 2000, output 250. Prices are $0.0015 / 1ktok input, $0.002 / 1 ktok for output.
That would be: $0.003 + $0.0005 = $0.0035 per turn. Or about 300 turns per dollar.

Character generation involves a large query with quiz results, generating keywords, fake
life story, fake favorites, fake description. Might be a combination of chatgpt and local
models. Rought calculation for all chatgpt would be maybe 2k tokens input, 1k tokens output.
That would be $0.003 + $0.002 = $0.005 or 200 generations per dollar.

Doing it in GPT-4 would be: $.03 input and $.06 output prices. So the numbers would be:
$0.06 + $.015 = $0.075 or 13 turns per dollar. Generation would be $0.06+$0.06=$0.12
per character or 8 generations per dollar.
