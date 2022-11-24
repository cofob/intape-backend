"""Authorization-related dependencies."""
from fastapi import Depends, Request

from intape.core.config import Config
from intape.core.exceptions import (
    AbstractException,
    AuthenticationRequiredException,
    InvalidCredentialsException,
)
from intape.core.security import oauth2_scheme
from intape.models import UserModel, UserTokenModel

from .config import get_config


async def get_current_session(
    request: Request, token: str = Depends(oauth2_scheme), config: Config = Depends(get_config)
) -> UserTokenModel:
    """Get current session."""
    db = request.state.db
    if token is None:
        raise AuthenticationRequiredException(detail="Authentication credentials were not provided.")
    try:
        token_model = await UserTokenModel.get_by_access_token(config, db, token)
    except AbstractException:
        raise InvalidCredentialsException()
    return token_model


async def get_current_user(request: Request, token_model: UserTokenModel = Depends(get_current_session)) -> UserModel:
    """Get current user."""
    db = request.state.db
    try:
        user = await UserModel.get_by_id(db, token_model.user_id)
    except AbstractException:
        raise InvalidCredentialsException()
    return user
