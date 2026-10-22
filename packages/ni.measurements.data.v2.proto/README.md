# NI Data Store V2 protobuf interfaces

`ni.measurements.data.v2.proto` provides generated Python protobuf messages,
type information, and synchronous and asynchronous gRPC stubs for the NI Data
Store V2 API. It contains no handwritten Data Store client and does not enable
V2 on a server.

This is an unpublished development package. It supports CPython 3.10 and newer
on Windows and Linux.

## Proto source and generation

The V2 definitions used for this development package are currently maintained
in the datastore-service checkout, not in this repository's pinned
`ni/ni-apis` submodule:

| Input | SHA-256 |
| --- | --- |
| `src/datastore/proto/data_store.proto` | `6e54841c93bb862e10f778e8df69b2f6b186dfef7588bd69cd77f5e6b72eb026` |
| `src/datastore/proto/data_store_service.proto` | `18b8d70da25e1cacb2daa48b0ee3eedaea841bc1f8557cc91f7bb420f2c23dd7` |

Shared proto imports were taken from `ni/ni-apis` revision
`dcf7881bc86d0cadf8c4f23734b716040790c11b`. These hashes identify the input
files used to generate the current package.

Generation uses the repository's `tools/grpc_generator` tool with output
format `subpackage`. The current V2 inputs are local to datastore-service, so
generation is not yet reproducible from a clean checkout of this repository
and this package is not yet registered in `packages.json` or the normal CI
generation workflow. The V2 definitions should be added to the canonical
`ni/ni-apis` source and registered here before standard CI/release integration.

## Build and test

From this package directory, install its development dependencies and run:

```powershell
poetry install --with docs
poetry run pytest -v
poetry run nps lint
poetry run mypy
poetry run pyright
poetry run bandit -c pyproject.toml -r src
poetry run sphinx-build docs docs\_build --builder html --fail-on-warning
poetry build
```

For distribution validation, install the built wheel in a separate virtual
environment and import the generated V2 messages and stubs. The V1 and V2
packages can be installed together; their protobuf definitions use distinct
`ni.measurements.data.v1` and `ni.measurements.data.v2` namespaces.

## API scope

The generated package exposes the protobuf contract, including
`DataStoreServiceStub` for synchronous gRPC calls and
`DataStoreServiceAsyncStub` for `asyncio` callers. Use
`ni.measurements.data.v2.client` for the handwritten synchronous low-level
client. A higher-level user-facing API is outside this package's scope.
