How to adopt the skeleton in an existing repo
=============================================

If you have an existing repo and would like to adopt the skeleton structure
then you can use the commandline tool to merge the skeleton into your repo::

    python3-pip-skeleton existing /path/to/existing/repo --org my_github_user_or_org --skeleton-org some_institution

This will:

- Take the repo name from the last element of the path
- Take the package name from the repo name unless overridden by ``--package``
- Clone the existing repo in /tmp
- Create a new orphan merge branch from the skeleton repo
- Use the version of the skeleton in ``some_institution``'s organization (default ``DiamondLightSource``)
- Create a single commit that modifies the skeleton with the repo and package name
- Push that merge branch back to the existing repo
- Merge with the currently checked out branch, leaving you to fix the conflicts

.. note::

    To enable publishing to PyPI see `../how-to/pypi`

.. note::

    To install the pre-commit see `../../developer/how-to/lint`

Example merge
-------------

As an example, `scanspec #46
<https://github.com/dls-controls/scanspec/pull/46>`_ shows the what this
adoption looks like. The commandline tool was run on the existing repo::

    $ cd /path/to/scanspec
    $ git checkout -b adopt-skeleton
    Switched to a new branch 'adopt-skeleton'
    $ python3-pip-skeleton existing .
    Auto-merging src/scanspec/__main__.py
    CONFLICT (add/add): Merge conflict in src/scanspec/__main__.py
    Auto-merging src/scanspec/__init__.py
    CONFLICT (add/add): Merge conflict in src/scanspec/__init__.py
    Auto-merging setup.cfg
    CONFLICT (add/add): Merge conflict in setup.cfg
    Auto-merging pyproject.toml
    CONFLICT (add/add): Merge conflict in pyproject.toml
    Auto-merging docs/tutorials/installation.rst
    CONFLICT (add/add): Merge conflict in docs/tutorials/installation.rst
    Auto-merging docs/reference/api.rst
    CONFLICT (add/add): Merge conflict in docs/reference/api.rst
    Auto-merging docs/index.rst
    CONFLICT (add/add): Merge conflict in docs/index.rst
    Auto-merging docs/conf.py
    CONFLICT (add/add): Merge conflict in docs/conf.py
    Auto-merging docs/_static/theme_overrides.css
    CONFLICT (add/add): Merge conflict in docs/_static/theme_overrides.css
    Auto-merging README.rst
    CONFLICT (add/add): Merge conflict in README.rst
    Auto-merging Pipfile
    CONFLICT (add/add): Merge conflict in Pipfile
    Auto-merging CONTRIBUTING.rst
    CONFLICT (add/add): Merge conflict in CONTRIBUTING.rst
    Auto-merging CHANGELOG.rst
    CONFLICT (add/add): Merge conflict in CHANGELOG.rst
    Auto-merging .vscode/settings.json
    CONFLICT (add/add): Merge conflict in .vscode/settings.json
    Auto-merging .vscode/launch.json
    CONFLICT (add/add): Merge conflict in .vscode/launch.json
    Auto-merging .github/workflows/docs.yml
    CONFLICT (add/add): Merge conflict in .github/workflows/docs.yml
    Auto-merging .github/workflows/code.yml
    CONFLICT (add/add): Merge conflict in .github/workflows/code.yml
    Auto-merging .gitattributes
    CONFLICT (add/add): Merge conflict in .gitattributes
    Automatic merge failed; fix conflicts and then commit the result.

    Please fix the conflicts above, then you can run:
        git branch -d skeleton-merge-branch
    Instructions on how to develop this module are in CONTRIBUTING.rst

First of the boilerplate files were removed::

    $ git rm src/scanspec/hello.py docs/images/dls-logo.svg docs/images/dls-favicon.ico docs/how-to/accomplish-a-task.rst docs/explanations/why-is-something-so.rst -f
    rm 'docs/explanations/why-is-something-so.rst'
    rm 'docs/how-to/accomplish-a-task.rst'
    rm 'docs/images/dls-favicon.ico'
    rm 'docs/images/dls-logo.svg'
    rm 'src/scanspec/hello.py'

Then the merge conflicts were fixed, and the dependencies updated::

    $ pip install -e .[dev]

The tests and docs were then run and checked::

    $ tox -p

Finally the results were committed, pushed, merged to main::

    $ git commit
    $ git push github adopt-skeleton

.. image:: ../images/git_merge.png
