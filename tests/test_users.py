from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from app.oauth2 import create_access_token
from app.config import settings
from app.database import engine, Base

# from app.db.base import Base
# from app.db.session import SessionLocal
from app.main import app

# engine = create_engine(  # noqa
#    f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DATABASE}?charset=utf8mb4",
# )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


# @pytest.fixture(scope="function")
# def db():
#    yield SessionLocal()
#
#
# @pytest.fixture(scope="function")
# def client(db) -> Generator:
#    try:
#        TestClient(app)
#        yield TestClient(app)
#    finally:
#        db.close()


def test_create_user():
    faker = Faker()
    response = client.post(
        "/users",
        json={"email": faker.company_email(), "password": faker.password(length=25)},
    )
    assert response.status_code == 201


def test_get_users():
    response = client.get(
        "/users",
    )
    assert response.status_code == 200
    print(response.json())

def test_get_user_with_id_1():
    response = client.get(
        "/users/1",
    )
    assert response.status_code == 200
    assert response.json().get('id') == 1
    assert response.json().get('email') is not None
    assert response.json().get('created_at') is not None
    print(response.json())
