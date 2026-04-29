#!/bin/bash
set -euo pipefail

# Install Python dependencies and pre-commit hooks
uv venv --clear
uv sync
pre-commit install --install-hooks

# Initialise git submodules if any are declared
[ -f .gitmodules ] && git submodule update --init || true
