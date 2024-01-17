This is a work-in-progress to evaluate the use of Copier templates in the Dev Portal.

To set up your PC at Diamond internally, you must install copier. One way to do this is via pipx.

.. code-block:: shell

    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    pipx install copier

To create a new project in your current directory, using this template and Copier from the command line, use:

.. code-block:: shell

    copier copy gh:DiamondLighSource/python_copier_template .
