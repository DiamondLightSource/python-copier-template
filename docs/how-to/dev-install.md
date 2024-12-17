# Setup Developer Environment

These instructions will take you through the minimal steps required to get a dev environment setup, so you can run the tests locally.

## Clone the repository

First clone the repository locally using [Git](https://git-scm.com/downloads). There is a link on the GitHub interface to allow you to do this. SSH is recommended if you have setup a key. Enter the directory that it is cloned into to continue.

## Install dependencies

You can choose to either develop on the host machine using a `venv` (which requires python 3.10 or later) or to run in a container under [VSCode](https://code.visualstudio.com/)

<!-- https://sphinx-design.readthedocs.io/en/latest/tabs.html# -->
::::{tab-set}

:::{tab-item} Local virtualenv
```
python -m venv venv
source venv/bin/activate
pip install -e '.[dev]'
```
:::

:::{tab-item} VSCode devcontainer

Ensure you have the [vscode devcontainer extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed.

If you are at DLS, then first [setup podman and its fix for devcontainer features](https://dev-portal.diamond.ac.uk/guide/containers/tutorials/podman/#enable-use-of-vscode-features) and then follow [these instructions](https://dev-portal.diamond.ac.uk/guide/containers/tutorials/devcontainer/) for setting up devcontainers on a DLS workstation.

```
code .
```

Click on 'Reopen in Container' when prompted on startup or, if vscode is already running, open the command menu with CTRL+SHIFT+P, search for and run 'Reopen in Container'.
Open a new terminal
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
