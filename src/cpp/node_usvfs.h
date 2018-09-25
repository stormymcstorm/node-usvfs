#pragma once

#define NAPI_VERSION 3

#include <napi.h>
#include <usvfs.h>
#include <usvfsparameters.h>
#include "napi-thread-safe-callback.hpp"

namespace node_usvfs {

class USVFS : public Napi::ObjectWrap<USVFS> {
	public:
		static Napi::Object Init(Napi::Env env, Napi::Object exports);
		USVFS(const Napi::CallbackInfo& info);

	private:
		static Napi::FunctionReference constructor;

		Napi::Value clearMappings(const Napi::CallbackInfo& info);
		Napi::Value linkFile(const Napi::CallbackInfo& info);
		Napi::Value linkDirectoryStatic(const Napi::CallbackInfo& info);
		Napi::Value disconnect(const Napi::CallbackInfo& info);
		Napi::Value spawnSync(const Napi::CallbackInfo& info);
		Napi::Value spawn(const Napi::CallbackInfo& info);

		USVFSParameters params_;
};

} // namespace node_usvfs
