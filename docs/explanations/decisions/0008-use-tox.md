# 8. Use tox and pre-commit

Date: 2023-01-18

## Status

Accepted

## Context

We require an easy way to locally run the same checks as CI. This provides a
rapid inner-loop developer experience.

## Decision

Use tox and pre-commit.

tox is an automation tool that we use to run all checks in parallel,
see <https://tox.wiki/en/latest/>.

pre-commit provides a hook into git commit which runs some of the checks
against the changes you are about to commit.

## Decision detail

There are a number of things that CI needs to run:

- pytest
- black
- mypy
- flake8
- isort
- build documentation

The initial approach this module took was to integrate everything
under pytest that had a plugin, and isort under flake8:

```{eval-rst}
.. digraph:: initial

    bgcolor=transparent
    graph [fontname="Lato" fontsize=10 style=filled fillcolor="#8BC4E9"]
    node [fontname="Lato" fontsize=10 shape=box style=filled fillcolor="#8BC4E9"]

    subgraph cluster_0 {
      label = "pytest"
      "pytest-black"
      "pytest-mypy"
      subgraph cluster_1 {
        label = "pytest-flake8"
        "flake8-isort"
      }
    }
```

This had the advantage that a `pytest tests` run in CI would catch and
report all test failures, but made each run take longer than it needed to. Also,
flake8 states that it [does not have a public, stable, Python API](https://flake8.pycqa.org/en/latest/user/python-api.html) so did not
recommend the approach taken by pytest-flake8.

To address this, the tree was rearranged:

```{eval-rst}
.. digraph:: rearranged

    bgcolor=transparent
    graph [fontname="Lato" fontsize=10 style=filled fillcolor="#8BC4E9"]
    node [fontname="Lato" fontsize=10 shape=box style=filled fillcolor="#8BC4E9"]

    pytest
    black
    mypy
    subgraph cluster_1 {
      label = "flake8"
      "flake8-isort"
    }
```

If using VSCode, this will still run black, flake8 and mypy on file save, but
for those using other editors and for CI another solution was needed. Enter
[pre-commit](https://pre-commit.com/). This allows hooks to be run at `git
commit` time on just the files that have changed, as well as on all tracked
files by CI. All that is needed is a one time install of the git commit hook:

```
$ pre-commit install
```

Finally tox was added to run all of the CI checks including
the documentation build. mypy was moved out of the pre-commit and into tox
because it was quite long running and
therefore intrusive. tox can be invoked to run all the checks in
parallel with:

```
$ tox -p
```

The graph now looks like:

```{eval-rst}
.. digraph:: rearranged

    bgcolor=transparent
    graph [fontname="Lato" fontsize=10 style=filled fillcolor="#8BC4E9"]
    node [fontname="Lato" fontsize=10 shape=box style=filled fillcolor="#8BC4E9"]

    subgraph cluster_0
    {
        label = "tox -p"
        pytest
        mypy
        "sphinx-build"
        subgraph cluster_1 {
            label = "pre-commit"
            black
            subgraph cluster_2 {
                label = "flake8"
                "flake8-isort"
            }
        }
    }
```

Now the workflow looks like this:

- Save file, VSCode runs black, flake8 and mypy on it
- Run 'tox -p' and fix issues until it succeeds
- Commit files and pre-commit runs black and flake8 on them (if the
  developer had not run tox then this catches some of the most common issues)
- Push to remote and CI runs black, flake8, mypy once on all files
  (using tox), then pytest multiple times in a test matrix

## Consequences

Running `tox -p` before pushing to GitHub verifies that the CI will *most
likely* succeed.

Committing changes to git will run all of the non-time critical checks and
help avoid some of the most common mistakes.
