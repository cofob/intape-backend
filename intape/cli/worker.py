"""Worker related commands."""
from asyncio import run

import click

from intape.worker import Worker

from .cli import cli


@cli.command()
@click.option("--debug", "-d", is_flag=True, help="Run all tasks immediately.")
def worker(debug: bool) -> None:
    """Run cron worker."""
    worker = Worker(debug=debug)
    run(worker.run())
