import asyncio
import pytest

from app.main import app
from app.schemas.users import UserCreate
from app.utils.users import create_user, create_user_token
from fastapi.testclient import TestClient


def test_sign_up(temp_db):
    request_data = {
        "email": "vader@deathstar.com",
        "name": "Darth",
        "password": "rainbow"
    }
    with TestClient(app) as client:
        response = client.post("/sign-up", json=request_data)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "vader@deathstar.com"
    assert response.json()["name"] == "Darth"
    assert response.json()["token"]["expires"] is not None
    assert response.json()["token"]["access_token"] is not None


def test_login(temp_db):
    request_data = {"username": "vader@deathstar.com", "password": "rainbow"}
    with TestClient(app) as client:
        response = client.post("/auth", data=request_data)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires"] is not None
    assert response.json()["access_token"] is not None


def test_login_with_invalid_password(temp_db):
    request_data = {"username": "vader@deathstar.com", "password": "unicorn"}
    with TestClient(app) as client:
        response = client.post("/auth", data=request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_user_detail(temp_db):
    with TestClient(app) as client:
        # Create user token to see user info
        loop = asyncio.get_event_loop()
        token = loop.run_until_complete(create_user_token(user_id=1))
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {token['token']}"}
        )
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "vader@deathstar.com"
    assert response.json()["name"] == "Darth"


def test_user_detail_forbidden_without_token(temp_db):
    with TestClient(app) as client:
        response = client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.freeze_time("2015-10-21")
def test_user_detail_forbidden_with_expired_token(temp_db, freezer):
    user = UserCreate(
        email="sidious@deathstar.com",
        name="Palpatine",
        password="unicorn"
    )
    with TestClient(app) as client:
        # Create user and use expired token
        loop = asyncio.get_event_loop()
        user_db = loop.run_until_complete(create_user(user))
        freezer.move_to("'2015-11-10'")
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {user_db['token']['token']}"}
        )
    assert response.status_code == 401
