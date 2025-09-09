# Contributing to `ni-apis-python`

Contributions to `ni-apis-python` are welcome from all!

`ni-apis-python` is managed via Git, with the canonical upstream
repository hosted on GitHub at https://github.com/ni/ni-apis-python. This repo
contains a collection of Python packages for [NI's gRPC APIs](https://github.com/ni/ni-apis).

`ni-apis-python` follows a pull-request model for development.  If you wish to
contribute, you will need to create a GitHub account, fork this project, push a
branch with your changes to your project, and then submit a pull request.

Please remember to sign off your commits (e.g., by using `git commit -s` if you
are using the command line client). This amends your Git commit message with a line
of the form `Signed-off-by: Name Lastname <name.lastmail@emailaddress.com>`. Please
include all authors of any given commit into the commit message with a
`Signed-off-by` line. This indicates that you have read and signed the Developer
Certificate of Origin (see below) and are able to legally submit your code to
this repository.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/)
for more details.

# Getting Started

## Prerequisites

- _(Optional)_ Install [Visual Studio Code](https://code.visualstudio.com/download)
- Install [Git](https://git-scm.com)
  -  _(Optional)_ Configure git to automatically add the `--recurse-submodules` flag with `git config submodule.recurse true`
- Install [Python](https://www.python.org/downloads/), any version from the [README](README.md)
- Install [Poetry](https://python-poetry.org/docs/#installation), version >= 2.1.4

## Clone or update the Git repository

To download the source, clone the Git repository.

```cmd
git clone --recurse-submodules https://github.com/ni/ni-apis-python.git
```

Specifying `--recurse-submodules` includes the [ni-apis](https://github.com/ni/ni-apis)
repository. This is required for the [update gRPC stubs](#update-grpc-stubs-if-needed) workflow.

To update the source, you can update the repository and its submodules.

```cmd
git checkout main
git pull
git submodule update --init --recursive
```

## Select a package to develop

This repository includes multiple Python packages. Some examples:
- `ni.protobuf.types`: types used by [NI's gRPC APIs](https://github.com/ni/ni-apis/)
- `ni.measurementlink.discovery.v1.client`: gRPC client for the NI Discovery Service
- `ni.panels.v1.proto`: Python gRPC stubs for the NI Panel Service

Open a terminal window and navigate to the package that you selected.

```powershell
# Example: Python gRPC stubs for the NI Panel Service
cd packages/ni.panels.v1.proto
```

## Install the package and its dependencies

From the package's subdirectory, run the [`poetry install`](https://python-poetry.org/docs/cli/#install)
command. This creates an in-project virtual environment (`.venv`) and installs
the package's dependencies and dev-dependencies, as specified in its
`pyproject.toml` and `poetry.lock` files.

```powershell
# Include dependencies for linting, analyzing, and testing the package
poetry install

# Include dependencies for building the documentation (requires Python 3.11 or newer)
poetry install --with docs

# Include supplemental dependencies if pyproject.toml has a section with 'extras' in its title
poetry install --extras "group1 group2 ..."
```

## Activate the virtual environment (if needed)

- _(Recommended)_ Activate for each command by prefixing the call with `poetry run {command}`
- Activate for the lifetime of the shell in the terminal with `poetry shell`
- Activate in VS Code ([link](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment))

# Simple Development Loop

```powershell
# Update from main
git checkout main
git pull
git submodule update --init --recursive

# Create a new branch
git switch --create users/{username}/{branch-purpose}

# Select and package and install its dependencies
# Example: APIs used by nipanel-python
cd packages/ni.panels.v1.proto
poetry install --with docs

# ✍ Make source changes

# Run the analyzers -- see files in .github/workflows for details
poetry run nps lint
poetry run mypy
poetry run pyright

# Apply safe fixes
poetry run nps fix

# Run the tests
poetry run pytest -v

# Build the documentation
poetry run sphinx-build docs docs/_build --builder html --fail-on-warning
start docs/_build/index.html
```

# Update gRPC Stubs (If Needed)

Packages that have `.proto` in their name contain Python files generated from the
matching protobuf package in the `ni-apis` Git submodule. These
Python files must be regenerated whenever the upstream `.proto` files change.

The Python package in `tools/grpc_generator` has scripts to help.

```powershell
# Initialize the tool
cd tools/grpc_generator
poetry install
```

## All packages

Regenerate the Python files for every package by running the `generate-stubs` script.

```powershell
# From tools/grpc_generator
poetry run generate-stubs
```

## Single package

Regenerate the Python files for a specific package by running the `grpc-generator` script.

```powershell
# From tools/grpc_generator
# Example: APIs used by nipanel-python
poetry run grpc-generator `
  --proto-subpath ni/panels/v1 `
  --output-basepath ../../packages/ni.panels.v1.proto/src `
  --output-format submodule
```

Each package lists its required generation options in this repository's [packages.json](./packages.json) file.

# Add a New Package

To add a new package to this repo:
1. Create a new folder under `packages` with the new package name.
2. Create the front matter files for the package:
   - `pyproject.toml`
   - `poetry.toml`
   - `README.md`
   - `.readthedocs.yml`
3. Create new folders under the new package:
   - `docs`
   - `src`
   - `tests`
4. Generate the gRPC stubs using `grpc-generator`
5. Create documentation control and content files under the `docs` folder
6. Create tests for the package under the `tests` folder
7. Update the `packages.json` file at the root of this repository

## packages.json

### Schema
- All keys are strings
- All values are strings or `null` when they do not apply to the package

```jsonc
// Folder name for the package
"string": {

  // Path to package folder, relative to the repo root
  "package-basepath": "string",

  // The base path to the proto files used for generation, relative to the repo root
  "proto-basepath": "string" | null,

  // The specific subpath to the proto files needed for generation, relative to the proto-basepath
  "proto-subpath": "string" | null,

  // Additional path to include during proto generation, relative to the repo root
  "proto-include-path": "string" | null,

  // The format for the generated stubs. Options are submodule and subpackage
  "output-format": "string" | null,

  // A space-separated list of package extras to install
  "install-extras": "string" | null
}
```

### Example for proto package

```json
"ni.panels.v1.proto": {
  "package-basepath": "packages",
  "proto-basepath": "third_party/ni-apis",
  "proto-subpath": "ni/panels/v1",
  "proto-include-path": "third_party/ni-apis",
  "output-format": "submodule",
  "install-extras": null
}
```

### Example for non-proto package

```json
"ni.measurementlink.sessionmanagement.v1.client": {
  "package-basepath": "packages",
  "proto-basepath": null,
  "proto-subpath": null,
  "proto-include-path": null,
  "output-format": null,
  "install-extras": "drivers"
}
```

# Publish a Package

You can publish one of the packages in the `packages` folder by creating a GitHub release
in the ni-apis-python repo. Here are the steps to follow to publish a package:

1. From the main GitHub repo page, select "Create a new release".
2. On the "New Release" page, create a new tag using the "Select Tag" drop down. The tag must be in the
format `<package-name>/<package-version>` where `package-name` and `package-version` match the
values found in pyproject.toml. Example: `ni.protobuf.types/0.1.0-dev0`.
3. Enter a title in the "Release title" field. The title should contain the package name and
version in the format `<package-name> <package-version>`. For example: `ni.protobuf.types 0.1.0-dev0`.
4. Click "Generate release notes" and edit the release notes.
   - Delete entries for PRs that do not affect users, such as "chore(deps):" and "fix(deps):" PRs.
   - Consider grouping related entries.
   - Reformat entries to be more readable. For example, change "Blah blah by so-and-so in \#123" to "Blah blah (\#123)".
5. If this is a pre-release release, check the "Set as a pre-release" checkbox.
6. Click "Publish release".
7. Creating a release will start the publish workflow. You can track the
progress of this workflow in the "Actions" page of the GitHub repo.
8. The workflow job that publishes a package to pypi requires code owner approval. This job will automatically send code owners a notification email, then it will wait for them to log in and approve the deployment.
9. After receiving code owner approval, the publish workflow will resume.
10. Once the publish workflow has finished, you should see your release on pypi.

# gRPC and Protobuf Version Support

- We use the newest version of `grpcio-tools` with binary wheels for each supported version of Python
- We generate stubs using Python 3.11 and test on all supported Python versions
- We rely on `poetry lock` to select the newest compatible version of `protobuf` newer than 4.21

# Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/ni/ni-apis-python/blob/main/LICENSE)
for details about how `ni-apis-python` is licensed.
