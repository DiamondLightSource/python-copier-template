# Setup the repository with recommended settings

When the repository has been created, it will require some settings to be changed for all the features of the python-copier-template to work. These are listed below.

## Discussions

The contributing guide for the template recommends that new users start a discussion for questions. You can enable this feature by navigating to your repository page and:

- Visiting `Settings` > `General`
- Scrolling down to `Features`
- Enabling it as shown

![Setup GitHub Features](../images/gh-features-setup.png)

## Branch protection

GitHub will prompt you that your `main` branch is not protected. It is recommended that a [branch protection rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule) is setup for `main` to require pull requests.

If the repository is in the `DiamondLightSource` org, then follow [the dev guide](https://dev-guide.diamond.ac.uk/version-control/how-tos/github-setup-prs/) to see the recommended settings.

## Code Coverage

To ensure that code coverage is correctly uploaded to codecov.io follow [](#installing-codecov-github-app)

## Renovate

To ensure that your dependencies are kept up to date follow [](./renovate.md)

## GitHub pages

If you configured the project to have sphinx docs then follow [](#building-docs-in-ci)

## PyPI uploading

If you configured the project to upload built wheels to PyPI then follow [](./pypi.md)
