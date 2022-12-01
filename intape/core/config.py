"""Global application configuration."""
import logging
from dataclasses import dataclass
from os import environ

log = logging.getLogger(__name__)

RESERVED_USERNAME_SPACES: tuple[str, ...] = ("admin", "intape", "staff")
RESERVED_USERNAMES: list[str] = [
    "about",
    "admin",
    "blog",
    "contact",
    "help",
    "intape",
    "notifications",
    "official",
    "pricing",
    "privacy",
    "profile",
    "settings",
    "staff",
    "terms",
    "tos",
]


@dataclass(frozen=True)
class Config:
    """Global application configuration."""

    DATABASE_URL: str
    IPFS_URL: str
    SECRET: str
    RPC_URL: str
    CONTRACT_ADDRESS: str = "0xe67bf587f00afdd30a564fe9a436ecf8845a6829"
    IPFS_AUTH: tuple[str, str] | None = None
    ORIGINS: tuple[str, ...] = ("*",)

    @staticmethod
    def _get_env(name: str, default: str | None = None) -> str:
        """Get environment variable.

        Args:
            name (str): Name of the environment variable.
            default (str | None): Default value if environment variable is not set.

        Returns:
            str: Value of the environment variable.

        Raises:
            ValueError: If environment variable is not set and default value is not provided.
        """
        val = environ.get(name)
        if val is None:
            if default is None:
                raise ValueError(f"Environment variable {name} is not set")
            return default
        return val

    @classmethod
    def from_env(cls) -> "Config":
        """Create application from environment variables."""
        ipfs_auth = cls._get_env("IPFS_AUTH", "undefined")
        if ipfs_auth == "undefined":
            IPFS_AUTH = None
        else:
            i = ipfs_auth.index(":")
            # black and flake8 disagree on this line
            IPFS_AUTH = (ipfs_auth[:i], ipfs_auth[i + 1 :])  # noqa: E203

        origins = cls._get_env("ORIGINS", "undefined")
        if origins == "undefined":
            log.warning("ORIGINS environment variable is not set. Using default ('*') value.")
            ORIGINS = ("*",)
        else:
            ORIGINS = tuple(origins.split(","))  # type: ignore

        contract_address = cls._get_env("CONTRACT_ADDRESS", "undefined")
        if contract_address == "undefined":
            log.warning("CONTRACT_ADDRESS environment variable is not set. Using default value.")
            CONTRACT_ADDRESS = "0xe67bf587f00afdd30a564fe9a436ecf8845a6829"
        else:
            CONTRACT_ADDRESS = contract_address

        return cls(
            DATABASE_URL=cls._get_env("DATABASE_URL"),
            IPFS_URL=cls._get_env("IPFS_URL"),
            IPFS_AUTH=IPFS_AUTH,
            CONTRACT_ADDRESS=CONTRACT_ADDRESS,
            RPC_URL=cls._get_env("RPC_URL"),
            SECRET=cls._get_env("SECRET"),
            ORIGINS=ORIGINS,
        )
