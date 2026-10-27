# 20. Support devcontainers as the opinionated way to contribute

Date: 2025-04-07

## Status

Accepted

## Context

The Python copier template is growing more opinionated over time. It includes a `.devcontainer` and `.vscode` directory committed to version control, providing out-of-box configuration for contributors to set up development environments. In general we have preferred contributors to use the devcontainer rather than a local [venv](https://docs.python.org/3/library/venv.html), as it means development takes place in a consistent environment and it is much easier to support contributors and diagnose their problems by locally reproducing their environments. We can also vend a consistent, tested set of recommended vscode plugins.

## Decision

[Devcontainers](https://code.visualstudio.com/docs/devcontainers/containers) are the opinionated way to contribute to projects based on this template. The template will be developed, maintained and tested on the assumption that a contributor is using a devcontainer.

## Consequences

The Python copier template development environment is no longer guaranteed to work outside of a devcontainer. Support is not guaranteed for contributors not using a devcontainer, in the first instance requests for such support should be answered with gentle encouragement to adopt them.

This does not mean non-devcontainer environments are forbidden or designed out, but it does mean the individual contributor is responsible for maintaining such environments, making them work and dealing with any breaking changes themselves. The devcontainer environment is provided for contributors who want something that works out-of-box and is supported, so they can get started quickly. 
