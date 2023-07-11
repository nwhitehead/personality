
import fs from 'fs';
import normal from '@stdlib/random/base/normal';

const data = fs.readFileSync('cholcov.npy');
const buff = data.buffer.slice(data.byteOffset, data.byteOffset + data.byteLength);

