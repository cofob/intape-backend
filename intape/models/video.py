"""Video database model."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from intape.core.database import Base

from .abc import AbstractModel

if TYPE_CHECKING:
    from .file import FileModel
    from .user import UserModel


class VideoModel(Base, AbstractModel):
    """Video model."""

    __tablename__ = "videos"

    id: int = Column("id", Integer, primary_key=True, index=True)
    description: str = Column("description", String(150), nullable=False)
    tags: list[str] = Column("tags", ARRAY(String(16)), nullable=False)
    created_at: datetime = Column("created_at", DateTime(timezone=True), server_default=func.now())
    is_deleted: bool = Column("is_deleted", Boolean, nullable=False, default=False)

    user_id: int = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    user: "UserModel" = relationship("UserModel", lazy="joined")

    file_cid: str = Column("file_cid", String(128), ForeignKey("files.cid"), nullable=False)
    file: "FileModel" = relationship("FileModel", lazy="joined")
