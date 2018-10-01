{
	"variables": {
		"boost_dir": "<!(node -p \"process.env.BOOST_LIB || '../../../deps/boost/stage/lib'\")",

		"conditions": [
			["target_arch=='x64'", {
				"arch": "x64",
			}],
			["target_arch=='ia32'", {
				"arch": "x32",
			}],
		],
	},

	"targets": [
		{
			"target_name": "build_deps",
			"actions": [
				{
					"action_name": "get_build_deps",
					"inputs": [],
					"outputs": [""],
					"action": ["node", "./get_build_deps.js"],
					"message": "Getting build dependencies"
				}
			],
		},
		{
			"target_name": "<(module_name)",
			"dependencies": [
				"build_deps",
				"./src/cpp/module.gyp:<(module_name)",
			],
		},
		{
			"target_name": "action_after_build",
			"type": "none",
			"dependencies": [ "<(module_name)" ],
			"copies": [
				{
				"files": [
					"<(PRODUCT_DIR)/<(module_name).node",
					"<(PRODUCT_DIR)/usvfs.dll",
					"<(PRODUCT_DIR)/usvfs.lib"
				],
				"destination": "<(module_path)"
				}
			]
		},
	]
}
