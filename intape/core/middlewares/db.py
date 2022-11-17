"""Database middleware."""

import logging

from fastapi import Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from intape.core.config import CONFIG

log = logging.getLogger(__name__)
engine = create_async_engine(CONFIG.DATABASE_URL)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class DBAsyncSessionMiddleware(BaseHTTPMiddleware):
    """Database session middleware."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch."""
        response = Response("Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            request.state.db = async_session_maker()
            response = await call_next(request)
        except Exception as error:
            await request.state.db.rollback()
            log.exception(f"Exception in db. Rolling back. Details: {error}")
        finally:
            await request.state.db.close()

        return response
