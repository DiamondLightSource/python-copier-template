# Use Pyright's Strict Mode

For projects using pyright you can enable strict mode for stricter than normal type checking. See [the docs](https://github.com/microsoft/pyright/blob/main/docs/configuration.md) for a full breakdown. 

## How to Enable

When creating a template, select `pyright` as the type checker and type `y` when prompted to enable strict mode.

## Who Should Use Strict Mode?

Strict mode enforces good practices such as type hints on function signatures, providing increased confidence in code that has been more thoroughly analyzed and a shorter development time thanks to fast feedback from the type checker. Starting a new project and continually keeping it passing provides a long-term benefit when it comes to maintanability and robustness. However, adopting strict mode on top of legacy projects is likely to lead to lots of errors to work through - probably thousands. Additionally it does not usually work well with libraries that do not have [type stubs](https://github.com/microsoft/pyright/blob/main/docs/type-stubs.md), you will likely need a `# type: ignore` on any line that directly uses the library code. This may limit the usefulness of pyright but it can still be worth doing to ensure your own code is internally consistent.

The recommended approach for brand new projects is to enable strict mode and stick with it for as long as is practical, moving away if it starts to cause more hindrance than help (e.g. because too many major dependencies do not support it).
