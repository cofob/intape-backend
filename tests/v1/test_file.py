"""Test file endpoints."""

from fastapi.testclient import TestClient

from intape import app


# TODO: Deal with authoization (access token should be passed)
def test_file_upload():
    """Test file upload endpoint."""
    client = TestClient(app())
    response = client.post("/v1/file/upload", files={"file": open("README.md", "rb")})
    print(f"Response: {response.text}")
    assert response.status_code == 500
    assert response.json()["error_code"] == "AuthenticationRequiredException"
