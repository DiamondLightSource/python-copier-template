# 16. Convert to mkdocs

Date: 2024-02-15

## Status

Rejected

## Context

Markdown is nicer to write, we have to write using mkdocs for the developer portal and backstage likes it, should we switch to using it?

It can mostly replace sphinx, but there are a few places it falls down:

- The API docs (mkdocstrings) have some paid for features that we already use in sphinx
- The plugin landscape is vast, but not well maintained
- The scientific python community (i.e. numpy, scipy, matplotlib, bluesky) uses sphinx exclusively
- There are custom directives like the ipython one that we would struggle to replace

## Decision

We will stick with sphinx for now, but use MyST so we can write markdown with it.

## Consequences

We will keep an eye on mkdocs.
