"""grpc_generator entry points."""

import logging


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def cli():
    """Main entry point for the command line interface."""
    print("Hello World")


if __name__ == "__main__":
    cli()
