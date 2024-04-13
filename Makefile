
docker_compose_path = "docker-compose.local.yaml"


lint:
	ruff check --fix
	ruff format ./src && ruff format ./tests
test:
	docker exec -it api-banner-local cd .. && pytest

dc-up:
	docker compose -f $(docker_compose_path) up -d
dc-down:
	docker compose -f $(docker_compose_path) down