# 15. Use ruff

Date: 2024-02-15

## Status

Accepted

## Context

Ruff is faster than flake8 and black, has mostly compatible output, and is gaining popularity.

## Decision

We will switch to using ruff for linting and formatting.

## Consequences

We may have to consider pinning ruff in the future if its output changes regularly.
