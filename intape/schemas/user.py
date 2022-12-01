"""User model."""
from abc import ABC

from pydantic import Field

from . import fields as f
from .abc import BaseSchema


class BaseUserSchema(BaseSchema, ABC):
    """Base user schema.

    This schema is used for all private user-related schemas, and it cannot be
    used without inheritance.
    """

    username: str = f.USERNAME
    eth_address: str = f.ETH_ADDRESS


class UserSchema(BaseUserSchema):
    """User schema.

    This schema is used to return a initialized user object.
    """

    id: int = f.USER_ID


class LoginUserSchema(BaseSchema):
    """Login user schema.

    This schema is used to login a user.
    """

    confirmation_jwt: str = f.JWT_TOKEN
    signature: str = f.SIGNATURE


class CreateUserSchema(LoginUserSchema):
    """Create user schema.

    This schema is used to create a new user.
    """

    username: str = f.USERNAME


class UserAuthSchema(BaseSchema):
    """User auth schema.

    This schema is used to return authentication information.
    """

    id: int = f.USER_ID
    username: str = f.USERNAME
    email: str | None = f.EMAIL
    refresh_token: str = f.JWT_TOKEN
    access_token: str = f.JWT_TOKEN
    session_id: int = f.SESSION_ID
    token_type: str = f.JWT_TOKEN_TYPE


class PublicUserSchema(BaseSchema):
    """Public user schema.

    This schema is used to return a user without their password.
    """

    id: int = f.USER_ID
    username: str = f.USERNAME
    bio: str | None = f.BIO
    first_name: str | None = f.FIRST_NAME
    last_name: str | None = f.LAST_NAME
    email: str | None = f.EMAIL
    avatar_cid: str | None = f.IPFS_CID
    eth_address: str | None = f.ETH_ADDRESS


class ConfitmationSignatureRequestSchema(BaseSchema):
    """Confirmation signature request schema.

    This schema is used to request a signature for a confirmation JWT.
    """

    eth_address: str = f.ETH_ADDRESS


class ConfirmationSignatureSchema(BaseSchema):
    r"""Confirmation signature schema.

    This schema is used to return a data, required to confirm a user's
    Ethereum address.
    """

    confirmation_jwt: str = f.JWT_TOKEN
    data: str = Field(description="Data to sign.")
