"""Default exception handlers for the intape package."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .abc import AbstractException


class ErrorSchema(BaseModel):
    """Error response for AbstractException."""

    ok: bool = False
    status_code: int = 500
    error_code: str = "Exception"
    error_code_description: str | None = None
    detail: str | None = None


def register_exception_handler(app: FastAPI) -> None:
    """Register exception handlers."""

    @app.exception_handler(AbstractException)
    async def abstract_exception_handler(request: Request, exc: AbstractException) -> JSONResponse:
        """Exception handler for AbstractException.

        Returns:
            JSON serialized ErrorModel.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorSchema(
                error_code=exc.__class__.__name__,
                detail=exc.detail if exc.detail is not None else exc.__class__.__doc__,
                status_code=exc.status_code,
                error_code_description=exc.__class__.__doc__,
            ).dict(),
            headers=exc.headers,
        )
