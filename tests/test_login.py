from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
from faker import Faker

from app.schemas import UserResponse, Token

TEST_USER_SIGNUP = {
    "email": Faker().company_email(),
    "password": Faker().password(length=25),
}


@pytest.fixture(scope="function")
def test_create_user(client: TestClient):
    # Create User
    print(f"Creating User: {TEST_USER_SIGNUP=}")
    response = client.post("/users", json=TEST_USER_SIGNUP)
    assert response.status_code == 201

    user_response = UserResponse(**response.json())
    assert user_response.email == TEST_USER_SIGNUP["email"]
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)

    return user_response


def test_login(test_create_user, client: TestClient):
    headers = {}
    data = {
        "username": TEST_USER_SIGNUP["email"],
        "password": TEST_USER_SIGNUP["password"],
    }
    response = client.post("/login", data=data, headers=headers)
    assert response.status_code == 200

    assert isinstance(test_create_user.id, int)
    assert isinstance(test_create_user.email, str)
    assert isinstance(test_create_user.created_at, datetime)

    auth_response = Token(**response.json())
    assert auth_response.token_type == "bearer"
    assert isinstance(auth_response.access_token, str)

    # Create access Token
    user_data = {
        "user_email": TEST_USER_SIGNUP["email"],
        "user_id": test_create_user.id,
    }

    token_data = create_access_token(data=user_data)
    assert token_data == auth_response.access_token
