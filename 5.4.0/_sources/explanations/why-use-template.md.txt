# Why Use a Copier Template?

Many projects start from some kind of template. These define some basic structure, customized with project specific variables, that developers can add their code into. One example of this is [cookiecutter](https://cookiecutter.readthedocs.io).

The problem with this approach is that it is difficult to apply changes to the template into projects that have been cut from it. Individual changes have to be copy/pasted into the code, leading to partially applied fixes and missed updates.

A previous attempt, [python3-pip-skeleton](https://github.com/DiamondLightSource/python3-pip-skeleton), took a different approach, being a repo that can be forked and updates merged into projects tracking it. This was initially encouraging, but led to downstream confusion on who had actually contributed to the repository, as well as messy merges when text that contained the project name (like documentation) was changed upstream.

This template now makes use of [copier](https://copier.readthedocs.io/) which gives the best of both worlds, a templating engine to expand the template, then an update mechanism to apply diffs of the updated template to the project.
