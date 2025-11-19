# Create a new repo from the template

Once you have followed the [](./installation) tutorial, you can use `copier` to make a new project from the template:

```
git init --initial-branch=main /path/to/my-project
# $_ resolves to /path/to/my-project
uvx copier copy https://github.com/DiamondLightSource/python-copier-template.git $_
```

This will:

- Ask some questions about the project to be created
- Expand the template with the answers give
- Record the answers in the project so they can be used in later updates
- Create a git repository if the directory is not already one

## Committing the results

You can now check what the template has created, tweak the results if desired, [](../how-to/lock-requirements), and commit the results:
```shell
$ cd /path/to/my-project
$ uv sync
$ git add .
$ git commit -m "Expand from python-copier-template x.x.x"
```

## Uploading to GitHub

You can now [create a new blank project on GitHub](https://github.com/new). Choose the same GitHub owner, repo name and description that you answered in the questions earlier. GitHub will now give you the commands needed to upload your repo from GitHub.

```{note}
At present you cannot make a project directly in the DiamondLightSource organisation, it must be made as a personal repository then [transferred in](https://dev-guide.diamond.ac.uk/version-control/how-tos/github-transfer-repo/). When it has been transferred then you can `copier update --vcs-ref=:current:` to re-answer the questions with the new org
```

## Getting started with your new repo

You can now [](../how-to/setup-repo), [](../how-to/dev-install), and then follow some of the other [](../how-to).
