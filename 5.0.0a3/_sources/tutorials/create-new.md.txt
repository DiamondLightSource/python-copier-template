# Create a new repo from the template

Once you have followed the [](./installation) tutorial, you can use `copier` to make a new project from the template:

```
$ git init --initial-branch=main /path/to/my-project
$ copier copy https://github.com/DiamondLightSource/python-copier-template.git $_
```

This will:

- Ask some questions about the project to be created
- Expand the template with the answers give
- Record the answers in the project so they can be used in later updates
- Create a git repository if the directory is not already one

## Committing the results

You can now check what the template has created, tweak the results if desired, and commit the results:
```
$ cd /path/to/my-project
$ git add .
$ git commit -m "Expand from python-copier-template x.x.x"
```

## Uploading to GitHub

If the project is to be under the DiamondLightSource organisation, request a new repository in the [#github-requests Slack channel](https://diamondlightsource.slack.com/archives/C06A18ZPP44) with the given repo name, description and who to add as an owner in addition to yourself. This will be replaced by [a template in the developer-portal in future.](https://github.com/DiamondLightSource/python-copier-template/issues/274)

Else, you can now [create a new blank project on GitHub](https://github.com/new). Choose the same GitHub owner and repo name that you answered in the questions earlier. GitHub will now give you the commands needed to upload your repo from GitHub.

## Settings

You can now go to the cogwheel on the main page next to the "About" header, and set the project description to match the answer you gave.

Then go to the `Settings` tab and set:

- Enable Pages if you chose to use sphinx for your documentation

## Getting started with your new repo

You can now [](../how-to/dev-install), and then follow some of the other [](../how-to).
