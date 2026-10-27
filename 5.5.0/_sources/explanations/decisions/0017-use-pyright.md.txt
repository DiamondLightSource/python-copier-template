# 17. Use pyright

Date: 2024-02-15

## Status

Accepted

## Context

Pyright is faster than mypy, and catches more errors.

## Decision

We will use it by default, but retain mypy as an option for existing projects where pyright gives too many errors to quickly migrate.

## Consequences

We will add a new question to let people switch between the two.
