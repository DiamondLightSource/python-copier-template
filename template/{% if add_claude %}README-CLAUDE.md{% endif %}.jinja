# Claude sandbox

This project's devcontainer is configured to run Claude Code with
`--dangerously-skip-permissions` (see `justfile`'s `claude` recipe). To make
that safe, the container is set up as a sandbox: Claude can use the project
toolchain, push/pull through PATs it owns, and persist its own settings —
but it cannot reach back to the host's identity or shared resources.

This file documents what's locked down, what's deliberately left exposed,
and how to verify the sandbox is intact.

## What's locked down

- **No host SSH keys.** `SSH_AUTH_SOCK` is unset in `remoteEnv`, so any
  SSH-agent forwarded by the host is invisible inside the container. No
  private keys are mounted into `/root/.ssh` either — only `known_hosts`.
- **No VS Code git credential injection.** `GIT_ASKPASS`,
  `VSCODE_GIT_IPC_HANDLE`, `VSCODE_GIT_ASKPASS_*` are blanked in
  `devcontainer.json`'s `remoteEnv`, but that only sets the *initial*
  environment of the remote server — VS Code's built-in Git extension
  re-injects `GIT_ASKPASS` and `VSCODE_GIT_IPC_HANDLE` per child-process
  spawn so any extension can prompt for credentials through the UI. The
  `just claude` recipe therefore re-blanks both vars on the `claude`
  command line itself, which is the only point at which they can be
  reliably stripped before `claude` inherits them.
  `VSCODE_GIT_ASKPASS_NODE`/`_MAIN` may remain populated; they are just
  paths to the askpass script and are inert without `IPC_HANDLE` (the
  socket the script phones home through), so they don't need blanking.
  Separately, `postStart.sh` aggressively unsets `credential.helper` and
  per-host helpers in BOTH `--system` (`/etc/gitconfig`) and `--global`
  scopes — VS Code writes the helper into the *system* gitconfig, so a
  global-only cleanup leaves the leak open. The script also removes the
  `/tmp/vscode-remote-containers-*.js` bridge that VS Code drops in.
  The cleanup re-runs on `postAttachCommand` because VS Code re-injects
  the helper after `postStartCommand`.
- **Per-host helpers point at the in-container CLI.** The host gitconfig
  often references `/usr/local/bin/gh`; here `gh` is at `/usr/bin/gh`. We
  rewrite the helper to `command -v gh` / `command -v glab` so it doesn't
  fall through to a stale entry.
- **All git remotes forced to HTTPS.** `url.<https>.insteadOf` rewrites
  `git@github.com:` and `git@gitlab.diamond.ac.uk:` so push/pull always
  uses the gh/glab credential helper rather than SSH.
- **Auth is per-repo.** `gh-auth-${repo}` and `glab-auth-${repo}` are
  named volumes, not bind mounts — each project gets its own scoped PAT
  via `just gh-auth` / `just glab-auth`. Authenticate once per repo and
  the token survives container rebuilds.

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

From inside the container:

```bash
# Should be empty / unset
echo "SSH_AUTH_SOCK='${SSH_AUTH_SOCK:-<unset>}'"
ssh-add -l                                         # "Could not open a connection..."
ls /root/.ssh                                      # only known_hosts

# Should NOT return a host PAT
printf 'protocol=https\nhost=github.com\n\n' | git credential fill

# Should show only gh/glab helpers (no /tmp/vscode-remote-containers-*.js)
git config --global --list | grep -i credential
```

If `git credential fill` returns a `password=gho_...` for github.com when
you have not run `just gh-auth`, the sandbox is leaking — open an issue
against the python-copier-template.

## Authenticating

```bash
just gh-auth     # paste a github.com PAT (repo + workflow scope is enough)
just glab-auth   # gitlab.com  (pass a hostname arg for self-hosted instances)
```

## Starting Claude

```bash
just claude      # runs `claude --dangerously-skip-permissions` with SSH_AUTH_SOCK blanked
```
