"""Video schemas."""
from datetime import datetime

from . import fields as f
from .abc import BaseSchema


class BaseVideoSchema(BaseSchema):
    """Base video schema."""

    description: str = f.VIDEO_DESCRIPTION
    tags: list[str] = f.VIDEO_TAGS
    file_cid: str = f.IPFS_CID


class CreateVideoSchema(BaseVideoSchema):
    """Create video schema."""

    pass


class VideoSchema(BaseVideoSchema):
    """Video schema."""

    id: int = f.VIDEO_ID
    created_at: datetime = f.CREATED_AT
    user_id: int = f.USER_ID
    metadata_cid: str = f.IPFS_PATH


class VideoMetadataSchema(BaseSchema):
    """Video metadata schema."""

    description: str = f.VIDEO_DESCRIPTION
    name: str = f.VIDEO_DESCRIPTION
    image: str = f.IPFS_PATH
