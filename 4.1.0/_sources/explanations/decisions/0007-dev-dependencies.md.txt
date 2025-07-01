# 7. Installing developer environment

Date: 2023-01-18

## Status

Accepted

## Context

We need to provide a way to setup a developer environment for a skeleton based
project.

## Decision

Use optional dependencies in pyproject.toml.

PEP 621 provides a mechanism for adding optional dependencies in pyproject.toml
<https://peps.python.org/pep-0621/#dependencies-optional-dependencies>.

We supply a list of developer dependencies under the title "dev". These
developer dependencies enable building and testing the project and
its documentation.

## Consequences

Any developer can update their virtual environment in order to work on
a skeleton based project with the command:

`` `bash
pip install -e .[dev]
` ``
