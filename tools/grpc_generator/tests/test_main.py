"""Tests for the command line interface."""

from click.testing import CliRunner

from grpc_generator import __main__


def test_console() -> None:
    """Does it invoke the base command group?"""
    runner = CliRunner()
    result = runner.invoke(__main__.cli)
    assert result.exit_code == 0
