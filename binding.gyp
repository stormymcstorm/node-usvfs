{
	"targets": [
		{
			"target_name": "<(module_name)",
			"cflags!": [ "-fno-exceptions" ],
      "cflags_cc!": [ "-fno-exceptions" ],
			"dependencies": [
				"./deps/deps.gyp:usvfs_x64",
				"<!(node -p \"require('node-addon-api').gyp\")"
			],
			"defines": [
				"BUILDING_USVFS_DLL",
				"ASMJIT_STATIC",
				"SPDLOG_NO_NAME",
				"SPDLOG_NO_REGISTRY_MUTEX",
				"NOMINMAX",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE",
				"NAPI_CPP_EXCEPTIONS",
				"_HAS_EXCEPTIONS=1"
			],
			"libraries": [
				"Shlwapi.lib",
				"Version.lib",
				"../deps/boost/stage/lib/libboost_atomic-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_atomic-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_chrono-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_chrono-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_context-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_context-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_coroutine-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_coroutine-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_date_time-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_date_time-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_filesystem-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_filesystem-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_locale-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_locale-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_log-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_log-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_log_setup-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_log_setup-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_regex-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_regex-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_system-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_system-vc141-mt-sgd-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_thread-vc141-mt-s-x64-1_67.lib",
				"../deps/boost/stage/lib/libboost_thread-vc141-mt-sgd-x64-1_67.lib"
			],
			"include_dirs": [
				"<!@(node -p \"require('node-addon-api').include\")",
				"<!@(node -p \"require('napi-thread-safe-callback').include\")",
				"src",
				"deps/usvfs/include",
				"deps/usvfs/src/usvfs_dll",
				"deps/usvfs/src/shared",
				"deps/usvfs/src/thooklib",
				"deps/usvfs/src/tinjectlib",
				"deps/usvfs/src/usvfs_helper",
				"deps/usvfs/asmjit/src/asmjit",
				"deps/usvfs/udis86",
				"deps/boost",
				"deps/usvfs/fmt",
				"deps/usvfs/spdlog/include/spdlog"
			],
			"sources": [
				"src/node_usvfs.cc",
				"src/bindings.cc"
			],
			"configurations": {
				"Release": {
					"msvs_settings": {
						"VCCLCompilerTool": {
							"ExceptionHandling": 1,
							"RuntimeTypeInfo": "true"
						}
					},
					"msvs_configuration_attributes": {
						"CharacterSet": 1
					},
					"msbuild_toolset": "v141",
					"msvs_windows_target_platform_version": "10.0.16299.0"
				}
			}
		},
		{
			"target_name": "action_after_build",
			"type": "none",
			"dependencies": [ "<(module_name)" ],
			"copies": [
				{
				"files": [
					"<(PRODUCT_DIR)/<(module_name).node",
					"<(PRODUCT_DIR)/usvfs_x64.dll",
					"<(PRODUCT_DIR)/usvfs_x64.lib"
				],
				"destination": "<(module_path)"
				}
			]
		},
	]
}
