"""Worker module."""
import logging
from asyncio import sleep
from datetime import datetime
from typing import Any, Callable, Coroutine

from aiocron import crontab
from asyncipfscluster import IPFSClient
from pytz import UTC
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intape.core.config import Config
from intape.core.rpc import EthClient, InputDecoder
from intape.core.rpc.erc721_abi import ERC721_ABI
from intape.dependencies import get_db_deprecated
from intape.dependencies.ipfs import get_ipfs_instance_deprecated
from intape.models import FileModel, VideoModel

log = logging.getLogger(__name__)


class Worker:
    """Worker class."""

    def __init__(self, debug: bool = False) -> None:
        """Initialize worker."""
        self.debug = debug
        self.cron = [
            crontab("*/10 * * * *", func=self.function_proxy(self.remove_old_files)),
            crontab("*/1 * * * *", func=self.function_proxy(self.verify_videos)),
        ]
        self.config = Config.from_env()
        log.debug("Worker initialized")

    async def run(self) -> None:
        """Run worker."""
        for cron in self.cron:
            cron.start()
        log.info("Worker started scheduled tasks.")
        if self.debug:
            log.info("Debug mode enabled. Starting all tasks...")
            for cron in self.cron:
                await cron.func()
        else:
            while True:
                await sleep(1)

    def function_proxy(
        self,
        func: Callable[..., Coroutine[Any, Any, None]],
        *args: list[Any],
        **kwargs: dict[str, Any],
    ) -> Callable[[], Coroutine[Any, Any, None]]:
        """Proxy function.

        Pass to it essential dependencies and catch errors.

        Essential dependencies are:
        - Database session (AsyncSession, first positional argument)
        - IPFS client (IPFSClient, second positional argument)
        - Ethereum client (EthClient, third positional argument)

        Args:
            func (Callable): Function to proxy.
            *args: Arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        """

        async def function_proxy_inner() -> None:
            try:
                db = get_db_deprecated(self.config)
                async with get_ipfs_instance_deprecated(self.config) as ipfs:
                    async with EthClient(self.config.RPC_URL) as eth:
                        log.debug(f"Running task {func.__name__}...")
                        await func(db, ipfs, eth, *args, **kwargs)
            except Exception as e:
                log.error(f"Error in function {func.__name__}")
                log.exception(e)

        return function_proxy_inner

    async def remove_old_files(self, db: AsyncSession, ipfs: IPFSClient, _eth: EthClient) -> None:
        """Remove old files."""
        log.info("Removing old files...")

        query = select(FileModel).where(FileModel.remove_at is not None)
        files: list[FileModel] = (await db.execute(query)).scalars().all()

        # Removed files counter
        i = 0

        # We store datetime.now() in a variable to avoid
        # calling it multiple times in the loop.
        # This is because datetime.now() is a slow function.
        now = datetime.now(tz=UTC)
        for file in files:
            # Show mypy that file.remove_at is not None
            if file.remove_at is None:
                continue

            if file.remove_at.replace(tzinfo=UTC) < now:
                log.debug(f"Removing file {file.cid} ({file.mime_type})...")
                await file.remove_all(db, ipfs)
                i += 1

        await db.commit()

        log.info(f"Removed {i} files of total {len(files)} scheduled for removal files.")

    async def verify_videos(self, db: AsyncSession, _ipfs: IPFSClient, eth: EthClient) -> None:
        """Verify videos.

        Verify new videos in blockchain.
        """
        log.info("Verifying videos...")
        query = select(VideoModel).where(VideoModel.is_confirmed == False).where(VideoModel.tx_hash != None)
        videos: list[VideoModel] = (await db.execute(query)).scalars().all()
        contract_decoder = InputDecoder(ERC721_ABI)  # type: ignore

        # Verified videos counter
        i = 0

        for video in videos:
            try:
                log.debug(f"Verifying video {video.id}...")
                if video.tx_hash is None:
                    continue
                tx = await eth.get_tx(video.tx_hash)
                inp = contract_decoder.decode_function(tx.raw_input)
                if inp.name != "mintNFT":
                    log.error(f"Transaction {video.tx_hash} is not mintNFT")
                    continue
                recipent, token = inp.arguments
                if recipent[2] != video.user.eth_address:
                    log.error(f"Transaction {video.tx_hash} is not for user {video.user.eth_address}")
                    continue
                if token[2] != video.metadata_cid:
                    log.error(f"Transaction {video.tx_hash} has wrong metadata CID {token[2]}")
                    continue
                video.is_confirmed = True
                await video.save(db)
                log.info(f"Verified video {video.id} with transaction {video.tx_hash}")
                i += 1
            except Exception as e:
                log.error(f"Error getting transaction {video.tx_hash}")
                log.exception(e)
                continue

        await db.commit()

        log.info(f"Verified {i} videos of total {len(videos)}.")
