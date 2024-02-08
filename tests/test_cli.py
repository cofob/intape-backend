"""Test CLI."""
from click.testing import CliRunner

from intape.cli import cli


def test_cli():
    """Test CLI."""
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0


def test_cli_db():
    """Test CLI db."""
    runner = CliRunner()
    result = runner.invoke(cli, ["db"])
    assert result.exit_code == 0


def test_cli_db_migrate():
    """Test CLI db migrate."""
    runner = CliRunner()
    result = runner.invoke(cli, ["db", "migrate"])
    assert result.exit_code == 0
