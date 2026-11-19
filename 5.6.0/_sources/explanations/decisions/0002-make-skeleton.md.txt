# 2. Make a skeleton repository

Date: 2022-06-18

## Status

Accepted

## Context

Many projects start from some kind of template. These define some basic structure, customized with project specific variables, that developers can add their code into. One example of this is [cookiecutter](https://cookiecutter.readthedocs.io).

The problem with this approach is that it is difficult to apply changes to the template into projects that have been cut from it. Individual changes have to be copy/pasted into the code, leading to partially applied fixes and missed updates.

## Decision

We will use a skeleton structure as defined in [Jaraco's blog](https://blog.jaraco.com/a-project-skeleton-for-python-projects/), using git to keep the downstream projects up to date.

## Consequences

We will need a cli module to ease the adoption of this
