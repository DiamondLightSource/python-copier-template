import shutil
from pathlib import Path

import treecomp
import yaml
from copier import run_copy

TOP = Path(__file__).absolute().parent.parent
INPUT = TOP / "example"
OUTPUT = TOP / "build" / "example"


def test_template():
    shutil.rmtree(OUTPUT, ignore_errors=True)
    answers = yaml.safe_load((INPUT / ".copier-answers.yml").read_text())
    run_copy(
        src_path=str(TOP),
        dst_path=OUTPUT,
        data=answers,
        vcs_ref="HEAD",
        unsafe=True,
    )
    #
    comparison = treecomp.diff_file_trees(INPUT, OUTPUT, ignore=[".copier-answers.yml"])
    if comparison.diffs:
        raise AssertionError(str(comparison))
