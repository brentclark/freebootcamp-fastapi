from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from faker import Faker

from app.schemas import UserResponse


def is_valid_email(email):
    import re

    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


def test_get_users(client: TestClient):
    response = client.get(
        "/users",
    )
    assert response.status_code == 200
    # print(response.json())


def test_get_user_by_id(create_user, client: TestClient):
    create_user = create_user
    create_user_response = UserResponse(**create_user.json())

    assert isinstance(create_user_response.id, int)
    assert isinstance(create_user_response.created_at, datetime)

    response = client.get(
        f"/users/{create_user_response.id}",
    )
    #print(response.json())

    user_response = UserResponse(**response.json())

    assert response.status_code == 200
    assert user_response.id == create_user_response.id
    assert user_response.email == create_user_response.email
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)
    assert (
        is_valid_email(user_response.email) != None
    ), f"Expected {user_response.email}, i.e. Does not match"
