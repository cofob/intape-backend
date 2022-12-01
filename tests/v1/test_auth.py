"""Test ping endpoint."""

from faker import Faker
from fastapi.testclient import TestClient

from intape import app
from tests.checks import is_jwt
from tests.fixtures import *


def test_register(access_token: str):
    """Test register endpoint."""
    assert is_jwt(access_token)


def test_login(signature: str, confirmation_jwt: str):
    """Test login endpoint."""
    client = TestClient(app())

    payload = {
        "confirmation_jwt": confirmation_jwt,
        "signature": signature,
    }
    print(f"Payload: {payload}")
    response = client.post("/v1/auth/login", json=payload)
    print(f"Response: {response.text}")
    assert response.status_code == 200
    assert response.json()["access_token"] != ""
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
    assert response.json()["username"] == username


def test_invalid_auth():
    """Test invalid auth."""
    client = TestClient(app())
    response = client.get("/v1/auth/check_auth", headers={"Authorization": f"Bearer some.invalid.token"})
    assert response.status_code != 200
