# Install template pre-requisites

This tutorial will take you through installing copier, the templating engine that will allow you
to create new projects from the template, update existing projects in line with it, and keep projects in sync with changes to it.

## Check your version of python

You will need python 3.8 or later. You can check your version of python by
typing into a terminal:

```
$ python3 --version
```

:::{note}
At Diamond you can use `module load python` to get a more recent version of python on your path
:::

## Create a virtual environment

It is recommended that you install into a “virtual environment” so this
installation will not interfere with any existing Python software:

```
$ python3 -m venv /path/to/venv
$ source /path/to/venv/bin/activate
```

:::{note}
You may wish to deactivate any existing virual environments before sourcing the new
environment. Deactivation can be performed by executing:

- `conda deactivate` for conda
- `deactivate` for venv or virtualenv
- `exit` for pipenv
:::

## Installing copier

You can now use `pip` to install copier so you can make your project from the template:

```
$ python3 -m pip install copier
```

## Conclusion

You now have the pre-requisites to allow you to [](./create-new) and [](./adopt-existing).
