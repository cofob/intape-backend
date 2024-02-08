"""Module containing the checks for the tests."""

from base64 import b64decode
from json import loads


def is_jwt(token: str) -> bool:
    """Check if the token is a JWT."""
    assert token.count(".") == 2

    header, payload, signature = token.split(".")
    assert len(header) > 0
    assert len(payload) > 0
    assert len(signature) > 0

    def pad(string: str) -> str:
        """Pad the b64 string."""
        return string + "=" * (4 - len(string) % 4)

    header = loads(b64decode(pad(header)).decode())
    assert "alg" in header

    payload = loads(b64decode(pad(payload)).decode())
    assert "exp" in payload

    return True
