"""Module containing all FastAPI Depend() functions.

All dependencies must be re-exported in this module.
"""
from .auth import get_current_session, get_current_user
from .config import get_config
from .database import get_db, get_db_deprecated
from .ipfs import get_ipfs, get_ipfs_deprecated

__all__ = [
    "get_db_deprecated",
    "get_current_user",
    "get_current_session",
    "get_ipfs_deprecated",
    "get_db",
    "get_config",
    "get_ipfs",
]
