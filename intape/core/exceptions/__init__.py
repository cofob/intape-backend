"""Module containing all exceptions.

All exceptions must be re-exported in this module.
"""
from .abc import AbstractException
from .auth import (
    AuthenticationRequiredException,
    EmailTakenException,
    EthAddressTakenException,
    InsufficientPermissionsException,
    InvalidCredentialsException,
    ReservedUsernameException,
    UsernameTakenException,
    UserNotFoundException,
)
from .file import (
    FileAlreadyExistsException,
    FileNotFoundException,
    UnsupportedMimeTypeException,
)
from .other import DatabaseException, IPFSException, NotImplementedException
from .token import (
    TokenException,
    TokenExpiredException,
    TokenInvalidException,
    TokenNotFoundException,
    TokenRevokedException,
)
from .video import VideoNotFoundException

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
    "ReservedUsernameException",
    "EmailTakenException",
    "InvalidCredentialsException",
    "AuthenticationRequiredException",
    "UserNotFoundException",
    "InsufficientPermissionsException",
    "EthAddressTakenException",
    # File exceptions
    "UnsupportedMimeTypeException",
    "FileAlreadyExistsException",
    "FileNotFoundException",
    # Video exceptions
    "VideoNotFoundException",
    # Other exceptions
    "NotImplementedException",
    "DatabaseException",
    "IPFSException",
]
