"""File model."""
from datetime import datetime
from typing import TYPE_CHECKING

from asyncipfscluster import IPFSClient
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from intape.core.database import Base
from intape.core.exceptions import (
    FileAlreadyExistsException,
    FileNotFoundException,
)

from .abc import AbstractModel

if TYPE_CHECKING:
    from .user import UserModel


class FileModel(Base, AbstractModel):
    """File model."""

    __tablename__ = "files"

    cid = Column("cid", String(128), primary_key=True, unique=True, index=True)
    mime_type: str = Column("mime_type", String(32), nullable=False)
    user_id: int = Column("user_id", Integer, ForeignKey("users.id"), nullable=False)
    user: "UserModel" = relationship("UserModel", lazy="joined")
    created_at: datetime = Column("created_at", DateTime(timezone=True), server_default=func.now())
    remove_at: datetime | None = Column("remove_at", DateTime(timezone=True), nullable=True)

    @classmethod
    async def get_by_cid(cls, db: AsyncSession, cid: str) -> "FileModel":
        """Get file by cid.

        Args:
            db (AsyncSession): Database session.
            cid (str): File cid.

        Returns:
            FileModel: File model.

        Raises:
            FileNotFoundException: If the file is not found.
        """
        query = await db.execute(select(cls).filter_by(cid=cid))
        file: FileModel | None = query.scalars().first()
        if file is None:
            raise FileNotFoundException()
        return file

    @classmethod
    async def create_obj(
        cls, db: AsyncSession, user: "UserModel", cid: str, mime_type: str, remove_at: datetime | None = None
    ) -> "FileModel":
        """Create new file.

        Args:
            db (AsyncSession): Database session.
            user (UserModel): User that uploaded this file.
            cid (str): File cid.
            mime_type (str): File mime type.
            remove_at (datetime): File remove date.

        Returns:
            FileModel: File model.

        Raises:
            FileAlreadyExistsException: If the file already exists.
        """
        file = cls(cid=cid, mime_type=mime_type, user=user, remove_at=remove_at)
        try:
            db.add(file)
            await db.commit()
        except Exception:
            await db.rollback()
            raise FileAlreadyExistsException()
        return file

    async def remove_all(self, db: AsyncSession, ipfs: IPFSClient) -> None:
        """Remove file.

        Args:
            db (AsyncSession): Database session.
            ipfs (IPFSClient): IPFS client.
        """
        await db.delete(self)
        await db.commit()
        await ipfs.remove(self.cid)
