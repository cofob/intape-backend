"""Ping endpoint."""
from datetime import datetime, timedelta

from asyncipfscluster import IPFSClient
from fastapi import APIRouter, Depends, Request, UploadFile
from pytz import UTC

from intape.core.exceptions import FileAlreadyExistsException
from intape.dependencies import get_current_user, get_ipfs
from intape.models import FileModel, UserModel

router = APIRouter(tags=["file"], prefix="/file")


@router.post("/upload", response_model=str)
async def upload_file(
    *,
    request: Request,
    ipfs: IPFSClient = Depends(get_ipfs),
    user: UserModel = Depends(get_current_user),
    file: UploadFile,
) -> str:
    """Upload a file.

    Uploads a file to IPFS and returns the CID.

    The file is stored for 10 minutes. If it receives no relation
    anywhere, it is deleted.

    File size is limited to 8MB on reverse proxy.

    Returns:
    - str: The CID of the uploaded file.
    """
    db = request.state.db

    file_content = await file.read()
    cid: str = await ipfs.add_bytes(file_content, file.content_type, file.filename, "InTape")

    try:
        await FileModel.create_obj(
            db,
            user,
            cid=cid,
            mime_type=file.content_type,
            remove_at=datetime.now(tz=UTC) + timedelta(minutes=10),
        )
    except FileAlreadyExistsException:
        pass

    return cid
