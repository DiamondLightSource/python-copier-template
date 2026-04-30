#!/bin/bash
# UserPromptSubmit hook: verify the Claude sandbox is intact before
# executing any prompt. Exit code 2 blocks the prompt and shows the
# message to the user. See README-CLAUDE.md for the full sandbox model.

fail() { echo "BLOCKED: $1" >&2; exit 2; }

# Are we in the devcontainer at all?
[ -n "${IN_DEVCONTAINER:-}" ] || \
    fail "not in the devcontainer (IN_DEVCONTAINER unset). Reopen the project in the devcontainer."

# Host SSH agent must not be reachable.
[ -z "${SSH_AUTH_SOCK:-}" ] || \
    fail "SSH_AUTH_SOCK is set ($SSH_AUTH_SOCK) — host SSH agent is reachable. run \"just claude\""

# VS Code git credential bridge must be silenced.
[ -z "${VSCODE_GIT_IPC_HANDLE:-}" ] || \
    fail "VSCODE_GIT_IPC_HANDLE is set — VS Code credential bridge is reachable. run \"just claude\""
[ -z "${GIT_ASKPASS:-}" ] || \
    fail "GIT_ASKPASS is set — VS Code askpass is injected. run \"just claude\""

# The /tmp credential helper script VS Code drops in must have been removed.
if compgen -G '/tmp/vscode-remote-containers-*.js' >/dev/null; then
    fail "/tmp/vscode-remote-containers-*.js bridge present — re-run .devcontainer/postStart.sh."
fi

# system-scope credential.helper is where VS Code injects; if anything
# is set there git will use it before our per-host helpers.
if git config --system --get credential.helper >/dev/null 2>&1; then
    fail "system credential.helper is still set — re-run .devcontainer/postStart.sh."
fi

exit 0
