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
| `src/datastore/proto/data_store.proto` | `49cdb98fca6b4dae02bc2e1117960ab9292b5161028c7ed219b680a3525841b2` |
| `src/datastore/proto/data_store_service.proto` | `6e84fcf45c6b9949ce8e26bb857e6b72d0b0036fcd601f959048b1088e2ffa32` |

The datastore-service checkout was at
`f8a07b98257eb4acf80f67bad26f810e3d5a0114` when the inputs were captured;
the hashes identify the actual working files.
Shared imports come from `ni/ni-apis` revision
`dcf7881bc86d0cadf8c4f23734b716040790c11b`.
Do not include the adjacent notification or streaming definitions: they still
declare V1.

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
