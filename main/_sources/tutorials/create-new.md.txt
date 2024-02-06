# Create a new repo from the template

Once you have followed the [](./installation) tutorial, you can use `copier` to make a new project from the template:

```
$ mkdir /path/to/my-project
$ copier copy gh:DiamondLightSource/python-copier-template /path/to/my-project
```

This will:

- Ask some questions about the project to be created
- Expand the template with the answers give
- Record the answers in the project so they can be used in later updates

## Uploading to GitHub

You can now [create a new blank project on GitHub](https://github.com/new). Choose the same GitHub owner and repo name that you answered in the questions earlier. GitHub will now give you the commands needed to upload your repo from GitHub

## Setings

You can now go to the `Settings` and set:

- The project description to match the answer you gave
- Enable Pages if you chose to use sphinx for your documentation

## Getting started with your new repo

You can now [](../how-to/dev-install), and then follow some of the other [](../how-to).
