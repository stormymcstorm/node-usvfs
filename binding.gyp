{
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
				"./src/binding.gyp:<(module_name)",
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
					"<(PRODUCT_DIR)/usvfs_x64.dll",
					"<(PRODUCT_DIR)/usvfs_x64.lib"
				],
				"destination": "<(module_path)"
				}
			]
		},
	]
}
