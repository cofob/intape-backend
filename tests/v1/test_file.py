"""Test file endpoints."""

from io import BytesIO

from fastapi.testclient import TestClient

from intape import app
from tests.fixtures import *


def test_file_upload(access_token: str):
    """Test file upload endpoint."""
    client = TestClient(app())
    client.headers["Authorization"] = f"Bearer {access_token}"
    response = client.post("/v1/file/upload", files={"file": BytesIO(b"test")})
    print(f"Response: {response.text}")
    assert response.status_code == 200
    assert response.json().startswith("Qm")
