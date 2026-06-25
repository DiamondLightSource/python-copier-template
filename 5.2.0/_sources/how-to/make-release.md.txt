# Make a release

To make a new release, please follow this checklist:

- Ensure that you have previously followed [](./pypi)
- Choose a new PEP440 compliant release number (see <https://peps.python.org/pep-0440/>)
- Go to the GitHub [release] page
- Choose `Draft New Release`
- Click `Choose Tag` and supply the new tag you chose (click create new tag)
- Click `Generate release notes`, review and edit these notes
- Choose a title and click `Publish Release`

Note that tagging and pushing to the main branch has the same effect except that
you will not get the option to edit the release notes.

A new release will be made and the wheel and sdist uploaded to PyPI.

[release]: https://github.com/DiamondLightSource/python-copier-template/releases
