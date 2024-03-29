# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from importlib.metadata import version
from pathlib import Path
from subprocess import check_output

import requests

# -- General configuration ------------------------------------------------

# General information about the project.
project = "python-copier-template"

# The full version, including alpha/beta/rc tags.
release = version(project)

# The short X.Y version.
if "+" in release:
    # Not on a tag, use branch name
    root = Path(__file__).absolute().parent.parent
    git_branch = check_output("git branch --show-current".split(), cwd=root)
    version = git_branch.decode().strip()
else:
    version = release

extensions = [
    # For graphviz diagrams
    "sphinx.ext.graphviz",
    # For linking to external sphinx documentation
    "sphinx.ext.intersphinx",
    # Add a copy button to each code block
    "sphinx_copybutton",
    # For the card element
    "sphinx_design",
    # So we can write markdown files
    "myst_parser",
]

# So we can use the ::: syntax
myst_enable_extensions = ["colon_fence"]

# If true, Sphinx will warn about all references where the target cannot
# be found.
nitpicky = True

# A list of (type, target) tuples (by default empty) that should be ignored when
# generating warnings in "nitpicky mode". Note that type should include the
# domain name if present. Example entries would be ('py:func', 'int') or
# ('envvar', 'LD_LIBRARY_PATH').
nitpick_ignore = []

# Output graphviz directive produced images in a scalable format
graphviz_output_format = "svg"

# The name of a reST role (builtin or Sphinx extension) to use as the default
# role, that is, for text marked up `like this`
default_role = "any"

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# These patterns also affect html_static_path and html_extra_path
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# This means you can link things like `str` and `asyncio` to the relevant
# docs in the python documentation.
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}

# A dictionary of graphviz graph attributes for inheritance diagrams.
inheritance_graph_attrs = {"rankdir": "TB"}

# Common links that should be available on every page
rst_epilog = """
.. _Diamond Light Source: http://www.diamond.ac.uk
.. _ruff: https://github.com/astral-sh/ruff
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pyright: https://microsoft.github.io/pyright/#/
.. _pre-commit: https://pre-commit.com/
"""

# Set copy-button to ignore python and bash prompts
# https://sphinx-copybutton.readthedocs.io/en/latest/use.html#using-regexp-prompt-identifiers
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
github_repo = project
github_user = "DiamondLightSource"
switcher_json = f"https://{github_user}.github.io/{github_repo}/switcher.json"
switcher_exists = requests.get(switcher_json).ok
if not switcher_exists:
    print(
        "*** Can't read version switcher, is GitHub pages enabled? \n"
        "    Once Docs CI job has successfully run once, set the "
        "Github pages source branch to be 'gh-pages' at:\n"
        f"    https://github.com/{github_user}/{github_repo}/settings/pages",
        file=sys.stderr,
    )

# Theme options for pydata_sphinx_theme
# We don't check switcher because there are 3 possible states for a repo:
# 1. New project, docs are not published so there is no switcher
# 2. Existing project with latest copier template, switcher exists and works
# 3. Existing project with old copier template that makes broken switcher,
#    switcher exists but is broken
# Point 3 makes checking switcher difficult, because the updated copier template
# will fix the switcher at the end of the docs workflow, but never gets a chance
# to complete as the docs build warns and fails.
html_theme_options = {
    "logo": {
        "text": project,
    },
    "use_edit_page_button": True,
    "github_url": f"https://github.com/{github_user}/{github_repo}",
    "switcher": {
        "json_url": switcher_json,
        "version_match": version,
    },
    "check_switcher": True,
    "navbar_end": ["theme-switcher", "icon-links", "version-switcher"],
}

# A dictionary of values to pass into the template engine’s context for all pages
html_context = {
    "github_user": github_user,
    "github_repo": github_repo,
    "github_version": version,
    "doc_path": "docs",
}

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = False

# Logo
html_logo = "images/dls-logo.svg"
html_favicon = html_logo
