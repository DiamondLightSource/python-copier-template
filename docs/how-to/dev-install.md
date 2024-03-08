# Setup Developer Environment

These instructions will take you through the minimal steps required to get a dev environment setup, so you can run the tests locally.

## Clone the repository

First clone the repository locally using [Git](https://git-scm.com/downloads). There is a link on the GitHub interface to allow you to do this. SSH is recommended if you have setup a key. Enter the directory that it is cloned into to continue.

## Install dependencies

You can choose to either develop on the host machine using a `venv` (which requires python 3.8 or later) or to run in a container under [VSCode](https://code.visualstudio.com/)

<!-- https://sphinx-design.readthedocs.io/en/latest/tabs.html# -->
::::{tab-set}

:::{tab-item} Local virtualenv
```
python3 -m venv venv
source venv/bin/activate
pip install -c requirements/constraints.txt -e .[dev]
```
:::

:::{tab-item} VSCode devcontainer
If you are at DLS, then first [setup podman and its fix for devcontainer features](https://dev-portal.diamond.ac.uk/guide/containers/tutorials/podman/#enable-use-of-vscode-features)

```
code .
# Click on 'Reopen in Container' when prompted
# Open a new terminal
:::

::::

## Build and test

Now you have a development environment you can run the tests in a terminal:

```
tox -p
```

This will run in parallel the following checks:

- [](./build-docs)
- [](./run-tests)
- [](./static-analysis)
- [](./lint)
