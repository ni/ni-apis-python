import json
import os
import subprocess

def get_path_from_root_directory_relative_path(root_directory_relative_path) -> str:
    return os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        convert_path_to_use_os_path_separators(root_directory_relative_path))

def convert_path_to_use_os_path_separators(path) -> str:
    return path.replace('/', os.path.sep)

packages_file_name = "packages.json"
packages_file_path = get_path_from_root_directory_relative_path(packages_file_name)

with open(packages_file_path, "r", encoding="utf-8") as packages_file:
    packages = json.load(packages_file)

for package_name, package_info in packages.items():
    # Skip package entries with no specified output format
    if not package_info.get("output-format"):
        continue

    proto_basepath = get_path_from_root_directory_relative_path(package_info["proto-basepath"])
    proto_subpath = convert_path_to_use_os_path_separators(package_info["proto-subpath"])
    proto_include_path = get_path_from_root_directory_relative_path(package_info["proto-include-path"])
    output_basepath = get_path_from_root_directory_relative_path(f"./packages/{package_name}/src")
    output_format = package_info["output-format"]

    args = [
        "poetry", "run", "grpc-generator",
        "--proto-basepath", proto_basepath,
        "--proto-subpath", proto_subpath,
        "--proto-include-path", proto_include_path,
        "--output-basepath", output_basepath,
        "--output-format", output_format
    ]

    print(f"Generating stubs for {package_name}...")
    print("------------------------------------------------------------------------")
    subprocess.run(args, check=True)
    print()