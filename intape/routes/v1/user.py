"""User-related endpoints."""
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from intape.core.exceptions import UserNotFoundException
from intape.dependencies import get_db
from intape.models import CollectionModel, UserModel, VideoModel
from intape.schemas.collection import CollectionSchema
from intape.schemas.user import PublicUserSchema
from intape.schemas.video import VideoSchema

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/{username_or_id}", response_model=PublicUserSchema)
async def get_user_info(
    *,
    db: AsyncSession = Depends(get_db),
    username_or_id: str,
) -> PublicUserSchema:
    """Get user info.

    Used to get the info of a user.

    Raises:
    - UserNotFoundException: If the user is not found.

    Returns:
    - PublicUserSchema: Info of the user.
    """
    if username_or_id[0].isdecimal():
        user = await UserModel.get_by_key(db, UserModel.id, int(username_or_id))
    else:
        user = await UserModel.get_by_key(db, UserModel.username, username_or_id)
    if user is None:
        raise UserNotFoundException()
    return user.to_public()


@router.get("/{username}/videos", response_model=list[VideoSchema])
async def get_user_videos(
    *,
    db: AsyncSession = Depends(get_db),
    username: str = Path(min_length=3, max_length=16, regex=r"^[a-zA-Z0-9_]+$"),
    page: int = 0,
) -> list[VideoSchema]:
    """Get user videos.

    Used to get the videos of a user.

    Raises:
    - UserNotFoundException: If the user is not found.

    Returns:
    - list[VideoSchema]: List of videos.
    """
    user = await UserModel.get_by_key(db, UserModel.username, username)
    if user is None:
        raise UserNotFoundException()
    videos = await VideoModel.get_list_by_keys(
        db, limit=10, offset=10 * page, user_id=user.id, is_deleted=False, is_confirmed=True
    )
    return [VideoSchema.from_orm(video) for video in videos]


@router.get("/{username}/collections", response_model=list[CollectionSchema])
async def get_user_collections(
    *,
    db: AsyncSession = Depends(get_db),
    username: str = Path(min_length=3, max_length=16, regex=r"^[a-zA-Z0-9_]+$"),
    page: int = 0,
) -> list[CollectionSchema]:
    """Get user collections.

    Used to get the collections of a user.

    Raises:
    - UserNotFoundException: If the user is not found.

    Returns:
    - list[CollectionSchema]: List of collections.
    """
    user = await UserModel.get_by_key(db, UserModel.username, username)
    if user is None:
        raise UserNotFoundException()
    collections = await CollectionModel.get_list_by_keys(db, limit=10, offset=10 * page, user_id=user.id)
    return [CollectionSchema.from_orm(collection) for collection in collections]
