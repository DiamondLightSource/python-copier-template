#!/bin/bash
set -euo pipefail

# Wipe any credential helpers and SSH URL rewrites that VS Code's Dev
# Containers extension injects when it copies the host gitconfig and
# spawns its own credential bridge. We need --unset-all (not =''),
# because VS Code stores the helper as a single multi-valued line that
# `git config <key> <value>` only replaces if there is a single value.
# IMPORTANT: VS Code writes its credential.helper to /etc/gitconfig
# (system scope), not ~/.gitconfig — so the system scope must also be
# cleared, otherwise the helper still runs.
for scope in --system --global; do
    git config $scope --unset-all credential.helper 2>/dev/null || true
    git config $scope --unset-all credential.https://github.com.helper 2>/dev/null || true
    git config $scope --unset-all credential.https://gitlab.diamond.ac.uk.helper 2>/dev/null || true
    git config $scope --unset-all url.ssh://git@github.com/.insteadOf 2>/dev/null || true
done

# VS Code drops a Node-based credential bridge in /tmp that talks back
# to the host over a named pipe — even with VSCODE_GIT_IPC_HANDLE blank
# it can still surface host PATs. Remove it so any stale `credential.helper`
# entries cannot fall through to it.
rm -f /tmp/vscode-remote-containers-*.js

# Force all SSH-style remotes to use HTTPS so the gh/glab credential helpers
# handle auth. This keeps the container SSH-key-free (Claude stays sandboxed)
# while still allowing push/pull on repos whose remotes are set to git@...:.
git config --global url."https://github.com/".insteadOf "git@github.com:"
git config --global url."https://gitlab.diamond.ac.uk/".insteadOf "git@gitlab.diamond.ac.uk:"

# Pin per-host helper to the in-container gh path. The host gitconfig may
# reference /usr/local/bin/gh which doesn't exist here (apt installs to
# /usr/bin/gh); without this, git falls through to the next helper.
if command -v gh >/dev/null; then
    git config --global credential.https://github.com.helper "!$(command -v gh) auth git-credential"
fi

# If gh CLI has cached credentials (survive container rebuild), re-register
# its git credential helper so HTTPS remotes authenticate automatically.
if gh auth status &>/dev/null; then
    gh auth setup-git
fi

# Pin per-host helper to the in-container glab path.
if command -v glab >/dev/null; then
    git config --global credential.https://gitlab.diamond.ac.uk.helper "!$(command -v glab) auth git-credential"
fi
