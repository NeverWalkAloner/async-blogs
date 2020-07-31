import asyncio

from app.main import app
from app.schemas.users import UserCreate
from app.utils.users import create_user, create_user_token
from fastapi.testclient import TestClient


def test_create_post(temp_db):
    user = UserCreate(
        email="vader@deathstar.com",
        name="Darth",
        password="rainbow"
    )
    request_data = {
      "title": "42",
      "content": "Don't panic!"
    }
    with TestClient(app) as client:
        # Create user and use his token to add new post
        loop = asyncio.get_event_loop()
        user_db = loop.run_until_complete(create_user(user))
        response = client.post(
            "/posts",
            json=request_data,
            headers={"Authorization": f"Bearer {user_db['token']['token']}"}
        )
    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["title"] == "42"
    assert response.json()["content"] == "Don't panic!"


def test_create_post_forbidden_without_token(temp_db):
    request_data = {
      "title": "42",
      "content": "Don't panic!"
    }
    with TestClient(app) as client:
        response = client.post("/posts", json=request_data)
    assert response.status_code == 401


def test_posts_list(temp_db):
    with TestClient(app) as client:
        response = client.get("/posts")
    assert response.status_code == 200
    assert response.json()["total_count"] == 1
    assert response.json()["results"][0]["id"] == 1
    assert response.json()["results"][0]["title"] == "42"
    assert response.json()["results"][0]["content"] == "Don't panic!"


def test_post_detail(temp_db):
    post_id = 1
    with TestClient(app) as client:
        response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "42"
    assert response.json()["content"] == "Don't panic!"


def test_update_post(temp_db):
    post_id = 1
    request_data = {
      "title": "42",
      "content": "Life? Don't talk to me about life."
    }
    with TestClient(app) as client:
        # Create user token to add new post
        loop = asyncio.get_event_loop()
        token = loop.run_until_complete(create_user_token(user_id=1))
        response = client.put(
            f"/posts/{post_id}",
            json=request_data,
            headers={"Authorization": f"Bearer {token['token']}"}
        )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "42"
    assert response.json()["content"] == "Life? Don't talk to me about life."


def test_update_post_forbidden_without_token(temp_db):
    post_id = 1
    request_data = {
      "title": "42",
      "content": "Life? Don't talk to me about life."
    }
    with TestClient(app) as client:
        response = client.put(f"/posts/{post_id}", json=request_data)
    assert response.status_code == 401
