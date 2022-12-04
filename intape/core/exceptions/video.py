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


class VideoNotConfirmedException(VideoException):
    """Video not confirmed exception.

    This exception is used when the video is not confirmed.

    For example, when the video not have an assigned NFT.
    """

    status_code = 403


class VideoNotYetConfirmedException(VideoNotConfirmedException):
    """Video not yet confirmed exception.

    This exception is used when the video is not yet confirmed.

    For example, when the video has an assigned NFT but it is not confirmed.
    """

    status_code = 403
