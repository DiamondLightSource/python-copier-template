<img src="https://raw.githubusercontent.com/DiamondLightSource/python3-pip-skeleton-cli/main/docs/images/dls-logo.svg"
     style="background: none" width="200px" height="200px" align="right">

[![CI](https://github.com/DiamondLightSource/python-copier-template/actions/workflows/ci.yml/badge.svg)](https://github.com/DiamondLightSource/python-copier-template/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# python-copier-template

Diamond's opinionated [copier](https://copier.readthedocs.io) template for pure Python projects managed by pip. It can be optionally used to:

- Create new projects from
- Update existing projects in line with it
- Keep projects in sync with changes to it
- Provide a source of inspiration to cherry-pick from

Source          | <https://github.com/DiamondLightSource/python-copier-template>
:---:           | :---:
Documentation   | <https://DiamondLightSource.github.io/python-copier-template>
Releases        | <https://github.com/DiamondLightSource/python-copier-template/releases>

It integrates the following tools:

- [setuptools](https://setuptools.pypa.io) and [setuptools-scm](https://setuptools-scm.readthedocs.io) for packaging
- [pip](https://pip.pypa.io) to manage installation
- [pytest](https://docs.pytest.org) for code testing and coverage
- [pre-commit](https://pre-commit.com) to run linting and formatting such as [ruff](https://docs.astral.sh/ruff)
- [pyright](https://microsoft.github.io/pyright) for static type checking
- [sphinx](https://www.sphinx-doc.org) for tutorials, how-to guides, explanations and reference documentation
- [tox](https://tox.wiki) to run the above tasks locally and in CI
- [GitHub Actions](https://docs.github.com/en/actions) to provide CI and deployment to PyPI and GitHub Pages
- [VSCode](https://code.visualstudio.com/docs) settings for running the above tools on save

## Create a new project via Developer Portal

> [!NOTE]
> Template creation from the developer portal is currently under construction, so these instructions do not work yet

Visit <https://dev-portal.diamond.ac.uk/create> and you will see a list of templates that you can create. Pick the one marked `Python Template` and fill in the details of the project.

## Create a new project from the commandline

You will need to `pip install copier` inside an activated `venv`, then you can create a new module via:

```
mkdir /path/to/my-project
# The --trust argument is required to run setup tasks such as initializing a git repository
copier copy --trust gh:DiamondLightSource/python-copier-template /path/to/my-project
```

You can also use it via `pipx run copier` if you have that installed.

<!-- README only content. Anything below this line won't be included in index.md -->

See https://DiamondLightSource.github.io/python-copier-template for more detailed documentation.

