# Tests and fixtures

The default suite is deterministic and self-contained:

```sh
cd zeus
cargo test --workspace
```

It must not require a real SSH host, a signed-in agent, or macOS Screen
Recording permission. Captures are faked; remote paths use fixture homes,
fake `ssh` executables, Unix sockets, and spawned test PTYs.

Integration targets live beside the crates under `zeus/crates/*/tests/`.
The most useful ones when touching sessions and transports:

| Target | Covers |
|--------|--------|
| `zeus-engine/tests/session.rs`, `pty.rs`, `pipeline.rs` | Session lifecycle, PTYs, output pipeline |
| `zeus-engine/tests/holder.rs`, `holder_session.rs` | Local holder ownership and adoption |
| `zeus-engine/tests/attach.rs`, `terminal_attach.rs`, `terminal_control.rs` | Attach, snapshots, controller behavior |
| `zeus-engine/tests/checkpoint.rs`, `wake.rs`, `deferred.rs` | Checkpoints, waking, deferred work |
| `zeus-engine/tests/mcp_tools.rs`, `inject_prompt.rs` | MCP bridge and prompt injection |
| `zeus-engine/tests/legacy_remote.rs` | Guards that removed transports stay removed |
| `zeus-remote/tests/holder_e2e.rs`, `real_ssh_soak.rs` | Remote holder end-to-end and the opt-in SSH soak |
| `zeus-companion/tests/integration.rs`, `security.rs` | Companion gateway contract and security |

When changing remote behavior, cover at least: noisy shell startup and
environment-capture timeout/failure; supported/unsupported OS and
architecture parsing; concurrent and interrupted bootstrap; corrupt artifacts
and protocol/Build ID mismatch; detach/reconnect with unchanged process
identity and terminal snapshot; slow-attach snapshot recovery; controller
lease revocation; normal exit, signal exit, and Holder failure; and all
persistence capability outcomes.

## Opt-in runs

Anything that needs a real app, agent, or host is opt-in, documented, and
never in ordinary CI:

- [Screenshot soak test](screenshot-soak.md) — a real Zeus window.
- Live agent delegation — see
  [Build and run](build-and-run.md#live-agent-smoke-test).
- SSH detach soak — `ZEUS_REMOTE_SSH_TARGET` plus `ZEUS_REMOTE_SOAK_SECONDS`,
  run through `zeus/scripts/remote-ssh-soak.sh`.
- Remote acceptance — `zeus/scripts/remote-acceptance.sh` runs the remote perf
  gate and the ignored slow-attach and supervisor Holder tests with a release
  build.

Any test that requires a real remote host must document its environment
variables and its cleanup behavior. Use a disposable account and remove
uploaded Helper artifacts and session state afterwards.

## Browser automation

The browser sidecar has its own install/audit path and its own tests:

```sh
./scripts/check.sh --browser
```

This runs `npm ci`, `npm audit --omit=dev`, installs the Playwright engines,
and executes `cargo test -p zeus-engine browser`.

## Performance measurements

`zeus/scripts/latency-probe.sh`, `perf-gate.sh`, and `remote-perf-gate.sh`
measure the packaged artifact and the remote transport. `zeus/PERF.md` and
`zeus/PERF-AUDIT.md` are dated records of past runs: context, not proof that
the current build passes. Release acceptance comes from the packaged-artifact
gates in CI.

## Documentation checks

Both books and their cross-links are validated in CI; see
[Writing documentation](writing-documentation.md) and
[Required checks](required-checks.md).
