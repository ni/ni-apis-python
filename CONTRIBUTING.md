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
- Install [Poetry](https://python-poetry.org/docs/#installation), version >= 1.8.2

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
- _(waiting for upload -- AB#3159540)_: APIs used by [`nipanel-python`](https://github.com/ni/nipanel-python)

Open a terminal window and navigate to the package that you selected.

```sh
# Example: APIs used by nipanel-python
cd packages\(waiting for upload -- AB#3159540)
```

## Install the package and its dependencies

From the package's subdirectory, run the [`poetry install`](https://python-poetry.org/docs/cli/#install)
command. This creates an in-project virtual environment (`.venv`) and installs
the package's dependencies and dev-dependencies, as specified in its
`pyproject.toml` and `poetry.lock` files.

```cmd
poetry install
```

## Activate the virtual environment (if needed)

- _(Recommended)_ Activate for each command by prefixing the call with `poetry run {command}`
- Activate for the lifetime of the shell in the terminal with `poetry shell`
- Activate in VS Code ([link](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment))

# Simple Development Loop

```sh
# Update from main
git checkout main
git pull
git submodule update --init --recursive

# Create a new branch
git switch --create users/{username}/{branch-purpose}

# Select and package and install its dependencies
# Example: APIs used by nipanel-python
cd packages\(waiting for upload -- AB#3159540)
poetry install

# ✍ Make source changes

# Run the analyzers -- see files in .github/workflows for details
poetry run nps lint
poetry run mypy

# Apply safe fixes
poetry run nps fix

# Run the tests
poetry run pytest -v
```

# Update gRPC Stubs (If Needed)

Each package in this repository contains Python files generated from the
matching protobuf (`.proto`) package in the `ni-apis` Git submodule. These
Python files must be regenerated whenever the `.proto` files change.

To regenerate the Python files for a package, run the code generator on its directory.

```sh
# Example: APIs used by nipanel-python
(waiting for upload -- AB#3159540)
```

To preview in-work `.proto` file changes, (waiting for upload -- AB#3159540).

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
