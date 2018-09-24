{
	"target_defaults": {
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
		},
	},

	"targets": [
		# build asmjit
		{
			"target_name": "asmjit",
			"type": "static_library",
			"defines": [
				"ASMJIT_STATIC",
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/asmjit/src/asmjit"
			],
			"sources": [
				"usvfs/asmjit/src/asmjit/base/assembler.cpp",
				"usvfs/asmjit/src/asmjit/base/compiler.cpp",
				"usvfs/asmjit/src/asmjit/base/compilercontext.cpp",
				"usvfs/asmjit/src/asmjit/base/constpool.cpp",
				"usvfs/asmjit/src/asmjit/base/containers.cpp",
				"usvfs/asmjit/src/asmjit/base/cpuinfo.cpp",
				"usvfs/asmjit/src/asmjit/base/globals.cpp",
				"usvfs/asmjit/src/asmjit/base/hlstream.cpp",
				"usvfs/asmjit/src/asmjit/base/logger.cpp",
				"usvfs/asmjit/src/asmjit/base/operand.cpp",
				"usvfs/asmjit/src/asmjit/base/podvector.cpp",
				"usvfs/asmjit/src/asmjit/base/runtime.cpp",
				"usvfs/asmjit/src/asmjit/base/utils.cpp",
				"usvfs/asmjit/src/asmjit/base/vmem.cpp",
				"usvfs/asmjit/src/asmjit/base/zone.cpp",
				"usvfs/asmjit/src/asmjit/x86/x86assembler.cpp",
				"usvfs/asmjit/src/asmjit/x86/x86compiler.cpp",
				"usvfs/asmjit/src/asmjit/x86/x86compilercontext.cpp",
				"usvfs/asmjit/src/asmjit/x86/x86compilerfunc.cpp",
				"usvfs/asmjit/src/asmjit/x86/x86inst.cpp",
				"usvfs/asmjit/src/asmjit/x86/x86operand.cpp",
				"usvfs/asmjit/src/asmjit/x86/x86operand_regs.cpp"
			],
		},

		# build fmt
		{
			"target_name": "fmt",
			"type": "static_library",
			"defines": [
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/fmt"
			],
			"sources": [
				"usvfs/fmt/fmt/format.cc",
				"usvfs/fmt/fmt/ostream.cc",
				"usvfs/fmt/fmt/posix.cc",
				"usvfs/fmt/fmt/printf.cc"
			],
		},

		# build spdlog
		{
			"target_name": "spdlog",
			"type": "static_library",
			"defines": [
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/spdlog/include/spdlog"
			],
			"sources": [],
		},

		# build udis86
		{
			"target_name": "udis86",
			"type": "static_library",
			"defines": [
				"_WINDOWS",
				"NDEBUG",
				"BOOST_CONFIG_SUPPRESS_OUTDATED_MESSAGE"
			],
			"include_dirs": [
				"usvfs/udis86"
			],
			"sources": [
				"usvfs/udis86/libudis86/decode.c",
				"usvfs/udis86/libudis86/itab.c",
				"usvfs/udis86/libudis86/syn-att.c",
				"usvfs/udis86/libudis86/syn-intel.c",
				"usvfs/udis86/libudis86/syn.c",
				"usvfs/udis86/libudis86/udis86.c"
			],
		},
	]
}
