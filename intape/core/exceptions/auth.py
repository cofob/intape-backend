"""Authorization exceptions."""
from .abc import AbstractException


class AuthException(AbstractException):
    """Base authorization exception."""

    pass


class UsernameTakenException(AuthException):
    """Username taken exception.

    This exception is used when the username is already taken.
    """

    pass


class ReservedUsernameException(UsernameTakenException):
    """Reserved username exception.

    This exception is used when the username is reserved.
    """

    pass


class EmailTakenException(AuthException):
    """Email taken exception.

    This exception is used when the email is already taken.
    """

    pass


class InvalidCredentialsException(AuthException):
    """Invalid credentials exception.

    This exception is used when the credentials are invalid.

    For example, when the username or password pair is incorrect.
    """

    status_code = 401


class AuthenticationRequiredException(AuthException):
    """Authentication required exception.

    This exception is used when the user is not authenticated.

    For example, when authentication headers are missing.
    """

    pass


class UserNotFoundException(AuthException):
    """User not found exception.

    This exception is used when the user is not found.

    For example, when the user ID is incorrect.
    """

    status_code = 404


class InsufficientPermissionsException(AuthException):
    """Insufficient permissions exception.

    This exception is used when the user does not have sufficient permissions.

    For example, when the user tries to delete a video, but they are not the
    owner of the video.
    """

    status_code = 403
