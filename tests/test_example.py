import functools
import shlex
import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml
from copier import run_copy

TOP = Path(__file__).absolute().parent.parent


def copy_project(project_path: Path, **kwargs):
    with open(TOP / "example-answers.yml") as f:
        answers = yaml.safe_load(f)
    answers.update(kwargs)
    run_pipe(f"git init {project_path}")
    run_copy(
        src_path=str(TOP),
        dst_path=project_path,
        data=answers,
        vcs_ref="HEAD",
    )
    run_pipe("git add .", cwd=str(project_path))


def run_pipe(cmd: str, cwd=None) -> str:
    sp = subprocess.run(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
    )
    output = sp.stdout.decode()
    assert sp.returncode == 0, output
    return output


def make_venv(project_path: Path) -> Callable[[str], str]:
    venv_path = project_path / ".venv"
    run = functools.partial(run_pipe, cwd=str(project_path))
    run("uv sync")  # Create a lockfile and install packages

    for exe_path in [
        venv_path / "bin" / "tox",
        venv_path / "bin" / "python",
    ]:
        assert exe_path.exists(), f"UV created a venv but did not install {exe_path}"

    return run


def test_template_defaults(tmp_path: Path):
    copy_project(tmp_path)
    run = make_venv(tmp_path)
    container_doc = tmp_path / "docs" / "how-to" / "run-container.md"
    pyproject_toml = tmp_path / "pyproject.toml"
    assert container_doc.exists()
    catalog_info = tmp_path / "catalog-info.yaml"
    assert catalog_info.exists()
    assert 'typeCheckingMode = "strict"' in pyproject_toml.read_text()
    run(".venv/bin/tox -p")
    if not run_pipe("git tag --points-at HEAD"):
        # Only run linkcheck if not on a tag, as the CI might not have pushed
        # the docs for this tag yet, so we will fail
        run(".venv/bin/tox -e docs -- -b linkcheck")
    run("uvx --from build pyproject-build")
    run("uvx twine check --strict dist/*")


def test_template_with_extra_code_and_api_docs(tmp_path: Path):
    copy_project(tmp_path)
    run = make_venv(tmp_path)
    # add some code
    init = tmp_path / "src" / "python_copier_template_example" / "__init__.py"
    init.write_text(
        init.read_text().replace(
            """
from ._version import __version__

__all__ = [""",
            '''
from python_copier_template_example import extra_pkg

from ._version import __version__


class TopCls:
    """A top level class."""


__all__ = ["TopCls", "extra_pkg", ''',
        )
    )
    extra_pkg = tmp_path / "src" / "python_copier_template_example" / "extra_pkg"
    extra_pkg.mkdir()
    (extra_pkg / "__init__.py").write_text('"""Extra Package."""\n')
    code = '''"""A module."""


class Thing:
    """A docstring."""
'''
    (extra_pkg / "extra_module.py").write_text(code)
    # Add to make sure pre-commit doesn't moan
    run("git add .")
    # Build
    run(".venv/bin/tox -p")
    # Check it generates the right output
    api_dir = tmp_path / "build" / "html" / "_api"
    top_html = api_dir / "python_copier_template_example.html"
    assert "extra_pkg" in top_html.read_text()
    assert "Extra Package." in top_html.read_text()
    assert "TopCls" in top_html.read_text()
    assert "A top level class." in top_html.read_text()
    assert "__version__" in top_html.read_text()
    assert "setuptools_scm" in top_html.read_text()
    package_html = api_dir / "python_copier_template_example.extra_pkg.html"
    assert "extra_module" in package_html.read_text()
    assert "A module." in package_html.read_text()
    module_html = api_dir / "python_copier_template_example.extra_pkg.extra_module.html"
    assert "Thing" in module_html.read_text()
    assert "A docstring." in module_html.read_text()


def test_template_mypy(tmp_path: Path):
    copy_project(tmp_path, type_checker="mypy")
    run = make_venv(tmp_path)
    run(".venv/bin/tox -p")


def test_template_no_docs(tmp_path: Path):
    copy_project(tmp_path, docs_type="README")
    run = make_venv(tmp_path)
    run(".venv/bin/tox -p")


def test_template_in_different_org_has_no_catalog(tmp_path: Path):
    copy_project(tmp_path, github_org="bluesky")
    catalog_info = tmp_path / "catalog-info.yaml"
    assert not catalog_info.exists()


def test_template_no_docker_has_no_docs_and_works(tmp_path: Path):
    copy_project(tmp_path, docker=False)
    container_doc = tmp_path / "docs" / "how-to" / "run-container.md"
    assert not container_doc.exists()
    run = make_venv(tmp_path)
    run(".venv/bin/tox -p")


def test_bad_repo_name(tmp_path: Path):
    with pytest.raises(ValueError, match="bad:thing is not a valid repo name"):
        copy_project(tmp_path, repo_name="bad:thing")


def test_dots_in_package_name(tmp_path: Path):
    copy_project(tmp_path, repo_name="dots.in.name")


