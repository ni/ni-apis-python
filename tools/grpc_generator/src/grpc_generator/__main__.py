"""grpc_generator entry points."""

import pathlib

import click

from . import generator


REPO_ROOT = next(
    (p for p in pathlib.Path(__file__).parents if (p / "third_party").exists()), pathlib.Path(".")
)


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
    type=click.Choice(choices=[entry.value for entry in generator.OutputFormat]),
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
    """Generate gRPC Python stubs from proto files.

    Specifying input and output locations

      This script uses the protobuf files from the folder specified by
    --proto-basepath and --proto-subpath and emits Python files into the
    folder specified by --output-basepath:

    \b
      {proto-basepath}/{proto-subpath}  -->  {output-basepath}/{proto-subpath}

      The script resolves gRPC imports from --proto-basepath by default. Include
    additional paths by using --proto-include-path for each required folder.

    Specifying output format

      The script supports generating gRPC packages as either subpackages
    or submodules with --output-format.

      When generating submodules, the script creates Python files with names
    that match the source protobuf files:

    \b
      waveform.proto  -->  waveform_pb2.py

      When generating subpackages, the script creates folders with names
    that match the source protobuf files:

    \b
      waveform.proto  -->  waveform_pb2/__init__.py

      Clients use the same "import waveform_pb2" syntax.

    """  # noqa: D301 - Use r""" if any backslashes in a docstring
    generator.handle_cli(
        proto_basepath=proto_basepath,
        proto_subpath=proto_subpath,
        proto_include_paths=proto_include_path,
        output_basepath=output_basepath,
        output_format=generator.OutputFormat(output_format),
    )


if __name__ == "__main__":
    cli()
