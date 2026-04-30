---
name: copier-derived
description: This project was generated from python-copier-template. Use when editing devcontainer / Dockerfile / .github / pre-commit / justfile / .gitleaks / renovate config, anything under .claude/ (hooks, skills, commands, settings), CLAUDE.md, or README-CLAUDE.md, or when the user asks about updating from the template, resolving copier conflicts, or why a config looks the way it does.
---

# Copier-template-derived project

This project was generated from
[python-copier-template](https://github.com/diamondlightsource/python-copier-template).
The template is recorded in `.copier-answers.yml`:

```bash
grep _src_path .copier-answers.yml   # template source
grep _commit   .copier-answers.yml   # version applied
```

## Template-managed files

`copier update` overwrites these from the template. Local edits will
either merge cleanly (good) or produce `.rej` / inline conflicts.
**Prefer editing the upstream template** for any change that should
apply to all projects — otherwise the next update reverts it.

- `.devcontainer/**`
- `Dockerfile`
- `.github/workflows/*.yml`, `.github/CONTRIBUTING.md`,
  `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE/`
- `.pre-commit-config.yaml`, `.gitleaks.toml`, `renovate.json`
- `justfile`
- `pyproject.toml` — top-level metadata, build-system, ruff/pyright/mypy
  config, tox config (project deps and scripts are project-owned)
- `tests/conftest.py`, `tests/test_cli.py`
- `CLAUDE.md`, `README-CLAUDE.md`, `.claude/**`

## Project-owned files

Edit freely; never overwritten by `copier update`:

- `src/<package>/**`
- New tests under `tests/` (other than the seeded `test_cli.py`)
- `README.md` (rendered once with placeholders, then yours)
- `.copier-answers.yml` answers (only `_commit` / `_src_path` are bumped
  by `copier update`)

## When the user asks to change a template-managed file

1. Make the requested change in this project so it works now.
2. **Tell the user** the file is template-managed, and offer to also
   update the upstream template if they have it checked out (commonly
   at `/workspaces/python-copier-template`). Phrase as a choice — they
   may want a project-only patch.
3. If both edits are made, the project edit can be reverted on the
   next `copier update` once the template change reaches a release.

## Running `copier update`

The user runs this themselves (it touches many files); only run it
yourself if explicitly asked. Always pass `--trust`. After update,
resolve any conflicts (look for `<<<<<<<` markers and `.rej` files)
before committing.

## Verifying template changes without committing

When editing files in `/workspaces/python-copier-template/template/`,
render a throwaway project to confirm the change works for both
branches of every conditional (`add_claude=true` and `false`):

```bash
cd /tmp && rm -rf render-true render-false
git init render-true -b main >/dev/null
uvx copier copy /workspaces/python-copier-template /tmp/render-true \
    --data-file /workspaces/python-copier-template/example-answers.yml \
    --vcs-ref HEAD --defaults --trust
git init render-false -b main >/dev/null
uvx copier copy /workspaces/python-copier-template /tmp/render-false \
    --data-file /workspaces/python-copier-template/example-answers.yml \
    --data add_claude=false --vcs-ref HEAD --defaults --trust
```

`--vcs-ref HEAD` makes copier render from the working tree (so
uncommitted edits are picked up). For each render, sanity-check the
key files: `.devcontainer/devcontainer.json` should parse as JSON
(strip `//` comments first), conditional files should appear or
not as expected, and shell scripts should preserve their `755` mode.
