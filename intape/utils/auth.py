"""Authorization utils."""

from calendar import timegm
from datetime import datetime, timedelta
from logging import getLogger
from typing import Any

from jose import JWTError, jwt

from intape.core.config import (
    RESERVED_USERNAME_SPACES,
    RESERVED_USERNAMES,
    Config,
)
from intape.core.exceptions import (
    InvalidCredentialsException,
    TokenInvalidException,
)
from intape.schemas.token import ConfirmationJWTResponse

from .crypto import verify_signature

ALGORITHM = "HS256"
JSON_TYPE = dict[str, str | int | float | bool | None | dict[str, "JSON_TYPE"] | list["JSON_TYPE"]]

logger = getLogger(__name__)


def is_username_reserved(username: str) -> bool:
    """Check if username is reserved."""
    return username in RESERVED_USERNAMES or username.startswith(RESERVED_USERNAME_SPACES)


def generate_confirmation_token(config: Config, eth_address: str, data: str) -> str:
    """Generate a token for a user."""
    return encode(
        config,
        ConfirmationJWTResponse(
            data=data,
            eth_address=eth_address,
            exp=timegm((datetime.utcnow() + timedelta(minutes=5)).utctimetuple()),
        ).dict(),
    )


def generate_confirmation_text(data: str) -> str:
    """Generate a confirmation text."""
    return f"""Sign this message to login to the site.
This doesn't cost you anything and is free of any gas fees.

Nonce: {data}"""


def confirm_user_signature(config: Config, jwt: str, signature: str) -> str:
    """Confirm a user's signature.

    This function will decode the JWT and verify the signature.

    Args:
        config (Config): The application config.
        jwt (str): The JWT.
        signature (str): The signature.

    Returns:
        str: The user's Ethereum address.
    """
    decoded_jwt = ConfirmationJWTResponse(**decode(config, jwt))
    text = generate_confirmation_text(decoded_jwt.data)
    if not verify_signature(text, signature, decoded_jwt.eth_address):
        raise InvalidCredentialsException(detail="Invalid signature.")
    return decoded_jwt.eth_address


def timegm_delta(**delta: Any) -> int:
    """Get timegm from timedelta."""
    return timegm((datetime.utcnow() + timedelta(**delta)).utctimetuple())


def timegm_now() -> int:
    """Get timegm from now."""
    return timegm(datetime.utcnow().utctimetuple())


def generate_iat_ts() -> int:
    """Get JWT iat field."""
    return timegm_now()


def encode(config: Config, data: JSON_TYPE) -> str:
    """Encode provided data to signed JWT token.

    Args:
        data: JWT data.

    Returns:
        str: JWT string.
    """
    return jwt.encode(data, config.SECRET, algorithm=ALGORITHM)


def decode(config: Config, token: str, options: dict[str, bool] = {}) -> JSON_TYPE:
    """Decode JWT token and return its data.

    Args:
        token: JWT token string.

    Raises:
        TokenInvalidException: If token is invalid.

    Returns:
        dict: Parsed JWT data.
    """
    # jose raises exception if jti field is not int, so we disable jti
    # check globally
    options["verify_jti"] = False
    try:
        return jwt.decode(
            token,
            config.SECRET,
            algorithms=[ALGORITHM],
            options=options,
        )
    except JWTError:
        logger.exception("JWT exception")
        raise TokenInvalidException(detail="JWT decode/verification error")
