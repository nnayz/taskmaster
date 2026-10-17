# Remote transport

[`zeus/REMOTE_PORT.md`](https://github.com/nnayz/zeus/blob/main/zeus/REMOTE_PORT.md)
is the active architecture and maintenance baseline for remote work. Read it
before changing remote session behavior, SSH handling, PTYs, holders, terminal
state, or packaging. This page is orientation only; when it and the canonical
document disagree, the canonical document wins.

## The shape

| Concern | Design |
|---------|--------|
| Byte transport | OpenSSH (`ssh -T`). SSH is the authenticated, encrypted pipe; it must not own the Agent PTY. |
| Remote process | One independent `zeus-remote` Holder process and Unix socket per session. The Holder owns only the PTY, the Agent process tree, the current terminal grid/modes/cursor, bounded output, exit facts, and the controller lease. |
| Local authority | The local Engine owns the session record, manifests, status reduction, orchestration, lifecycle policy, and host management. There is no multi-session Zeus supervisor on the host. |
| Bootstrap | Idempotent: probe the platform, select an exact local artifact, upload to a nonce temp path, verify, then atomically rename. Versioned binaries coexist by protocol and Build ID; GC retains every Build ID referenced by a session. |
| Failure | Fail closed. Missing, corrupt, unsupported, or capability-incompatible artifacts produce a structured error (`remote_transport_unavailable`) — never a fallback transport. |
| Attach | Exactly one live attach/controller. A new attach atomically increments the controller epoch and revokes the old one. |
| Snapshot | Full Snapshot carries the visible grid, cursor, modes, dimensions, and sequence. Scrollback is bounded and served on demand. |

The former Rust SSH + `tmux` transport was deleted. It must not return as
`legacy_tmux`, a feature flag, a migration path, or a runtime fallback.

## Where the code lives

| Piece | Location |
|-------|----------|
| Protocol (`remote_pty`) | `zeus/crates/zeus-proto` — versioned and additive for live sessions |
| Helper binary and Holder | `zeus/crates/zeus-remote` (keep it free of GPUI, `zeus-app`, `zeus-client`, `zeus-node`) |
| Bootstrap and SSH seam | `zeus/crates/zeus-engine` |
| Terminal parser/grid/diff | `zeus/crates/zeus-terminal-state` — shared with the local Engine; do not add a second parser |
| Host catalog and settings | `zeus/crates/zeus-app` (Settings → Remote), stored in `hosts.json` |

## Performance gates

The canonical document defines the acceptance numbers; the short version is:
snapshot p90 ≤ 100 ms, input-to-PTY p95 ≤ 10 ms, output-to-diff p90 ≤ 50 ms,
and loopback interaction median ≤ 75 ms / p90 ≤ 150 ms. Among correct designs,
prefer lower latency, CPU, memory, copies, and wakeups; do not add a
supervisor, fan-out, lock, or cache without benchmark evidence.

## Persistence outcomes

Remote persistence is detected, not assumed. A remote session reports one of
`native-detach`, `user-supervisor`, or `non-persistent` distinctly, using only
an already-available, no-configuration transient user supervisor when one
exists. `setsid()` surviving logout is never assumed. Never fall back to
`tmux`.

A finite-lived OpenSSH ControlMaster may be reused for performance; session
survival must never depend on it.

## Tests and release gates

- Fallback-free Helper behavior is guarded by
  `zeus/scripts/verify-remote-refactor.sh` (Repo guards job).
- [`zeus/scripts/remote-acceptance.sh`](https://github.com/nnayz/zeus/blob/main/zeus/scripts/remote-acceptance.sh)
  runs the remote perf gate plus the opt-in slow-attach and supervisor
  Holder end-to-end tests with a release build.
- [`zeus/scripts/remote-ssh-soak.sh`](https://github.com/nnayz/zeus/blob/main/zeus/scripts/remote-ssh-soak.sh)
  runs a detach/reconnect soak against a disposable ordinary-user SSH account
  (`ZEUS_REMOTE_SSH_TARGET`). CI provisions a throwaway `sshd` for it.
- CI builds and executes `zeus-remote probe` natively on Linux x86_64/aarch64
  and macOS arm64. macOS x86_64 and Rosetta are not supported Helper targets.

See [Tests and fixtures](testing.md) for how to run these locally and
[Required checks](required-checks.md) for the CI mapping.
