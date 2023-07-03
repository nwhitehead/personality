import { partialParse } from "./partial-json-parser.js";

const test = "\'abc\'";
const test2 = '{ "name": { "first": "ind", "last": "go';

// console.log(test);
// console.log(partialParse(test));
// console.log(test2);
const result = partialParse(test2);
//console.log(result);
