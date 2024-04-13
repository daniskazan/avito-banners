
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
	docker exec -it pg-banner-local psql -U banner -d banner -c "INSERT INTO tags (tag_name) VALUES (substr(md5(random()::text), 1, 10)), (substr(md5(random()::text), 1, 10));INSERT INTO features (feature_name) VALUES (substr(md5(random()::text), 1, 10)), (substr(md5(random()::text), 1, 10));"
show-data:
	docker exec -it pg-banner-local psql -U banner -d banner -c "SELECT * FROM banners;"
	docker exec -it pg-banner-local psql -U banner -d banner -c "SELECT * FROM features;"
fill-db:
	make insert-data
	make show-data