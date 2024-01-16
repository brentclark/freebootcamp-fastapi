from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

from app.oauth2 import create_access_token
from app.config import settings
from app.database import engine, Base
from app.schemas import UserResponse
from app.main import app
from datetime import datetime

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def is_valid_email(email):
    import re

    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


@pytest.mark.parametrize(
    ("email", "password", "status"),
    ((Faker().company_email(), Faker().password(length=25), 201),),
)
def test_create_user(email, password, status):
    response = client.post(
        "/users",
        json={"email": email, "password": password},
    )
    user_response = UserResponse(**response.json())

    assert response.status_code == status
    assert user_response.email == email
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)


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
    print(response.json())

    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") is not None
    assert response.json().get("created_at") is not None

    user_response = UserResponse(**response.json())
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)
    assert (
        is_valid_email(user_response.email) != None
    ), f"Expected {user_response.email}, i.e. Does not match"

