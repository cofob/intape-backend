"""User model module."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from intape.core.database import Base
from intape.core.exceptions import UserNotFoundException
from intape.schemas.user import PublicUserSchema

from .abc import AbstractModel


class UserModel(Base, AbstractModel):
    """User model."""

    __tablename__ = "users"

    id: int = Column("id", Integer, primary_key=True, index=True)

    # Name
    username: str = Column("username", String(16), unique=True, index=True, nullable=False)
    first_name: str | None = Column("first_name", String(32), nullable=True)
    last_name: str | None = Column("last_name", String(32), nullable=True)

    # Bio
    bio = Column("bio", String(512), nullable=True)

    # Web3 stuff
    eth_address: str = Column("eth_address", String(42), unique=True, index=True, nullable=False)

    # Email
    email: str | None = Column("email", String(64), unique=True, index=True, nullable=True)
    is_email_public: bool = Column("is_email_public", Boolean, nullable=False, default=False)
    is_email_verified: bool = Column("is_email_verified", Boolean, nullable=False, default=False)

    # Avatar
    avatar_cid: str | None = Column("avatar_cid", String(128), nullable=True)

    # Other
    created_at: datetime = Column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column("updated_at", DateTime(timezone=True), onupdate=func.now())

    @classmethod
    async def get_by_name_or_email(cls, db: AsyncSession, username: str) -> "UserModel":
        """Get user by name or email.

        Args:
            db (AsyncSession): Database session.
            username (str): Username or email.

        Returns:
            UserModel: User model.

        Raises:
            UserNotFoundException: If the user is not found.
        """
        query = await db.execute(select(cls).filter(or_(cls.username == username, cls.email == username)))
        user: UserModel | None = query.scalars().first()
        if user is None:
            raise UserNotFoundException()
        return user

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int) -> "UserModel":
        """Get user by id.

        Args:
            db (AsyncSession): Database session.
            id (int): User id.

        Returns:
            UserModel: User model.

        Raises:
            UserNotFoundException: If the user is not found.
        """
        query = await db.execute(select(cls).filter_by(id=id))
        user: UserModel | None = query.scalars().first()
        if user is None:
            raise UserNotFoundException()
        return user

    def to_public(self) -> PublicUserSchema:
        """Convert user model to public schema.

        Returns:
            PublicUserSchema: Public user schema.
        """
        return PublicUserSchema(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email if self.is_email_public else None,
            avatar_cid=self.avatar_cid,
            bio=self.bio,
            eth_address=self.eth_address,
        )
