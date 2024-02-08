"""Ping endpoint."""
from fastapi import APIRouter

from intape.core.exceptions.handler import ErrorSchema

router = APIRouter(tags=["ping"], prefix="/ping")


@router.get("/", response_model=str, responses={500: {"model": ErrorSchema}})
async def ping() -> str:
    """Ping endpoint.

    Used to check if the API is up. Returns "ok" if it is.
    Used in docker container to set healthly status.
    """
    return "ok"
