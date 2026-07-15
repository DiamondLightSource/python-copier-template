# 21. Semantic Versioning and Conventional Commits

Date: 2025-04-07

## Status

Proposed

## Context

The template is in a period of both upheaval and uptake, where new users may adopt its use amidst major version changes.
To give some certainty to users, we should document changes and highlight important ones.
As dependency management becomes more automated, we should ensure that semantic versioning is used accurately, and make allowances for automation.

## Decision

Commits to the default branch of the copier template should be made using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), and the Conventional Commit standard should be used to identify the next released version and create changelogs/release notes.

## Consequences

A [GitHub Action](https://github.com/ytanikin/PRConventionalCommits) has been configured to ensure that PRs may not be merged without being in the form of a Conventional Commit.
PRs will be squash-and-merged, with the complete git history of the change preserved in the PR but only a single commit on the default branch.
PR commit messages will be taken from the title and body of the PR, ensuring that the commit will be compatible with the standard.
Tooling (dependabot etc.) will be configured to make compatible PRs.
