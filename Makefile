code:
	# ===========================================================
	autoflake hatm -r --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --in-place --recursive
	# ===========================================================
	black hatm
	# ===========================================================
	isort hatm
	# ===========================================================
	pylint --extension-pkg-whitelist='pydantic' hatm
