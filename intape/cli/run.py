"""Server launch related commands."""
import alembic.config
import click
import uvicorn

from .cli import cli


@cli.command()
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to.")
@click.option("--port", "-p", default=8000, help="Port to bind to.")
@click.option("--migrate", "-m", is_flag=True, help="Run migrations before starting.")
@click.option("--reload", "-r", is_flag=True, help="Reload on code changes.")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode.")
@click.option("--workers", "-w", default=1, help="Number of workers.")
def run(host: str, port: int, migrate: bool, reload: bool, debug: bool, workers: int) -> None:
    """Run the InTape webserver."""
    if migrate:
        alembic.config.main(argv=["upgrade", "head"])  # type: ignore
    uvicorn.run("intape:app", host=host, port=port, reload=reload, debug=debug, workers=workers)


@cli.command()
def dev() -> None:
    """Run the development server."""
    uvicorn.run("intape:app", host="127.0.0.1", port=8000, reload=True, debug=True, workers=1)
