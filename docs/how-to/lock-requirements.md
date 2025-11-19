# Lock requirements

## Introduction

Since the move to `uv`, this project natively supports a lockfile. This is a set of "known good" dependencies that the tests are run against, and will be used to create a container if one is built.

## Specifying dependencies

The source of dependencies is the project's `pyproject.toml`. They can come from:
- Project dependencies (from `[project]` `dependencies =`)
- Dev dependencies (from `[dependency-groups]` `dev =`)
- Transitive dependencies (child dependencies of the above)

Dependencies are loosely specified in `pyproject.toml`, like `sphinx-autobuild` or `pydata-sphinx-theme>=0.12`. They should state a minimum version if you are using features that are added in a specific version. There should be no upper bound by default, only insert one if an upstream release of a dependency breaks your code, and you don't have time to fix it immediately.

## Updating the lockfile

When you have updated `pyproject.toml` then run:
```
$ uv sync
```

This will ensure that any new dependencies you add will be placed in the lockfile, and your venv updated to match. It will *not* update any existing dependencies, unless `pyproject.toml` requires a later version.

This command will be run by [pre-commit](./lint) during a `git commit` and by CI.

To update all dependencies to their latest versions run:
```
uv sync --upgrade
```
This command will be run [renovate](./renovate) once a week in CI.

```{seealso}
[The uv docs on locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync)
```

## Modifying the venv to add other projects

Peer projects (those checked out next to the project) are visible in the devcontainer, and can be added into the venv by running `uv pip install -e ../other_project`. This will allow live changes made in this other project to be immediately reflected in the venv.

```{note}
This venv is activated by default, and global to the container, so if you `uv sync` from `other_project` then it will **replace** the contents of the venv with `other_project`'s dependencies.
```
