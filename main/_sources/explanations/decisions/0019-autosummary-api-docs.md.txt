# 19. Use autosummary to create API docs

Date: 2024-09-10

## Status

Accepted

## Context

The current sphinx API documentation requires you to paste automodule directives in for each subpackage. This is counter intuitive and also places all the docs on one page. People saw a blank page and assumed API generation was broken.

Using autosummary would give a nicer summary, but requires pasting custom templates in which makes sphinx-autobuild keep reloading forever.

Using autodoc2 would allow md docstrings, but doesn't work with pydantic, and doesn't support google or numpy docstrings.

## Decision

Decided to use autosummary, with one page per subpackage. This means at most 2 reloads of sphinx-autobuild before it settles, which is reasonable.

## Consequences

Try to push a bit of the custom template (generating public_members in member order) up to sphinx.
