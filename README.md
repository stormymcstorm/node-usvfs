# node_usvfs
Node.js bindings for [User Space Virtual File System (USVFS)](https://github.com/modorganizer2/usvfs).

This only works on 64-bit Windows 10

# Install
```
npm install @stormymcstorm/node_usvfs -S
```
**WARNING**: if this there is not already a prebuilt binary for your system this module will take a long time to compile and will require a lot of space

# Usage

```js
const USVFS = require('@stormymcstorm/node_usvfs');
const path = require('path');

const vfs = new USVFS('node');

// create a virtual link between directories
vfs.linkDirectoryStatic(path.resolve('example/s'), path.resolve('example/d'));

// notepad will have access to the virtual file system
vfs.spawn('notepad.exe', () => {
	console.log('done');
});
```

# Documentation

## clearMappings()
```
vfs.clearMappings();
```
The clear mappings method will clear all virtual links

## linkFile(string src, string dest)
Creates a virtual link to the file
```
const wasLinked = vfs.linkFile(pathTosrc, pathToDest);
```
* `string src` the source file to link. Must be a absolute path
* `string dest` the destination for the link

Returns a `boolean` indicating whether or not the file was successfuly linked

## linkDirectoryStatic(string src, string dest)
Creates virtual links for all the files in the directory
```
const wasLinked = vfs.linkDirectoryStatic(pathTosrc, pathToDest);
```
* `string src` the source directory to link. Must be a absolute path
* `string dest` the destination for the link

Returns a `boolean` indicating whether or not the directory was successfuly linked

## disconnect()
disconnects from the current vfs
```
vfs.disconnect();
```

## spawnSync(string command)
Spawns the given command and blocks until the process exits
```
vfs.spawnSync('notepad.exe');
```
* `string command` the command to spawn

## spawn(string command, [function callback])
Spawns the given command asynchronously
```
vfs.spawn('notepad.exe', () => console.log('done'));
```
* `string command` the command to spawn
* `[function callback]` a optional callback to be called when the process exits

# Requirements

## Operating System
Windows 10 64-bit

## Software

### Windows build tools
node-gyp requires [windows-build-tools](https://www.npmjs.com/package/windows-build-tools) to run

### Visual Studio 2017
USVFS requires
[Visual Studio 2017](https://visualstudio.microsoft.com/vs/) to compile.
  - Workloads
    - Desktop development with C++
  - Individual components
    - Windows 10 SDK (10.0.16299.0) for Desktop C++ [x86 and x64]

# TODO
- [ ] allow for relative paths
- [ ] support 32 bit windows
- [ ] add support for creating multiple virtual file systems

# License
[MIT](LICENSE)
