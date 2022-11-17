"""Module containing all SQLAlchemy models.

All models must be re-exported in this module, to make them available to the
Alembic migrations generator.
"""
from .user import UserModel

__all__ = ["UserModel", "UserTokenModel"]

from .token import UserTokenModel
