"""Module with JWT token models."""

from calendar import timegm
from datetime import datetime, timedelta
from logging import getLogger
from typing import TYPE_CHECKING, Type, TypeVar

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from intape.core.config import Config
from intape.core.database import Base
from intape.core.exceptions import TokenNotFoundException, TokenRevokedException
from intape.schemas.token import AccessTokenSchema, RefreshTokenSchema
from intape.utils.auth import decode, encode, generate_iat_ts

from .abc import AbstractModel

if TYPE_CHECKING:
    from .user import UserModel

logger = getLogger(__name__)

REFRESH_TOKEN_EXPIRE_TIME: dict[str, int] = {"days": 90}
ACCESS_TOKEN_EXPIRE_TIME: dict[str, int] = {"minutes": 15}

T = TypeVar("T", bound="UserTokenModel")


def generate_refresh_token_expire_ts() -> int:
    """Get JWT refresh token expire timestamp."""
    return timegm((datetime.utcnow() + timedelta(**REFRESH_TOKEN_EXPIRE_TIME)).utctimetuple())


def generate_access_token_expire_ts() -> int:
    """Get JWT access token expire timestamp."""
    return timegm((datetime.utcnow() + timedelta(**ACCESS_TOKEN_EXPIRE_TIME)).utctimetuple())


class UserTokenModel(Base, AbstractModel):
    """User token model."""

    __tablename__ = "user_tokens"

    id: int = Column("id", Integer, primary_key=True, index=True)
    user_id: int = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    user: "UserModel" = relationship("UserModel", lazy="joined")
    iat: int = Column("iat", Integer, nullable=False, default=generate_iat_ts)
    exp: int = Column("exp", Integer, nullable=False, default=generate_refresh_token_expire_ts)
    session_info: str | None = Column("session_info", String(64), nullable=True)
    revoked: bool = Column("revoked", Boolean, nullable=False, default=False)
    # If the token was updated last 15 minutes ago, the session is online
    updated_at: datetime = Column("updated_at", DateTime(timezone=True), onupdate=func.now())

    @classmethod
    async def create_obj(
        cls: Type[T],
        session: Session,
        user_id: int,
        session_info: str | None = None,
    ) -> T:
        """Create user token model.

        Args:
            session: Database session.
            user_id: User id.
            session_info: Session info.

        Returns:
            UserTokenModel: Created user token model.
        """
        user_token = cls(
            user_id=user_id,
            session_info=session_info,
        )
        session.add(user_token)
        await session.commit()
        return user_token

    def issue_refresh_token(self, config: Config) -> str:
        """Issue refresh token.

        Returns:
            str: Refresh token.
        """
        data = RefreshTokenSchema.parse_obj(
            {
                "jti": self.id,
                "iat": self.iat,
                "exp": self.exp,
                "uid": self.user_id,
            }
        )
        return encode(config, data.dict())

    def issue_access_token(self, config: Config) -> str:
        """Issue access token.

        Returns:
            str: Access token.
        """
        data = AccessTokenSchema.parse_obj(
            {
                "jti": self.id,
                "iat": generate_iat_ts(),
                "exp": generate_access_token_expire_ts(),
                "uid": self.user_id,
            }
        )
        return encode(config, data.dict())

    @classmethod
    async def get_user_by_access_token(cls, config: Config, session: Session, token: str) -> "UserModel":
        """Get user by access token.

        Args:
            session: Database session.
            token: Access token.

        Raises:
            TokenInvalidException: If token is invalid.
            TokenExpiredException: If token is expired.
            TokenRevokedException: If token is revoked.
            TokenNotFoundException: If token is not found.

        Returns:
            UserModel: User model.
        """
        data = decode(config, token, options={"verify_exp": True})
        schema = AccessTokenSchema.parse_obj(data)
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == schema.jti))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token.user

    @classmethod
    async def issue_new_access_token(cls, config: Config, session: Session, token: str) -> str:
        """Issue new access token.

        Args:
            session: Database session.
            token: Refresh token.

        Raises:
            TokenInvalidException: If token is invalid.
            TokenExpiredException: If token is expired.
            TokenRevokedException: If token is revoked.
            TokenNotFoundException: If token is not found.

        Returns:
            str: New access token.
        """
        data = decode(config, token, options={"verify_exp": True})
        schema = RefreshTokenSchema.parse_obj(data)
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == schema.jti))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token.issue_access_token(config)

    @classmethod
    async def get_by_refresh_token(cls, config: Config, session: Session, token: str) -> "UserTokenModel":
        """Get user token by refresh token.

        Args:
            session: Database session.
            token: Refresh token.

        Raises:
            TokenInvalidException: If token is invalid.
            TokenExpiredException: If token is expired.
            TokenRevokedException: If token is revoked.
            TokenNotFoundException: If token is not found.

        Returns:
            UserTokenModel: User token model.
        """
        data = decode(config, token, options={"verify_exp": True})
        schema = RefreshTokenSchema.parse_obj(data)
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == schema.jti))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token

    @classmethod
    async def get_by_access_token(cls, config: Config, session: Session, token: str) -> "UserTokenModel":
        """Get user token by access token.

        Args:
            session: Database session.
            token: Access token.

        Raises:
            TokenInvalidException: If token is invalid.
            TokenExpiredException: If token is expired.
            TokenRevokedException: If token is revoked.
            TokenNotFoundException: If token is not found.

        Returns:
            UserTokenModel: User token model.
        """
        data = decode(config, token, options={"verify_exp": True})
        schema = AccessTokenSchema.parse_obj(data)
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == schema.jti))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token
