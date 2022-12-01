"""Settings endpoints."""

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from intape.core.exceptions.file import FileNotFoundException
from intape.dependencies import get_current_user, get_db
from intape.models import FileModel, UserModel

router = APIRouter(tags=["settings"], prefix="/settings")


@router.post("/update_avatar", response_model=bool)
async def update_avatar(
    *,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
    avatar_cid: str = Body(embed=True),
) -> bool:
    """Update avatar.

    Used to update the avatar of the user.

    Returns:
    - bool: True if the avatar was updated.
    """
    avatar: FileModel | None = await FileModel.get_by_key(db, FileModel.cid, avatar_cid)
    if avatar is None:
        raise FileNotFoundException()
    user.avatar_cid = avatar.cid
    await user.save(db)
    return True


@router.post("/update_username", response_model=bool)
async def update_username(
    *,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
    username: str = Body(embed=True),
) -> bool:
    """Update username.

    Used to update the username of the user.

    Returns:
    - bool: True if the username was updated. False if the username is already taken.
    """
    # Check if the username is already taken
    if await UserModel.get_by_key(db, UserModel.username, username) is not None:
        return False
    user.username = username
    await user.save(db)
    return True


@router.post("/update_email", response_model=bool)
async def update_email(
    *,
    db: AsyncSession = Depends(get_db),
    user: UserModel = Depends(get_current_user),
    email: str = Body(embed=True),
    is_public: bool = Body(embed=True),
) -> bool:
    """Update email.

    Used to update the email of the user.

    Returns:
    - bool: True if the email was updated. False if the email is already taken.
    """
    # Check if the email is already taken
    if await UserModel.get_by_key(db, UserModel.email, email) is not None:
        return False
    user.email = email
    user.is_email_verified = False
    user.is_email_public = is_public
    await user.save(db)
    return True
