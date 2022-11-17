"""Module containing all exceptions.

All exceptions must be re-exported in this module.
"""
from . import handler  # noqa: F401
from .abc import AbstractException
from .auth import (
    EmailTakenException,
    InvalidCredentialsException,
    UsernameTakenException,
)
from .token import (
    TokenException,
    TokenExpiredException,
    TokenInvalidException,
    TokenNotFoundException,
    TokenRevokedException,
)

__all__ = [
    "AbstractException",
    # Token exceptions
    "TokenException",
    "TokenRevokedException",
    "TokenExpiredException",
    "TokenInvalidException",
    "TokenNotFoundException",
    # Auth exceptions
    "UsernameTakenException",
    "EmailTakenException",
    "InvalidCredentialsException",
]
