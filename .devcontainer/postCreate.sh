#!/bin/bash
set -euo pipefail

# Refuse to continue without a git repo. setuptools-scm needs git
# tags to compute the package version, and pre-commit installs its
# hooks into .git/hooks — both fail with cryptic errors that VS Code
# then hides behind a generic "postCreateCommand failed" message.
# Better to stop here with a clear explanation.
if [ ! -d .git ]; then
    cat >&2 <<'EOF'

================================================================
ERROR: This directory is not a git repository.

setuptools-scm needs git history to compute the package version,
and pre-commit installs its hooks into .git/hooks. Neither will
work without a git repo.

To fix this, run on the host (outside the devcontainer):

    git init -b main && git add . && git commit -m 'Initial commit'

then rebuild the devcontainer.

================================================================

EOF
    exit 1
fi

# Install Python dependencies and pre-commit hooks. `uv venv --clear` wipes
# the venv that lives in /cache (a persistent named volume), so any bash
# hash entries pointing into the old venv (e.g. cached `pre-commit` path)
# are stale. `hash -r` after `uv sync` forces re-resolution against the
# freshly populated venv and against any new `uv` location after a base
# image bump.
uv venv --clear
hash -r
uv sync
pre-commit install --install-hooks

# Init only submodules that aren't checked out yet — first-clone
# protection without touching already-initialized submodules (which
# would yank in-progress branch work to detached HEAD on rebuild).
if [ -f .gitmodules ]; then
    missing=$(git submodule status | awk '/^-/ {print $2}')
    [ -n "$missing" ] && git submodule update --init $missing
fi


# Install Claude Code CLI
curl -fsSL https://claude.ai/install.sh | bash

