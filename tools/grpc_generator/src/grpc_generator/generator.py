"""Generate gRPC Python stubs from proto files."""

import importlib.resources
import pathlib
import shutil
from enum import StrEnum
from typing import NamedTuple

import click
import grpc_tools.protoc  # type: ignore[import-untyped]
from google.protobuf import descriptor_pb2


class OutputFormat(StrEnum):
    """Supported Python output formats for generated gRPC packages."""

    Submodule = "Submodule"
    Subpackage = "Subpackage"


class GenerationSpec(NamedTuple):
    """A NamedTuple that describes a gRPC package for code generation."""

    proto_basepath: pathlib.Path
    proto_subpath: pathlib.Path
    proto_include_paths: list[pathlib.Path]
    output_basepath: pathlib.Path
    output_format: OutputFormat

    @property
    def name(self) -> str:
        """Return the name of the protobuf package."""
        subpath_as_name = self.proto_subpath.as_posix().replace("/", ".")
        return subpath_as_name

    @property
    def package_folder(self) -> pathlib.Path:
        """Return the full path to the folder for the generated files."""
        return self.output_basepath.joinpath(self.proto_subpath)

    @property
    def package_descriptor_file(self) -> pathlib.Path:
        """Return the path to use for the package's FileDescriptorSet."""
        return self.output_basepath.joinpath(f"{self.name}-descriptor.pb")

    @property
    def proto_paths(self) -> list[pathlib.Path]:
        """Return a list of all proto files under proto_subpath."""
        full_proto_path = self.proto_basepath.joinpath(self.proto_subpath)
        proto_files = sorted(full_proto_path.glob("*.proto"))
        return proto_files

    def get_matching_message_files(
        self, relative_proto_file_path: pathlib.Path
    ) -> list[pathlib.Path]:
        """Get the full paths to the message files for the specified proto package path."""
        full_path = self.output_basepath.joinpath(relative_proto_file_path)
        logic_file = full_path.with_name(f"{full_path.stem}_pb2.py")
        types_file = full_path.with_name(f"{full_path.stem}_pb2.pyi")
        return [logic_file, types_file]

    def get_matching_service_files(
        self, relative_proto_file_path: pathlib.Path
    ) -> list[pathlib.Path]:
        """Get the full paths to the service files for the specified proto package path."""
        full_path = self.output_basepath.joinpath(relative_proto_file_path)
        logic_file = full_path.with_name(f"{full_path.stem}_pb2_grpc.py")
        types_file = full_path.with_name(f"{full_path.stem}_pb2_grpc.pyi")
        return [logic_file, types_file]


def handle_cli(
    proto_basepath: pathlib.Path,
    proto_subpath: pathlib.Path,
    proto_include_paths: list[pathlib.Path],
    output_basepath: pathlib.Path,
    output_format: OutputFormat,
) -> None:
    """Handle the command line interface invocation."""
    all_include_paths = set([proto_basepath, *proto_include_paths])
    generation_spec = GenerationSpec(
        proto_basepath=proto_basepath,
        proto_subpath=proto_subpath,
        proto_include_paths=sorted(all_include_paths),
        output_basepath=output_basepath,
        output_format=output_format,
    )

    do_generation(generation_spec)


def do_generation(generation_spec: GenerationSpec) -> None:
    """Regenerate the gRPC package according to the generation_spec."""
    click.echo(
        f"Starting {click.style(generation_spec.name, 'bright_cyan')} as {click.style(generation_spec.output_format, 'bright_cyan')}"
    )
    reset_python_package(generation_spec)
    generate_python_files(generation_spec)
    finalize_python_package(generation_spec)


def reset_python_package(generation_spec: GenerationSpec) -> None:
    """Delete all generated gRPC files to accommodate API name changes and deletions."""
    click.echo(
        f"  {click.style('Deleting', 'red')} all files under {click.style(str(generation_spec.package_folder), 'bright_cyan')}"
    )
    if not generation_spec.package_folder.exists():
        return

    match generation_spec.output_format:
        case OutputFormat.Subpackage:
            shutil.rmtree(generation_spec.package_folder)
        case OutputFormat.Submodule:
            grpc_files = sorted(generation_spec.package_folder.glob("*_pb2.py*"))
            grpc_files.extend(generation_spec.package_folder.glob("*_pb2_grpc.py*"))
            for file in grpc_files:
                file.unlink()


