"""Collection schemas."""

from datetime import datetime

from . import fields as f
from .abc import BaseSchema


class BaseCollectionSchema(BaseSchema):
    """Base collection schema."""

    name: str = f.COLLECTION_NAME
    description: str = f.COLLECTION_DESCRIPTION
    is_public: bool = f.COLLECTION_IS_PUBLIC


class CreateCollectionSchema(BaseCollectionSchema):
    """Create collection schema."""

    pass


class CollectionSchema(BaseCollectionSchema):
    """Collection schema."""

    id: int = f.COLLECTION_ID
    user_id: int = f.USER_ID
    created_at: datetime = f.CREATED_AT
    updated_at: datetime = f.UPDATED_AT


class BaseCollectionEntrySchema(BaseSchema):
    """Base collection entry schema."""

    video_id: int = f.VIDEO_ID


class CreateCollectionEntrySchema(BaseCollectionEntrySchema):
    """Create collection entry schema."""

    pass


class CollectionEntrySchema(BaseCollectionEntrySchema):
    """Collection entry schema."""

    id: int = f.COLLECTION_ENTRY_ID
    user_id: int = f.USER_ID
    collection_id: int = f.COLLECTION_ID
    created_at: datetime = f.CREATED_AT
