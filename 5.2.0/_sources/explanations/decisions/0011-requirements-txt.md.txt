# 11. Pinning requirements

Date: 2023-01-18

## Status

Accepted

## Context

Require the ability to pin requirements for a guaranteed rebuild.
By default CI builds against the latest version of all dependencies, but we
need a mechanism for overriding this behaviour with a lock file
when there are issues.

## Decision

Have every release generate requirements.txt files using pip freeze and
publish them as release assets.

Request that the user download the asset and commit it into the repo in order
to lock dependencies for the next CI build.

## Consequences

There is less overhead in managing lock files. Incoming issues with dependencies
will be highlighted early but can be worked around quickly if needed.
