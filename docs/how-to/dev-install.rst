Setup Developer Environment
===========================

These instructions will take you through the minimal steps required to get a dev
environment setup, so you can run the tests locally.

Clone the repository
--------------------

First clone the repository locally using `Git
<https://git-scm.com/downloads>`_::

    $ git clone git://github.com/DiamondLightSource/python3-pip-skeleton-cli.git

Install dependencies
--------------------

You can choose to either develop on the host machine using a `venv` (which
requires python 3.8 or later) or to run in a container under `VSCode
<https://code.visualstudio.com/>`_

.. tab-set::

    .. tab-item:: Local virtualenv

        .. code::

            $ cd python3-pip-skeleton-cli
            $ python3 -m venv venv
            $ source venv/bin/activate
            $ pip install -c requirements/constraints.txt -e .[dev]

    .. tab-item:: VSCode devcontainer

        .. code::

            $ code python3-pip-skeleton-cli
            # Click on 'Reopen in Container' when prompted
            # Open a new terminal

Build and test
--------------

Now you have a development environment you can run the tests in a terminal::

    $ tox -p

This will run in parallel the following checks:

- `./build-docs`
- `./run-tests`
- `./static-analysis`
- `./lint`
