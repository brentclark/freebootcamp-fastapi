from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from faker import Faker
from app.schemas import PostCreateResponse, PostOut


@pytest.mark.parametrize(
    ("title", "content", "published"),
    (
        (
            Faker().sentence(nb_words=4),
            Faker().sentence(nb_words=4),
            Faker().random_element(elements=("True", "False")),
        ),
    ),
)
@pytest.mark.testclient
def test_posts_by_user(
    create_user_return_header_with_access_token,
    client: TestClient,
    title,
    content,
    published,
):
    # Create test user and get token
    headers = create_user_return_header_with_access_token

    payload = {
        "title": title,
        "content": content,
        "published": published,
    }

    # Create a post
    response = client.post("/posts", headers=headers, json=payload)
    assert response.status_code == 201

    post_response = PostCreateResponse(**response.json())

    assert isinstance(post_response.id, int)
    assert isinstance(post_response.title, str)
    assert isinstance(post_response.created_at, datetime)


@pytest.mark.testclient
def test_get_all_posts(create_user_return_header_with_access_token, client: TestClient):
    # Create test user and get token
    headers = create_user_return_header_with_access_token

    # Get all posts
    response = client.get("/posts", headers=headers)
    print(response.json())
    assert response.status_code == 200


@pytest.mark.skip(reason="Cant delete post that it does not own")
@pytest.mark.testclient
def test_delete_a_post(create_user_return_header_with_access_token, client: TestClient):
    # Create test user and get token
    headers = create_user_return_header_with_access_token

    # Get all posts
    response = client.get("/posts", headers=headers)
    assert response.status_code == 200

    id = response.json()[0]["Posts"].get("id")
    delete_response = client.delete(f"/posts/{id}", headers=headers)
    print(delete_response)
