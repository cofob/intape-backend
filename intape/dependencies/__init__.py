"""Module containing all FastAPI Depend() functions.

All dependencies must be re-exported in this module.
"""
from .database import get_db

__all__ = ["get_db"]
