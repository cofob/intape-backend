"""Abstract base classes for exceptions."""
from abc import ABCMeta

from fastapi import status


class AbstractException(Exception, metaclass=ABCMeta):
    """Abstract exception.

    All custom exceptions must inherit from this class.
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        detail: str | None = None,
        status_code: int | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Exception init method.

        Args:
            detail: Short error description.
            status_code: HTTP status code that will be returned.
            headers: Dict with HTTP headers that will be returned.
        """
        # If detail is specified, then pass it to Exception() constructor.
        # This logs the exception with detail to the console.
        if detail is not None:
            super().__init__(detail)

        self.detail = detail
        self.headers = headers
        if status_code is not None:
            self.status_code = status_code
