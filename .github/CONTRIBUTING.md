# Contribute to the template
Contributions and issues are most welcome! All issues and pull requests are handled through [GitHub](https://github.com/DiamondLightSource/python-copier-template/issues). Also, please check for any existing issues before filing a new one. If you have a great idea but it involves big changes, please file a ticket before making a pull request! We want to make sure you don't spend your time coding something that might not fit the scope of the project.

## Issue or Discussion?

Github also offers [discussions](https://github.com/DiamondLightSource/python-copier-template/discussions) as a place to ask questions and share ideas. If your issue is open ended and it is not obvious when it can be "closed", please raise it as a discussion instead.

## Getting changes into the template

This template is a place to pull together agreed best practices from various sources. As such, it is difficult to demonstrate a change without seeing it in action in another repo. Please link to a repo that has the desired behaviour when proposing changes to the template.

## Checking your changes before making a PR

The template has some tests that generating from scratch and updating the [example](https://github.com/DiamondLightSource/python-copier-template-example) produce the same result, but it is difficult to that things like CI and docs are still generated correctly. You can ease this process by:

- Making your changes on a branch of <https://github.com/DiamondLightSource/python-copier-template>
- Running `copier update --vcs-ref=<branch_name>` in the repo where you would like to demonstrate the behaviour
- Linking to that demonstration repo in the PR

## Developer Information

It is recommended that developers use a [vscode devcontainer](https://code.visualstudio.com/docs/devcontainers/containers). This repository contains configuration to set up a containerized development environment that suits its own needs.

For more information on common tasks like setting up a developer environment, running the tests, and setting a pre-commit hook, see the [How-to guides](https://diamondlightsource.github.io/python-copier-template/main/how-to.html)
