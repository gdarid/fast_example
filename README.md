# FastAPI example

This is a basic FastAPI application 

# Starting the server

The server can be started, in development mode, with reload option

``` bash
uv run uvicorn app.main:app --reload
```

Once the application is running, some documentation is available :
- [Swagger documentation](http://localhost:8000/docs)
- [Redoc documentation](http://localhost:8000/redoc)

# Simple requests

Here’s a set of simple curl examples you can use to interact with the application once it’s running (default at http://localhost:8000):

- Create a User

curl -X POST "http://localhost:8000/api/v1/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "Ada Lovelace"}'


- Get All Users

curl -X GET "http://localhost:8000/api/v1/users"


- Get a User by ID

(Replace 1 with the actual ID from the create response)

curl -X GET "http://localhost:8000/api/v1/users/1"


- Update a User

curl -X PUT "http://localhost:8000/api/v1/users/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "Grace Hopper"}'


- Delete a User

curl -X DELETE "http://localhost:8000/api/v1/users/1"

# Tests

Simple tests can be launched (pytest)

``` bash
pytest .
```

The tests can also be launched with coverage

``` bash
pytest --cov=.
```

The tests can be launched with coverage and a report in HTML

``` bash
pytest --cov=. --cov-report html
```
