"""Generate gRPC Python stubs from proto files."""

import logging

import click


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def handle_cli() -> None:
    """Handle the command line interface invocation."""
    color_world = {
        "W": "red",
        "o": "yellow",
        "r": "green",
        "l": "blue",
        "d": "magenta",
    }
    message = "".join([click.style(text, color) for text, color in color_world.items()])
    click.echo(f"Hello {message}!")
