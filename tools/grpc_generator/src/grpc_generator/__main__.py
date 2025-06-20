"""grpc_generator entry points."""

import logging

import click

from . import generator


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


@click.command()
@click.help_option()
def cli() -> None:
    """Generate gRPC Python stubs from proto files."""
    logging.basicConfig(
        format="{levelname:<8} {module:>16}:{funcName:<30} L{lineno:<4} {message}",
        style="{",
        level=logging.INFO,
    )
    generator.handle_cli()


if __name__ == "__main__":
    cli()
