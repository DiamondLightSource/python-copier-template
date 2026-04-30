# Claude sandbox

This project's devcontainer is configured to run Claude Code with
`--dangerously-skip-permissions` (see `justfile`'s `claude` recipe). To make
that safe, the container is set up as a sandbox: Claude can use the project
toolchain, push/pull through PATs it owns, and persist its own settings —
but it cannot reach back to the host's identity or shared resources.

This file documents what's locked down, what's deliberately left exposed,
and how to verify the sandbox is intact.

## What's locked down

- **No host bridges via VS Code IPC sockets.** VS Code's server creates
  several unix sockets in `/tmp` and `/run/user/<uid>/` that are bridges
  back to the host: `vscode-ipc-*.sock` (runs `code` CLI on the host),
  `vscode-git-*.sock` (git credential bridge — surfaces host PATs),
  `vscode-ssh-auth-*.sock` (host SSH agent forward), and
  `vscode-remote-containers-ipc-*.sock` (Dev Containers extension RPC).
  These are re-created on every window attach and continue to appear up
  to ~60s later — see [the threat-model writeup][demmel-blog] — so any
  one-shot cleanup leaves a window. The defence is the **`unshare -m`**
  call in `just claude`: Claude runs in a private mount namespace where
  `/tmp` and `/run/user/<uid>/` are fresh tmpfs. The bridges still exist
  in the parent namespace (VS Code keeps using them normally) but are
  invisible to Claude. No race, no sweeper, no recurring check needed.
  Requires `--cap-add=SYS_ADMIN` in `runArgs` for rootless podman.

  [demmel-blog]: https://www.danieldemmel.me/blog/coding-agents-in-secured-vscode-dev-containers
- **No host SSH keys, AWS/GCP/Azure/Docker credentials, GPG keys, or
  netrc.** The same `unshare -m` masks `/root/.ssh`, `/root/.gnupg`,
  `/root/.aws`, `/root/.azure`, `/root/.gcloud`, `/root/.docker`, and
  `/root/.netrc` (where present) with empty tmpfs. This means you *can*
  bind-mount your host `~/.ssh` into the container if you want to use
  SSH keys from a regular terminal — Claude's namespace blanks them out
  while non-Claude shells see the originals. `SSH_AUTH_SOCK` is blanked
  in the namespace exec line so VS Code's agent forwarding (which the
  user terminal keeps) cannot reach Claude.
- **Claude dies with its parent shell.** `setpriv --pdeathsig SIGKILL`
  on the inner `claude` exec sets `PR_SET_PDEATHSIG`, so if the wrapping
  `unshare`'d shell exits (terminal closed, Ctrl-C, etc.) the kernel
  immediately kills Claude — there's no orphaned-claude window where the
  namespace context is gone but Claude is still running tools.
