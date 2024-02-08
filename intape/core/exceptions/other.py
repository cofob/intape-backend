"""Other exceptions."""
from .abc import AbstractException


class NotImplementedException(AbstractException):
    """Non implemented exception.

    This exception is used when the method is not implemented.
    """

    pass


class DatabaseException(AbstractException):
    """Database exception.

    This exception is used when the database is not available.
    """

    pass


class IPFSException(AbstractException):
    """IPFS exception.

    This exception is used when the IPFS is not available.
    """

    pass
