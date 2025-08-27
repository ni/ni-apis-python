# About

`grpc_generator` is a Python tool that generates gRPC stubs from proto files.

It supports emitting stubs into namespace packages, transforming them as necessary from submodules to subpackages.

## Setup

```pwsh
# Initialize the tool
cd tools\grpc_generator
poetry install
```

## Generate

```pwsh
# PowerShell
poetry run grpc-generator `
   --proto-basepath ..\..\third_party\ni-apis `
   --proto-subpath ni\protobuf\types `
   --output-basepath ..\..\packages\ni.protobuf.types\src `
   --output-format submodule
```

## Generate into a namespace package

```pwsh
# PowerShell
poetry run grpc-generator `
   --proto-basepath ..\..\third_party\ni-apis `
   --proto-subpath ni\measurementlink\pinmap\v1 `
   --output-basepath ..\..\packages\ni.measurementlink.pinmap.v1\src `
   --output-format subpackage
```

## Generate (stubs for all packages)

You can also use the `generate_stubs.py` script to invoke `grpc_generator` and regenerate the gRPC stubs for all packages in the repository.

```pwsh
# PowerShell
poetry run python generate_stubs.py
```

## Options

**`grpc-generator --help`**
```
Usage: grpc-generator [OPTIONS]

  Generate gRPC Python stubs from proto files.

  Specifying input and output locations

    This script uses the protobuf files from the folder specified by --proto-
    basepath and --proto-subpath and emits Python files into the folder
    specified by --output-basepath:

    {proto-basepath}/{proto-subpath}  -->  {output-basepath}/{proto-subpath}

    The script resolves gRPC imports from --proto-basepath by default. Include
    additional paths by using --proto-include-path for each required folder.

  Specifying output format

    The script supports generating gRPC packages as either subpackages or
    submodules with --output-format.

    When generating submodules, the script creates Python files with names
    that match the source protobuf files:

    waveform.proto  -->  waveform_pb2.py

    When generating subpackages, the script creates folders with names that
    match the source protobuf files:

    waveform.proto  -->  waveform_pb2/__init__.py

    Clients use the same "import waveform_pb2" syntax.

Options:
  --output-basepath PATH          Emit the generated gRPC files to PATH
                                  [required]
  --output-format [submodule|subpackage]
                                  Generate a Python submodule or subpackage
                                  [required]
  --proto-basepath PATH           Use PATH as the base for --proto-subpath
                                  [default: C:\dev\ni\git\github\ni-apis-
                                  python\third_party\ni-apis]
  --proto-include-path PATH       Add PATH to the import search list, can be
                                  used more than once  [default:
                                  C:\dev\ni\git\github\ni-apis-
                                  python\third_party\ni-apis]
  --proto-subpath PATH            Use the proto files under PATH as input
                                  [required]
  --help                          Show this message and exit.
  --version                       Show the version and exit.

  Example:

  grpc-generator  --proto-subpath ni/protobuf/types  --output-basepath ../../packages/ni.protobuf.types/src  --output-format submodule
```
