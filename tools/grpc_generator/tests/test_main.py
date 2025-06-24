"""Acceptance tests for the command line interface."""

import pathlib

from click.testing import CliRunner, Result
from grpc_generator import __main__


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


def test_console() -> None:
    """Does it invoke the base command group?"""
    result = call_generate(args=["--help"])
    assert result.exit_code == 0


def test_generate_submodules(tmp_path: pathlib.Path) -> None:
    """Does it generate Python submodules?"""
    result = call_generate(
        [
            "--output-basepath",
            f"{pathlib.Path(tmp_path)!s}",
            "--output-format",
            "Submodule",
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )

    assert result.exit_code == 0
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    assert_is_submodule(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0


def test_generate_subpackages(tmp_path: pathlib.Path) -> None:
    """Does it generate Python subpackages?"""
    result = call_generate(
        [
            "--output-basepath",
            f"{pathlib.Path(tmp_path)!s}",
            "--output-format",
            "Subpackage",
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )
    assert result.exit_code == 0
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    assert_is_subpackage(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0


def test_regeneration(tmp_path: pathlib.Path) -> None:
    """Does it regenerate a Python package?"""
    result = call_generate(
        [
            "--output-basepath",
            f"{pathlib.Path(tmp_path)!s}",
            "--output-format",
            "Submodule",
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )
    assert result.exit_code == 0
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    assert_is_submodule(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0

    # Mimic an API change by pretending the first version has this file
    previous_file = output_folder.joinpath("previous_grpc_file.py")
    previous_file.touch()

    result = call_generate(
        [
            "--output-basepath",
            f"{pathlib.Path(tmp_path)!s}",
            "--output-format",
            "Submodule",
            "--proto-subpath",
            "ni/protobuf/types",
        ]
    )
    assert result.exit_code == 0
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    assert_is_submodule(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0
    assert not previous_file.exists()
