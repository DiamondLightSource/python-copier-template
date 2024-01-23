10. Include vscode settings
===========================

Date: 2023-01-18

Status
------

Accepted

Context
-------

For vscode users a couple of settings are required for neat integration with
the IDE.

Decision
--------

Include a .vscode folder in the repo with some json files that enable:

- recommended extension for best experience
- launcher to make debugging of python code override the coverage settings
- settings to make code verification match the tools in CI
- a task to launch the tox tests from the IDE

Consequences
------------

Users of vscode should find that their development environment just works.
Users of other editors will be unaffected.