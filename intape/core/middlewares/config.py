"""Database middleware."""

from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp

from intape.core.config import Config


class ConfigMiddleware(BaseHTTPMiddleware):
    """Config middleware.

    Sets the config object in the request state.
    """

    def __init__(self, app: ASGIApp, config: Config) -> None:
        """Initialize."""
        super().__init__(app)
        self.config = config

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch."""
        request.state.config = self.config
        return await call_next(request)
