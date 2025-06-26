"""Acceptance tests for the command line interface."""

import pathlib

from click.testing import CliRunner, Result
from grpc_generator import __main__, generator


def call_generate(args: list[str]) -> Result:
    """Invoke the 'generate' CLI command."""
    runner = CliRunner()
    result = runner.invoke(
        __main__.cli,
        args,
    )
    return result


def assert_is_submodule(output_path: pathlib.Path) -> None:
    """Assert the output_path contains Python submodules."""
    assert output_path.joinpath("__init__.py").exists()
    assert output_path.joinpath("py.typed").exists()
    assert all(entry.is_file() for entry in output_path.iterdir())


def assert_is_subpackage(output_path: pathlib.Path) -> None:
    """Assert the output_path contains Python subpackages."""
    assert not output_path.joinpath("__init__.py").exists()
    assert not output_path.joinpath("py.typed").exists()
    assert all(entry.is_dir() for entry in output_path.iterdir())
    for entry in output_path.iterdir():
        assert entry.joinpath("__init__.py").exists()
        assert entry.joinpath("__init__.pyi").exists()
        assert entry.joinpath("py.typed").exists()


def test___generator___call_generator_help___succeeds() -> None:
    """Does it invoke the base command group?"""
    result = call_generate(args=["--help"])
    assert result.exit_code == 0


def test___empty_package___generate_submodules___creates_submodules(
    tmp_path: pathlib.Path,
) -> None:
    """Does it generate Python submodules?"""
    result = call_generate(
        [
            "--output-basepath",
            f"{tmp_path!s}",
            "--output-format",
            generator.OutputFormat.SUBMODULE.value,
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )

    assert result.exit_code == 0
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    assert_is_submodule(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0


def test___empty_package___generate_subpackages___creates_subpackages(
    tmp_path: pathlib.Path,
) -> None:
    """Does it generate Python subpackages?"""
    result = call_generate(
        [
            "--output-basepath",
            f"{tmp_path!s}",
            "--output-format",
            generator.OutputFormat.SUBPACKAGE.value,
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )
    assert result.exit_code == 0
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    assert_is_subpackage(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0


def test___existing_package___generate_submodules___updates_submodules(
    tmp_path: pathlib.Path,
) -> None:
    """Does it correctly regenerate a Python package?"""
    # Add files to the package that are not gRPC APIs
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    output_folder.mkdir(parents=True, exist_ok=True)
    support_files = [
        output_folder.joinpath("helper.py"),
        output_folder.joinpath("converter.py"),
    ]
    for support_file in support_files:
        support_file.touch()
    result = call_generate(
        [
            "--output-basepath",
            f"{tmp_path!s}",
            "--output-format",
            generator.OutputFormat.SUBMODULE.value,
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )
    assert result.exit_code == 0
    assert_is_submodule(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0
    for support_file in support_files:
        assert support_file.exists(), "Support file incorrectly deleted!"

    # Mimic an API change by pretending the first version has this API
    previous_api_files = [
        output_folder.joinpath("previous_grpc_file_pb2.py"),
        output_folder.joinpath("previous_grpc_file_pb2.pyi"),
        output_folder.joinpath("previous_grpc_file_pb2_grpc.py"),
        output_folder.joinpath("previous_grpc_file_pb2_grpc.pyi"),
    ]
    for previous_api_file in previous_api_files:
        previous_api_file.touch()

    result = call_generate(
        [
            "--output-basepath",
            f"{tmp_path!s}",
            "--output-format",
            generator.OutputFormat.SUBMODULE.value,
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )
    assert result.exit_code == 0
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    assert_is_submodule(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0
    for previous_api_file in previous_api_files:
        assert not previous_api_file.exists()
    for support_file in support_files:
        assert support_file.exists(), "Support file incorrectly deleted!"
