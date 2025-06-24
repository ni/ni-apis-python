"""Generate gRPC Python stubs from proto files."""

import importlib.resources
import logging
import pathlib
import shutil
from enum import StrEnum
from typing import NamedTuple

import click
import grpc_tools.protoc
from google.protobuf import descriptor_pb2


class OutputFormat(StrEnum):
    """Supported Python output formats for generated gRPC packages."""

    Submodule = "Submodule"
    Subpackage = "Subpackage"


class GenerationSpec(NamedTuple):
    """A NamedTuple that describes a gRPC package for code generation."""

    name: str
    proto_paths: list[pathlib.Path]
    include_paths: list[pathlib.Path]
    output_root_path: pathlib.Path
    output_format: OutputFormat

    @property
    def package_folder(self) -> pathlib.Path:
        """Return the full path to the folder for the generated files."""
        name_as_path = self.name.replace(".", "/")
        return self.output_root_path.joinpath(name_as_path)

    @property
    def package_descriptor_file(self) -> pathlib.Path:
        """Return the path for the package's FileDescriptorSet."""
        return self.output_root_path.joinpath(f"{self.name}-descriptor.pb")

    def get_matching_message_files(self, relative_path: pathlib.Path) -> list[pathlib.Path]:
        """Get the full paths to the generated message files for the specified proto package path."""
        full_path = self.output_root_path.joinpath(relative_path)
        logic_file = full_path.with_name(f"{full_path.stem}_pb2.py")
        types_file = full_path.with_name(f"{full_path.stem}_pb2.pyi")
        return [logic_file, types_file]

    def get_matching_service_files(self, relative_path: pathlib.Path) -> list[pathlib.Path]:
        """Get the full paths to the generated service files for the specified proto package path."""
        full_path = self.output_root_path.joinpath(relative_path)
        logic_file = full_path.with_name(f"{full_path.stem}_pb2_grpc.py")
        types_file = full_path.with_name(f"{full_path.stem}_pb2_grpc.pyi")
        return [logic_file, types_file]


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


def handle_cli() -> None:
    """Handle the command line interface invocation."""
    do_generation()


def do_generation() -> None:
    """Generate gRPC files."""
    hardcoded_output = pathlib.Path("C:\\dev\\scratch")
    hardcoded_include = [
        pathlib.Path("C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis"),
    ]
    hardcoded_protos = [
        pathlib.Path(
            "C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis\\ni\\protobuf\\types\\array.proto"
        ),
        pathlib.Path(
            "C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis\\ni\\protobuf\\types\\precision_timestamp.proto"
        ),
        pathlib.Path(
            "C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis\\ni\\protobuf\\types\\waveform.proto"
        ),
        pathlib.Path(
            "C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis\\ni\\protobuf\\types\\xydata.proto"
        ),
    ]

    preview_spec = GenerationSpec(
        name="ni.protobuf.types",
        proto_paths=hardcoded_protos,
        include_paths=hardcoded_include,
        output_root_path=hardcoded_output,
        output_format=OutputFormat.Submodule,
    )

    device_spec = GenerationSpec(
        name="ni.grpcdevice.v1",
        proto_paths=[pathlib.Path("C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis\\ni\\grpcdevice\\v1\\session.proto")],
        include_paths=hardcoded_include,
        output_root_path=hardcoded_output,
        output_format=OutputFormat.Subpackage,
    )

    all_specs = [preview_spec, device_spec]

    for spec in all_specs:
        _logger.info(f"Starting {click.style(spec.name, 'bright_cyan')} as {click.style(spec.output_format, 'bright_cyan')}")
        reset_python_package(spec)
        generate_python_files(spec)
        finalize_python_package(spec)


def reset_python_package(generation_spec: GenerationSpec) -> None:
    """Delete all generated gRPC files to accommodate API name changes and deletions."""
    _logger.info(
        f"  {click.style('Deleting', 'red')} all files under {click.style(str(generation_spec.package_folder), 'bright_cyan')}"
    )
    if not generation_spec.package_folder.exists():
        return
    shutil.rmtree(generation_spec.package_folder)


