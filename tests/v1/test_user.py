"""Test user endpoints."""

from fastapi.testclient import TestClient

from intape import app
from tests.fixtures import *


def test_get_user_info(username: str):
    """Test get user info endpoint."""
    client = TestClient(app())
    response = client.get(f"/v1/user/{username}")
    print(f"Response: {response.text}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["username"] == username
