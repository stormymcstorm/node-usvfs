#include <node_usvfs.h>
#include <iostream>
#include <exception>

#define NAPI_EXPERIMENTAL

namespace node_usvfs {

// Utilities
struct SpawnOptions {
	Napi::String cwd;
	Napi::Object env;
};

LPWSTR stringToLPWSTR(const char* str) {
	int n = MultiByteToWideChar(CP_UTF8, 0, str, -1, NULL, 0); // get length

	LPWSTR result = new TCHAR[n];
	MultiByteToWideChar(CP_UTF8, 0, str, -1, result, n);

	return result;
}

// TODO: implment env and cwd options
bool spawnHookedProcess(Napi::String command, SpawnOptions opts, STARTUPINFO *si, PROCESS_INFORMATION *pi) {
	// clean startup and process info
	ZeroMemory(si, sizeof(*si));
	(*si).cb = sizeof(si);

	ZeroMemory(pi, sizeof(*pi));

	// create process
	return CreateProcessHooked(
		NULL,
		stringToLPWSTR(command.Utf8Value().c_str()),
		NULL,
		NULL,
		FALSE,
		NULL,
		NULL,
		NULL,
		si,
		pi
	);
}

SpawnOptions getSpawnOptions(Napi::Env env, Napi::Object opts) {
	SpawnOptions options;
	Napi::Value tmp;

	if (opts.Has("cwd")) {
		tmp = opts.Get("cwd");

		if (! tmp.IsString()) Napi::Error::New(env, "cwd must be a string").ThrowAsJavaScriptException();

		options.cwd = tmp.As<Napi::String>();
	}

	if (opts.Has("env")) {
		tmp = opts.Get("env");

		if (! tmp.IsObject()) Napi::Error::New(env, "env must be a object").ThrowAsJavaScriptException();

		options.env = tmp.As<Napi::Object>();
	}

	return options;
}

void throwLastError(Napi::Env env, const char* format) {
	char message [200];
	int lastError = GetLastError();

	sprintf(message, format, lastError);
	Napi::Error::New(env, message).ThrowAsJavaScriptException();
}

// Module functions
Napi::FunctionReference USVFS::constructor;

Napi::Object USVFS::Init(Napi::Env env, Napi::Object exports) {
	Napi::HandleScope scope(env);

	Napi::Function func = DefineClass(env, "USVFS", {
		InstanceMethod("ClearMappings", &USVFS::clearMappings),
		InstanceMethod("LinkFile", &USVFS::linkFile),
		InstanceMethod("LinkDirectoryStatic", &USVFS::linkDirectoryStatic),
		InstanceMethod("SpawnSync", &USVFS::spawnSync),
		InstanceMethod("Spawn", &USVFS::spawn),
		InstanceMethod("Disconnect", &USVFS::disconnect),
	});

	constructor = Napi::Persistent(func);
	constructor.SuppressDestruct();

	exports.Set("USVFS", func);
	return exports;
}

USVFS::USVFS(const Napi::CallbackInfo& info) : Napi::ObjectWrap<USVFS>(info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	int length = info.Length();

	if (length <= 0 || (! info[0].IsString() && ! info[0].IsObject())) {
		Napi::TypeError::New(env, "USVFS only accepts a instanceName or a parameters object").ThrowAsJavaScriptException();
	}

	const char* instanceName;
	bool debugMode = false;
	LogLevel logLevel = LogLevel::Info;
	CrashDumpsType crashDumpsType = CrashDumpsType::None;
	const char* crashDumpsPath = "";

	Napi::Value arg0 = info[0];

	if (arg0.IsString()) {
		instanceName = arg0.As<Napi::String>().Utf8Value().c_str();
	} else {
		Napi::Object params = arg0.As<Napi::Object>();
		Napi::Value tmp;

		// get instanceName property
		if (! params.Has("instanceName"))
		 Napi::TypeError::New(env, "params must contain the instanceName property").ThrowAsJavaScriptException();

		tmp = params.Get("instanceName");

		if (! tmp.IsString())
			Napi::TypeError::New(env, "instanceName must be a string").ThrowAsJavaScriptException();

		instanceName = tmp.As<Napi::String>().Utf8Value().c_str();

		// get debugMode property
		if (params.Has("debugMode")) {
			tmp = params.Get("debugMode");

			if (! tmp.IsBoolean())
				Napi::TypeError::New(env, "debugMode must be a boolean").ThrowAsJavaScriptException();

			debugMode = tmp.As<Napi::Boolean>().Value();
		}

		// get logLevel property
		if (params.Has("logLevel")) {
			tmp = params.Get("logLevel");

			if (! tmp.IsNumber())
				Napi::TypeError::New(env, "logLevel must be a number").ThrowAsJavaScriptException();

			int level = tmp.As<Napi::Number>().Int32Value();

			if (level < 0 || level > 3)
				Napi::RangeError::New(env, "logLevel must be between 0 and 3").ThrowAsJavaScriptException();

			switch (level) {
			case 0:
				logLevel = LogLevel::Error;
				break;
			case 1:
				logLevel = LogLevel::Warning;
				break;
			case 2:
				logLevel = LogLevel::Info;
				break;
			case 3:
				logLevel = LogLevel::Debug;
				break;
			}
		}

		// get crashDumpsType and crashDumpsPath properties
		if (params.Has("crashDumpsType")) {
			tmp = params.Get("crashDumpsType");

			if (! tmp.IsNumber())
				Napi::TypeError::New(env, "crashDumpsType must be a number");

			int type = tmp.As<Napi::Number>().Int32Value();

			if (type < 0 || type > 4)
				Napi::RangeError::New(env, "crashDumpsType must be between 0 and 3");

			switch (type) {
			case 0:
				crashDumpsType = CrashDumpsType::None;
				break;
			case 1:
				crashDumpsType = CrashDumpsType::Mini;
				break;
			case 2:
				crashDumpsType = CrashDumpsType::Data;
				break;
			case 3:
				crashDumpsType = CrashDumpsType::Full;
				break;
			}

			if (crashDumpsType != CrashDumpsType::None) {
				if (! params.Has("crashDumpsPath"))
					Napi::Error::New(env, "params must specifiy a crashDumpsPath when crashDumpsType is not none")
						.ThrowAsJavaScriptException();

				tmp = params.Get("crashDumpsPath");

				if (! tmp.IsString())
					Napi::TypeError::New(env, "crashDumpsPath must be a string");

				crashDumpsPath = tmp.As<Napi::String>().Utf8Value().c_str();
			}
		}
	}

	USVFSInitParameters(&this->params_, instanceName, debugMode, logLevel, crashDumpsType, crashDumpsPath);

	bool worked;

	worked = CreateVFS(&this->params_);

	if (! worked)
		Napi::Error::New(env, "Failed to create new VFS").ThrowAsJavaScriptException();
}

Napi::Value USVFS::clearMappings(const Napi::CallbackInfo& info) {
	ClearVirtualMappings();

	return info.This();
}

Napi::Value USVFS::linkFile(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	int length = info.Length();

	if (length < 2)
		Napi::Error::New(env, "USVFS#LinkFile requires a source and destination").ThrowAsJavaScriptException();

	if (! info[0].IsString())
		Napi::TypeError::New(env, "source must be a string").ThrowAsJavaScriptException();

	if (! info[1].IsString())
		Napi::TypeError::New(env, "dest must be a string").ThrowAsJavaScriptException();

	LPWSTR source = stringToLPWSTR(info[0].As<Napi::String>().Utf8Value().c_str());
	LPWSTR dest = stringToLPWSTR(info[1].As<Napi::String>().Utf8Value().c_str());
	unsigned int flags = NULL;

	if (length > 2) {
		if (! info[2].IsNumber())
			Napi::TypeError::New(env, "flags must be a number");

		flags = info[2].As<Napi::Number>().Int32Value();
	}

	bool worked = VirtualLinkFile(source, dest, flags);

	return Napi::Boolean::New(env, worked);
}

Napi::Value USVFS::linkDirectoryStatic(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);