def generate_python_files(generation_spec: GenerationSpec) -> None:
    """Generate Python files from the Protobuf files."""
    click.echo(
        f"  {click.style('Generating', 'green')} new gRPC files in {click.style(str(generation_spec.package_folder), 'bright_cyan')}"
    )
    _ = [click.echo(f"    Include: {path!s}") for path in generation_spec.proto_include_paths]  # type: ignore[func-returns-value]
    _ = [click.echo(f"    Compile: {path!s}") for path in generation_spec.proto_paths]  # type: ignore[func-returns-value]

    proto_include_options = [
        f"--proto_path={source_path!s}" for source_path in generation_spec.proto_include_paths
    ]
    output_path_options = [
        f"{arg_name}={generation_spec.output_basepath!s}"
        for arg_name in ["--python_out", "--mypy_out", "--grpc_python_out", "--mypy_grpc_out"]
    ]
    proto_file_args = [f"{proto_file!s}" for proto_file in generation_spec.proto_paths]

    protoc_arguments = [
        "protoc",
        *proto_include_options,
        *output_path_options,
        f"--descriptor_set_out={generation_spec.package_descriptor_file!s}",
        *proto_file_args,
    ]

    generation_spec.output_basepath.mkdir(parents=True, exist_ok=True)
    invoke_protoc(protoc_arguments)


def finalize_python_package(generation_spec: GenerationSpec) -> None:
    """Post process the generated files according to the generation_spec."""
    with open(generation_spec.package_descriptor_file, "rb") as f:
        package_descriptor_set = descriptor_pb2.FileDescriptorSet()
        package_descriptor_set.ParseFromString(f.read())

    for file_descriptor in package_descriptor_set.file:
        relative_proto_file_path = pathlib.Path(file_descriptor.name)
        if not file_descriptor.message_type:
            click.echo(
                f"  {click.style('Removing', 'yellow')} empty gRPC message files for {click.style(file_descriptor.name, 'bright_cyan')}"
            )
            remove_files(generation_spec.get_matching_message_files(relative_proto_file_path))

        if not file_descriptor.service:
            click.echo(
                f"  {click.style('Removing', 'yellow')} empty gRPC service files for {click.style(file_descriptor.name, 'bright_cyan')}"
            )
            remove_files(generation_spec.get_matching_service_files(relative_proto_file_path))

    match generation_spec.output_format:
        case OutputFormat.Subpackage:
            transform_files_for_namespace(generation_spec)
        case OutputFormat.Submodule:
            add_submodule_files(generation_spec)

    generation_spec.package_descriptor_file.unlink()


def transform_files_for_namespace(generation_spec: GenerationSpec) -> None:
    """Convert a submodule to a subpackage."""
    click.echo(f"  {click.style('Transforming', 'yellow')} gRPC submodules to subpackages")
    files = sorted(generation_spec.package_folder.glob("*.py*"))
    new_subpackage_folders: set[pathlib.Path] = set()
    for file in files:
        subpackage_folder = file.with_name(file.stem)
        new_subpackage_folders.add(subpackage_folder)
        submodule_file = subpackage_folder.joinpath(f"__init__{file.suffix}")
        subpackage_folder.mkdir(exist_ok=True)
        file.rename(submodule_file)
        click.echo(f"    Xformed: {submodule_file!s}")
    for folder in new_subpackage_folders:
        py_typed_file = folder.joinpath("py.typed")
        py_typed_file.touch()
        click.echo(f"    Created: {folder.joinpath('py.typed')!s}")


def add_submodule_files(generation_spec: GenerationSpec) -> None:
    """Add an __init__.py file to the specified protobuf package."""
    click.echo(f"  {click.style('Initializing', 'yellow')} gRPC submodules")

    init_file = generation_spec.package_folder.joinpath("__init__.py")
    init_file.touch()
    init_file.write_text(f'"""Package for {generation_spec.name}."""\n')
    click.echo(f"    Created: {init_file!s}")

    py_typed_file = init_file.with_name("py.typed")
    py_typed_file.touch()
    click.echo(f"    Created: {py_typed_file!s}")


def remove_files(files: list[pathlib.Path]) -> None:
    """Delete the specified files."""
    for file in files:
        file.unlink()
        click.echo(f"    Removed: {file!s}")


def invoke_protoc(protoc_arguments: list[str]) -> None:
    """Invoke the Protobuf compiler."""
    builtin_proto_folder = importlib.resources.files(grpc_tools).joinpath("_proto")
    protoc_arguments.insert(1, f"--proto_path={builtin_proto_folder!s}")

    click.echo(f"    Invoking '{click.style(' '.join(protoc_arguments), 'bright_white')}'")
    exit_code = grpc_tools.protoc.main(protoc_arguments)
    click.echo(f"    Outcome: {exit_code}")
    if exit_code != 0:
        raise RuntimeError(
            click.style(f"protoc exited with error code {exit_code}", "bright_magenta")
        )
