"""Test ping endpoint."""

from hashlib import sha512

from faker import Faker
from fastapi.testclient import TestClient
from jose import jwt

from intape import app

client = TestClient(app)
faker = Faker()


# For some reason, test with database is not working
# TODO: Fix tests with database
# def test_get_salt():
#     """Test get salt endpoint."""
#     username = faker.first_name() + faker.last_name()
#
#     response = client.get(f"/v1/auth/get_salt?username={username}")
#     assert response.status_code == 200
#     assert response.json() != ""
#
#
# def test_register():
#     """Test register endpoint."""
#     username = faker.first_name() + faker.last_name()

#     salt_response = client.get(f"/v1/auth/get_salt?username={username}")
#     assert salt_response.status_code == 200
#     salt = salt_response.json()
#     print(f"Salt: {salt}")

#     password = faker.password()
#     print(f"Password: {password}")
#     password_hash = sha512(password.encode() + salt.encode()).hexdigest()

#     payload = {
#         "name": username,
#         "email": faker.email(),
#         "password": password_hash,
#         "client_salt": salt,
#     }
#     print(f"Payload: {payload}")

#     response = client.post(
#         "/v1/auth/register",
#         json=payload,
#     )
#     print(f"Response: {response.text}")
#     assert response.status_code == 200
#     assert response.json() != ""
#
#
# def test_check_username():
#     """Test check username endpoint."""
#     username = faker.first_name() + faker.last_name()

#     response = client.get(f"/v1/auth/check_username?username={username}")
#     assert response.status_code == 200
#     assert response.json() is True
