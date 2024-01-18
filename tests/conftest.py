from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.database import engine, Base
from app.oauth2 import create_access_token
from app.main import app

from app.schemas import UserResponse
from datetime import datetime
from faker import Faker

# from alembic import command
# from alembic.config import Config

# Load the Alembic configuration
# alembic_cfg = Config("../alembic.ini")

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

# Show Tables
# for table in reversed(Base.metadata.sorted_tables):
#    print(table)


@pytest.fixture(scope="session")
def db_session() -> Generator:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # command.upgrade(alembic_cfg, "base")
    # command.upgrade(alembic_cfg, "head")

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def client(db_session) -> Generator:
    yield TestClient(app)


TEST_USER_SIGNUP = {
    "email": Faker().company_email(),
    "password": Faker().password(length=25),
}


@pytest.fixture(scope="session")
def create_user(client):
    # Create User
    print(f"Creating User: {TEST_USER_SIGNUP=}")
    response = client.post("/users", json=TEST_USER_SIGNUP)
    assert response.status_code == 201

    user_response = UserResponse(**response.json())
    assert user_response.email == TEST_USER_SIGNUP["email"]
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)

    return response


@pytest.fixture(scope="function")
def create_user_return_create_access_token(create_user):
    response = create_user
    user_response = UserResponse(**response.json())

    assert response.status_code == 201
    assert user_response.email == TEST_USER_SIGNUP["email"]
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)

    # Create access Token
    user_data = {
        "user_email": user_response.email,
        "user_id": user_response.id,
    }

    token_data = create_access_token(data=user_data)
    assert token_data is not None

    print(f"{token_data=}")
    return token_data


@pytest.fixture(scope="function")
def create_user_return_header_with_access_token(create_user_return_create_access_token):
    # Create test user and get token
    token_data = create_user_return_create_access_token

    # Create header / payload
    headers = {}
    headers["Authorization"] = "Bearer " + token_data

    return headers
