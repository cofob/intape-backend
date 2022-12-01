"""Authentication routes."""

from secrets import token_hex

from fastapi import APIRouter, Body, Depends, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intape.core.config import Config
from intape.core.exceptions import (
    EthAddressTakenException,
    InvalidCredentialsException,
    ReservedUsernameException,
    UsernameTakenException,
)
from intape.dependencies import get_config, get_current_user, get_db
from intape.models import UserModel, UserTokenModel
from intape.schemas.user import (
    ConfirmationSignatureSchema,
    ConfitmationSignatureRequestSchema,
    CreateUserSchema,
    LoginUserSchema,
    PublicUserSchema,
    UserAuthSchema,
)
from intape.utils.auth import (
    confirm_user_signature,
    generate_confirmation_text,
    generate_confirmation_token,
    is_username_reserved,
)

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/request_confirmation", response_model=ConfirmationSignatureSchema)
async def request_confirmation(
    *, config: Config = Depends(get_config), signature_request: ConfitmationSignatureRequestSchema
) -> ConfirmationSignatureSchema:
    """Request confirmation signature.

    Used to request a confirmation signature.

    Returns:
    - ConfirmationSignatureSchema: Confirmation signature.
    """
    data = token_hex(32)
    jwt = generate_confirmation_token(config, signature_request.eth_address, data)
    return ConfirmationSignatureSchema(confirmation_jwt=jwt, data=generate_confirmation_text(data))


@router.post("/register", response_model=UserAuthSchema)
async def register(
    *, db: AsyncSession = Depends(get_db), config: Config = Depends(get_config), user: CreateUserSchema
) -> UserAuthSchema:
    """Register endpoint.

    Used to register a new user.

    Raises:
    - UsernameTakenException: If the username is taken.
    - EthAddressTakenException: If the Ethereum address is taken.
    - InvalidCredentialsException: If the signature is invalid.
    - ReservedUsernameException: If the username is reserved.

    Returns:
    - UserAuthSchema: User authentication schema with JWT tokens.
    """
    # TODO: Add captcha
    eth_address = confirm_user_signature(config, user.confirmation_jwt, user.signature)

    if is_username_reserved(user.username):
        raise ReservedUsernameException(detail="Username is reserved.")

    # Check if username is taken
    query = await db.execute(select(UserModel).filter_by(username=user.username))
    if query.scalars().first() is not None:
        raise UsernameTakenException()

    # Check if eth address is taken
    query = await db.execute(select(UserModel).filter_by(eth_address=eth_address))
    if query.scalars().first() is not None:
        raise EthAddressTakenException()

    # Create user
    db_user = UserModel(username=user.username, eth_address=eth_address)
    await db_user.save(db)

    # Return auth info
    refresh_token_model = await UserTokenModel.create_obj(db, db_user.id)
    refresh_token = refresh_token_model.issue_refresh_token(config)
    access_token = refresh_token_model.issue_access_token(config)
    return UserAuthSchema(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        refresh_token=refresh_token,
        access_token=access_token,
        session_id=refresh_token_model.id,
    )


@router.post("/login", response_model=UserAuthSchema)
async def login(
    *, db: AsyncSession = Depends(get_db), config: Config = Depends(get_config), user: LoginUserSchema
) -> UserAuthSchema:
    """Login endpoint.

    Used to login a user.

    Raises:
    - InvalidCredentialsException: If the credentials are invalid.

    Returns:
    - UserAuthSchema: User authentication schema with JWT tokens.
    """
    eth_address = confirm_user_signature(config, user.confirmation_jwt, user.signature)

    # Get user by eth address
    db_user: UserModel | None = await UserModel.get_by_key(db, UserModel.eth_address, eth_address)
    if db_user is None:
        raise InvalidCredentialsException(detail="User not found.")

    # Return auth info
    refresh_token_model = await UserTokenModel.create_obj(db, db_user.id)
    refresh_token = refresh_token_model.issue_refresh_token(config)
    access_token = refresh_token_model.issue_access_token(config)
    return UserAuthSchema(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        refresh_token=refresh_token,
        access_token=access_token,
        session_id=refresh_token_model.id,
    )


@router.post("/access_token", response_model=str)
async def refresh_access_token(
    request: Request, config: Config = Depends(get_config), refresh_token: str = Body()
) -> str:
    """Refresh access token endpoint.

    Used to refresh an access token.

    Raises:
    - InvalidCredentialsException: If the refresh token is invalid.

    Returns:
    - str: JWT access token.
    """
    db = request.state.db

    # Get refresh token model
    refresh_token_model: UserTokenModel = await UserTokenModel.get_by_refresh_token(config, db, refresh_token)

    # Save, to update "updated_at" field
    await refresh_token_model.save(db)

    # Generate access token
    return refresh_token_model.issue_access_token(config)


@router.get("/check_auth", response_model=PublicUserSchema)
async def check_auth(db_user: UserModel = Depends(get_current_user)) -> PublicUserSchema:
    """Check auth endpoint.

    Used to check if a user is authenticated.

    Raises:
    - InvalidCredentialsException: If the access token is invalid.

    Returns:
    - PublicUserSchema: User data.
    """
    return db_user.to_public()


@router.get("/check_username", response_model=bool)
async def check_username(
    *, db: AsyncSession = Depends(get_db), username: str = Query(regex=r"^[a-zA-Z0-9_]+$", max_length=16, min_length=3)
) -> bool:
    """Check username.

    Used to check if a username is available.

    Returns:
    - bool: `true` if username is available, `false` if username is taken.
    """
    if is_username_reserved(username):
        raise ReservedUsernameException(detail="Username is reserved.")
    user: UserModel | None = await UserModel.get_by_key(db, UserModel.username, username)
    if user is None:
        return True
    return False
