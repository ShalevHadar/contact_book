# Phone Contact API

A simple phone book API built with Python, FastAPI, and Postgres.


## Features

- **CRUD operations**: Create, read (with pagination), update, and delete contacts.
- **Search**: Query contacts by phone number
- **Pagination**: Lists contacts 10 per page.
- **Scale**: Asynchronous routes and handlers for concurrency and not blocking threadpool.
- **Logging**: Logs to stdout and file.
- **Dockerized**: Easily run the app and database with Docker Compose.

## API documentation

`http://localhost:8000/docs`

![hi](https://i.ibb.co/qYMc2RVJ/Screenshot-2025-02-22-at-21-57-06.png)

## Technologies

- Python, FastAPI, SQLAlchemy
- Postgres database
- Docker & Docker Compose

## Setup - Server

1. Clone the repository
2. Make sure you got Docker and Docker Compose installed
2. Fill in the environment variables in `server/.env`
3. cd in terminal `cd server`
4. run in terminal `docker-compose build --no-cache && docker-compose up`

## Client

FastAPI provides a built-in web-based interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## Testing

- Run `docker-compose exec server pytest` to run the tests.

## Resources

- https://github.com/zhanymkanov/fastapi-best-practices
- https://fastapi.tiangolo.com/
- https://www.sqlalchemy.org/
- https://www.postgresql.org/
- https://www.docker.com/
- https://docs.pytest.org/en/stable/

## TODO

- CRUD - Done
- Search by all args - Done
- Logging - Done
- E2E tests - Done


## Additional Improvements

- Add cacheing for repeating requests
- Failing Tests (HTTP variant responses)
- Authentication (middleware tokens) & Security (Server-to-Server validation)
- Phone number validation (According to Country)
- UI (frontend)
- Linter
- CI/CD
- Metrics
- Monitoring
- Manage Shell-oriented subprocesses using pyinvoke
- More validation for input and output
- Profiling and performance tuning
- Async routes (giving up on threadpool and using event loop)
