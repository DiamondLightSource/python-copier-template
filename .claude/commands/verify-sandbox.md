---
description: Verify Claude's mount-namespace sandbox is intact — env canaries, masked credentials, gitconfig bind, and the four VS Code IPC sockets from the Demmel writeup.
---

# Verify sandbox

Run the full sandbox verification described in `README-CLAUDE.md` and
report a PASS/FAIL table. The threat model these checks defend against
is documented in:

- `README-CLAUDE.md` (this repo) — sections **What's locked down** and
  **Verifying the sandbox**.
- Daniel Demmel, *Coding agents in secured VS Code dev containers* —
  <https://www.danieldemmel.me/blog/coding-agents-in-secured-vscode-dev-containers>
  — describes the `vscode-ipc-*.sock`, `vscode-git-*.sock`,
  `vscode-ssh-auth-*.sock`, and `vscode-remote-containers-ipc-*.sock`
  bridges in `/tmp` that re-appear up to ~60s after window attach. Our
  defence is the private mount namespace set up by `just claude`, not a
  one-shot sweep.

## How to run

Execute every check below in a single Bash invocation where practical
(parallel them when independent). For each item, report PASS or FAIL
with a one-line reason. Do not skip a check because an earlier one
failed — collect everything, then summarise.

If any check FAILs, end the report with: "Sandbox is leaking — do not
trust `--dangerously-skip-permissions` until fixed. Open an issue
against `gilesknap/python-copier-template`."

## Checks

### 1. Namespace markers

- `IS_SANDBOX` env var must be `1` (set by `claude-sandbox.sh` after
  `unshare -m`). If unset, Claude was not launched via `just claude`.
- `IN_DEVCONTAINER` env var must be set.

### 2. Host bridge env vars (must all be unset)

`SSH_AUTH_SOCK`, `GIT_ASKPASS`, `VSCODE_GIT_IPC_HANDLE`,
`VSCODE_GIT_ASKPASS_NODE`, `VSCODE_GIT_ASKPASS_MAIN`,
`VSCODE_IPC_HOOK_CLI`, `BROWSER`.

### 3. SSH agent unreachable

`ssh-add -l` must fail with "Could not open a connection to your
authentication agent." Anything that lists keys is a FAIL.

### 4. `/tmp` and `/run/user` are private tmpfs

- `mount | grep ' on /tmp '` must show a `tmpfs` entry (this confirms
  the mount namespace is active for `/tmp`).
- `ls /tmp` must NOT contain any of the four Demmel sockets:
  `vscode-ipc-*.sock`, `vscode-git-*.sock`, `vscode-ssh-auth-*.sock`,
  `vscode-remote-containers-ipc-*.sock`. Glob each one explicitly.
- `ls /run/user/*/` must NOT contain `vscode-*` entries.

### 5. Host credential dirs masked

Each of these must be empty or absent:
`/root/.ssh`, `/root/.gnupg`, `/root/.aws`, `/root/.azure`,
`/root/.gcloud`, `/root/.docker`, `/root/.netrc`.

A non-empty `/root/.ssh` (containing `id_*` or `authorized_keys`) is a
critical FAIL — the host SSH keys are reachable.

### 6. Gitconfig bind-mount

- `mount | grep '/root/.gitconfig'` must show a bind mount (typically
  `fuse-overlayfs` or `bind` from `/etc/claude-gitconfig`).
- `git config --global --list` must contain ONLY:
  - `user.name` / `user.email` (host identity, copied through),
  - `safe.directory=*`,
  - `url.https://github.com/.insteadof=git@github.com:`,
  - `url.https://gitlab.diamond.ac.uk/.insteadof=git@gitlab.diamond.ac.uk:`,
  - `credential.https://github.com.helper=` then `!/usr/bin/gh auth git-credential`,
  - `credential.https://gitlab.diamond.ac.uk.helper=` then `!/usr/local/bin/glab auth git-credential`.
- Any other `credential.*.helper` (especially one pointing at
  `/tmp/vscode-remote-containers-*.js` or `/.vscode-server/...`) is a
  FAIL.
- `/etc/gitconfig` must be masked (bind-mounted to `/dev/null` or
  absent). `mount | grep '/etc/gitconfig'` should show a bind mount
  whose source is `/dev/null` (appears as `devtmpfs` with `mode=755`,
  inode for major 1 / minor 3), OR `ls /etc/gitconfig` returns
  "No such file or directory". A regular file at `/etc/gitconfig` with
  any contents is a FAIL — the host's system-scope gitconfig is
  reachable and could carry `url.insteadof`, `http.proxy`,
  `core.hooksPath`, or credential helpers that bypass /root/.gitconfig.
- System scope must be empty: `git config --system --list` must produce
  no output (exit 0 with empty stdout, or exit non-zero). Any line is a
  FAIL — broader than just `credential.helper`, since `core.hooksPath`
  or `url.insteadof` at system scope are equally dangerous.

### 7. Credential source is gh, not a host bridge

`printf 'protocol=https\nhost=github.com\n\n' | git credential fill`
must return a `password=` line. The token prefix tells you the source:

- `gho_…` or `github_pat_…` from `gh auth git-credential` → PASS.
- Anything else (e.g. a token from a `vscode-git-*.sock` bridge) → FAIL.

Do NOT print the token. Redact with `sed 's/password=.*/password=<REDACTED>/'`.
Skip this check (mark N/A, not FAIL) if `just gh-auth` has not been run
for this repo — the README explicitly carves that out.

## Output format

Print a single table:

```
CHECK                                        STATUS  DETAIL
1.  IS_SANDBOX=1                              PASS/FAIL  ...
2.  Host bridge env vars unset                PASS/FAIL  ...
3.  ssh-add -l fails                          PASS/FAIL  ...
4a. /tmp is tmpfs                             PASS/FAIL  ...
4b. No vscode-*.sock in /tmp                  PASS/FAIL  ...
4c. No vscode-* in /run/user                  PASS/FAIL  ...
5.  Host credential dirs masked               PASS/FAIL  ...
6a. /root/.gitconfig bind-mounted             PASS/FAIL  ...
6b. Gitconfig contents are sandbox-only       PASS/FAIL  ...
6c. /etc/gitconfig masked                     PASS/FAIL  ...
6d. System-scope gitconfig is empty           PASS/FAIL  ...
7.  git credential fill source is gh          PASS/FAIL/N/A  ...
```

End with one line: `RESULT: SANDBOX OK` if every check is PASS or N/A,
otherwise `RESULT: SANDBOX LEAKING — see failures above` and the issue
pointer.
