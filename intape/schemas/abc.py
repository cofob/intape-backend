"""Abstract base classes for schemas."""

from abc import ABC

from pydantic import BaseModel


class BaseSchema(BaseModel, ABC):
    """Base schema."""

    class Config:
        """Config."""

        orm_mode = True
