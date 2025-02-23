import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from contact_book.src.models import Base
from contact_book.src.main import app

TEST_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import contact_book.shared.database as database_module
database_module.engine = engine
database_module.SessionLocal = TestingSessionLocal  # Override session

@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Ensures fresh DB for each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def override_get_db_fixture(setup_test_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture
def client(override_get_db_fixture):
    app.dependency_overrides[get_db] = lambda: override_get_db_fixture
    return TestClient(app)

# Correctly override the FastAPI dependency
from contact_book.src.api.v1.endpoints.contacts import get_db
app.dependency_overrides[get_db] = lambda: override_get_db_fixture()

