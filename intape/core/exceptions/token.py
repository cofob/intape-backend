"""Token (JWT) exceptions."""
from .abc import AbstractException


class TokenException(AbstractException):
    """Base token exception.

    This exception is used for all token-related exceptions. Must be inherited.
    """

    pass


class TokenRevokedException(TokenException):
    """Token revoked exception.

    This exception is used when the token is revoked.

    This exception can caused by the following reasons:
        - Session is closed.
        - User is deleted.
        - User is blocked.
    """

    pass


class TokenExpiredException(TokenException):
    """Token expired exception.

    This exception is used when the token is expired.

    This exception can caused by the following reasons:
        - EXP field of JWT is too old.
    """

    pass


class TokenInvalidException(TokenException):
    """Token invalid exception.

    This exception is used when the token is invalid.

    This exception can caused by the following reasons:
        - Token is not a valid JWT.
        - Token is not signed with correct key.
        - Token is not signed with correct algorithm.
        - Token does not contain required fields, or contains invalid fields.
    """

    pass


class TokenNotFoundException(TokenException):
    """Token not found exception.

    This exception is used when the token is not found in the database.

    This exception can caused by the following reasons:
        - Token is not in the database.
    """

    status_code = 404
