import { partialParse } from "../partial-json-parser.js";

const test = "{\n  \"emotion\": \"cheerful\",\n  \"data\": \"Ashani grew up in a small town in India, surrounded by a loving and supportive family. At the age of 12, she moved to the USA with her parents, where she faced the challenges of adapting to a new culture and language. Despite the initial difficulties, Ashani's positive outlook and determination helped her excel in academics and build strong relationships. She pursued her passion for psychology in college, which further enhanced her people-focused and caring nature. Ashani's experiences of immigration and cultural integration have shaped her into a compassionate and understanding individual, always ready to lend a helping hand and make a positive impact\"}";

for (let i = 0; i < test.length; i++) {
    const t = test.slice(0, i);
    console.log(`Parsing type=${typeof t} length=${t.length}\n${t}`);
    const result = partialParse(t);
    console.log(`Parsing type=${typeof t} length=${t.length}\n${t} result=${JSON.stringify(result)}`);
}
