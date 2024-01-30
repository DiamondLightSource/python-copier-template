# Run static analysis using pyright

Static type analysis is done with [pyright](https://microsoft.github.io/pyright/). It checks type definition in source files without running them, and highlights potential issues where types do not match. You can run it with:

```
$ tox -e pyright
```
