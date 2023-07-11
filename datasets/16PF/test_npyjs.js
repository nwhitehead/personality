// Client-side parser for .npy files
// See the specification: http://docs.scipy.org/doc/numpy-dev/neps/npy-format.html
function asciiDecode(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
}

function readUint16LE(buffer) {
    const view = new DataView(buffer);
    let val = view.getUint8(0);
    val |= view.getUint8(1) << 8;
    return val;
}

function parseNumpy(buf) {
    // Check the magic number
    const magic = asciiDecode(buf.slice(0,6));
    if (magic.slice(1,6) != 'NUMPY') {
        throw new Error('unknown file type');
    }

    const version = new Uint8Array(buf.slice(6,8));
    const headerLength = readUint16LE(buf.slice(8,10));
    const headerStr = asciiDecode(buf.slice(10, 10+headerLength));
    const offsetBytes = 10 + headerLength;

    // Hacky conversion of dict literal string to JS Object
    const headerStrR = headerStr.replaceAll("'", '"').replaceAll('True', 'true').replaceAll('False', 'false').replaceAll('(','[').replaceAll('),',']');

    const info = JSON.parse(headerStrR);
    // Intepret the bytes according to the specified dtype
    let data;
    if (info.descr === "|u1") {
        data = new Uint8Array(buf, offsetBytes);
    } else if (info.descr === "|i1") {
        data = new Int8Array(buf, offsetBytes);
    } else if (info.descr === "<u2") {
        data = new Uint16Array(buf, offsetBytes);
    } else if (info.descr === "<i2") {
        data = new Int16Array(buf, offsetBytes);
    } else if (info.descr === "<u4") {
        data = new Uint32Array(buf, offsetBytes);
    } else if (info.descr === "<i4") {
        data = new Int32Array(buf, offsetBytes);
    } else if (info.descr === "<f4") {
        data = new Float32Array(buf, offsetBytes);
    } else if (info.descr === "<f8") {
        data = new Float64Array(buf, offsetBytes);
    } else {
        throw new Error('unknown numeric dtype')
    }

    return {
        shape: info.shape,
        fortran_order: info.fortran_order,
        data: data
    };
}

import fs from 'fs';
const data = fs.readFileSync('cholcov.npy');
const buff = data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength);
const parsed = parseNumpy(buff);
console.log(parsed);
// const arr = await n.load("./cholcov.npy");
// console.log(arr);