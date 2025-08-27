"""Script to generate gRPC stubs for all packages in the repository."""

import json
import subprocess
from pathlib import Path


def main():
    """Executes the generation of the gRPC stubs based on the specified package information."""
    repo_root = Path(__file__).parent.parent.parent

    packages_file_path = repo_root / "packages.json"

    with open(packages_file_path, "r", encoding="utf-8") as packages_file:
        packages = json.load(packages_file)

    for package_name, package_info in packages.items():
        # Skip package entries with no specified output format
        if not package_info.get("output-format"):
            continue

        proto_basepath = repo_root.joinpath(package_info["proto-basepath"])
        proto_subpath = Path(package_info["proto-subpath"])
        proto_include_path = repo_root.joinpath(package_info["proto-include-path"])
        output_basepath = repo_root.joinpath(f"./packages/{package_name}/src")
        output_format = package_info["output-format"]

        args = [
            "poetry",
            "run",
            "grpc-generator",
            "--proto-basepath",
            proto_basepath,
            "--proto-subpath",
            proto_subpath,
            "--proto-include-path",
            proto_include_path,
            "--output-basepath",
            output_basepath,
            "--output-format",
            output_format,
        ]

        print(f"Generating stubs for {package_name}...")
        print("------------------------------------------------------------------------")
        subprocess.run(args, check=True)
        print()


if __name__ == "__main__":
    main()
