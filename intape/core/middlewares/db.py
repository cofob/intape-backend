"""Database middleware."""

import logging

from fastapi import Request, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp

from intape.core.config import Config
from intape.core.exceptions import DatabaseException

log = logging.getLogger(__name__)


class DBAsyncSessionMiddleware(BaseHTTPMiddleware):
    """Database session middleware."""

    def __init__(self, app: ASGIApp, config: Config) -> None:
        """Initialize."""
        super().__init__(app)
        engine = create_async_engine(config.DATABASE_URL)
        self.async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch."""
        try:
            request.state.db = self.async_session_maker()
            return await call_next(request)
        except SQLAlchemyError as error:
            await request.state.db.rollback()
            log.exception(f"Exception in db. Rolling back. Details: {error}")
            raise DatabaseException("Database error")
        finally:
            await request.state.db.close()
