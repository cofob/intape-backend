"""Module containing database setup and dependency."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from intape.core.config import CONFIG

# postgresql+asyncpg://postgres:postgres@db:5432/foo
engine = create_async_engine(CONFIG.DATABASE_URL, future=True)


def get_db() -> AsyncSession:
    """Get async database session instance with current engine."""
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)()


__all__ = ["get_db", "engine"]
