# 12. Use containers

Date: 2023-01-18

## Status

Accepted

## Context

Allow developers and users to take advantage of containers.

## Decision

Provide a single Dockerfile that can build two kinds of container:

- a minimal runtime container that can be used to execute the application in
  isolation without setting up a virtual environment or installing system
  dependencies
- a devcontainer for working on the project with the same isolation as above

CI builds the runtime container and publishes it to ghcr.io.

A .devcontainer folder provides the means to build and launch the developer
container using vscode.

## Consequences

We can label projects as cloud native.
