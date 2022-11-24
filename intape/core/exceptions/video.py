"""Video exceptions."""
from .abc import AbstractException


class VideoException(AbstractException):
    """Base video exception."""

    pass


class VideoNotFoundException(VideoException):
    """Video not found exception.

    This exception is used when the video is not found.

    For example, when the video ID is invalid.
    """

    status_code = 404
