## Stack: FastAPI, PostgreSQL

## Cтруктура проекта
```
src
|-api
|    |
     v1
     |
     banners
|    |   |-serializers(схема входных и выходных данных)
|    |   |-controllers(ручки)
|    |   |-dependencies(Depends которые относятся ко всему что связано с баннерами)
|    | - auth_exceptions.py - ошибки авторизации
|    | - routing.py - Настройка роутера
|
| --- configs - настройки
| --- service - сервисы( слой логики, вызовы репозитория
| --- storages - операции с хранилищами/БД
| --- utils
|        | - generic_reponse - дженерик модель ответа от сервера. удобно использовать + можно документировать OpenAPI передавая в response_model=OkResponse[MyResponseModel]
| --- main.py - asgi-app
| - tests
```

## Benchmark
```
Тестировалось на 150 параллельных подключениях 60s и 5 воркерах(uvicorn)
```

![](./docs/imgs/benchmarks.png)


## Makefile
```shell
make lint - runs ruff linter
make test - runs tests
make dc-up  - serves the app
make fill-db - creates samples of features and tags
```

# Примеры запросов
```shell

curl -X 'POST' \
  'http://localhost:8000/api/v1/banners/banner' \
  -H 'accept: application/json' \
  -H 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.7DXwNbHtZoPUCoGv_Odt-jIOY2bBJDhBJeZKwpWCvCM' \
  -H 'Content-Type: application/json' \
  -d '{
  "tagIds": [
    1
  ],
  "featureId": 1,
  "content": {},
  "isActive": false
}'
```
```shell
Response
{
  "statusCode": 201,
  "payload": {
    "bannerId": 11
  }
}
```