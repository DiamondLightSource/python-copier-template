# 14. Split up CI YAML

Date: 2024-01-31

## Status

Accepted

## Context

The existing monolithic CI had some problems:

- We want some parts to be optional, which required templated CI which then couldn't be easily tested
- We wanted to reuse some parts of the CI in the template repo
- It was long and hard to read
- It was split into multiple top level jobs

## Decision

Break it into multiple [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows) that are called from:
- A single `ci` workflow that runs on push, and tests, builds, and adds artifacts to releases
- A single `periodic` workflow that runs once a week and checks links aren't broken

## Consequences

We can reuse workflows in the template repo
