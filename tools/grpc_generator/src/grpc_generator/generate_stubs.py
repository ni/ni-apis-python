"""Script to generate gRPC stubs for all packages in the repository."""

import json
from pathlib import Path

from grpc_generator import generator


def main():
    """Executes the generation of the gRPC stubs based on the specified package information."""
    repo_root_path = Path(__file__).parent.parent.parent.parent.parent

    packages_file_path = repo_root_path / "packages.json"

    packages = json.loads(packages_file_path.read_text(encoding="utf-8"))

    for package_name, package_info in packages.items():
        # Skip package entries with no specified output format
        if not package_info.get("output-format"):
            continue

        proto_basepath = repo_root_path.joinpath(package_info["proto-basepath"])
        proto_subpath = Path(package_info["proto-subpath"])
        proto_include_path = repo_root_path.joinpath(package_info["proto-include-path"])
        output_basepath = repo_root_path.joinpath(f"./packages/{package_name}/src")
        output_format = package_info["output-format"]

        print(f"Generating stubs for {package_name}...")
        print("------------------------------------------------------------------------")
        generator.handle_cli(
            proto_basepath=proto_basepath,
            proto_subpath=proto_subpath,
            proto_include_paths=[proto_include_path],
            output_basepath=output_basepath,
            output_format=generator.OutputFormat(output_format),
        )
        print()


if __name__ == "__main__":
    main()
