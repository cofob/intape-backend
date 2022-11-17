"""Authentication routes."""
from secrets import token_urlsafe

from fastapi import APIRouter, Body, Query, Request
from sqlalchemy import select

from intape.core.exceptions import (
    EmailTakenException,
    InvalidCredentialsException,
    UsernameTakenException,
)
from intape.models import UserModel, UserTokenModel
from intape.schemas import (
    ChangeUserPasswordSchema,
    CreateUserSchema,
    LoginUserSchema,
    UserAuthSchema,
)
from intape.utils.passwords import get_password_hash, verify_password

router = APIRouter(tags=["auth"], prefix="/auth")


@router.get("/check_username", response_model=bool)
async def check_username(
    request: Request, username: str = Query(regex=r"^[a-zA-Z0-9_]+$", max_length=16, min_length=3)
) -> bool:
    """Check username.

    Used to check if a username is available.

    Returns `true` if username is available, `false` if username is taken.
    """
    query = await request.state.db.execute(select(UserModel).filter_by(name=username))
    user: UserModel | None = query.scalars().first()
    if user is None:
        return True
    return False


@router.get("/get_salt", response_model=str)
async def get_salt(
    request: Request, username: str = Query(regex=r"^[a-zA-Z0-9_]+$", max_length=16, min_length=3)
) -> str:
    """Get salt.

    Used to get the salt for a user.

    Returns the salt for the user. If the user does not exist, returns an random string.
    """
    query = await request.state.db.execute(select(UserModel).filter_by(name=username))
    user: UserModel | None = query.scalars().first()
    if user is None:
        return token_urlsafe(32)

    if not user.client_salt:
        return ""

    return user.client_salt


@router.post("/register", response_model=UserAuthSchema)
async def register(request: Request, user: CreateUserSchema) -> UserAuthSchema:
    """Register endpoint.

    Used to register a new user.

    Raises:
    - UsernameTakenException: If the username is taken.
    - EmailTakenException: If the email is taken.

    Returns:
    - str: JWT refresh token.
    """
    # TODO: Add captcha
    # TODO: Add email verification
    db = request.state.db

    # Check if username is taken
    query = await db.execute(select(UserModel).filter_by(name=user.name))
    if query.scalars().first() is not None:
        raise UsernameTakenException()

    # Check if email is taken
    query = await db.execute(select(UserModel).filter_by(email=user.email))
    if query.scalars().first() is not None:
        raise EmailTakenException()

    # Hash password
    hashed_password = get_password_hash(user.password)

    # Create user
    db_user = UserModel(name=user.name, email=user.email, password=hashed_password, client_salt=user.client_salt)
    db.add(db_user)
    await db.commit()

    # Return auth info
    refresh_token_model = await UserTokenModel.create(db, db_user.id)
    refresh_token = refresh_token_model.issue_refresh_token()
    access_token = refresh_token_model.issue_access_token()
    return UserAuthSchema(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        refresh_token=refresh_token,
        access_token=access_token,
        session_id=refresh_token_model.id,
    )


@router.post("/login", response_model=UserAuthSchema)
async def login(request: Request, user: LoginUserSchema) -> UserAuthSchema:
    """Login endpoint.

    Used to login a user.

    Raises:
    - InvalidCredentialsException: If the username or password is incorrect.

    Returns:
    - str: JWT refresh token.
    """
    # TODO: Add captcha
    # TODO: Add email notification about new login
    db = request.state.db

    # Get user
    query = await db.execute(select(UserModel).filter_by(name=user.name))
    db_user: UserModel | None = query.scalars().first()
    if db_user is None:
        query = await db.execute(select(UserModel).filter_by(email=user.name))
        db_user = query.scalars().first()
        if db_user is None:
            raise InvalidCredentialsException(detail="Username is incorrect")

    # Verify password
    if not verify_password(user.password, db_user.password):
        raise InvalidCredentialsException(detail="Password is incorrect")

    # Return auth info
    refresh_token_model = await UserTokenModel.create(db, db_user.id)
    refresh_token = refresh_token_model.issue_refresh_token()
    access_token = refresh_token_model.issue_access_token()
    return UserAuthSchema(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        refresh_token=refresh_token,
        access_token=access_token,
        session_id=refresh_token_model.id,
    )


@router.post("/change_password", response_model=bool)
async def change_password(request: Request, form: ChangeUserPasswordSchema) -> bool:
    """Change password endpoint.

    Used to change a user's password. All other sessions will be revoked.

    Raises:
    - InvalidCredentialsException: If the old password is incorrect.

    Returns:
    - bool: True if password was changed.
    """
    # TODO: use authentication provider instead of custom schema field
    db = request.state.db

    # Get refresh token model
    token_model = await UserTokenModel.get_by_access_token(db, form.access_token)
    query = select(UserModel).filter_by(id=token_model.user_id)
    db_user: UserModel = (await db.execute(query)).scalars().first()
    if not db_user:
        raise InvalidCredentialsException(detail="User does not exist")

    # Verify password
    if not verify_password(form.old_password, db_user.password):
        raise InvalidCredentialsException(detail="Old password is incorrect")

    # Hash password
    hashed_password = get_password_hash(form.new_password)

    # Update password and salt
    db_user.password = hashed_password
    if form.client_salt is not None:
        db_user.client_salt = form.client_salt

    db.add(db_user)
    await db.commit()

    # Terminate all other sessions
    query = (
        select(UserTokenModel)
        .filter_by(user_id=db_user.id)
        .where(UserTokenModel.id != token_model.id)
        .where(UserTokenModel.revoked is False)
    )
    sessions: list[UserTokenModel] = (await db.execute(query)).scalars().all()
    for token in sessions:
        token.revoked = True
        db.add(token)

    await db.commit()

    return True


@router.post("/access_token", response_model=str)
async def refresh_access_token(request: Request, refresh_token: str = Body()) -> str:
    """Refresh access token endpoint.

    Used to refresh an access token.

    Raises:
    - InvalidCredentialsException: If the refresh token is invalid.

    Returns:
    - str: JWT access token.
    """
    db = request.state.db

    # Get refresh token model
    refresh_token_model: UserTokenModel = await UserTokenModel.get_by_refresh_token(db, refresh_token)

    # Generate access token
    return refresh_token_model.issue_access_token()
