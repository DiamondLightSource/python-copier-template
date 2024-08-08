# Enable Pyright's Strict Mode

For projects using pyright you can enable strict mode for stricter than normal type checking. See [the docs](https://github.com/microsoft/pyright/blob/main/docs/configuration.md) for a full breakdown. The primary benefits are increased confidence in code that has been more thoroughly analyzed and a shorter development time thanks to fast feedback from the type checker.

## Configuration

Add the `strict` line to `pyproject.toml` as follows:

```toml
[tool.pyright]
strict = ["src", "tests"]
reportMissingImports = false # Ignore missing stubs in imported modules
```

## Third Party Libraries

Strict mode does not usually work well with libraries that do not have [type stubs](https://github.com/microsoft/pyright/blob/main/docs/type-stubs.md), you will likely need a `# type: ignore` on any line that directly uses the library code. This may limit the usefulness of pyright but it can still be worth doing to ensure your own code is internally consistent.