def test_example_repo_updates(tmp_path: Path):
    generated_path = tmp_path / "generated"
    example_url = (
        "https://github.com/DiamondLightSource/python-copier-template-example.git"
    )
    example_path = tmp_path / "example"
    copy_project(generated_path)
    run_pipe(f"git clone {example_url} {example_path}")
    with open(example_path / ".copier-answers.yml") as f:
        d = yaml.safe_load(f)
    d["_src_path"] = str(TOP)
    with open(example_path / ".copier-answers.yml", "w") as f:
        yaml.dump(d, f)
    run = functools.partial(run_pipe, cwd=str(example_path))
    run("git config user.email 'you@example.com'")
    run("git config user.name 'Your Name'")
    run("git commit -am 'Update src'")
    run(f"copier update --vcs-ref=HEAD --data-file {TOP}/example-answers.yml")
    output = run(
        # Git directory expected to be different
        "diff -ur --exclude=.git "
        # uv lock expected to be different
        "--exclude=uv.lock "
        # The commit hash is different for some reason
        "--ignore-matching-lines='^_commit: ' "
        # If we tag an existing commit that has been pushed to main, then the copier
        # update on the old commit id will be generated with the new tag name, which
        # means the link will not be updated. As this only affects the example repo
        # which is the only thing that points to main then we ignore it
        "--ignore-matching-lines='^For more information on common tasks like setting' "
        f"{generated_path} {example_path}"
    )
    assert not output, output


def test_gitignore_same():
    with (
        open(TOP / ".gitignore") as top_gi,
        open(TOP / "template" / ".gitignore") as template_gi,
    ):
        assert top_gi.read() == template_gi.read()


def test_private_member_access(tmp_path: Path):
    code = """
class MyClass:
    def __init__(self):
        self.foo: int = 1
        self._bar: int = 2

obj = MyClass()
print(obj.foo)
print(obj._bar)
"""

    copy_project(tmp_path)
    run = make_venv(tmp_path)

    # Private member access should be allowed in tests
    test_file = tmp_path / "tests" / "test_private_access.py"
    with test_file.open("w") as stream:
        stream.write(code)
    run("ruff check")

    # Private member access should not be allowed in src
    src_file = tmp_path / "src" / "python_copier_template_example" / "private_access.py"
    with src_file.open("w") as stream:
        stream.write(code)
    with pytest.raises(AssertionError, match="SLF001 Private member accessed: `_bar`"):
        run("ruff check")


def test_pep8_naming(tmp_path: Path):
    code = """
myVariable = "foo"
"""

    copy_project(tmp_path)
    run = make_venv(tmp_path)

    src_file = tmp_path / "src" / "python_copier_template_example" / "bad_example.py"
    with src_file.open("w") as stream:
        stream.write(code)
    with pytest.raises(AssertionError, match=r"N816 .*"):
        run("ruff check")


def test_pyright_works_in_standard_typing_mode(tmp_path: Path):
    copy_project(tmp_path, type_checker="pyright", strict_typing=False)
    pyproject_toml = tmp_path / "pyproject.toml"

    # Check standard mode is configured
    assert 'typeCheckingMode = "standard"' in pyproject_toml.read_text()

    # Ensure pyright is still happy
    run = make_venv(tmp_path)
    run(f".venv/bin/pyright {tmp_path}")


def test_pyright_works_with_external_deps(tmp_path: Path):
    copy_project(tmp_path)
    # Add an external dependency
    pyproject_toml = tmp_path / "pyproject.toml"
    text = pyproject_toml.read_text().replace(
        "dependencies = []", 'dependencies = ["numpy"]'
    )
    pyproject_toml.write_text(text)
    # And some code that uses it
    src_file = tmp_path / "src" / "python_copier_template_example" / "example.py"
    src_file.write_text("""
import numpy as np

def is_big(arr: np.ndarray) -> bool:
    return arr.size > 0
""")
    # Ensure pyright is still happy
    run = make_venv(tmp_path)
    run(".venv/bin/tox -e type-checking")


def test_ignores_mypy_strict_mode(tmp_path: Path):
    copy_project(tmp_path, type_checker="mypy", strict_typing=True)
    pyproject_toml = tmp_path / "pyproject.toml"

    # Check strict mode is not configured
    assert "typeCheckingMode =" not in pyproject_toml.read_text()


def test_works_with_pydocstyle(tmp_path: Path):
    copy_project(tmp_path)
    pyproject_toml = tmp_path / "pyproject.toml"
    text = (
        pyproject_toml.read_text()
        .replace('"C4",', '"C4", "D",')  # Enable all pydocstyle
        .replace(
            '"tests/**/*" = ["SLF001"]',
            # But exclude on tests and allow o put their own docstring on __init__.py
            '"tests/**/*" = ["SLF001", "D"]\n"__init__.py" = ["D104"]',
        )
    )
    pyproject_toml.write_text(text)

    # Ensure ruff is still happy
    run = make_venv(tmp_path)
    run("ruff check")


def test_catalog_info(tmp_path: Path):
    copy_project(tmp_path)
    catalog_info_path = tmp_path / "catalog-info.yaml"
    with catalog_info_path.open("r") as stream:
        catalog_info = yaml.safe_load(stream)
    assert catalog_info == {
        "apiVersion": "backstage.io/v1alpha1",
        "kind": "Component",
        "metadata": {
            "name": "dls-python-copier-template-example",
            "title": "python-copier-template-example",
            "description": "An expanded "
            "https://github.com/DiamondLightSource/python-copier-template "
            "to illustrate how it looks with all the options enabled.",
        },
        "spec": {
            "type": "service",
            "lifecycle": "experimental",
            "owner": "group:default/daq",
        },
    }
