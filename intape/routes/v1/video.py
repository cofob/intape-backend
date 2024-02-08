"""Video endpoint."""
from asyncipfscluster import IPFSClient
from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intape.core.exceptions import (
    FileNotFoundException,
    InsufficientPermissionsException,
    UnsupportedMimeTypeException,
    VideoNotFoundException,
)
from intape.dependencies import get_current_user, get_db, get_ipfs
from intape.models import FileModel, UserModel, VideoModel
from intape.schemas.video import CreateVideoSchema, VideoSchema

router = APIRouter(tags=["video"], prefix="/video")


@router.get("/", response_model=list[VideoSchema])
async def get_videos(
    request: Request, _user: UserModel = Depends(get_current_user), offset: int = 0
) -> list[VideoSchema]:
    """Get videos.

    Get videos in local timeline.

    Returns:
    - list[VideoSchema]: List of videos. Limited to 10 videos.
    """
    db = request.state.db
    query = (
        select(VideoModel).filter_by(is_deleted=False).order_by(VideoModel.created_at.desc()).offset(offset).limit(10)
    )
    videos: list[VideoModel] = (await db.execute(query)).scalars().all()
    return [VideoSchema.from_orm(video) for video in videos]


@router.post("/", response_model=VideoSchema)
async def create_video(
    *,
    db: AsyncSession = Depends(get_db),
    ipfs: IPFSClient = Depends(get_ipfs),
    user: UserModel = Depends(get_current_user),
    video: CreateVideoSchema,
) -> VideoSchema:
    """Create video.

    Create a new video.

    Raises:
    - FileNotFoundException: If the file CID is not found in the database.
    - UnsupportedMimeTypeException: If the file CID is not a video.

    Returns:
    - VideoSchema: Created video.
    """
    # Get file
    query = select(FileModel).where(FileModel.cid == video.file_cid)
    file: FileModel | None = (await db.execute(query)).scalars().first()
    if not file:
        raise FileNotFoundException()
    if not file.mime_type.startswith("video/"):
        raise UnsupportedMimeTypeException(detail="Only video files are supported.")

    # Create video
    db_video = VideoModel(**video.dict(), user_id=user.id)
    db_video.metadata_cid = await db_video.get_metadata_cid(db, ipfs)

    # Save file
    file.remove_at = None

    db.add(db_video)
    db.add(file)

    await db.commit()

    # Get video from database.
    # SA for some reason doesn't return the video correctly and
    # raises greenlet error with the user relation.
    db_video: VideoModel | None = await VideoModel.get(db, db_video.id)
    if not db_video:
        raise VideoNotFoundException(detail="Video was not created.")

    return VideoSchema.from_orm(db_video)


@router.post("/{video_id}/set_tx", response_model=bool)
async def set_video_tx(
    *,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
    video_id: int,
    tx_hash: str = Body(embed=True),
) -> bool:
    """Set video transaction hash.

    Returns:
    - bool: True if the video was updated. False if the video already has a transaction hash.

    Raises:
    - VideoNotFoundException: If the video is not found.
    - InsufficientPermissionsException: If the user is not the owner of the video.
    """
    # Get video
    db_video: VideoModel | None = await VideoModel.get(db, video_id)
    if not db_video:
        raise VideoNotFoundException()

    # Check permissions
    if db_video.user_id != user.id:
        raise InsufficientPermissionsException()

    # Check if tx hash is already set
    if db_video.tx_hash:
        return False

    # Set tx hash
    db_video.tx_hash = tx_hash
    await db_video.save(db)

    return True


@router.get("/{video_id}", response_model=VideoSchema)
async def get_video(*, request: Request, video_id: int) -> VideoSchema:
    """Get video.

    Get a video by ID.

    Raises:
    - VideoNotFoundException: If the video is not found or is deleted.

    Returns:
    - VideoSchema: Video.
    """
    db = request.state.db
    query = select(VideoModel).filter_by(id=video_id)
    video: VideoModel | None = (await db.execute(query)).scalars().first()
    if not video:
        raise VideoNotFoundException(detail="Video not found.")
    if video.is_deleted:
        raise VideoNotFoundException(detail="Video is deleted.")
    return VideoSchema.from_orm(video)


@router.delete("/{video_id}", response_model=bool)
async def hide_video(*, request: Request, user: UserModel = Depends(get_current_user), video_id: int) -> bool:
    """Hide video.

    Hide a video by ID. Video can't be deleted, only hidden (because of the IPFS & blockchain).

    This action is irreversible.

    Raises:
    - VideoNotFoundException: If the video is not found or is deleted.
    - InsufficientPermissionsException: If the user is not the owner of the video.

    Returns:
    - bool: True if the video was deleted.
    """
    db = request.state.db
    query = select(VideoModel).filter_by(id=video_id)
    video: VideoModel | None = (await db.execute(query)).scalars().first()
    if not video:
        raise VideoNotFoundException()
    if video.user_id != user.id:
        raise InsufficientPermissionsException(detail="You can only hide your own videos.")
    video.is_deleted = True
    db.add(video)
    await db.commit()
    return True
