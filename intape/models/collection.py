"""Collection models module."""
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from intape.core.database import Base

from .abc import AbstractModel

if TYPE_CHECKING:
    from .user import UserModel
    from .video import VideoModel


class CollectionModel(Base, AbstractModel):
    """Collection model."""

    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id: int = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    user: "UserModel" = relationship("UserModel", lazy="joined")


class CollectionEntryModel(Base, AbstractModel):
    """Collection entry model."""

    __tablename__ = "collection_entries"

    id = Column(Integer, primary_key=True)
    collection_id: int = Column("collection_id", Integer, ForeignKey("collections.id"), nullable=False)
    collection: CollectionModel = relationship("CollectionModel", lazy="joined")
    user_id: int = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    user: "UserModel" = relationship("UserModel", lazy="joined")
    video_id: int = Column("video_id", Integer, ForeignKey("videos.id"), nullable=False)
    video: "VideoModel" = relationship("VideoModel", lazy="joined")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
