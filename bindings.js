const binary = require('node-pre-gyp');
const path = require('path');
const binding_path = binary.find(path.resolve(path.join(__dirname,'./package.json')));
const {USVFS} = require(binding_path);

module.exports = USVFS;
