Why Use a Skeleton Structure?
=============================

Many projects start from some kind of template. These define some basic
structure, customized with project specific variables, that developers can add
their code into. One example of this is cookiecutter_.

.. _cookiecutter: https://cookiecutter.readthedocs.io

The problem with this approach is that it is difficult to apply changes to the
template into projects that have been cut from it. Individual changes have to be
copy/pasted into the code, leading to partially applied fixes and missed
updates.

This module takes a different approach, as explained in `jaraco's blog post`_.
It is a repo that can be forked, and updates merged to the skeleton can be
merged into projects tracking it with a ``git pull`` operation. No more
copy/pasting.

.. _jaraco's blog post: https://blog.jaraco.com/a-project-skeleton-for-python-projects/

Why do you need the commandline tool?
-------------------------------------

The reason for the commandline tool is because this skeleton module has more
code and docs content than `jaraco/skeleton`_. There are numerous references to
the repo and package name, so the commandline tool applies a single commit on
top of the repo that customizes it to the particular project. Once the initial
creation/adoption has occurred however, a simple ``git pull`` is sufficient to
keep it updated.

.. _jaraco/skeleton: https://github.com/jaraco/skeleton

What happens if the merges become too difficult?
------------------------------------------------

If projects diverge too much, then merging in changes will become increasingly
difficult. This is probably a sign that the approach the project has taken is
too different from the skeleton structure for it to be of much benefit. At this
point, the merge can be abandoned, the section from ``CONTRIBUTING.rst``
deleted, and the project need not pull from the skeleton repo any more.
