"""File related exceptions."""
from .abc import AbstractException


class BaseFileException(AbstractException):
    """Base file exception."""


class UnsupportedMimeTypeException(BaseFileException):
    """Exception raised when the video has an unsupported mime type.

    This exception is used when the file has an unsupported mime type.

    For example, when the video has a mime type of "image/png".
    """


class FileAlreadyExistsException(BaseFileException):
    """Exception raised when a file already exists."""


class FileNotFoundException(BaseFileException):
    """Exception raised when a file is not found.

    This exception is used when the file is not found.

    For example, when the file CID is invalid.
    """

    status_code = 404
