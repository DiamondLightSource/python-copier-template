# 13. Switch to copier

Date: 2024-01-18

## Status

Accepted

## Context

The previous attempt, [python3-pip-skeleton](https://github.com/DiamondLightSource/python3-pip-skeleton) was a repo that can be forked and updates merged into projects tracking it. This was initially encouraging, but led to downstream confusion on who had actually contributed to the repository, as well as messy merges when text that contained the project name (like documentation) was changed upstream.

## Decision

Use [copier](https://copier.readthedocs.io/) which gives the best of both worlds, a templating engine to expand the template, then an update mechanism to apply diffs of the updated template to the project.

## Consequences

We will need to create and document an adoption process for existing skeleton projects to move to this copier template
