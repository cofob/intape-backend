"""Config dependency."""
from fastapi import Request

from intape.core.config import Config


def get_config(request: Request) -> Config:
    """Get config."""
    return request.state.config


__all__ = ["get_config"]
