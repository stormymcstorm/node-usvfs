{
	"variables": {
		"boost_dir": "<!(node -p \"process.env.BOOST_LIB || '../../deps/boost/stage/lib'\")",

		"conditions": [
			["target_arch=='x64'", {
				"arch": "x64",
			}],
			["target_arch=='ia32'", {
				"arch": "x32",
			}],
		],
	},

	"target_defaults": {
		"libraries": [
			"Shlwapi.lib",
			"Version.lib",
			"<(boost_dir)/libboost_atomic-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_atomic-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_chrono-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_chrono-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_context-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_context-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_coroutine-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_coroutine-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_date_time-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_date_time-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_filesystem-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_filesystem-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_locale-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_locale-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_log-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_log-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_log_setup-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_log_setup-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_regex-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_regex-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_system-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_system-vc141-mt-sgd-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_thread-vc141-mt-s-<(arch)-1_67.lib",
			"<(boost_dir)/libboost_thread-vc141-mt-sgd-<(arch)-1_67.lib"
		],
	},

	"targets": [
		# build shared
		{
			"target_name": "shared",
			"type": "static_library",
			"dependencies": [
				"./usvfs_deps.gyp:fmt",
				"./usvfs_deps.gyp:spdlog"
			],
			"defines": [
				"_WIN64",
				"SPDLOG_NO_NAME",
				"SPDLOG_NO_REGISTRY_MUTEX",
				"NOMINMAX",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/src/shared",
				"usvfs/include",
				"<(boost_dir)",
				"usvfs/fmt",
				"usvfs/spdlog/include/spdlog"
			],
			"sources": [
				"usvfs/src/shared/addrtools.cpp",
				"usvfs/src/shared/debug_monitor.cpp",
				"usvfs/src/shared/directory_tree.cpp",
				"usvfs/src/shared/exceptionex.cpp",
				"usvfs/src/shared/loghelpers.cpp",
				"usvfs/src/shared/ntdll_declarations.cpp",
				"usvfs/src/shared/scopeguard.cpp",
				"usvfs/src/shared/shmlogger.cpp",
				"usvfs/src/shared/stringcast_win.cpp",
				"usvfs/src/shared/stringutils.cpp",
				"usvfs/src/shared/test_helpers.cpp",
				"usvfs/src/shared/unicodestring.cpp",
				"usvfs/src/shared/wildcard.cpp",
				"usvfs/src/shared/winapi.cpp",
				"usvfs/src/shared/windows_error.cpp"
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

		# build thooklib
		{
			"target_name": "thooklib",
			"type": "static_library",
			"dependencies": [
				"./usvfs_deps.gyp:asmjit",
				"shared",
				"./usvfs_deps.gyp:spdlog"
			],
			"defines": [
				"_WIN64",
				"ASMJIT_STATIC",
				"SPDLOG_NO_NAME",
				"SPDLOG_NO_REGISTRY_MUTEX",
				"NOMINMAX",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/src/thooklib",
				"usvfs/src/shared",
				"usvfs/src/tinjectlib",
				"usvfs/src/usvfs_helper",
				"usvfs/asmjit/src/asmjit",
				"usvfs/udis86",
				"usvfs/include",
				"<(boost_dir)",
				"usvfs/fmt",
				"usvfs/spdlog/include/spdlog"
			],
			"sources": [
				"usvfs/src/thooklib/hooklib.cpp",
				"usvfs/src/thooklib/ttrampolinepool.cpp",
				"usvfs/src/thooklib/udis86wrapper.cpp",
				"usvfs/src/thooklib/utility.cpp"
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

		# build tinjectlib
		{
			"target_name": "tinjectlib",
			"type": "static_library",
			"dependencies": [
				"./usvfs_deps.gyp:asmjit",
				"shared"
			],
			"defines": [
				"_WIN64",
				"ASMJIT_STATIC",
				"SPDLOG_NO_NAME",
				"SPDLOG_NO_REGISTRY_MUTEX",
				"NOMINMAX",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/src/tinjectlib",
				"usvfs/src/shared",
				"usvfs/src/thooklib",
				"usvfs/src/usvfs_helper",
				"usvfs/asmjit/src/asmjit",
				"usvfs/udis86",
				"usvfs/include",
				"<(boost_dir)",
				"usvfs/fmt",
				"usvfs/spdlog/include/spdlog"
			],
			"sources": [
				"usvfs/src/tinjectlib/injectlib.cpp"
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

		# usvfs_helper
		{
			"target_name": "usvfs_helper",
			"type": "static_library",
			"dependencies": [
				"shared",
				"tinjectlib"
			],
			"defines": [
				"BUILDING_USVFS_DLL",
				"_WIN64",
				"ASMJIT_STATIC",
				"SPDLOG_NO_NAME",
				"SPDLOG_NO_REGISTRY_MUTEX",
				"NOMINMAX",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/src/usvfs_helper",
				"usvfs/src/shared",
				"usvfs/src/thooklib",
				"usvfs/src/tinjectlib",
				"usvfs/asmjit/src/asmjit",
				"usvfs/udis86",
				"usvfs/include",
				"<(boost_dir)",
				"usvfs/fmt",
				"usvfs/spdlog/include/spdlog"
			],
			"sources": [
				"usvfs/src/usvfs_helper/inject.cpp"
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

		# usvfs
		{
			"target_name": "usvfs",
			"type": "shared_library",
			"dependencies": [
				"./usvfs_deps.gyp:asmjit",
				"./usvfs_deps.gyp:fmt",
				"shared",
				"./usvfs_deps.gyp:spdlog",
				"thooklib",
				"tinjectlib",
				"./usvfs_deps.gyp:udis86",
				"usvfs_helper"
			],
			"defines": [
				"BUILDING_USVFS_DLL",
				"ASMJIT_STATIC",
				"SPDLOG_NO_NAME",
				"SPDLOG_NO_REGISTRY_MUTEX",
				"NOMINMAX",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/include",
				"usvfs/src/usvfs_dll",
				"usvfs/src/shared",
				"usvfs/src/thooklib",
				"usvfs/src/tinjectlib",
				"usvfs/src/usvfs_helper",
				"usvfs/asmjit/src/asmjit",
				"usvfs/udis86",
				"<(boost_dir)",
				"usvfs/fmt",
				"usvfs/spdlog/include/spdlog"
			],
			"sources": [
				"usvfs/src/usvfs_dll/hookcallcontext.cpp",
				"usvfs/src/usvfs_dll/hookcontext.cpp",
				"usvfs/src/usvfs_dll/hookmanager.cpp",
				"usvfs/src/usvfs_dll/hooks/kernel32.cpp",
				"usvfs/src/usvfs_dll/hooks/ntdll.cpp",
				"usvfs/src/usvfs_dll/redirectiontree.cpp",
				"usvfs/src/usvfs_dll/semaphore.cpp",
				"usvfs/src/usvfs_dll/stringcast_boost.cpp",
				"usvfs/src/usvfs_dll/usvfs.cpp"
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

		# usvfs_proxy
		{
			"target_name": "usvfs_proxy",
			"type": "executable",
			"dependencies": [
				"./usvfs_deps.gyp:asmjit",
				"shared",
				"tinjectlib",
				"usvfs",
				"usvfs_helper"
			],
			"defines": [
				"_WIN64",
				"ASMJIT_STATIC",
				"SPDLOG_NO_NAME",
				"SPDLOG_NO_REGISTRY_MUTEX",
				"NOMINMAX",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/src/shared",
				"usvfs/src/thooklib",
				"usvfs/src/tinjectlib",
				"usvfs/src/usvfs_helper",
				"usvfs/asmjit/src/asmjit",
				"usvfs/udis86",
				"usvfs/include",
				"<(boost_dir)",
				"usvfs/fmt",
				"usvfs/spdlog/include/spdlog"
			],
			"sources": [
				"usvfs/src/usvfs_proxy/main.cpp"
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
	]
}
