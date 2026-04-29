#!/bin/bash
set -euo pipefail

# Install Python dependencies and pre-commit hooks
uv venv --clear
uv sync
pre-commit install --install-hooks

# Init only submodules that aren't checked out yet — first-clone
# protection without touching already-initialized submodules (which
# would yank in-progress branch work to detached HEAD on rebuild).
if [ -f .gitmodules ]; then
    missing=$(git submodule status | awk '/^-/ {print $2}')
    [ -n "$missing" ] && git submodule update --init $missing
fi
