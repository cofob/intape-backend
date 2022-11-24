"""Pydantic schemas for the intape API.

All schemas must be re-exported in this module, to be used by the API.
"""
from .user import (
    ChangeUserPasswordSchema,
    CreateUserSchema,
    LoginUserSchema,
    PublicUserSchema,
    UserAuthSchema,
    UserSchema,
)
from .video import CreateVideoSchema, VideoSchema

__all__ = [
    # User schemas
    "CreateUserSchema",
    "LoginUserSchema",
    "ChangeUserPasswordSchema",
    "UserAuthSchema",
    "PublicUserSchema",
    "UserSchema",
    # Video schemas
    "CreateVideoSchema",
    "VideoSchema",
]
