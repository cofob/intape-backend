"""Ethereum RPC client."""

from logging import getLogger
from types import TracebackType
from typing import Any, Type

from aiohttp import ClientSession

from .types import Transaction
from .utils import hex_to_int

log = getLogger(__name__)


def _construct_data(method: str, id: int, params: Any) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": id,
    }


class RPCProxy:
    """RPC proxy."""

    def __init__(self, url: str, method_name: str, session: ClientSession, id: int) -> None:
        """Initialize the proxy."""
        self.url = url
        self.method_name = method_name
        self.session = session
        self.id = id

    async def __call__(self, *args: Any) -> Any:
        """Call the RPC method."""
        log.debug("Calling %s with %s", self.method_name, args)
        response = await self.session.post(self.url, json=_construct_data(self.method_name, self.id, args))
        response.raise_for_status()
        response_json = await response.json()
        log.debug("Response: %s", response_json)
        return response_json["result"]


class RPCClient:
    """Low level RPC client."""

    id_counter = 0

    def __init__(self, url: str, session: ClientSession) -> None:
        """Initialize the client."""
        self.url = url
        self.session = session

    def __getattr__(self, name: str) -> RPCProxy:
        """Get the RPC proxy."""
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        self.id_counter += 1
        return RPCProxy(self.url, name, self.session, self.id_counter)


class EthClient:
    """Ethereum RPC client."""

    def __init__(self, url: str, session: ClientSession | None = None):
        """Initialize the Ethereum client."""
        self.url = url
        self.session = session or ClientSession()
        self.rpc = RPCClient(url, self.session)

    async def __aenter__(self) -> "EthClient":
        """Enter the context manager."""
        return self

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """Exit the context manager."""
        await self.session.__aexit__(exc_type, exc_val, exc_tb)

    async def get_block_number(self) -> int:
        """Get the current block number."""
        return hex_to_int(await self.rpc.eth_blockNumber())

    async def get_tx(self, tx_hash: str, abi: list[dict[Any, Any]] | None = None) -> Transaction:
        """Get the transaction input."""
        tx = await self.rpc.eth_getTransactionByHash(tx_hash)
        return Transaction(
            blockHash=tx["blockHash"],
            blockNumber=hex_to_int(tx["blockNumber"]),
            from_=tx["from"],
            to=tx["to"],
            gas=hex_to_int(tx["gas"]),
            gasPrice=hex_to_int(tx["gasPrice"]),
            hash=tx["hash"],
            raw_input=tx["input"],
            abi=abi,
            nonce=hex_to_int(tx["nonce"]),
        )
