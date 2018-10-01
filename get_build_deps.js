const path = require('path');
const fs = require('fs');
const {spawn} = require('child_process');
const os = require('os');

let args = {};

args = process.argv.slice(2).reduce((argMap, arg) => {
	if (arg.charAt(0) === '-') {
		const keyIndex = arg.charAt(1) == '-' ? 2 : 1;
		const key = arg.indexOf('=') > -1 ? arg.substring(keyIndex, arg.indexOf('=')) : arg.substring(keyIndex);
		const value = arg.indexOf('=') > -1 ? arg.substring(arg.indexOf('=') + 1) : true;

		argMap[key] = value;
		return argMap;
	}

	argMap.unknown.push(arg);
	return argMap;
}, {
	unknown: [],
});

// clone deps
const usvfsPath = path.resolve(__dirname, "deps", "usvfs");
const boostPath = path.resolve(__dirname, "deps", "boost");
const udis86Path = path.resolve(usvfsPath, "udis86");

const boostLibArch = (args.arch || os.arch()) == 'x64' ? '64' : '32';
const boostBackupLib = path.resolve(boostPath, 'stage', 'lib');
const boostLib = process.env.BOOST_LIB || boostBackupLib;

console.log(`Checking if boost is ready to use at ${boostLib}`);
isBoostReady(boostLib)
	.then(isReady => {
		if (! isReady) return buildLocalBoost();
	})
	.then(() => {
		console.log('boost is ready');
		console.log('Checking if deps/usvfs is cloned');
		return isCloned(usvfsPath);
	})
	.then(usvfsIsCloned => {
		if (! usvfsIsCloned) {
			console.log('Cloning deps/usvfs');
			return spawnCommand("git", ["submodule", "update", "deps/usvfs", "--recursive"], {
				cwd: __dirname,
				stdio: 'inherit',
			});
		}
	})
	.then(() => {
		console.log('deps/usvfs is cloned');
		console.log('Checking if udis86 is ready');
		return allExist([
			path.resolve(udis86Path, "libudis86/decode.c"),
			path.resolve(udis86Path, "libudis86/itab.c"),
			path.resolve(udis86Path, "libudis86/syn-att.c"),
			path.resolve(udis86Path, "libudis86/syn-intel.c"),
			path.resolve(udis86Path, "libudis86/syn.c"),
			path.resolve(udis86Path, "libudis86/udis86.c"),
		]);
	})
	.then(udis86IsReady => {
		if (! udis86IsReady) {
			console.log('Building udis86');
			return spawnCommand('python', ["scripts/ud_itab.py", "docs/x86/optable.xml", "libudis86"], {
				cwd: udis86Path,
				stdio: 'inherit',
			});
		}

		console.log('udis86 is ready');
	})
	.then(() => {
		console.log('Build depedencies are ready');
		process.exit(0);
	})
	.catch((err) => {
		console.error(err);
		process.exit(err.code || 1);
	});

function buildLocalBoost() {
	console.log('Checking if deps/boost is cloned');
	return isCloned(boostPath)
		.then(boostIsCloned => {
			if (! boostIsCloned) {
				console.log('Cloning deps/boost');
				return spawnCommand("git", ["submodule", "update", "deps/boost", "--recursive"], {
					cwd: __dirname,
					stdio: 'inherit',
				});
			}
		})
		.then(() => {
			console.log('deps/boost is cloned');
			console.log('Building boost');
			return spawnCommand(".\\bootstrap.bat", {cwd: boostPath, stdio: 'inherit'})
				.then(() => spawnCommand(".\\b2.exe", [
					"--with-date_time",
					"--with-coroutine",
					"--with-filesystem",
					"--with-thread",
					"--with-log",
					"--with-locale",
					`address-model=${boostLibArch}`,
					"architecture=x86",
					"link=static",
					"runtime-link=static"
				], {cwd: boostPath, stdio: 'inherit'}));
		});
}

function isBoostReady(lib) {
	return allExist([
		path.resolve(boostLib, `libboost_atomic-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_atomic-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_chrono-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_chrono-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_context-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_context-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_coroutine-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_coroutine-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_date_time-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_date_time-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_filesystem-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_filesystem-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_locale-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_locale-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_log-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_log-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_log_setup-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_log_setup-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_regex-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_regex-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_system-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_system-vc141-mt-sgd-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_thread-vc141-mt-s-x${boostLibArch}-1_67.lib`),
		path.resolve(boostLib, `libboost_thread-vc141-mt-sgd-x${boostLibArch}-1_67.lib`)
	]);
}

function isCloned(path) {
	return allExist([path])
		.then(exists => {
			if (exists) return isEmpty(path).then(empty => ! empty);
			return false;
		});
}

function spawnCommand(...args) {
	return new Promise((resolve, reject) => {
		const p = spawn(...args);

		p.once('close', code => {
			p.removeAllListeners();
			if (code != 0) reject(new Error(`'${args.join(' ')}' exited with a non-zero code`));
			else resolve();
		});

		p.once('error', err => {
			p.removeAllListeners();
			reject(err);
		});
	});
}

function isEmpty(path) {
	return new Promise((resolve, reject) => {
		fs.stat(path, (err, stats) => {
			if (err) reject(err);
			else if (! stats.isDirectory()) reject(`${path} is not a directory`);
			else fs.readdir(path, (err, files) => {
				if (err) reject(err);
				else resolve(! files.filter(name => name != ".git").length);
			});
		});
	});
}

function allExist(files) {
	const proms = files.map(file => new Promise((resolve, reject) => fs.access(file, fs.constants.F_OK, err => {
		if (err) {
			if (err.code === 'ENOENT') resolve(false);
			else reject(err);
		}
		else resolve(true);
	})));

	return Promise.all(proms).then(results => results.every(exists => exists));
}
