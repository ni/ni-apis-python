"""grpc_generator entry points."""

import pathlib

import click

from . import generator


REPO_ROOT = pathlib.Path(__file__).parents[pathlib.Path(__file__).parts.index("ni-apis-python") - 1]


@click.command(epilog=generator.USAGE_EXAMPLE)
@click.option(
    "--output-basepath",
    metavar="PATH",
    type=click.Path(file_okay=False, writable=True, path_type=pathlib.Path),
    required=True,
    help="Emit the generated gRPC files to PATH",
)
@click.option(
    "--output-format",
    type=click.Choice(choices=[value for value in generator.OutputFormat]),
    required=True,
    help="Generate a Python submodule or subpackage",
)
@click.option(
    "--proto-basepath",
    metavar="PATH",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    default=REPO_ROOT.joinpath("third_party/ni-apis"),
    show_default=True,
    help="Use PATH as the base for --proto-subpath",
)
@click.option(
    "--proto-include-path",
    metavar="PATH",
    multiple=True,
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    default=[REPO_ROOT.joinpath("third_party/ni-apis")],
    show_default=True,
    help="Add PATH to the import search list, can be used more than once",
)
@click.option(
    "--proto-subpath",
    metavar="PATH",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    required=True,
    help="Use the proto files under PATH as input",
)
@click.help_option()
@click.version_option()
def cli(
    proto_basepath: pathlib.Path,
    proto_subpath: pathlib.Path,
    proto_include_path: list[pathlib.Path],
    output_basepath: pathlib.Path,
    output_format: str,
) -> None:
    """Generate gRPC Python stubs from proto files."""
    generator.handle_cli(
        proto_basepath=proto_basepath,
        proto_subpath=proto_subpath,
        proto_include_paths=proto_include_path,
        output_basepath=output_basepath,
        output_format=generator.OutputFormat(output_format),
    )


if __name__ == "__main__":
    cli()