def generate_python_files(generation_spec: GenerationSpec) -> None:
    """Generate Python files from the Protobuf files."""
    _logger.info(
        f"  {click.style('Generating', 'green')} new gRPC files in {click.style(str(generation_spec.package_folder), 'bright_cyan')}"
    )
    _ = [_logger.info(f"    Include: {path!s}") for path in generation_spec.include_paths]  # type: ignore[func-returns-value]
    _ = [_logger.info(f"    Compile: {path!s}") for path in generation_spec.proto_paths]  # type: ignore[func-returns-value]

    proto_include_options = [
        f"--proto_path={source_path!s}" for source_path in generation_spec.include_paths
    ]
    output_path_options = [
        f"{arg_name}={generation_spec.output_root_path!s}"
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

    invoke_protoc(protoc_arguments)


def finalize_python_package(generation_spec: GenerationSpec) -> None:
    """Post process the generated files according to the generation_spec."""
    with open(generation_spec.package_descriptor_file, "rb") as f:
        package_descriptor_set = descriptor_pb2.FileDescriptorSet()
        package_descriptor_set.ParseFromString(f.read())

    for file_descriptor in package_descriptor_set.file:
        relative_proto_file_path = pathlib.Path(file_descriptor.name)
        if not file_descriptor.message_type:
            _logger.info(
                f"  {click.style('Removing', 'yellow')} empty gRPC message files for {click.style(file_descriptor.name, 'bright_cyan')}"
            )
            remove_files(generation_spec.get_matching_message_files(relative_proto_file_path))

        if not file_descriptor.service:
            _logger.info(
                f"  {click.style('Removing', 'yellow')} empty gRPC service files for {click.style(file_descriptor.name, 'bright_cyan')}"
            )
            remove_files(generation_spec.get_matching_service_files(relative_proto_file_path))

    match generation_spec.output_format:
        case OutputFormat.Subpackage:
            transform_files_for_namespace(generation_spec)
        case OutputFormat.Submodule:
            add_submodule_files(generation_spec)


def transform_files_for_namespace(generation_spec: GenerationSpec) -> None:
    """Convert a submodule to a subpackage."""
    _logger.info(f"  {click.style('Transforming', 'yellow')} gRPC submodules to subpackages")
    files = sorted(generation_spec.package_folder.glob("*.py*"))
    new_subpackage_folders: set[pathlib.Path] = set()
    for file in files:
        subpackage_folder = file.with_name(file.stem)
        new_subpackage_folders.add(subpackage_folder)
        submodule_file = subpackage_folder.joinpath(f"__init__{file.suffix}")
        subpackage_folder.mkdir(exist_ok=True)
        file.rename(submodule_file)
        _logger.info(f"    Xformed: {submodule_file!s}")
    for folder in new_subpackage_folders:
        py_typed_file = folder.joinpath("py.typed")
        py_typed_file.touch()
        _logger.info(f"    Created: {folder.joinpath('py.typed')!s}")


def add_submodule_files(generation_spec: GenerationSpec) -> None:
    """Add an __init__.py file to the specified protobuf package."""
    _logger.info(f"  {click.style('Initializing', 'yellow')} gRPC submodules")

    init_file = generation_spec.package_folder.joinpath("__init__.py")
    init_file.touch()
    init_file.write_bytes(b'"""Auto generated gRPC files."""\n')
    _logger.info(f"    Created: {init_file!s}")

    py_typed_file = init_file.with_name("py.typed")
    py_typed_file.touch()
    _logger.info(f"    Created: {py_typed_file!s}")


def remove_files(files: list[pathlib.Path]) -> None:
    """Delete the specified files."""
    for file in files:
        file.unlink()
        _logger.info(f"    Removed: {file!s}")


def invoke_protoc(protoc_arguments: list[str]) -> None:
    """Invoke the Protobuf compiler."""
    builtin_proto_folder = importlib.resources.files(grpc_tools).joinpath("_proto")
    protoc_arguments.insert(1, f"--proto_path={builtin_proto_folder!s}")

    _logger.info(f"    Invoking '{click.style(' '.join(protoc_arguments), 'bright_white')}'")
    exit_code = grpc_tools.protoc.main(protoc_arguments)
    _logger.info(f"    Outcome: {exit_code}")
    if exit_code != 0:
        raise RuntimeError(click.style(f"protoc exited with error code {exit_code}", "bright_magenta"))
