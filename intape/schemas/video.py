"""Video schemas."""
from datetime import datetime

from pydantic import BaseModel, Field

from .user import PublicUserSchema


class BaseVideoSchema(BaseModel):
    """Base video schema."""

    description: str = Field(description="Video description.", max_length=150, min_length=3)
    tags: list[str] = Field(description="Video tags.", max_length=16, min_length=1)
    file_cid: str = Field(description="Video file CID.", max_length=128, min_length=10)


class CreateVideoSchema(BaseVideoSchema):
    """Create video schema."""

    pass


class VideoSchema(BaseVideoSchema):
    """Video schema."""

    id: int = Field(description="Video ID.")
    created_at: datetime = Field(description="Video creation date.")
    user: PublicUserSchema = Field(description="Video author.")

    class Config:
        """Config."""

        orm_mode = True
