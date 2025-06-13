# Run linting using pre-commit

Code linting is handled by [ruff](https://docs.astral.sh/ruff) run under [pre-commit](https://pre-commit.com/).

## Running pre-commit

You can run the above checks on all files with this command:

```
$ tox -e pre-commit
```

Or you can install a pre-commit hook that will run each time you do a `git commit` on just the files that have changed:

```
$ pre-commit install
```

It is also possible to [automatically enable pre-commit on cloned repositories](https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories). This will result in pre-commits being enabled on every repo your user clones from now on.

## Fixing issues

The typical workflow is:

- Make a code change
- `git add` it
- Try to commit
- Pre-commit will run, and ruff will try and fix any issues it finds
- If anything changes it will be left in your working copy
- Review and commit the results

## VSCode support

The `.vscode/settings.json` will run ruff formatters on save, but will not try to auto-fix as that does things like removing unused imports which is too intrusive while editing.
