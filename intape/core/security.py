"""Security variables and functions."""
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/auth/login",
    auto_error=False,
    description="User authorization. Access token valid for 15 minutes. Cant be used inside Swagger UI.",
)
