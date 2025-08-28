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
        # Assumption: Any subpackage dir that does not end in _pb2
        # contains handwritten mixin files we want to keep and won't
        # have the same format as a generated subpackage dir.
        if generator.is_generated_subpackage_dir(entry):
            assert entry.joinpath("__init__.py").exists()
            assert entry.joinpath("__init__.pyi").exists()
            assert entry.joinpath("py.typed").exists()


def test___generator___call_generator_help___succeeds() -> None:
    result = call_generate(args=["--help"])
    assert result.exit_code == 0


def test___empty_package___generate_submodules___creates_submodules(
    tmp_path: pathlib.Path,
) -> None:
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


def test___existing_package___generate_subpackages___updates_subpackages(
    tmp_path: pathlib.Path,
) -> None:
    # Add files to a separate subpackage that aren't generated files.
    output_folder = tmp_path.joinpath("ni/protobuf/types")
    mixin_folder = output_folder.joinpath("mixin")
    mixin_folder.mkdir(parents=True, exist_ok=True)
    support_files = [
        mixin_folder.joinpath("helper.py"),
        mixin_folder.joinpath("converter.py"),
    ]
    for support_file in support_files:
        support_file.touch()

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
    assert_is_subpackage(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0
    for support_file in support_files:
        assert support_file.exists(), "Support file incorrectly deleted!"

    # Mimic an API change by adding "previous" generated subpackage dirs
    previous_pb2_dir = output_folder.joinpath("prev_dir_pb2")
    previous_pb2_dir.mkdir(parents=True, exist_ok=True)
    previous_pb2_grpc_dir = output_folder.joinpath("prev_dir_pb2_grpc")
    previous_pb2_grpc_dir.mkdir(parents=True, exist_ok=True)
    previous_api_files = [
        previous_pb2_dir.joinpath("__init__.py"),
        previous_pb2_dir.joinpath("__init__.pyi"),
        previous_pb2_dir.joinpath("py.typed"),
        previous_pb2_grpc_dir.joinpath("__init__.py"),
        previous_pb2_grpc_dir.joinpath("__init__.pyi"),
        previous_pb2_grpc_dir.joinpath("py.typed"),
    ]
    for previous_api_file in previous_api_files:
        previous_api_file.touch()

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
    assert_is_subpackage(output_folder)
    assert len(sorted(output_folder.glob("*_pb2_grpc.*"))) == 0
    assert not previous_pb2_dir.exists(), "Previous subpackage dir not deleted correctly!"
    assert not previous_pb2_grpc_dir.exists(), "Previous subpackage dir not deleted correctly!"
