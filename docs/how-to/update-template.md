# How to update to the latest template structure

## Overview

To track changes to the upstream template, run

```
copier update --trust
```

This will fetch the latest tagged release of the template, and apply any changes to your working copy. It will prompt for answers again, giving your previous answers as the defaults.

It will stage all the changes for commit, but there may be merge conflicts that need fixing first, find them with

```
git diff --check
```

Once they are all fixed, make a commit.

## Recommended Workflow

The following steps are recommended to update your project, especially for infreqently updated projects:

- first make sure all the tools are updated to latest versions
    - for devcontainers
        - `ctrl+shift+p` -> `Remote-Containers: Rebuild Without Cache and Reopen in Container`
    - for local development
        - `pip install -e .[dev] --force-reinstall`
- validate your project against the latest tools
    - `tox -p`
- fix issues found by the above
- commit the changes
- update the template
    - `copier update --trust`
- fix any merge conflicts
- validate that the project still works
    - `tox -p`
- fix any issues found by the above
- commit the changes
