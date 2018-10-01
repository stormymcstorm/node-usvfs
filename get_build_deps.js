const path = require('path');
const fs = require('fs');
const {spawn} = require('child_process');
const os = require('os');

// clone deps
const usvfsPath = path.resolve(__dirname, "deps", "usvfs");
const boostPath = path.resolve(__dirname, "deps", "boost");

const boostLibArch = os.arch() == 'x64' ? '64' : '32';

allExist([usvfsPath, boostPath])
	.then(exist => {
		if (exist) return Promise.all([isEmpty(usvfsPath), isEmpty(boostPath)])
			.then(res => res.every(empty => ! empty));
		else return false;
	})
	.then(areCloned => {
		if (! areCloned) {
			console.log("Clonning submodules");
			return spawnCommand("git", ["submodule", "update", "--init", "--recursive"]);
		}
		else console.log("Submodules are cloned");
	})
	.then(() => allExist([path.resolve(boostPath, 'stage', 'lib', `libboost_atomic-vc141-mt-s-x${boostLibArch}-1_67.lib`)]))
	.then(boostIsBuilt => {
		if (! boostIsBuilt) {
			console.log("Building boost");
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
		} else console.log('Boost is built');
	})
	.then(() => allExist([path.resolve(usvfsPath, 'udis86', 'libudis86', 'itab.c')]))
	.then(udisIsBuilt => {
		if (! udisIsBuilt) {
			console.log('Building udis86');

			return spawnCommand(path.resolve(process.env.USERPROFILE, '.windows-build-tools', 'python27', 'python'), ["scripts/ud_itab.py", "docs/x86/optable.xml", "libudis86"], {
				cwd: path.resolve(usvfsPath, 'udis86'),
				stdio: 'inherit',
			});
		}
		else console.log('udis86 is built')
	})
	.catch(console.error);

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
