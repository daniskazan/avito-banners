lint:
	ruff check --fix
	ruff format ./src && ruff format ./tests
