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
from intape.dependencies import get_db_deprecated
from intape.dependencies.ipfs import get_ipfs_instance_deprecated
from intape.models import FileModel

log = logging.getLogger(__name__)


class Worker:
    """Worker class."""

    def __init__(self, debug: bool = False) -> None:
        """Initialize worker."""
        self.debug = debug
        self.cron = [crontab("*/2 * * * *", func=self.function_proxy(self.remove_old_files))]
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

        Args:
            func (Callable): Function to proxy.
            *args: Arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.
        """

        async def function_proxy_inner() -> None:
            try:
                db = get_db_deprecated(self.config)
                async with get_ipfs_instance_deprecated(self.config) as ipfs:
                    log.debug(f"Running task {func.__name__}...")
                    await func(db, ipfs, *args, **kwargs)
            except Exception as e:
                log.error(f"Error in function {func.__name__}")
                log.exception(e)

        return function_proxy_inner

    async def remove_old_files(self, db: AsyncSession, ipfs: IPFSClient) -> None:
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
