
# How to check code coverage

Code coverage is reported to the command line and to a `cov.xml` file by the command `tox -e tests`. The file is uploaded to the Codecov service in CI.

## Adding a Codecov Token

If the repo is not hosted in DiamondLightSource, then you need to visit `https://app.codecov.io/account/gh/<org_name>/org-upload-token` to generate a token for your org, and store it as a secret named `CODECOV_TOKEN` in `https://github.com/organizations/<org_name>/settings/secrets/actions`
