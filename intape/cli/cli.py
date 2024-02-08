"""Module with main CLI function."""
import logging
from os import environ

import click


@click.group()
def cli() -> None:
    """Control interface for InTape."""
    log_level = environ.get("LOG_LEVEL", "INFO").upper()
    if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        raise ValueError(f"Invalid log level: {log_level}")
    log_format = environ.get("LOG_FORMAT", "%(asctime)s   %(name)-25s %(levelname)-8s %(message)s")
    log_file = environ.get("LOG_FILE", None)
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file) if log_file else logging.NullHandler(),
        ],
    )
