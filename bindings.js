const path = require('path')
const gyp = require('node-pre-gyp')

const binaryPath = gyp.find(path.resolve(__dirname, 'package.json'))

// eslint-disable-next-line node/no-unpublished-require
const binary = require(binaryPath)

module.exports = binary.USVFS
