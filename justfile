# Start Claude Code in sandbox mode (no SSH agent, skip permission prompts).
# Runs Claude inside a private mount namespace so VS Code's host-bridge
# sockets (vscode-ipc-*.sock, vscode-git-*.sock, vscode-ssh-auth-*.sock,
# vscode-remote-containers-ipc-*.sock) in /tmp and /run/user/<uid>/ are
# invisible — Claude sees empty tmpfs at those paths. setpriv
# --pdeathsig SIGKILL inside the inner script makes Claude die if the
# wrapping shell exits. See README-CLAUDE.md for the full sandbox model.
claude:
    exec unshare -m --propagation private .devcontainer/claude-sandbox.sh


# Authenticate gh CLI with a GitHub PAT (token not stored in shell history)
gh-auth:
    #!/bin/bash
    read -sp "GitHub PAT: " t && echo
    echo "$t" | gh auth login --with-token
    unset t
    gh auth setup-git
    gh auth status


# Authenticate glab CLI with a GitLab PAT (token not stored in shell history).
# --git-protocol https prevents glab's SSH insteadOf rewrite.
glab-auth hostname="gitlab.com":
    #!/bin/bash
    read -sp "GitLab PAT for {{ hostname }}: " t && echo
    echo "$t" | glab auth login --stdin --hostname {{ hostname }} --git-protocol https
    unset t
    glab auth status
