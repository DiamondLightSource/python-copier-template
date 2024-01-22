How to update to the latest skeleton structure
==============================================

If you used the commandline tool to create your repo (or adopt the skeleton
structure in an existing repo) some time ago, there may be some changes to the
structure that you could pick up. You can optionally check what differences
these changes make to the files by doing::

    $ git fetch https://github.com/DiamondLightSource/python3-pip-skeleton main
    $ git diff ...FETCH_HEAD

To merge the changes in do::

    $ git pull https://github.com/DiamondLightSource/python3-pip-skeleton main
