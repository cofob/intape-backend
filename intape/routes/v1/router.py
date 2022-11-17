"""Version 1 API."""
from fastapi import APIRouter

from . import auth, ping

router = APIRouter(tags=["v1"])
router.include_router(ping.router)
router.include_router(auth.router)
