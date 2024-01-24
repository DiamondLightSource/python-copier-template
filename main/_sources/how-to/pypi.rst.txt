Creating a PyPI Token
=====================

To publish your package on PyPI requires a PyPI account and for GitHub Actions
to have a PyPI token authorizing access to that account.

The simplest approach is to set up a PyPI token that is scoped to your PyPI account
and add it to the secrets for your GitHub Organization (or user). This means
that all new projects created in the Organization will automatically gain
permission to publish to PyPI.

Alternatively you can create a project scoped token for each project. This 
is more work but more secure as a bad actor that obtains the key can only 
affect a single project.

If you do not already have a PyPI account use this link: create_account_.

To learn how to create a token and store it in Github see: adding_a_token_.
You can ignore the other sections of the page regarding Github Actions because
these are already provided by skeleton. Note that skeleton uses ``PYPI_TOKEN``
as the secret name instead of ``PYPI_API_TOKEN`` described in the link.


.. _create_account: https://pypi.org/account/register/
.. _adding_a_token: https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/#saving-credentials-on-github
