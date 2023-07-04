import * as dotenv from 'dotenv';
dotenv.config();

import { parseArgs } from "node:util";
import fs from "fs";
import { partialParse } from "./tests/partial-json-parser.js";

import { Configuration, OpenAIApi } from "openai";
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Async iterator from chunk to lines
async function* chunksToLines(chunksAsync) {
    let previous = "";
    for await (const chunk of chunksAsync) {
        const bufferChunk = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
        previous += bufferChunk;
        let eolIndex;
        while ((eolIndex = previous.indexOf("\n")) >= 0) {
            // line includes the EOL
            const line = previous.slice(0, eolIndex + 1).trimEnd();
            if (line === "data: [DONE]") break;
            if (line.startsWith("data: ")) yield line;
            previous = previous.slice(eolIndex + 1);
        }
    }
}

// Async iterator from lines to messages (for web streaming)
async function* linesToMessages(linesAsync) {
    for await (const line of linesAsync) {
        const message = line.substring("data :".length);
        yield message;
    }
}

async function* streamCompletion(data) {
    yield* linesToMessages(chunksToLines(data));
}

function applyDelta(data, delta) {
    for (const [key, value] of Object.entries(delta)) {
        if (key in data) {
            if (typeof data[key] === 'string') {
                data[key] += value;
            } else {
                applyDelta(data[key], value);
            }
        } else {
            data[key] = value;
        }
    }
}

function applyPartialParse(data) {
    let result = {};
    for (const [key, value] of Object.entries(data)) {
        if (key === 'arguments') {
            result[key] = partialParse(value);
        } else {
            if (typeof value === 'object') {
                result[key] = applyPartialParse(value);
            } else {
                result[key] = value;
            }
        }
    }
    return result;
}

function specializedPartialParse(data) {
    let result = JSON.parse(JSON.stringify(data)); // deep clone to avoid changing input
    if (result.function_call && result.function_call.arguments) {
        result.function_call.arguments = partialParse(result.function_call.arguments);
    }
    return result;
}

async function getCompletion(prompt, system, stop, allowfunctions, cb) {
    const functions = [
        {
            "name": "reply",
            "description": "Specify the reply for a character in the dialogue.",
            "parameters": {
                "type": "object",
                "properties": {
                    "emotion": {
                        "type": "string",
                        "description": "The emotion to associate with the reply, e.g. 'angry', or 'neutral' for no specific emotion.",
                    },
                    "data": {
                        "type": "string",
                        "description": "The actual reply of the character in the dialogue.",
                    },
                },
                "required": ["emotion", "data"],
            },
        },
    ];
    const req = {
        model: "gpt-3.5-turbo",
        messages: system ? [
            {role: "system", content:system}, 
            {role: "user", content: prompt},
        ] : [
            {role: "user", content: prompt},
        ],
        temperature: 0.5,
        max_tokens: 500,
        stream: true,
        functions: functions,
        function_call: {
            "name": "reply",
        },
    };
    if (stop) {
        req.stop = stop;
    }
    const response = await openai.createChatCompletion(req, {
        responseType: "stream",
    });
    let data = {};
    let dataParsed = {};
    for await (const message of streamCompletion(response.data)) {
        try {
            const parsed = JSON.parse(message);
            const delta = parsed.choices[0].delta;
            applyDelta(data, delta);
            if (allowfunctions) {
                dataParsed = specializedPartialParse(data);
                cb(dataParsed);
            }
            process.stdout.write(JSON.stringify(data));
        } catch (error) {
            console.error("Could not JSON parse stream message", message, error);
        }
    }
}

async function main() {
    const { values: { nosystem, system, number, include, stop, allowfunctions }, positionals } = parseArgs({
        options: {
            nosystem: {
                type: "boolean",
                short: "x",
            },
            system: {
                type: "string",
                short: "s",  
            },
            number: {
                type: "string",
                short: "n",
            },
            include: {
                type: "string",
                short: "i",
                multiple: true,
            },
            stop: {
                type: "string",
                short: "e",
            },
            allowfunctions: {
                type: "boolean",
                short: "f",
            },
        },
        allowPositionals: true,
    });
    const num = Number(number) || 1;
    const msg = positionals.join(' ');
    let systemPrompt = nosystem ? undefined : (system || 'You are a helpful cheerful assistant.');
    let prompt = "";
    for (let file of include || []) {
        process.stdout.write(`READING ${file}\n`);
        const data = fs.readFileSync(file, { encoding: 'utf-8' });
        prompt += data;
    }
    prompt += msg;
    process.stdout.write(`N=${num}\nsystemPrompt=${systemPrompt}\nstop=${stop}\nprompt=${prompt}\n`);
    for (let i = 0; i < num; i++) {
        await getCompletion(prompt, systemPrompt, stop, allowfunctions, (data) => {
            console.log(data);
        });
    }
}

main()
