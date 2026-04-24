# 6. Use setuptools_scm

Date: 2023-01-18

## Status

Accepted

## Context

We require a mechanism for generating version numbers in python.

## Decision

Generate the version number from git tags using setuptools scm.

See <https://github.com/pypa/setuptools_scm/>

## Consequences

Versions are generated automatically from git tags. This means you can
can verify if you are running a released version of the code as
setup tools scm adds a suffix to untagged commits.
