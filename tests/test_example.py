import shlex
import subprocess
from pathlib import Path

from copier import run_copy

TOP = Path(__file__).absolute().parent.parent


def test_template(tmp_path: Path):
    project = tmp_path / "project"
    venv = tmp_path / "venv"
    answers = {
        "author_email": "tom.cobb@diamond.ac.uk",
        "author_name": "Tom Cobb",
        "component_owner": "group:default/sscc",
        "description": "An expanded python-copier-template with all the options",
        "distribution_name": "dls-python-copier-template-example",
        "docker": True,
        "docs_type": "sphinx",
        "git_platform": "github.com",
        "github_org": "DiamondLightSource",
        "package_name": "python_copier_template_example",
        "repo_name": "python-copier-template-example",
    }
    run_copy(
        src_path=str(TOP),
        dst_path=project,
        data=answers,
        vcs_ref="HEAD",
        unsafe=True,
    )

    def run(cmd: str):
        sp = subprocess.run(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=str(project),
        )
        assert sp.returncode == 0, sp.stdout.decode()

    run(f"python -m venv {venv}")
    run(f"{venv}/bin/python -m pip install -e .[dev]")
    run(f"{venv}/bin/tox -p")


# TODO: check that copier update python-copier-template-example matches generated
