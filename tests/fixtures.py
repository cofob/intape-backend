"""Fixtures for tests."""

from hashlib import sha512
from secrets import token_hex

import pytest
from fastapi.testclient import TestClient

from intape import app


@pytest.fixture(scope="session")
def username() -> str:
    """Return a random username."""
    return token_hex(3)


@pytest.fixture(scope="session")
def salt() -> str:
    """Return a random salt."""
    return token_hex(8)


@pytest.fixture(scope="session")
def password() -> str:
    """Return a random password."""
    return token_hex(8)


@pytest.fixture(scope="session")
def password_hash(password: str, salt: str) -> str:
    """Return a random password hash."""
    return sha512(password.encode() + salt.encode()).hexdigest()


@pytest.fixture(scope="session", autouse=True)
def tokens(username: str, password_hash: str, salt: str) -> tuple[str, str]:
    """Register user."""
    client = TestClient(app())

    payload = {
        "name": username,
        "email": f"{token_hex(6)}@example.com",
        "password": password_hash,
        "client_salt": salt,
    }
    print(f"Payload: {payload}")

    response = client.post(
        "/v1/auth/register",
        json=payload,
    )
    print(f"Response: {response.text}")
    assert response.status_code == 200

    return response.json()["refresh_token"], response.json()["access_token"]


@pytest.fixture(scope="session")
def refresh_token(tokens: tuple[str, str]) -> str:
    """Return refresh token."""
    return tokens[0]


@pytest.fixture(scope="session")
def access_token(tokens: tuple[str, str]) -> str:
    """Return access token."""
    return tokens[1]
