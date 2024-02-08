"""Pydantic fields for schemas."""

from datetime import datetime

from pydantic import Field

SIGNATURE = Field(
    min_length=132,
    max_length=132,
    description="Signature of the user's Ethereum address.",
    regex="^0x[0-9a-f]{130}$",
)

EMAIL: str = Field(
    min_length=6,
    max_length=64,
    regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
    description="Email address.",
)

USERNAME: str = Field(
    min_length=3,
    max_length=16,
    regex=r"^[a-zA-Z][a-zA-Z0-9_]+$",
    description="Username. Can only contain letters, numbers and underscores. Must start with a letter.",
)

FIRST_NAME: str = Field(
    min_length=1,
    max_length=32,
    description="First name.",
)

LAST_NAME: str = Field(
    min_length=1,
    max_length=32,
    description="Last name.",
)

BIO: str = Field(
    min_length=3,
    max_length=512,
    description="User bio.",
)

ETH_ADDRESS: str = Field(
    min_length=42,
    max_length=42,
    regex=r"^0x[a-f0-9]{40}$",
    description="Ethereum address. Can only contain hexadecimal characters. Must be 42 characters long.",
)

USER_ID: int = Field(description="User ID.", ge=0)

SESSION_ID: int = Field(description="Session ID.", ge=0)

JWT_TOKEN: str = Field(description="JWT token.", regex=r"^[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.?[a-zA-Z0-9-_]+$")

JWT_TOKEN_TYPE: str = Field(description="JWT token type.", regex=r"^(bearer)$", default="bearer")

IPFS_CID: str = Field(
    min_length=46,
    max_length=46,
    regex=r"^Qm[a-zA-Z0-9]{44}$",
    description="IPFS CID. Can only contain alphanumeric characters. Must be 46 characters long.",
)

IPFS_PATH: str = Field(regex=r"^ipfs://Qm[a-zA-Z0-9]{44}$", max_length=64, description="IPFS path.")

VIDEO_ID: int = Field(description="Video ID.", ge=0)

VIDEO_DESCRIPTION: str = Field(description="Video description.", max_length=150, min_length=3)

VIDEO_TAGS: list[str] = Field(description="Video tags.", max_length=16, min_length=1)

COLLECTION_ID: int = Field(description="Collection ID.", ge=0)

COLLECTION_NAME: str = Field(description="Collection name.", max_length=32, min_length=3)

COLLECTION_DESCRIPTION: str = Field(description="Collection description.", max_length=150, min_length=3)

COLLECTION_IS_PUBLIC: bool = Field(description="Is collection public and can be updated by anyone.")

COLLECTION_ENTRY_ID: int = Field(description="Collection entry ID.", ge=0)

CREATED_AT: datetime = Field(description="Created at timestamp.")

UPDATED_AT: datetime = Field(description="Updated at timestamp.")
