"""Types."""

from dataclasses import dataclass
from typing import Any

from .abi import ContractCall, decode_function


@dataclass
class Transaction:
    """Blockchain transaction."""

    blockHash: str
    blockNumber: int
    from_: str
    to: str
    gas: int
    gasPrice: int
    hash: str
    nonce: int
    raw_input: str
    abi: list[dict[Any, Any]] | None = None
    input: ContractCall | None = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.abi:
            self.input = decode_function(self.abi, self.raw_input)
