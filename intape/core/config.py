"""Global application configuration."""
from dataclasses import dataclass
from os import environ


@dataclass(frozen=True)
class Config:
    """Global application configuration."""

    DATABASE_URL: str
    IPFS_URL: str
    SECRET: str
    ORIGIN: str = "*"


# Yea, I know, this is a global variable. But I don't know how to do FastAPI
# without it. I'm open to suggestions (and PRs).
CONFIG = Config(DATABASE_URL=environ["DATABASE_URL"], IPFS_URL=environ["IPFS_URL"], SECRET=environ["SECRET"])
