import functools
import shlex
import subprocess
from pathlib import Path

import pytest
import yaml
from copier import run_copy
from prompt_toolkit.validation import ValidationError

TOP = Path(__file__).absolute().parent.parent


def copy_project(project_path: Path, **kwargs):
    with open(TOP / "example-answers.yml") as f:
        answers = yaml.safe_load(f)
    answers.update(kwargs)
    run_copy(
        src_path=str(TOP),
        dst_path=project_path,
        data=answers,
        vcs_ref="HEAD",
        unsafe=True,
    )


def run_pipe(cmd: str, cwd=None):
    sp = subprocess.run(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
    )
    output = sp.stdout.decode()
    assert sp.returncode == 0, output
    return output


def make_venv(project_path: Path) -> callable:
    venv_path = project_path / "venv"
    run_pipe(f"python -m venv {venv_path}")
    run = functools.partial(run_pipe, cwd=str(project_path))
    run("./venv/bin/pip install -e .[dev]")
    return run


def test_template(tmp_path: Path):
    copy_project(tmp_path)
    run = make_venv(tmp_path)
    run("./venv/bin/tox -p")
    run("./venv/bin/pip install build twine")
    run("./venv/bin/python -m build")
    run("./venv/bin/twine check --strict dist/*")


def test_template_no_docs(tmp_path: Path):
    copy_project(tmp_path, docs_type="README")
    run = make_venv(tmp_path)
    run("./venv/bin/tox -p")


def test_bad_repo_name(tmp_path: Path):
    with pytest.raises(ValidationError, match="bad:thing is not a valid repo name"):
        copy_project(tmp_path, repo_name="bad:thing")


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
    run(f"copier update --trust --vcs-ref=HEAD --data-file {TOP}/example-answers.yml")
    output = run(
        # Git directory expected to be different
        "diff -ur --exclude=.git "
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
    with open(TOP / ".gitignore") as top_gi, open(
        TOP / "template" / ".gitignore"
    ) as template_gi:
        assert top_gi.read() == template_gi.read()
