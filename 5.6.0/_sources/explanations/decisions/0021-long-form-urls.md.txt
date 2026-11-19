# 21. Use long-form URLs in documentation

Date: 2025-05-07

## Status

Accepted

## Context

Copier supports shortcut URLs (see [docs](https://copier.readthedocs.io/en/stable/generating)) of the form `gh:namespace/project`. This was convenient for making our documentation look neater and more digestible to new users, however it is just a convention. When trying to integrate other tools with copier we find that they do not necessarily support the convention. See [this discussion](https://github.com/renovatebot/renovate/discussions/35577) for example.

## Decision

Remove shortcut URLs from this repository and replace them with standard URLs. 

## Consequences

Downstream projects following the documentation will be created with standard URLs and will be supported by renovate and other tools. The alternative solution is to open PRs to these tools so they too support the shortcuts. It was decided that it was quicker, easier and probably more architecturally correct to use long-form URLs since they are already a well-known and widely adopted standard. See [this discussion](https://github.com/epics-containers/services-template-helm/issues/21#issuecomment-2855125741).
