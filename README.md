# Phone Contact API

A simple phone book API built with Python, FastAPI, and Postgres.

## How to run the project

1. Clone the repository
2. Cd into the project directory
3. Run `cp .env.example .env`
3. Run `docker-compose up --build`
4. Visit `http://localhost:8000/api/v1/docs` to view the API documentation
5. To run tests, run `docker-compose exec web pytest`

## Key Features 

## 🚀 Features
- **RESTful API** with FastAPI  
- **Manage Contacts** (Create, Read, Update, Delete, Pagination)  
- **Search contacts** by phone number or full name  
- **Pagination** for retrieving contacts efficiently  
- **Validation & Error Handling** using Pydantic  
- **Database Layer** with SQLModel & AsyncSession  
- **Tested** (Unit & Integration Tests)   
- **Dockerized Setup** for easy deployment  
- **Mocked Tests** for API, Service, and Database layers  
- **Asynchronous** implementation for high performance

## 🛠️ Tech Stack
- **Framework**: FastAPI
- **Database**: PostgresSQL
- **ORM**: SQLAlchemy, SQLModel, Alembic
- **API Testing**: Pytest, Requests
- **API Documentation**: Swagger UI, ReDoc
- **Containerization**: Docker, Docker Compose
- **Linting**: Ruff