from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from faker import Faker

from app.schemas import UserResponse


def is_valid_email(email):
    import re

    pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


@pytest.mark.parametrize(
    ("email", "password", "status"),
    ((Faker().company_email(), Faker().password(length=25), 201),),
)
def test_create_user(client: TestClient, email: str, password: str, status: int):
    response = client.post(
        "/users",
        json={"email": email, "password": password},
    )
    user_response = UserResponse(**response.json())

    assert response.status_code == status
    assert user_response.email == email
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)


def test_get_users(client: TestClient):
    response = client.get(
        "/users",
    )
    assert response.status_code == 200
    print(response.json())


@pytest.mark.parametrize(("id", "status_code"), ((2, 200),))
def test_get_user_with_id_1(client: TestClient, id: int, status_code: int):
    response = client.get(
        f"/users/{id}",
    )
    print(response.json())

    assert response.status_code == status_code
    assert response.json().get("id") == id
    assert response.json().get("email") is not None
    assert response.json().get("created_at") is not None

    user_response = UserResponse(**response.json())
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)
    assert (
        is_valid_email(user_response.email) != None
    ), f"Expected {user_response.email}, i.e. Does not match"
