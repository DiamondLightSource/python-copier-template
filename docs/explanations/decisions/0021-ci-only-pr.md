# 21. Run CI on pull requests and main branch only

Date: 2025-05-06

## Status

Accepted

## Context

CI has been being run on branches that do not have open pull requests, which has: added spurious jobs to the organisation's compute limit; made workflow definitions more complex; made the results page harder to parse; and allowed known working development branches to become stale or forgotten.

Running CI only on branches that have open pull requests will: reduce compute jobs created for code that is known to not be working; simplify workflow definitions; simplify the CI results page; encourage early creation of pull requests, adding visibility to development.

Draft pull requests will still have CI jobs run, ensuring that code quality is maintained while allowing reviewers to ignore changes that are not ready for human review.

## Decision

CI will only be run on all PRs when changes are made, and on the main branch when PRs are merged into it: not on branches that do not have open PRs.
Opening a draft PR will allow CI to be run, with the understanding that the PR may not be ready for review.

## Consequences

The `check` job will be removed and CI will run on all PRs and on the `main` branch.
