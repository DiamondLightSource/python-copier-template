# Run static analysis using pyright or mypy

Static type analysis is done with [pyright](https://microsoft.github.io/pyright) or [mypy](https://www.mypy-lang.org) dependent on the settings in `pyproject.toml`. It checks type definition in source files without running them, and highlights potential issues where types do not match. You can run it with:

```
$ tox -e type-checking
```
