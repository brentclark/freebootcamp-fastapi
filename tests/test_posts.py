from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from faker import Faker

from app.oauth2 import create_access_token
from app.database import engine, Base
from app.schemas import UserResponse, PostCreateResponse
from app.main import app

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.mark.parametrize(
    ("email", "password"),
    ((Faker().company_email(), Faker().password(length=25)),),
)
def test_posts_by_user(email, password):
    # First create user
    response = client.post(
        "/users",
        json={"email": email, "password": password},
    )
    user_response = UserResponse(**response.json())

    assert response.status_code == 201
    assert user_response.email == email
    assert isinstance(user_response.id, int)
    assert isinstance(user_response.created_at, datetime)

    # Create access Token
    user_data = {
        "user_email": user_response.email,
        "user_id": user_response.id,
    }
    token_data = create_access_token(data=user_data)
    assert token_data is not None
    print(f"\n{token_data=}")

    # Create a post
    headers = {}
    payload = {
        "title": Faker().sentence(nb_words=4),
        "content": Faker().sentence(nb_words=4),
        "published": Faker().random_element(elements=("True", "False")),
    }
    headers["Authorization"] = "Bearer " + token_data
    response = client.post("/posts", headers=headers, json=payload)
    assert response.status_code == 201

    post_response = PostCreateResponse(**response.json())
    print(post_response)
    assert isinstance(post_response.id, int)
    assert isinstance(post_response.title, str)
    assert isinstance(post_response.created_at, datetime)

    # Get all posts
    headers = {}
    headers["Authorization"] = "Bearer " + token_data
    response = client.get("/posts", headers=headers)
    print(response.text)
    assert response.status_code == 200
