lint:
	ruff check --fix
	ruff format ./src && ruff format ./tests

dc-up:
	docker compose -f "docker-compose.local.yaml" up -d