"""Fixtures for tests."""

from secrets import token_hex

import pytest
from eth_account import Account
from eth_account.messages import encode_defunct
from fastapi.testclient import TestClient

from intape import app


@pytest.fixture(scope="session")
def username() -> str:
    """Return a random username."""
    return "T" + token_hex(3)


@pytest.fixture(scope="session")
def eth_account() -> Account:
    """Return a random eth account."""
    return Account.create()


@pytest.fixture(scope="session")
def address(eth_account: Account) -> str:
    """Return a random address."""
    return eth_account.address.lower()


@pytest.fixture(scope="session")
def confirmation_jwt_data(address: str) -> dict[str, str]:
    """Return a confirmation JWT."""
    client = TestClient(app())
    response = client.post("/v1/auth/request_confirmation", json={"eth_address": address})
    return response.json()


@pytest.fixture(scope="session")
def confirmation_jwt(confirmation_jwt_data: dict[str, str]) -> str:
    """Return a confirmation JWT."""
    return confirmation_jwt_data["confirmation_jwt"]


@pytest.fixture(scope="session")
def confirmation_jwt_text(confirmation_jwt_data: dict[str, str]) -> str:
    """Return a confirmation JWT."""
    return confirmation_jwt_data["data"]


@pytest.fixture(scope="session")
def signature(eth_account: Account, confirmation_jwt_text: str) -> str:
    """Return a signature."""
    message = encode_defunct(text=confirmation_jwt_text)
    return eth_account.sign_message(message).signature.hex()


@pytest.fixture(scope="session", autouse=True)
def tokens(username: str, confirmation_jwt: str, address: str, signature: str) -> tuple[str, str]:
    """Register user."""
    client = TestClient(app())

    payload = {
        "username": username,
        "eth_address": address,
        "confirmation_jwt": confirmation_jwt,
        "signature": signature,
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
