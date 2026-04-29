#!/bin/bash
set -euo pipefail

# Install Claude Code CLI
curl -fsSL https://claude.ai/install.sh | bash

# Install Python dependencies and pre-commit hooks
uv venv --clear
uv sync
pre-commit install --install-hooks

# Initialise git submodules if any are declared
[ -f .gitmodules ] && git submodule update --init || true
