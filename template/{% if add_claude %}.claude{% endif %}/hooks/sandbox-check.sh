#!/bin/bash
# UserPromptSubmit hook: verify the Claude sandbox is intact before
# executing any prompt. Exit code 2 blocks the prompt and shows the
# message to the user. See README-CLAUDE.md for the full sandbox model.

fail() { echo "BLOCKED: $1" >&2; exit 2; }

# Are we in the devcontainer at all?
[ -n "${IN_DEVCONTAINER:-}" ] || \
    fail "not in the devcontainer (IN_DEVCONTAINER unset). Reopen the project in the devcontainer."

# IS_SANDBOX=1 is set by the inner `just claude` script after it sets up
# the private mount namespace. If it's missing, Claude was launched
# without the namespace and /tmp/vscode-*.sock host bridges are reachable.
[ -n "${IS_SANDBOX:-}" ] || \
    fail "IS_SANDBOX unset — Claude was not launched via \"just claude\", so the mount-namespace sandbox is not active."

# Host SSH agent must not be reachable. remoteEnv blanks SSH_AUTH_SOCK and
# `just claude` re-blanks it; if it is set, neither layer applied.
[ -z "${SSH_AUTH_SOCK:-}" ] || \
    fail "SSH_AUTH_SOCK is set ($SSH_AUTH_SOCK) — host SSH agent is reachable. run \"just claude\" or rebuild the devcontainer."

# GIT_ASKPASS points at a script under /.vscode-server, which the
# namespace does NOT mask. If the env var is non-empty AND the file is
# reachable, claude-sandbox.sh's exec-line blank failed to apply.
[ ! -e "${GIT_ASKPASS:-}" ] || \
    fail "GIT_ASKPASS script ($GIT_ASKPASS) is reachable — claude-sandbox.sh did not blank the env var. Rebuild the devcontainer or re-run \"just claude\"."

# /root/.gitconfig must be the bind-mounted /etc/claude-gitconfig (gh/glab
# helpers only). VS Code reconnects can drop the bind and re-expose the
# host gitconfig, whose [credential] helper invokes a node script under
# /.vscode-server via /tmp/vscode-remote-containers-*.js — leaking the
# host's git credentials into the sandbox.
! grep -q -e 'vscode-remote-containers' -e '\.vscode-server' /root/.gitconfig 2>/dev/null || \
    fail "/root/.gitconfig contains a VS Code credential bridge — the bind on /root/.gitconfig has been dropped (likely by a VS Code reconnect). Exit Claude and re-run \"just claude\"."

# /etc/gitconfig must be masked (bind-mounted to /dev/null by claude-sandbox.sh).
# If the host's system-scope gitconfig is reachable, it can carry url.insteadof,
# core.hooksPath, http.proxy, or credential helpers that bypass /root/.gitconfig.
# `git config --system --list` returning any content means the mask is gone.
[ -z "$(git config --system --list 2>/dev/null)" ] || \
    fail "/etc/gitconfig is exposing system-scope settings — the bind-mount mask on /etc/gitconfig has been dropped. Exit Claude and re-run \"just claude\"."

exit 0
