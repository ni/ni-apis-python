"""Generate gRPC Python stubs from proto files."""

import logging
import pathlib
from typing import NamedTuple

import click
import grpc_tools.protoc


class GenerationSpec(NamedTuple):
    """A NamedTuple that describes a gRPC package for code generation."""

    proto_paths: list[pathlib.Path]
    include_paths: list[pathlib.Path]
    output_path: pathlib.Path


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
        proto_paths=hardcoded_protos,
        include_paths=hardcoded_include,
        output_path=hardcoded_output,
    )

    device_spec = GenerationSpec(
        proto_paths=[pathlib.Path("C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis\\ni\\grpcdevice\\v1\\session.proto")],
        include_paths=[pathlib.Path("C:\\dev\\ni\\git\\github\\ni-apis-python\\third_party\\ni-apis")],
        output_path=hardcoded_output
    )

    all_specs = [preview_spec, device_spec]

    for spec in all_specs:
        delete_generated_files(output_path=spec.output_path)
        generate_python_files(spec)
        remove_empty_service_files()
        transform_files_for_namespace()


def delete_generated_files(output_path: pathlib.Path) -> None:
    """Delete all generated gRPC files to accommodate API name changes and deletions."""
    _logger.info(
        f"{click.style('Deleting', 'red')} old gRPC files in {click.style(str(output_path), 'bright_cyan')}"
    )


def generate_python_files(generation_spec: GenerationSpec) -> None:
    """Generate Python files from the Protobuf files."""
    _logger.info(
        f"{click.style('Generating', 'green')} new gRPC files in {click.style(str(generation_spec.output_path), 'bright_cyan')}"
    )
    _ = [_logger.info(f"  Include: {path!s}") for path in generation_spec.include_paths]  # type: ignore[func-returns-value]
    _ = [_logger.info(f"  Compile: {path!s}") for path in generation_spec.proto_paths]  # type: ignore[func-returns-value]

    proto_include_options = [
        f"--proto_path={source_path!s}" for source_path in generation_spec.include_paths
    ]
    output_path_options = [
        f"{arg_name}={generation_spec.output_path!s}"
        for arg_name in ["--python_out", "--mypy_out", "--grpc_python_out", "--mypy_grpc_out"]
    ]
    proto_file_args = [f"{proto_file!s}" for proto_file in generation_spec.proto_paths]

    protoc_arguments = ["protoc"]
    protoc_arguments.extend(proto_include_options)
    protoc_arguments.extend(output_path_options)
    protoc_arguments.extend(proto_file_args)

    _logger.info(f"  Invoking '{click.style(' '.join(protoc_arguments), 'bright_white')}'")
    grpc_tools.protoc.main(protoc_arguments)


def remove_empty_service_files() -> None:
    """Detect and remove empty '..._grpc.py' stubs files."""
    _logger.info(f"{click.style('Removing', 'yellow')} empty gRPC service files.")


def transform_files_for_namespace() -> None:
    """Convert a submodule to a subpackage."""
    _logger.info(f"{click.style('Transforming', 'yellow')} gRPC submodules to subpackages")
