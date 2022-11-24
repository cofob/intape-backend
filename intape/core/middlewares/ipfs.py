"""Database middleware."""

import logging

from asyncipfscluster import IPFSClient, exceptions
from fastapi import Request, Response
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp

from intape.core.config import Config
from intape.core.exceptions import IPFSException

log = logging.getLogger(__name__)


class IPFSAsyncSessionMiddleware(BaseHTTPMiddleware):
    """IPFS session middleware."""

    def __init__(self, app: ASGIApp, config: Config) -> None:
        """Initialize."""
        super().__init__(app)
        self.config = config

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Dispatch."""
        try:
            async with IPFSClient(self.config.IPFS_URL, self.config.IPFS_AUTH) as session:
                request.state.ipfs = session
                return await call_next(request)
        except exceptions.IPFSException as error:
            log.exception(f"Exception in IPFS. Details: {error}")
            raise IPFSException("IPFS cluster connection error")
