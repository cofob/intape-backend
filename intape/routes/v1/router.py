"""Version 1 API."""
from fastapi import APIRouter

from . import auth, collection, file, ping, search, settings, user, video

router = APIRouter(tags=["v1"])
router.include_router(auth.router)
router.include_router(collection.router)
router.include_router(file.router)
router.include_router(ping.router)
router.include_router(search.router)
router.include_router(settings.router)
router.include_router(user.router)
router.include_router(video.router)
