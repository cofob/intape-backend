"""Collection exceptions."""

from .abc import AbstractException


class BaseCollectionException(AbstractException):
    """Base collection exception."""

    pass


class CollectionNotFound(BaseCollectionException):
    """Collection not found exception."""

    status_code = 404


class CollectionEntryNotFound(BaseCollectionException):
    """Collection entry not found exception."""

    status_code = 404


class CollectionEntryAlreadyExists(BaseCollectionException):
    """Collection entry already exists exception."""

    status_code = 409
