"""Version 1 API."""
from fastapi import APIRouter

from . import auth, file, ping, user, video

router = APIRouter(tags=["v1"])
router.include_router(ping.router)
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(video.router)
router.include_router(file.router)
