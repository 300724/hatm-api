code:
	autoflake src -r --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --in-place --recursive
	black src
	isort src
	pylint --extension-pkg-whitelist='pydantic' src
