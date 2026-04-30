#!/bin/bash
# Inner script for `just claude`: runs inside a private mount namespace
# (created by `unshare -m` from the justfile recipe). Mounts tmpfs over
# the locations VS Code uses for host bridges, builds a Claude-only
# /root/.gitconfig, then exec's claude with PR_SET_PDEATHSIG so it dies
# if its parent shell does. Requires CAP_SYS_ADMIN — granted via
# --cap-add=SYS_ADMIN in devcontainer.json's runArgs. See
# README-CLAUDE.md for the full sandbox model.
set -euo pipefail

# VS Code drops IPC sockets (vscode-ipc-*.sock, vscode-git-*.sock,
# vscode-ssh-auth-*.sock, vscode-remote-containers-ipc-*.sock) and the
# vscode-remote-containers-*.js credential shim in /tmp, plus more in
# /run/user/<uid>/. Replacing those directories with tmpfs in Claude's
# namespace makes them invisible. Outside the namespace (the user's
# regular terminal) VS Code keeps using them normally.
mount -t tmpfs tmpfs /tmp
if [ -d /run/user ]; then
    mount -t tmpfs tmpfs /run/user
fi

# Mask credential directories the user may bind-mount from the host for
# their own use from non-Claude terminals (e.g. ~/.ssh for SSH-based
# git push). Claude sees an empty tmpfs; the user's regular shell sees
# the originals.
for d in /root/.ssh /root/.gnupg /root/.aws /root/.azure /root/.gcloud /root/.docker; do
    if [ -d "$d" ]; then
        mount -t tmpfs tmpfs "$d"
    fi
done
# .netrc is a single file, not a dir — mask via bind to /dev/null.
if [ -e /root/.netrc ]; then
    mount --bind /dev/null /root/.netrc
fi

# Build a Claude-only /root/.gitconfig containing the in-container
# credential helpers (gh / glab) and HTTPS rewrites — and nothing else
# the user has on the host (no SSH url rewrites, no host-specific
# helpers). User identity is read from the original gitconfig BEFORE
# we bind over it, so commits Claude makes are still attributed.
git_name=$(git config --get user.name 2>/dev/null || true)
git_email=$(git config --get user.email 2>/dev/null || true)
gh_path=$(command -v gh || echo /usr/bin/gh)
glab_path=$(command -v glab || echo /usr/local/bin/glab)
cat > /etc/claude-gitconfig <<EOF
[user]
    name = $git_name
    email = $git_email
[safe]
    directory = *
[url "https://github.com/"]
    insteadOf = git@github.com:
[url "https://gitlab.diamond.ac.uk/"]
    insteadOf = git@gitlab.diamond.ac.uk:
[credential "https://github.com"]
    helper =
    helper = !$gh_path auth git-credential
[credential "https://gitlab.diamond.ac.uk"]
    helper =
    helper = !$glab_path auth git-credential
EOF
mount --bind /etc/claude-gitconfig /root/.gitconfig

# IS_SANDBOX=1 is the canary `.claude/hooks/sandbox-check.sh` keys off.
# Env-blanks: SSH_AUTH_SOCK / VSCODE_GIT_IPC_HANDLE / VSCODE_IPC_HOOK_CLI
# all point into /tmp (already tmpfs in this namespace), but blanking
# the vars stops Claude from even *trying* the path. GIT_ASKPASS and
# VSCODE_GIT_ASKPASS_* point under /.vscode-server which the namespace
# does NOT mask — blanking them is the actual defence against Claude
# triggering the VS Code "log in to GitHub" popup. BROWSER points at a
# host helper that opens URLs in the user's browser — blanked so
# Claude cannot drive the user's browser.
exec setpriv --pdeathsig SIGKILL env \
    SSH_AUTH_SOCK= \
    GIT_ASKPASS= \
    VSCODE_GIT_IPC_HANDLE= \
    VSCODE_GIT_ASKPASS_NODE= \
    VSCODE_GIT_ASKPASS_MAIN= \
    VSCODE_IPC_HOOK_CLI= \
    BROWSER= \
    IS_SANDBOX=1 \
    claude --dangerously-skip-permissions
