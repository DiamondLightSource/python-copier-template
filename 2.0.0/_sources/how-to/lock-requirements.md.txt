# Lock requirements

## Introduction

By design this project only defines dependencies in one place, i.e. in the `requires` table in `pyproject.toml`.

In the `requires` table it is possible to pin versions of some dependencies as needed. For library projects it is best to leave  pinning to a minimum so that your library can be used by the widest range of applications.

When CI builds the project it will use the latest compatible set of dependencies available (after applying your pins and any dependencies' pins).

This approach means that there is a possibility that a future build may break because an updated release of a dependency has made a breaking change.

The correct way to fix such an issue is to work out the minimum pinning in `requires` that will resolve the problem. However this can be quite hard to do and may be time consuming when simply trying to release a minor update.

For this reason we provide a mechanism for locking all dependencies to the same version as a previous successful release. This is a quick fix that should guarantee a successful CI build.

## Finding the lock files

Every release of the project will have a set of requirements files published as release assets.

For example take a look at the release page for python-copier-template [here](https://github.com/DiamondLightSource/python-copier-template/releases/tag/1.1.0)

There is a single `dev-requirements.txt` file showing as an asset on the release. This has been created using `pip freeze --exclude-editable` on a successful test run using the same version of python as the devcontainer, and will contain a full list of the dependencies and sub-dependencies with pinned versions. You can download this file by clicking on it.

## Applying the lock file

To apply a lockfile:

- copy the requirements file you have downloaded to the root of your repository
- commit it into the repo
- push the changes

The CI looks for a `dev-requirements.txt` in the root and will pass it to pip as a constraint when installing the dev environment. If a package is required to be installed by `pyproject.toml` then `pip` will use the version specified in `dev-requirements.txt`.

## Removing dependency locking from CI

Once the reasons for locking the build have been resolved it is a good idea to go back to an unlocked build. This is because you get an early indication of any incoming problems.

To restore unlocked builds in CI simply remove `dev-requirements.txt` from the root of the repo and push.
