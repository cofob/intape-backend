"""Module with JWT token models."""

from calendar import timegm
from datetime import datetime, timedelta
from logging import getLogger
from typing import Type, TypeVar

from jose import JWTError, jwt
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy.orm import relationship

from intape.core.config import CONFIG
from intape.core.database import Base
from intape.core.exceptions import (
    TokenInvalidException,
    TokenNotFoundException,
    TokenRevokedException,
)
from intape.models import UserModel

logger = getLogger(__name__)

ALGORITHM = "HS256"
REFRESH_TOKEN_EXPIRE_TIME: dict[str, int] = {"days": 90}
ACCESS_TOKEN_EXPIRE_TIME: dict[str, int] = {"minutes": 15}

# JWT payload recursive type
JSONType = dict[str, str | int | float | bool | None | dict[str, "JSONType"] | list["JSONType"]]
T = TypeVar("T", bound="UserTokenModel")


def generate_refresh_token_expire_ts() -> int:
    """Get JWT refresh token expire timestamp."""
    return timegm((datetime.utcnow() + timedelta(**REFRESH_TOKEN_EXPIRE_TIME)).utctimetuple())


def generate_access_token_expire_ts() -> int:
    """Get JWT access token expire timestamp."""
    return timegm((datetime.utcnow() + timedelta(**ACCESS_TOKEN_EXPIRE_TIME)).utctimetuple())


def generate_iat_ts() -> int:
    """Get JWT iat field."""
    return timegm(datetime.utcnow().utctimetuple())


def encode(data: JSONType) -> str:
    """Encode provided data to signed JWT token.

    Args:
        data: JWT data.

    Returns:
        str: JWT string.
    """
    return jwt.encode(data, CONFIG.SECRET, algorithm=ALGORITHM)  # type: ignore


def decode(token: str, options: dict[str, bool] = {}) -> JSONType:
    """Decode JWT token and return its data.

    Args:
        token: JWT token string.

    Raises:
        TokenInvalidException: If token is invalid.

    Returns:
        dict: Parsed JWT data.
    """
    # jose raises exception if jti field is not int, so we disable jti
    # check globally
    options["verify_jti"] = False
    try:
        return jwt.decode(  # type: ignore
            token,
            CONFIG.SECRET,
            algorithms=[ALGORITHM],
            options=options,
        )
    except JWTError:
        logger.exception("JWT exception")
        raise TokenInvalidException(detail="JWT decode/verification error")


class UserTokenModel(Base):
    """User token model."""

    __tablename__ = "user_tokens"

    id: int = Column("id", Integer, primary_key=True, index=True)
    user_id: int = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    user: UserModel = relationship("UserModel")
    iat: int = Column("iat", Integer, nullable=False, default=generate_iat_ts)
    exp: int = Column("exp", Integer, nullable=False, default=generate_refresh_token_expire_ts)
    session_info: str | None = Column("session_info", String(64), nullable=True)
    revoked: bool = Column("revoked", Boolean, nullable=False, default=False)

    @classmethod
    async def create(
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

    def issue_refresh_token(self) -> str:
        """Issue refresh token.

        Returns:
            str: Refresh token.
        """
        data: JSONType = {
            "jti": self.id,
            "iat": self.iat,
            "exp": self.exp,
            "sub": "refresh",
        }
        return encode(data)

    def issue_access_token(self) -> str:
        """Issue access token.

        Returns:
            str: Access token.
        """
        data: JSONType = {
            "jti": self.id,
            "iat": generate_iat_ts(),
            "exp": generate_access_token_expire_ts(),
            "sub": "access",
        }
        return encode(data)

    @classmethod
    async def get_user_by_access_token(cls, session: Session, token: str) -> UserModel:
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
        data = decode(token, options={"verify_exp": True})
        if data["sub"] != "access":
            raise TokenInvalidException(detail="Invalid token subject")
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == data["jti"]))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token.user

    @classmethod
    async def issue_new_access_token(cls, session: Session, token: str) -> str:
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
        data = decode(token, options={"verify_exp": True})
        if data["sub"] != "refresh":
            raise TokenInvalidException(detail="Invalid token subject")
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == data["jti"]))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token.issue_access_token()

    @classmethod
    async def get_by_refresh_token(cls, session: Session, token: str) -> "UserTokenModel":
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
        data = decode(token, options={"verify_exp": True})
        if data["sub"] != "refresh":
            raise TokenInvalidException(detail="Invalid token subject")
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == data["jti"]))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token

    @classmethod
    async def get_by_access_token(cls, session: Session, token: str) -> "UserTokenModel":
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
        data = decode(token, options={"verify_exp": True})
        if data["sub"] != "access":
            raise TokenInvalidException(detail="Invalid token subject")
        user_token: "UserTokenModel" | None = (
            (await session.execute(select(cls).where(cls.id == data["jti"]))).scalars().first()
        )
        if user_token is None:
            raise TokenNotFoundException(detail="Token not found")
        if user_token.revoked:
            raise TokenRevokedException(detail="Token revoked")
        return user_token
