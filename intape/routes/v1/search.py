"""Search endpoints."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intape.dependencies import get_db
from intape.models import UserModel, VideoModel
from intape.schemas.user import PublicUserSchema
from intape.schemas.video import VideoSchema

router = APIRouter(tags=["search"], prefix="/search")


@router.get("/videos", response_model=list[VideoSchema])
async def search_videos(
    *,
    db: AsyncSession = Depends(get_db),
    query: str = Query(),
) -> list[VideoSchema]:
    """Search videos.

    Used to search for videos.

    Returns:
    - list[VideoModel]: List of videos.
    """
    query = select(VideoModel).where(VideoModel.description.like(f"%{query}%"))
    videos = (await db.execute(query)).scalars().all()
    return [VideoSchema.from_orm(video) for video in videos]


@router.get("/users", response_model=list[PublicUserSchema])
async def search_users(
    *,
    db: AsyncSession = Depends(get_db),
    query: str = Query(),
) -> list[PublicUserSchema]:
    """Search users.

    Used to search for users.

    Returns:
    - list[PublicUserSchema]: List of users.
    """
    query = select(UserModel).where(UserModel.username.like(f"%{query}%"))
    users = (await db.execute(query)).scalars().all()
    return [PublicUserSchema.from_orm(user) for user in users]
