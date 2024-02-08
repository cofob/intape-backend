"""Collection endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from intape.core.exceptions import (
    CollectionEntryAlreadyExists,
    CollectionEntryNotFound,
    CollectionNotFound,
    InsufficientPermissionsException,
    VideoNotConfirmedException,
    VideoNotFoundException,
    VideoNotYetConfirmedException,
)
from intape.dependencies import get_current_user, get_db
from intape.models import (
    CollectionEntryModel,
    CollectionModel,
    UserModel,
    VideoModel,
)
from intape.schemas.collection import (
    CollectionEntrySchema,
    CollectionSchema,
    CreateCollectionEntrySchema,
    CreateCollectionSchema,
)

router = APIRouter(tags=["collection"], prefix="/collection")


@router.post("/", response_model=CollectionSchema)
async def create_collection(
    collection: CreateCollectionSchema,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> CollectionSchema:
    """Create a collection.

    Returns:
    - CollectionSchema: The created collection.
    """
    db_collection = CollectionModel.from_schema(collection)
    db_collection.user = user
    await db_collection.save(db)
    return CollectionSchema.from_orm(db_collection)


@router.get("/{collection_id}", response_model=CollectionSchema)
async def get_collection(
    collection_id: int,
    db: AsyncSession = Depends(get_db),
) -> CollectionSchema:
    """Get a collection.

    Raises:
    - CollectionNotFound: If the collection does not exist.

    Returns:
    - CollectionSchema: The collection.
    """
    db_collection = await CollectionModel.get(db, collection_id)
    if db_collection is None:
        raise CollectionNotFound()
    return CollectionSchema.from_orm(db_collection)


@router.post("/{collection_id}/entry", response_model=CollectionEntrySchema)
async def create_collection_entry(
    collection_id: int,
    collection_entry: CreateCollectionEntrySchema,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
) -> CollectionEntrySchema:
    """Create a collection entry.

    Raises:
    - CollectionNotFound: If the collection does not exist.
    - VideoNotFoundException: If the video does not exist.
    - VideoNotYetConfirmedException: If the video has minted NFT, but not confirmed.
    - VideoNotConfirmedException: If the video has not NFT minted.

    Returns:
    - CollectionEntrySchema: The created collection entry.
    """
    # Check if the collection exists.
    db_collection = await CollectionModel.get(db, collection_id)
    if db_collection is None:
        raise CollectionNotFound()

    # Check if the video exists.
    db_video = await VideoModel.get(db, collection_entry.video_id)
    if db_video is None:
        raise VideoNotFoundException()
    if db_video.user_id != user.id:
        raise InsufficientPermissionsException(detail="You do not own this video.")
    if db_video.tx_hash is not None and not db_video.is_confirmed:
        raise VideoNotYetConfirmedException()
    if not db_video.is_confirmed:
        raise VideoNotConfirmedException()

    # Check if user has permission to add this video to the collection.
    if not db_collection.is_public:
        if db_collection.user_id != user.id:
            raise InsufficientPermissionsException(detail="Collection is private")

    # Check if the entry already exists.
    entry = await CollectionEntryModel.get_by_keys(db, collection_id=collection_id, video_id=collection_entry.video_id)
    if entry is not None:
        raise CollectionEntryAlreadyExists()

    # Create the entry.
    db_collection_entry = CollectionEntryModel.from_schema(collection_entry)
    db_collection_entry.user_id = user.id
    db_collection_entry.collection_id = collection_id
    await db_collection_entry.save(db)

    return CollectionEntrySchema.from_orm(db_collection_entry)


@router.get("/{collection_id}/entry", response_model=list[CollectionEntrySchema])
async def get_collection_entries(
    collection_id: int,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
) -> list[CollectionEntrySchema]:
    """Get a collection's entries.

    Raises:
    - CollectionNotFound: If the collection does not exist.

    Returns:
    - list[CollectionEntrySchema]: The collection's entries.
    """
    # Check if the collection exists.
    db_collection = await CollectionModel.get(db, collection_id)
    if db_collection is None:
        raise CollectionNotFound()

    db_collection_entries = await CollectionEntryModel.get_list_by_key(
        db, CollectionEntryModel.collection_id, collection_id, limit, offset
    )
    return [CollectionEntrySchema.from_orm(db_collection_entry) for db_collection_entry in db_collection_entries]


@router.get("/{collection_id}/entry/{collection_entry_id}", response_model=CollectionEntrySchema)
async def get_collection_entry(
    collection_id: int,
    collection_entry_id: int,
    db: AsyncSession = Depends(get_db),
) -> CollectionEntrySchema:
    """Get a collection entry.

    Raises:
    - CollectionNotFound: If the collection does not exist.
    - CollectionEntryNotFound: If the collection entry does not exist.

    Returns:
    - CollectionEntrySchema: The collection entry.
    """
    # Check if the collection exists.
    db_collection = await CollectionModel.get(db, collection_id)
    if db_collection is None:
        raise CollectionNotFound()

    db_collection_entry = await CollectionEntryModel.get(db, collection_entry_id)
    if db_collection_entry is None:
        raise CollectionEntryNotFound()
    return CollectionEntrySchema.from_orm(db_collection_entry)
