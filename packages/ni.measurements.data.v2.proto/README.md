# NI Data Store V2 protobuf interfaces

`ni.measurements.data.v2.proto` provides generated messages, type information,
and raw gRPC stubs for `ni.measurements.data.v2`. It does not provide a
handwritten client or enable V2 on a server. This is an unpublished development
package supporting CPython 3.10+ on Windows and Linux.

## Local development inputs

V2 definitions are not yet in this repository's pinned `ni/ni-apis` revision.
For this phase, generation uses these files from the datastore-service checkout:

| Input | SHA-256 |
| --- | --- |
| `src/datastore/proto/data_store.proto` | `6e54841c93bb862e10f778e8df69b2f6b186dfef7588bd69cd77f5e6b72eb026` |
| `src/datastore/proto/data_store_service.proto` | `18b8d70da25e1cacb2daa48b0ee3eedaea841bc1f8557cc91f7bb420f2c23dd7` |

The input hashes were refreshed on 2026-10-22 and identify the actual working
files, independently of the datastore-service checkout's commit.
Shared imports come from `ni/ni-apis` revision
`dcf7881bc86d0cadf8c4f23734b716040790c11b`.
Do not include the adjacent notification or streaming definitions: they still
declare V1.

The current contract uses `ReadMeasurementValues`, with a `read_mask` selecting
`value`, `upper_limit`, and `lower_limit`. An omitted or empty mask selects all
three. The previous singular `ReadMeasurementValue` RPC and message names are
not part of this contract.

## Generate locally

Install the existing generator with Python 3.11, following
[CONTRIBUTING.md](../../CONTRIBUTING.md). From this package directory:

```powershell
.\generate.ps1 `
  -DatastoreProtoPath 'C:\path\to\datastore-service\src\datastore\proto' `
  -SharedProtoPath 'C:\path\to\ni-apis'
```

The shared-proto path must contain the `ni` directory and match the recorded
revision. The helper creates a temporary namespace-organized copy of the two
V2 inputs and qualifies the service's `data_store.proto` import. It invokes the
existing generator with `subpackage` output and removes the temporary inputs.
It does not change the datastore checkout, update submodules, or edit generated
Python. Proto filenames in descriptors use the future upstream namespace path.
The message definitions and RPC contracts are unchanged.

For reproducibility, run the same command twice with identical inputs and the
generator's locked Python 3.11 environment, and compare hashes under `src`.

## Build and test

```powershell
poetry env use 'C:\path\to\python3.11.exe'
poetry lock
poetry install --with docs
poetry run pytest -v
poetry run nps lint
poetry run mypy
poetry run pyright
poetry run bandit -c pyproject.toml -r src
poetry run sphinx-build docs docs\_build --builder html --fail-on-warning
poetry build
```

Install the built wheel in a separate virtual environment to validate the
distribution, not just the source checkout. Runtime dependency declarations use
package versions; local paths are development-only. V1 is a development
dependency for coexistence tests, not a runtime dependency.

## Upstream integration before release

This local-only package is intentionally not registered in `packages.json` or
the publish workflow yet. A clean CI checkout cannot regenerate from a
developer's datastore folder. No generation check has been disabled.

Once the approved definitions are merged into `ni/ni-apis`:

1. With approval, update the submodule pin to the approved upstream revision.
2. Register this package in `packages.json` with `proto-basepath` and
   `proto-include-path` set to `third_party/ni-apis`, `proto-subpath` set to
   `ni/measurements/data/v2`, and `output-format` set to `subpackage`.
3. Regenerate with the normal repository tool, review contract differences,
   and rerun tests, analyzers, documentation, and installed-wheel checks.
4. Remove the local-only helper and replace these generation instructions.
5. During the separate publishing task, configure the package's publishing
   selector, ownership, version, and approved release process.

The existing package-discovery workflows then include the package in CI.
Linux and the full Python 3.10-3.14 matrix require that CI integration.