	int length = info.Length();

	if (length < 2)
		Napi::Error::New(env, "USVFS#LinkDirectoryStatic requires a source and destination").ThrowAsJavaScriptException();

	if (! info[0].IsString())
		Napi::TypeError::New(env, "source must be a string").ThrowAsJavaScriptException();

	if (! info[1].IsString())
		Napi::TypeError::New(env, "dest must be a string").ThrowAsJavaScriptException();

	LPWSTR source = stringToLPWSTR(info[0].As<Napi::String>().Utf8Value().c_str());
	LPWSTR dest = stringToLPWSTR(info[1].As<Napi::String>().Utf8Value().c_str());
	unsigned int flags = NULL;

	if (length > 2) {
		if (! info[2].IsNumber())
			Napi::TypeError::New(env, "flags must be a number");

		flags = info[2].As<Napi::Number>().Int32Value();
	}

	bool worked = VirtualLinkDirectoryStatic(source, dest, flags);

	return Napi::Boolean::New(env, worked);
}

Napi::Value USVFS::disconnect(const Napi::CallbackInfo& info) {
	DisconnectVFS();

	return info.This();
}

Napi::Value USVFS::spawnSync(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);
	SpawnOptions options;

	// get arguments
	int length = info.Length();

	if (length < 1)
		Napi::Error::New(env, "USVFS#SpawnSync requires a command").ThrowAsJavaScriptException();

	if (! info[0].IsString())
		Napi::TypeError::New(env, "command must be a string").ThrowAsJavaScriptException();

	if (length > 1) {
		if (info[1].IsObject()) options = getSpawnOptions(env, info[1].As<Napi::Object>());
		else Napi::Error::New(env, "SpawnSync only accepts spawn options").ThrowAsJavaScriptException();
	}

	// spawn process
	STARTUPINFO si;
	PROCESS_INFORMATION pi;

	bool worked = spawnHookedProcess(info[0].As<Napi::String>(), options, &si, &pi);

	if (! worked)
		throwLastError(env, "USVFS::SpawnSync failed (%d)");

	// wait for process to exit
	WaitForSingleObject(pi.hProcess, INFINITE);

	// close handles
	CloseHandle(pi.hProcess);
	CloseHandle(pi.hThread);

	return Napi::Value();
}

