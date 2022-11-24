"""User-related endpoints."""
from fastapi import APIRouter, Path, Request

from intape.core.exceptions import UserNotFoundException
from intape.models import UserModel
from intape.schemas import PublicUserSchema

router = APIRouter(tags=["user"], prefix="/user")


@router.get("/{username}", response_model=PublicUserSchema)
async def get_user_info(
    request: Request,
    username: str | None = Path(min_length=3, max_length=16, regex=r"^[a-zA-Z0-9_]+$", default=None),
) -> PublicUserSchema:
    """Get user info.

    Used to get the info of a user.

    Returns:
    - PublicUserSchema: Info of the user.
    """
    db_user: UserModel | None = await UserModel.get_by_key(request.state.db, UserModel.name, username)
    if db_user is None:
        raise UserNotFoundException()
    return PublicUserSchema.from_orm(db_user)
