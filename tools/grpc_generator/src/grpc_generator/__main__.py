"""grpc_generator entry points."""

import logging

import click


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


@click.command()
@click.help_option()
def cli() -> None:
    """Generate gRPC Python stubs from proto files."""
    print("Hello World")


if __name__ == "__main__":
    cli()