- **Claude has its own `/root/.gitconfig` via bind-mount.**
  `claude-sandbox.sh` writes `/etc/claude-gitconfig` containing only the
  in-container gh/glab credential helpers, the `git@*:` → `https://`
  url rewrites, `safe.directory = *`, and the user identity (read from
  the host-copied gitconfig before we bind over it, so commits Claude
  makes are still attributed). It then `mount --bind`s that file onto
  `/root/.gitconfig` inside Claude's namespace. The user's regular
  terminal keeps the original `/root/.gitconfig` (host content, copied
  by `dev.containers.copyGitConfig`'s default), so the host's SSH url
  rewrites, custom credential helpers, and identity all work normally
  outside Claude — but Claude only ever sees the curated config.
- **The "log in to GitHub" popup is closed for Claude.** The user
  terminal keeps `git.terminalAuthentication` at its default (true), so
  `GIT_ASKPASS` and `VSCODE_GIT_IPC_HANDLE` are injected into terminals
  and the user gets the natural VS Code OAuth popup when an HTTPS git
  operation needs credentials. For Claude two things close that channel:
  `claude-sandbox.sh`'s exec line blanks `GIT_ASKPASS`,
  `VSCODE_GIT_IPC_HANDLE`, `VSCODE_GIT_ASKPASS_NODE`,
  `VSCODE_GIT_ASKPASS_MAIN`, `VSCODE_IPC_HOOK_CLI`, and `BROWSER`; and
  the IPC socket the askpass script would talk to lives in `/tmp`,
  which is tmpfs-masked. Both layers must be defeated for Claude to
  surface a popup.

  `.claude/hooks/sandbox-check.sh` is the periodic verifier: it fires
  on every prompt submit and refuses to run Claude if `IS_SANDBOX` is
  unset, `SSH_AUTH_SOCK` is set, or the path `GIT_ASKPASS` references
  is reachable.
- **Auth is per-repo.** `gh-auth-${repo}` and `glab-auth-${repo}` are
  named volumes, not bind mounts — each project gets its own scoped PAT
  via `just gh-auth` / `just glab-auth`. Authenticate once per repo and
  the token survives container rebuilds.

## What the user terminal gets (and why)

VS Code's regular terminal runs *outside* Claude's namespace. It is
deliberately set up with the standard developer experience so working
in the devcontainer feels natural:

- **Host gitconfig copied in.** `dev.containers.copyGitConfig` defaults
  to true, so `/root/.gitconfig` carries the user's name, email, push
  preferences, and any host url rewrites. Claude overrides this via
  bind-mount; the user terminal sees the original.
- **SSH agent forwarding.** VS Code forwards the host SSH agent into
  the container as it normally would; `SSH_AUTH_SOCK` points at
  `/tmp/vscode-ssh-auth-*.sock`. Inside Claude's namespace `/tmp` is
  tmpfs and the variable is blanked, so Claude cannot reach the agent.
- **VS Code OAuth popup for HTTPS git.** `git.terminalAuthentication`
  is left at its default, so when an HTTPS git operation needs creds
  the user gets the standard "log in to GitHub" popup. Claude's exec
  blanks `GIT_ASKPASS` / `VSCODE_GIT_IPC_HANDLE` and masks the IPC
  socket path, so the popup channel does not exist for Claude.
- **`code` CLI and host browser.** `VSCODE_IPC_HOOK_CLI` and `BROWSER`
  are inherited by the user terminal so `code <file>` and tools that
  open URLs do the natural thing. Both env vars are blanked in
  Claude's exec and the sockets they reference live in `/tmp`.

## What's deliberately exposed (and why)

- **`/root/.claude` is bind-mounted from the host's `~/.claude`.** Claude's
  settings, memory, hooks, and skills are shared between the host and the
  container — that's the whole point. Anything Claude writes to its own
  config persists to the host home directory. Treat `~/.claude` on the
  host as part of the sandbox boundary, not outside it.
- **`/workspaces` is the parent of the project, not the project itself.**
  The `workspaceMount` source is `${localWorkspaceFolder}/..`, so all
  sibling repos in the same parent directory are visible inside the
  container. This is intentional — it lets `pip install -e ../peer-repo`
  work and lets Claude read across related projects when asked. If you
  keep unrelated work in the same parent dir, Claude can see it.
- **`--net=host` shares the host's network namespace.** The container's
  hostname will match the host's, and any service bound to `localhost` on
  the host is reachable from inside. This is needed for X11, EPICS CA,
  and to avoid devcontainer port-forwarding hassles. It also means the
  container can talk to anything the host can talk to on its LAN.
- **`/cache` is a shared named volume across all devcontainers** built
  from this template — uv cache, pre-commit cache, and the project venv
  live there. Faster rebuilds; the trade-off is that a poisoned cache
  affects every project sharing the volume.

## Verifying the sandbox

Run inside `just claude` itself (use Claude's bash tool, or run the same
commands manually after dropping into a shell that has `unshare -m` set
up the way `just claude` does). The mount-namespace defences only apply
inside that namespace — a regular VS Code terminal will see the bridges
exactly as VS Code created them, which is correct.

```bash
# Canaries: should be unset (env blanks) and 1 (sandbox marker)
echo "SSH_AUTH_SOCK='${SSH_AUTH_SOCK:-<unset>}'"
echo "GIT_ASKPASS='${GIT_ASKPASS:-<unset>}'"
echo "VSCODE_GIT_IPC_HANDLE='${VSCODE_GIT_IPC_HANDLE:-<unset>}'"
echo "VSCODE_IPC_HOOK_CLI='${VSCODE_IPC_HOOK_CLI:-<unset>}'"
echo "BROWSER='${BROWSER:-<unset>}'"
echo "IS_SANDBOX='${IS_SANDBOX:-<unset>}'"          # should be 1
ssh-add -l                                          # "Could not open a connection..."

# /tmp and /run/user should be empty tmpfs inside Claude's namespace.
ls /tmp                                             # only claude-* runtime dirs
ls /run/user/*/ 2>/dev/null                         # nothing matching vscode-*
mount | grep -E ' on /tmp |/run/user'               # tmpfs entries from claude-sandbox.sh

# /root/.ssh and friends should be empty even if you bind-mount the host
# originals via devcontainer.json — Claude's namespace masks them.
ls /root/.ssh /root/.gnupg /root/.aws 2>/dev/null   # all empty (or missing)

# Claude's bind-mounted gitconfig: only gh/glab helpers + HTTPS rewrites,
# no host SSH url rewrites or unrelated host helpers.
git config --global --list | grep -E 'credential|insteadof'
mount | grep '/root/.gitconfig'                     # bind from /etc/claude-gitconfig

# Should return creds only if `just gh-auth` has been run for this repo.
printf 'protocol=https\nhost=github.com\n\n' | git credential fill
```

If `git credential fill` returns a `password=gho_...` for github.com when
you have not run `just gh-auth`, or if `ls /tmp` shows any `vscode-*`
entries inside the namespace, the sandbox is leaking — open an issue
against the python-copier-template.

## Authenticating

```bash
just gh-auth     # paste a github.com PAT (repo + workflow scope is enough)
just glab-auth   # gitlab.com  (pass a hostname arg for self-hosted instances)
```

## Starting Claude

```bash
just claude      # runs `claude --dangerously-skip-permissions` inside the mount namespace
```

After a rebuild from a previous version of this template, the user
terminal's `/root/.gitconfig` may still carry HTTPS rewrites or per-host
helpers that older `postStart.sh` runs added globally. Either rebuild
the devcontainer for a clean state, or `git config --global --unset-all`
the affected keys.
