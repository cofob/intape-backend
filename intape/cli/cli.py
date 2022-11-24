"""Module with main CLI function."""
import logging
from os import environ

import click


@click.group()
def cli() -> None:
    """Control interface for InTape."""
    logging.basicConfig(level=environ.get("LOG_LEVEL", "INFO").upper())
