"""Extension to update the context of Copier."""
import os
import subprocess
from pathlib import Path

from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    """Context updater."""

    update = False

    def hook(self, context):
        """Update the context before applying the template."""
        # Skip git initialization if the git repository is already initialized
        twd = context.get("_copier_conf", {}).get("dst_path")
        cwd = os.getcwd()

        try:
            if twd is not None and Path(twd).exists():
                os.chdir(twd)
            status = subprocess.run(["git", "status"], capture_output=True)
        finally:
            os.chdir(cwd)

        if status.returncode == 0:
            context["init_git"] = False
