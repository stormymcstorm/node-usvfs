#include <napi.h>
#include <node_usvfs.h>

Napi::Object Init(Napi::Env env, Napi::Object exports) {
	return node_usvfs::USVFS::Init(env, exports);
}

NODE_API_MODULE(NODE_GYP_MODULE_NAME, Init);
