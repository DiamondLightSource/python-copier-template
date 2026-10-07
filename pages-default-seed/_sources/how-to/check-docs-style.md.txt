# Check docs for style

Ruff has the ability to check that you have:

- Documented all public modules, classes, methods and functions
- Written your docstrings according to a particular style
- Not missed parameters from method and function docstrings

This is not turned on by default, as it is not able to [distinguish between a missing docstring, and one that is inherited from a parent class](https://github.com/astral-sh/ruff/issues/9149)

## Enabling docstring checking

There are a number of competing docstring styles, ruff supports numpy, google and pep257. If you would like to check for the google docstring style, you can configure in ``pyproject.toml`` by:

- Turning on the checker

```toml
[tool.ruff.lint]
extend-select = [
    # ...
    "D",   # pydocstyle - https://docs.astral.sh/ruff/rules/#pydocstyle-d
    # ...
]
```

- Selecting a convention

```toml
[tool.ruff.lint.pydocstyle]
convention = "google"
```

- Ignoring docstring checking in tests

```toml
[tool.ruff.lint.per-file-ignores]
"tests/**/*" = [
    # ...
    "D",      # Don't check docstrings in tests
    # ...
]
```
