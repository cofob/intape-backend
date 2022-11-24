"""InTape Backend."""
from fastapi import FastAPI

from .app import App


def app() -> FastAPI:
    """Return FastAPI application.

    This function is used by Uvicorn to run the application.
    """
    return App.from_env().app
