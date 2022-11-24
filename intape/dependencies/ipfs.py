"""Dependencies for the IPFS."""
from typing import AsyncGenerator

from asyncipfscluster import IPFSClient
from fastapi import Request

from intape.core.config import Config

__all__ = ["get_ipfs_instance_deprecated", "get_ipfs_deprecated", "get_ipfs"]


def get_ipfs_instance_deprecated(config: Config) -> IPFSClient:
    """Get IPFS instance.

    *Deprecated*: Use request.state.ipfs instead.

    Returns:
        IPFSClient: Prepared IPFS session.
    """
    return IPFSClient(config.IPFS_URL, config.IPFS_AUTH)


async def get_ipfs_deprecated(config: Config) -> AsyncGenerator[IPFSClient, None]:
    """Generate IPFS session.

    *Deprecated*: Use request.state.ipfs instead or get_ipfs.

    Returns:
        IPFSClient: Prepared IPFS session.
    """
    # TODO: Add support for authentication
    async with get_ipfs_instance_deprecated(config) as client:
        yield client


def get_ipfs(request: Request) -> IPFSClient:
    """Get IPFS session from request.

    Returns:
        IPFSClient: Prepared IPFS session.
    """
    return request.state.ipfs
