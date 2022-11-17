"""Authorization exceptions."""
from .abc import AbstractException


class UsernameTakenException(AbstractException):
    """Username taken exception.

    This exception is used when the username is already taken.
    """

    pass


class EmailTakenException(AbstractException):
    """Email taken exception.

    This exception is used when the email is already taken.
    """

    pass


class InvalidCredentialsException(AbstractException):
    """Invalid credentials exception.

    This exception is used when the credentials are invalid.

    For example, when the username or password pair is incorrect.
    """

    pass
