Creating a new repo from the skeleton
=====================================

Once you have followed the ``installation`` tutorial, you can use the
commandline tool to make a new repo that inherits the skeleton::

    python3-pip-skeleton new /path/to/be/created --org my_github_user_or_org --skeleton-org some_institution

This will:

- Take the repo name from the last element of the path
- Take the package name from the repo name unless overridden by ``--package``
- Create a new repo at the requested path, forked from the skeleton repo
- Create a single commit that modifies the skeleton with the repo and package name
- Use the version of the skeleton in ``some_institution``'s organization (default ``DiamondLightSource``)


Getting started with your new repo
----------------------------------

Your new repo has a workflow based on pip. The first thing to do is to use
pip to install packages in a virtual environment::

    python -m venv .venv
    source .venv/bin/activate
    pip install -e .[dev]

.. note::

    You may wish to deactivate any existing virual environments before sourcing the new
    environment. Deactivation can be performed by executing:

    - :code:`conda deactivate` for conda
    - :code:`deactivate` for venv or virtualenv
    - :code:`exit` for pipenv

You can then run any entry points declared in setup.cfg e.g.::

    python3-pip-skeleton --version

will run the python interpreter with access to all the packages you need to
develop your repo.

PyPI Token
----------

The Github Actions Continuous Integration will publish your package to PyPI.
To do so you need a PyPI account and and a PyPI Token configured in your 
project or github Organization. 

see `../how-to/pypi`

Setting up pre-commit
---------------------

To install the pre-commit see `../../developer/how-to/lint`.

Running the tests
-----------------

There are also some extra convenience scripts provided via tox::

    tox -p

Will run in parallel all of the checks that CI performs.

It will run ``pytest`` to find all the unit tests and run them. The first time you
run this, there will be some failing tests::

    ============================================================================ short test summary info ============================================================================
    FAILED tests/test_boilerplate_removed.py::test_module_description - AssertionError: Please change description in ./setup.cfg to be a one line description of your module
    FAILED tests/test_boilerplate_removed.py::test_changed_README_intro - AssertionError: Please change ./README.rst to include an intro on what your module does
    FAILED tests/test_boilerplate_removed.py::test_changed_README_body - AssertionError: Please change ./README.rst to include some features and why people should use it
    FAILED tests/test_boilerplate_removed.py::test_removed_CHANGELOG_note - AssertionError: Please change ./CHANGELOG.rst To remove the note at the top
    FAILED tests/test_boilerplate_removed.py::test_changed_CHANGELOG - AssertionError: Please change ./CHANGELOG.rst To summarize changes to your module as you make them
    ========================================================================== 8 failed, 5 passed in 0.28s ==========================================================================

When you change the template text mentioned in the error, these tests will pass.
If you intend to fix the test later, you can mark the tests as "expected to
fail" by adding a decorator to the relevant function. For example:

.. code-block:: python

    @pytest.mark.xfail(reason="docs not written yet")
    def test_explanations_written():
        ...

Building the docs
-----------------

There is also a convenience script for building the docs::

    tox -e docs

You can then view the docs output with a web browse::

    firefox build/html/index.html

Pushing to GitHub
-----------------

To push the resulting repo to GitHub, first create an empty repo from the GitHub
website, then run the following::

    git remote add $(cat .gitremotes)
    git push -u github main

This will then run the continuous integration (CI) jobs, which run the tests and
build the docs using the commands above.

Once the docs build has passed, you can use the Settings on the repo page on the
GitHub website to enable github pages publishing of the ``gh-pages`` branch.

What next?
----------

Now you can make the repo your own, add code, write docs, delete what you don't
like, then push a tag and CI will make a release and push it to PyPI. Look at
the `How-To <../index>` for articles on these and other topics.
