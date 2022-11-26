"""Test ping endpoint."""

from faker import Faker
from fastapi.testclient import TestClient

from intape import app
from tests.checks import is_jwt
from tests.fixtures import *


def test_get_salt(username: str):
    """Test get salt endpoint."""
    client = TestClient(app())
    response = client.get(f"/v1/auth/get_salt?username={username}")
    assert response.status_code == 200
    assert response.json() != ""


def test_register(access_token: str):
    """Test register endpoint."""
    assert is_jwt(access_token)


def test_login(username: str, password_hash: str):
    """Test login endpoint."""
    client = TestClient(app())

    payload = {
        "name": username,
        "password": password_hash,
    }
    print(f"Payload: {payload}")
    response = client.post("/v1/auth/login", json=payload)
    print(f"Response: {response.text}")
    assert response.status_code == 200
    assert response.json()["access_token"] != ""
    assert is_jwt(response.json()["access_token"])


def test_simple_login(username: str, password: str):
    """Test simple login endpoint."""
    client = TestClient(app())

    payload = {
        "username": username,
        "password": password,
    }
    print(f"Payload: {payload}")
    # Send request with payload in form data
    response = client.post("/v1/auth/simple_login", data=payload)
    print(f"Response: {response.text}")
    assert response.status_code == 200
    assert is_jwt(response.json()["access_token"])


def test_refresh_token(refresh_token: str):
    """Test refresh token endpoint."""
    client = TestClient(app())
    response = client.post("/v1/auth/access_token", json=refresh_token)
    print(f"Response: {response.text}")
    assert response.status_code == 200
    assert is_jwt(response.json())


def test_check_username(faker: Faker):
    """Test check username endpoint."""
    client = TestClient(app())
    username = faker.user_name()[:16]

    response = client.get(f"/v1/auth/check_username?username={username}")
    assert response.status_code == 200
    assert isinstance(response.json(), bool)


def test_valid_auth(access_token: str, username: str):
    """Test valid auth."""
    client = TestClient(app())
    response = client.get("/v1/auth/check_auth", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["name"] == username


def test_invalid_auth():
    """Test invalid auth."""
    client = TestClient(app())
    response = client.get("/v1/auth/check_auth", headers={"Authorization": f"Bearer some.invalid.token"})
    assert response.status_code != 200
