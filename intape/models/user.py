"""User model module."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from intape.core.database import Base


class UserModel(Base):
    """User model."""

    __tablename__ = "users"

    id: int = Column("id", Integer, primary_key=True, index=True)
    name: str = Column("name", String(16), unique=True, index=True, nullable=False)
    email: str = Column("email", String(64), unique=True, index=True, nullable=False)
    password: str = Column("password", String(64), nullable=False)
    client_salt: str = Column("client_salt", String(64), nullable=False, server_default="")
    created_at: datetime = Column("created_at", DateTime(timezone=True), server_default=func.now())
    updated_at: datetime = Column("updated_at", DateTime(timezone=True), onupdate=func.now())
