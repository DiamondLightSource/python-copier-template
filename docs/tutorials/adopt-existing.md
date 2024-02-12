# Adopt the template into an existing repo

To adopt the latest version of this template to an existing project run:
```shell
copier copy gh:DiamondLightSource/python-copier-template /path/to/existing-project
```

This will:

- Ask some questions about the existing project
- Expand the template with the answers given
- Ask if you would like to overwrite conflicting files (always choose yes)
- Record the answers in the project so they can be used in later updates

## Conflicting Files
After choosing to overwrite the conflicting files, open your project in an editor and go through the changes and any merge conflicts ensure that you have the right files and contents.

:::{note}
Copier does not touch any already existing files that do not conflict with the ones in the template. Therefore, you may end up with files in your project you no longer need such as old github workflows. These would need to be manually deleted.  
:::
