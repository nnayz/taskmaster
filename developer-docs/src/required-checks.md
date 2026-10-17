# Required checks

Run these from `zeus/` before handing off a change:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo build --workspace --release
```

They are the gates CI enforces and the ones the repository instructions call
for. While iterating, run the narrowest relevant package or test first, then
the full set before handoff.

The repository-wide wrapper adds the shell and release-guard checks:

```sh
./scripts/check.sh            # shell syntax + release guards + full Rust suite
./scripts/check.sh --browser  # additionally install and run the browser sidecar
```

`check.sh` requires `bash`, `cargo`, and `python3`.

## What CI runs

| CI job | Covers | Local equivalent |
|--------|--------|------------------|
| Rust app (zeus) | fmt, clippy, workspace tests, remote acceptance gates, release build | the four commands above, plus `scripts/remote-acceptance.sh` |
| Repo guards | shell syntax, `verify-remote-refactor.sh`, release-publishing guard tests, sidecar audit | `bash -n scripts/*.sh zeus/scripts/*.sh`, then the named scripts |
| Closed-lid mock safety | `zeus-power` policy tests, holder identity tests, package guard self-test | `cargo test --locked -p zeus-power` and the holder test targets |
| Remote Helper (native targets) | builds and executes `zeus-remote probe` on Linux x86_64/aarch64 and macOS arm64 | `cargo build --locked --release -p zeus-remote --target <target>` plus the probe |
| Remote OpenSSH detach/reconnect | detach/reconnect against a disposable ordinary-user sshd | `ZEUS_REMOTE_SSH_TARGET=<host> scripts/remote-ssh-soak.sh` |
| Package zeus.app (unsigned) | universal bundle assembly, helper layout, signatures | `zeus/scripts/package.sh` |
| Homebrew cask | cask syntax, style, and metadata guards | `ruby -c Casks/zeus.rb`, `brew style Casks/zeus.rb` |
| Companion web contract | fixture and client conformance tests | `npm test` in `prototypes/companion-web` |
| Browser sidecar | sidecar install/audit and `zeus-engine` browser tests | `./scripts/check.sh --browser` |

The remote Helper targets are release gates: Linux x86_64, Linux aarch64, and
macOS arm64. macOS x86_64 and Rosetta are not supported Remote Helper
targets.

## Tests that need a real machine or app

These are explicitly opt-in and must never run in ordinary CI:

| Run | Enables | Environment |
|-----|---------|-------------|
| [Screenshot soak](screenshot-soak.md) | A real Zeus window under Screen Recording | `ZEUS_SCREENSHOT_SOAK=1` |
| Live agent delegation | A hosted, authenticated agent and its Zeus MCP connection | `ZEUS_REAL_AGENT_SMOKE=1`, `ZEUS_REAL_AGENT_KIND`, `ZEUS_REAL_AGENT_CWD`, `ZEUS_REAL_AGENT_TIMEOUT_SECONDS` |
| SSH detach soak | A disposable ordinary-user SSH account | `ZEUS_REMOTE_SSH_TARGET`, `ZEUS_REMOTE_SOAK_SECONDS` |
| Remote acceptance | Release-built `zeus-remote` plus the slow-attach and supervisor fixtures | none beyond a normal macOS/Linux host |

Any test that requires a real remote host must document its environment
variables and its cleanup behavior. Use a disposable account you can delete,
and remove uploaded Helper artifacts and session state when you are done.

## Documentation checks

Both books must build, and internal links and assets are validated:

```sh
mdbook build docs
mdbook build developer-docs
python3 scripts/check-docs-links.py --site-build site/build
```

CI assembles both books under `site/build/` and runs the link checker before
uploading Pages. See [Writing documentation](writing-documentation.md).
