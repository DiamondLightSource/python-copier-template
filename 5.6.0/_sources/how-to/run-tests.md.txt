(using-pytest)=

# Run the tests using pytest

Testing is done with [pytest]. It will find functions in the project that [look like tests][look like tests], and run them to check for errors. You can run it with:

```
$ pytest
```

When you have some fully working tests then you can run it with coverage:

```
$ tox -e tests
```

It will also report coverage to the commandline and to `cov.xml`.

[look like tests]: https://docs.pytest.org/explanation/goodpractices.html#test-discovery
[pytest]: https://pytest.org/