Napi::Value USVFS::spawn(const Napi::CallbackInfo& info) {
	Napi::Env env = info.Env();
	Napi::HandleScope scope(env);
	SpawnOptions options;

	bool hasCallback = false;
	Napi::Function callback;

	LPWSTR command;

	// get arguments
	int length = info.Length();

	if (length < 1)
		Napi::Error::New(env, "USVFS#Spawn requires a command").ThrowAsJavaScriptException();

	if (! info[0].IsString())
		Napi::TypeError::New(env, "command must be a string");

	if (length > 1) {
		if (info[1].IsFunction()) {
			hasCallback = true;
			callback = info[1].As<Napi::Function>();
		} else if(info[1].IsObject()) options = getSpawnOptions(env, info[1].As<Napi::Object>());
		else Napi::Error::New(env, "Spawn only accepts spawn options and or a callback").ThrowAsJavaScriptException();
	}

	if (length > 2) {
		if (info[2].IsFunction()) {
			hasCallback = true;
			callback = info[2].As<Napi::Function>();
		} else if(info[2].IsObject()) options = getSpawnOptions(env, info[2].As<Napi::Object>());
		else Napi::Error::New(env, "Spawn only accepts spawn options and or a callback").ThrowAsJavaScriptException();
	}

	command = stringToLPWSTR(info[0].As<Napi::String>().Utf8Value().c_str());

	// spawn process
	STARTUPINFO si;
	PROCESS_INFORMATION pi;

	bool worked = spawnHookedProcess(info[0].As<Napi::String>(), options, &si, &pi);

	if (! worked)
		throwLastError(env, "USVFS::SpawnSync failed (%d)");

	// wait for process to exit
	if (hasCallback) {
		HANDLE waitHandle;
		ThreadSafeCallback* ts_cb = new ThreadSafeCallback(callback);

		WAITORTIMERCALLBACK onExit = [](void* vPtr, BOOLEAN timedOut) {
			ThreadSafeCallback* ts_cb = static_cast<ThreadSafeCallback*>(vPtr);

			ts_cb->call();

			delete ts_cb;
		};

		RegisterWaitForSingleObject(&waitHandle, pi.hProcess, onExit, ts_cb, INFINITE, WT_EXECUTEONLYONCE);
	}

	// close handles
	CloseHandle(pi.hProcess);
	CloseHandle(pi.hThread);

	return info.This();
}

} // namespace node_usvfs
