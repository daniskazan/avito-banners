
docker_compose_path = "docker-compose.local.yaml"


lint:
	ruff check --fix
	ruff format ./src && ruff format ./tests
test:
	docker exec -it api-banner-local sh -c "cd .. && pytest"


dc-up:
	docker compose -f $(docker_compose_path) up -d
dc-down:
	docker compose -f $(docker_compose_path) down


## Db init
insert-data:
	docker exec -it pg-banner-local psql -U banner -d banner -c "INSERT INTO tags (tag_name) VALUES ('tag1'), ('tag2');INSERT INTO features (feature_name) VALUES ('feature1'), ('feature2');"
show-data:
	docker exec -it pg-banner-local psql -U banner -d banner -c "SELECT * FROM banners;"
	docker exec -it pg-banner-local psql -U banner -d banner -c "SELECT * FROM features;"
fill-db:
	make insert-data
	make show-data