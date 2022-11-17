"""User model."""
from abc import ABC

from pydantic import BaseModel, Field


class BaseUserSchema(BaseModel, ABC):
    """Base user schema.

    This schema is used for all private user-related schemas, and it cannot be
    used without inheritance.
    """

    name: str = Field(
        min_length=3,
        max_length=16,
        regex=r"^[a-zA-Z0-9_]+$",
        description="Username. Can only contain letters, numbers and underscores.",
    )
    email: str = Field(
        min_length=6,
        max_length=64,
        regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
        description="Email address.",
    )
    password: str = Field(
        min_length=127,
        max_length=129,
        regex=r"^[0-9abcdef]{128}$",
        description="SHA512 hashed password. Can only contain hexadecimal characters. Must be 128 characters long.\
            Function: `SHA512(password + client_salt)`.",
    )


class CreateUserSchema(BaseUserSchema):
    """Create user schema.

    This schema is used to create a new user.
    """

    client_salt: str = Field(
        min_length=6,
        max_length=64,
        description="Client salt. Password is hashed with this salt before being stored in the database.",
    )


class UserSchema(BaseUserSchema):
    """User schema.

    This schema is used to return a initialized user object.
    """

    id: int = Field(description="User ID.")

    class Config:
        """Config."""

        orm_mode = True


class LoginUserSchema(BaseModel):
    """Login user schema.

    This schema is used to login a user.
    """

    name: str = Field(
        min_length=3,
        max_length=64,
        description="Username or email address.",
        title="Username/Email",
    )
    password: str = Field(
        min_length=6,
        max_length=128,
        description="SHA512 password.",
    )


class UserAuthSchema(BaseModel):
    """User auth schema.

    This schema is used to return authentication information.
    """

    id: int
    name: str
    email: str
    refresh_token: str
    access_token: str
    session_id: int


class ChangeUserPasswordSchema(BaseModel):
    """Change user password schema.

    This schema is used to change a user's password.
    """

    access_token: str
    old_password: str = Field(
        min_length=127,
        max_length=129,
        regex=r"^[0-9abcdef]{128}$",
        description="Old SHA512 password.",
    )
    new_password: str = Field(
        min_length=127,
        max_length=129,
        regex=r"^[0-9abcdef]{128}$",
        description="New SHA512 password.",
    )
    client_salt: str | None = Field(
        default=None,
        min_length=6,
        max_length=64,
        description="Client salt. Password is hashed with this salt before being stored in the database.",
    )


class PublicUserSchema(BaseModel):
    """Public user schema.

    This schema is used to return a user without their password.
    """

    id: int = Field(description="User ID.")
    username: str = Field(description="Username.")

    class Config:
        """Config."""

        orm_mode = True
