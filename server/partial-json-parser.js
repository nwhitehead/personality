// https://github.com/indgov/partial-json-parser/blob/master/partial-json-parser.js
// https://github.com/indgov/partial-json-parser
// MIT, 2017

function getNonWhitespaceCharacterOfStringAt(s, i) {
    if (s === "") {
        return {
            character: undefined,
            index: i
        };
    }
    while (s[i].match(/\s/) !== null) {
        i--;
    }
    return {
        character: s[i],
        index: i
    };
};

export function partialParse(s) {
    s = s.replace(/\r\n/g, '');
    if (s === "") {
        return undefined;
    }
    if (s === '"') {
        return '';
    }
    if (s === null) {
        return null;
    }
    if (s === undefined) {
        return undefined;
    }
    let tail = [], i, lastCharacter;
    for (i = 0; i < s.length; i++) {
        if (s[i] === '{') {
            tail.push('}');
        }
        else if (s[i] === '[') {
            tail.push(']');
        }
        else if (s[i] === '}') {
            tail.splice(tail.lastIndexOf('}'), 1);
        }
        else if (s[i] === ']') {
            tail.splice(tail.lastIndexOf(']'), 1);
        }
    }

    if (tail[tail.length - 1] === '}') {
        // Ignore checking if the last key is an array:
        if (s[s.length - 1] !== ']') {
            var insideLiteral = (s.split(/."/).length - 1) % 2 === 1 ? true : false, // If there are an odd number of double quotes, then we are in a string
                    lastKV = '',
                    metAColon = false,
                    j;
            for (j = s.length - 1; j >= 0; j--) {
                if (s[j] === ':') {
                    if (!insideLiteral) {
                        metAColon = true;
                        insideLiteral = false;
                    }
                }
                else if (s[j] === '{') {
                    if (!insideLiteral) {
                        if (!metAColon) {
                            lastKV = '';
                        }
                        j++;
                        break;
                    }
                } else if (s[j] === ',') {
                    if (!insideLiteral) {
                        if (!metAColon) {
                            lastKV = '';
                        }
                        break;
                    }
                } else {
                    if (s[j] === '"') {
                        insideLiteral = !insideLiteral;
                    }
                    if (!metAColon) {
                        if (j !== s.length - 1 || s[j] !== '}') {
                            lastKV = lastKV + s[j];
                        }
                    }
                }
            }
            lastKV = lastKV.split('').reverse().join('').trimStart();
            const isPartialString = lastKV.length > 1 && lastKV[0] === '"' && lastKV[lastKV.length - 1] !== '"';
            if (isPartialString) {
                s += '"';
            } else {
                const isFinishedString = lastKV.length !== 1 && lastKV[0] === '"' && lastKV[lastKV.length - 1] === '"';
                const isLegalConst = lastKV === 'false' || lastKV === 'true' || lastKV === 'null';
                const isLegalNumber = lastKV.match(/^\d+$/) !== null;
                if (!isLegalConst && !isLegalNumber && !isFinishedString && !isPartialString) {
                    s = s.slice(0, j);
                }
            }
        }
    }
    else if (tail[tail.length - 1] === ']') {
        if ((s.slice(s.lastIndexOf('[')).split('"').length - 1) % 2 === 1) {
            s = s.slice(0, s.lastIndexOf('"'));
        }
    }
    lastCharacter = getNonWhitespaceCharacterOfStringAt(s, s.length - 1);
    if (lastCharacter.character === ',') {
        s = s.slice(0, lastCharacter.index);
    }
    tail = tail.reverse();
    return JSON.parse(s + tail.join(''));
}
