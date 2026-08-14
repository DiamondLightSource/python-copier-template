# Setup Developer Environment

These instructions will take you through the minimal steps required to get a dev environment setup, so you can run the tests locally.

## Clone the repository

First clone the repository locally using [Git](https://git-scm.com/downloads). There is a link on the GitHub interface to allow you to do this. SSH is recommended if you have setup a key. Enter the directory that it is cloned into to continue.

## Install dependencies

It is recommended that developers use a [vscode devcontainer](https://code.visualstudio.com/docs/devcontainers/containers). This repository contains configuration to set up a containerized development environment that suits its own needs.

Ensure you have the [vscode devcontainer extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed.

If you are at DLS, then first [setup podman and its fix for devcontainer features](https://dev-portal.diamond.ac.uk/guide/containers/tutorials/podman/#enable-use-of-vscode-features) and then follow [these instructions](https://dev-portal.diamond.ac.uk/guide/containers/tutorials/devcontainer/) for setting up devcontainers on a DLS workstation.

```
code .
```

Click on 'Reopen in Container' when prompted on startup or, if vscode is already running, open the command menu with CTRL+SHIFT+P, search for and run 'Reopen in Container'.

The developer container creates and activates a venv (stored in `/cache/venv-for/path/to/project`) and this will be managed by any `uv sync` command as explained in [](./lock-requirements.md). Any rebuild of the container will recreate this venv, but the dependencies will be stored in a cross container cache so that rebuilds are quick.

## Build and test

Now you have a development environment you can run the tests in a new terminal:

```
tox -p
```

This will run in parallel the following checks:

- [](./build-docs)
- [](./run-tests)
- [](./static-analysis)
- [](./lint)
