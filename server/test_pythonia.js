import { python } from 'pythonia';
import fs from 'fs';

const txt = fs.readFileSync('./tests/test_result.md', { 'encoding': 'utf-8' });
const txts = txt.split('\n\n');

// Which model to use.
// Default is intfloat/e5-base-v2 which is quite good.
// Alternatives are:
//     intfloat/e5-small-v2
//     intfloat/e5-large-v2
const MODEL = 'intfloat/e5-base-v2';

// Load the module
const embedder = await python('./embedder.py');
const Embedder = await embedder.Embedder;
const score = await embedder.score;
// Instantiate the Embedder with our specific model
// This loads the model, downloading it into cache as needed.
const embedobj = await Embedder(MODEL);

async function embed(inputs, prefix) {
    // Call embedder object 
    const rawResult = await embedobj.embed(inputs, prefix);
    // Convert result from pytorch.Tensor to Python list
    const result = await (await (await (await (rawResult).cpu()).detach()).numpy()).tolist();
    // Now convert result to JavaScript
    return (await result.valueOf());
}

// const input_passages = [
//     'Suzy sells seashells by the seashore',
//     'The number 6 is a perfect number. That means the sum of its prime factors including 1 is equal to the number.',
//     'This is a red herring. A herring is a type of fish, and the fact that it is red makes it surprising and novel.',
// ];
const input_passages = txts;

const input_queries = [
    'What is your eye color?',
    'What is your favorite classic Hollywood flick?',
    'Is 8 a perfect number?',
    'Do you like painting?',
];

const passages_embeddings = await embed(input_passages, 'passage: ');
const passages_queries = await embed(input_queries, 'query: ');

console.log(passages_embeddings.length);
console.log(passages_queries.length);

const scores = await score(passages_embeddings, passages_queries);

console.log(scores);

python.exit();
