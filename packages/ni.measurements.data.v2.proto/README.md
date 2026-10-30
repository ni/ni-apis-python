# Table of Contents

- [Table of Contents](#table-of-contents)
- [About](#about)
  - [Operating System Support](#operating-system-support)
  - [Python Version Support](#python-version-support)
- [Installation](#installation)

# About

`ni.measurements.data.v2.proto` is a Python package that provides data types
and service stubs for the NI Data Store V2 gRPC API defined in the
[ni.measurements.data.v2 package](https://github.com/ni/ni-apis/tree/main/ni/measurements/data/v2).

NI created and supports this package.

## Operating System Support

`ni.measurements.data.v2.proto` supports Windows and Linux operating systems.

## Python Version Support

`ni.measurements.data.v2.proto` supports CPython 3.10+.

## Installation

You can directly install the `ni.measurements.data.v2.proto` package using
`pip` or by listing it as a dependency in your project's `pyproject.toml` file.

To use the generated gRPC service stubs, install the optional `grpc` extra:

```shell
pip install "ni.measurements.data.v2.proto[grpc]"
```
