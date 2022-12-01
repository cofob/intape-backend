"""Token schemas."""
from pydantic import Field

from . import fields as f
from .abc import BaseSchema


class BaseTokenSchema(BaseSchema):
    """Base token schema."""

    iat: int = Field(ge=0)
    exp: int = Field(ge=0)
    jti: int = Field(ge=0)
    uid: int = Field(ge=0)
    type: str


class RefreshTokenSchema(BaseTokenSchema):
    """Refresh token schema."""

    type: str = Field("refresh", const=True)


class AccessTokenSchema(BaseTokenSchema):
    """Access token schema."""

    type: str = Field("access", const=True)


class ConfirmationJWTResponse(BaseSchema):
    """Confirmation JWT response."""

    data: str
    eth_address: str = f.ETH_ADDRESS
    type: str = Field("eth_confirmation", const=True)
    exp: int = Field(ge=0)
