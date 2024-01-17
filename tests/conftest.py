from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database import engine, Base
from app.main import app

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(scope="session")
def db():
    yield TestingSessionLocal()


@pytest.fixture(scope="session")
def client(db) -> Generator:
    try:
        TestClient(app)
        yield TestClient(app)
    finally:
        db.close()