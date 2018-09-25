import path from 'path';
import gyp from 'node-pre-gyp';

const binaryPath = gyp.find(path.resolve(__dirname, '..', 'package.json'));
const {USVFS} = require(binaryPath);

export default USVFS;
