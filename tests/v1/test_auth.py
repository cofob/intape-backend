"""Test ping endpoint."""

from hashlib import sha512
from secrets import token_hex

from faker import Faker
from fastapi.testclient import TestClient

from intape import app


def test_get_salt(faker: Faker):
    """Test get salt endpoint."""
    client = TestClient(app())
    username = faker.user_name()[:16]

    response = client.get(f"/v1/auth/get_salt?username={username}")
    assert response.status_code == 200
    assert response.json() != ""


def test_register(faker: Faker):
    """Test register endpoint."""
    client = TestClient(app())
    username = faker.user_name()[:16]

    salt = token_hex(8)
    print(f"Salt: {salt}")

    password = token_hex(8)
    print(f"Password: {password}")
    password_hash = sha512(password.encode() + salt.encode()).hexdigest()

    payload = {
        "name": username,
        "email": faker.email(),
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
    assert response.json() != ""


def test_check_username(faker: Faker):
    """Test check username endpoint."""
    client = TestClient(app())
    username = faker.user_name()[:16]

    response = client.get(f"/v1/auth/check_username?username={username}")
    assert response.status_code == 200
    assert type(response.json()) == bool
