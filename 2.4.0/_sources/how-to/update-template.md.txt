# How to update to the latest template structure

To track changes to the upstream template, run

```
copier update --trust
```

This will fetch the latest tagged release of the template, and apply any changes to your working copy. It will prompt for answers again, giving your previous answers as the defaults.

It will stage all the changes for commit, but there may be merge conflicts that need fixing first, find them with

```
git diff --check
```

Once they are all fixed, make a commit.
