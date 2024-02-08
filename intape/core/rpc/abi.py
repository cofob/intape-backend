"""ABI decoding tools."""

from dataclasses import dataclass
from typing import Any

from eth_abi.abi import decode

from .utils import (
    detect_constructor_arguments,
    get_constructor_type,
    get_selector_to_function_type,
    get_types_names,
    hex_to_bytes,
)


@dataclass(frozen=True)
class ContractCall:
    """Contract call."""

    name: str
    arguments: list[tuple[str, str, Any]]


class InputDecoder:
    """Input decoder."""

    def __init__(self, abi: list[dict[Any, Any]]):
        """Initialize."""
        self._constructor_type = get_constructor_type(abi)
        self._selector_to_func_type = get_selector_to_function_type(abi)

    def decode_function(self, tx_input: str | bytes) -> ContractCall:
        """Decode function."""
        tx_input = hex_to_bytes(tx_input)
        selector, args = tx_input[:4], tx_input[4:]
        type_def = self._selector_to_func_type.get(selector, None)
        if not type_def:
            raise ValueError("Function not found")

        types, names = get_types_names(type_def["inputs"])

        try:
            values = decode(types, args)  # type: ignore
        except OverflowError:
            raise ValueError("Invalid arguments")

        return ContractCall(type_def["name"], list(zip(types, names, values)))

    def decode_constructor(
        self,
        tx_input: str | bytes,
        bytecode: str | bytes | None = None,
    ) -> ContractCall:
        """Decode constructor."""
        tx_input = hex_to_bytes(tx_input)

        if not self._constructor_type:
            raise ValueError("No constructor")

        if bytecode is not None:
            bytecode_len = len(hex_to_bytes(bytecode))
            tx_input = tx_input[bytecode_len:]
        else:
            tx_input = detect_constructor_arguments(self._constructor_type, tx_input)

        types, names = get_types_names(self._constructor_type["inputs"])
        values = decode(types, tx_input)  # type: ignore

        return ContractCall("constructor", list(zip(types, names, values)))


def decode_function(abi: list[dict[Any, Any]], tx_input: str | bytes) -> ContractCall:
    """Decode function."""
    return InputDecoder(abi).decode_function(tx_input)


def decode_constructor(
    abi: list[dict[Any, Any]], tx_input: str | bytes, bytecode: str | bytes | None = None
) -> ContractCall:
    """Decode constructor."""
    return InputDecoder(abi).decode_constructor(tx_input, bytecode)
