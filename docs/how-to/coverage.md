
# How to check code coverage

Code coverage is reported to the command line and to a `cov.xml` file by the command `tox -e tests`. The file is uploaded to the Codecov service in CI.

(installing-codecov-github-app)=
## Installing Codecov GitHub app

If your repo is hosted in the DiamondLightSource org, then the codecov GitHub app is already installed and a global token stored so you don't need to do anything.

If your repo is in an org where the codecov GitHub app is not installed, then follow these steps to install it on the org:

- Visit https://github.com/apps/codecov
- Click `Configure`
- Select the org your repo is hosted in
- Select `All repositories` and click `Install`

![Install Codecov](../images/gh-install-codecov.png)

Now you need to visit `https://app.codecov.io/account/gh/<org_name>/org-upload-token` to generate a token for your org, and store it as a secret named `CODECOV_TOKEN` in `https://github.com/organizations/<org_name>/settings/secrets/actions`

Next time you create a pull request or merge to main, the code coverage will be uploaded, and the badge on the repository updated.
