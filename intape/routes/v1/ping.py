"""Ping endpoint."""
from fastapi import APIRouter

router = APIRouter(tags=["ping"], prefix="/ping")


@router.get("/", response_model=str)
async def ping() -> str:
    """Ping endpoint.

    Used to check if the API is up. Returns "ok" if it is.
    Used in docker container to set healthly status.
    """
    return "ok"
