# 18. Forbid Private Member Access in Production Code

Date: 2024-07-02

## Status

Accepted

## Context

Most programming languages forbid access to private member variables at compile time to guarantee encapsulation. Python only does this by convention. Ruff now provides a rule (SLF001) that forbids it.
See https://github.com/DiamondLightSource/python-copier-template/issues/154 for further discussion.

## Decision

We will enable SLF001 for the `src` directory but not the `tests` directory, as we want to keep production code clean without raising the barrier to entry for writing tests.

## Consequences

Any private member access in `src` will cause CI to fail, the ultimate override of `noqa` remains available.
