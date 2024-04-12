lint:
	ruff check --fix
	ruff format ./src && ruff format ./tests
test:
	docker exec -it api-banner-local cd .. && pytest
dc-up:
	docker compose -f "docker-compose.local.yaml" up -d