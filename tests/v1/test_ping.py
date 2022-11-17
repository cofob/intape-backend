"""Test ping endpoint."""

from fastapi.testclient import TestClient

from intape import app

client = TestClient(app)


def test_ping():
    """Test ping endpoint."""
    response = client.get("/v1/ping")
    assert response.status_code == 200
    assert response.text == '"ok"'
