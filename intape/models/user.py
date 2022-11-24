"""User model module."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from intape.core.database import Base
from intape.core.exceptions import UserNotFoundException

from .abc import AbstractModel


class UserModel(Base, AbstractModel):
    """User model."""

    __tablename__ = "users"

    id: int = Column("id", Integer, primary_key=True, index=True)
    name: str = Column("name", String(16), unique=True, index=True, nullable=False)
    email: str = Column("email", String(64), unique=True, index=True, nullable=False)
    password: str = Column("password", String(128), nullable=False)
    client_salt: str = Column("client_salt", String(64), nullable=False, server_default="")
    created_at: datetime = Column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column("updated_at", DateTime(timezone=True), onupdate=func.now())

    @classmethod
    async def get_by_name_or_email(cls, db: AsyncSession, name: str) -> "UserModel":
        """Get user by name or email.

        Args:
            db (AsyncSession): Database session.
            name (str): Username or email.

        Returns:
            UserModel: User model.

        Raises:
            UserNotFoundException: If the user is not found.
        """
        query = await db.execute(select(cls).filter(or_(cls.name == name, cls.email == name)))
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
