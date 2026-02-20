<img src="https://raw.githubusercontent.com/adrien-berchet/python-copier-template/main/docs/images/DUMMY-LOGO.svg"
     style="background: none" width="120px" height="120px" align="right">

[![CI](https://github.com/adrien-berchet/python-copier-template/actions/workflows/ci.yml/badge.svg)](https://github.com/adrien-berchet/python-copier-template/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# python-copier-template

Based on the Diamond's opinionated [copier](https://copier.readthedocs.io) template for pure Python projects. It can be optionally used to:

- Create new projects from
- Update existing projects in line with it
- Keep projects in sync with changes to it
- Provide a source of inspiration to cherry-pick from

Source          | <https://github.com/adrien-berchet/python-copier-template>
:---:           | :---:
Documentation   | <https://adrien-berchet.github.io/python-copier-template>
Releases        | <https://github.com/adrien-berchet/python-copier-template/releases>

It integrates the following tools:

- [setuptools](https://setuptools.pypa.io) and [setuptools-scm](https://setuptools-scm.readthedocs.io) for packaging
- [uv](https://docs.astral.sh/uv/) to manage installation and project lockfile
- [pytest](https://docs.pytest.org) for code testing and coverage
- [pre-commit](https://pre-commit.com) to run linting and formatting such as [ruff](https://docs.astral.sh/ruff)
- [pyright](https://microsoft.github.io/pyright) or [mypy](https://www.mypy-lang.org) for static type checking
- [sphinx](https://www.sphinx-doc.org) for tutorials, how-to guides, explanations and reference documentation
- [tox](https://tox.wiki) to run the above tasks locally and in CI
- [GitHub Actions](https://docs.github.com/en/actions) to provide CI and deployment to PyPI and GitHub Pages

## Example

You can see the template in action in the [example project](https://github.com/adrien-berchet/python-copier-template-example). This is an up to date expansion of the template to illustrate how it looks with all the options enabled.

## Create a new project from the commandline

We recommend that you invoke copier via `uvx`, which will download, install, and run it in its own isolated `venv`.

```
git init --initial-branch=main /path/to/my-project
# $_ resolves to /path/to/my-project
uvx copier copy https://github.com/adrien-berchet/python-copier-template.git $_
```

<!-- README only content. Anything below this line won't be included in index.md -->

See https://adrien-berchet.github.io/python-copier-template for more detailed documentation.
