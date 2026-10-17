# Development setup

Zeus is a monorepo. The desktop app, Engine, CLI, and transports are Rust and
live under `zeus/`; the native iOS Companion is a SwiftUI client under
`ios/ZeusCompanion/`.

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| macOS 15 or newer | The desktop app, holders, and packaging target macOS. |
| Xcode Command Line Tools | The Rust build needs the macOS SDK. Install with `xcode-select --install`. |
| [rustup](https://rustup.rs) | The toolchain is pinned by [`zeus/rust-toolchain.toml`](https://github.com/nnayz/zeus/blob/main/zeus/rust-toolchain.toml); rustup installs and selects it automatically inside `zeus/`. |
| git | Worktree and review features are exercised against real repositories. |

The pinned toolchain currently ships clippy and rustfmt, which the required
checks use. The workspace declares `edition = "2024"`.

Optional, depending on what you work on:

- **Packaging** needs Homebrew `zig`, `cargo-packager`, and `cargo-zigbuild`.
  See [Packaging](packaging.md).
- **Watch mode** uses [watchexec](https://github.com/watchexec/watchexec)
  (`brew install watchexec`).
- **The website and prototypes** need Node 22 (`site/`, `sidecar/`,
  `prototypes/companion-web/`).
- **The iOS Companion** needs Xcode 26 or newer; see
  [Companion clients and prototypes](companion-clients.md).

Building Zeus itself requires none of the Node tooling, Python, or a
preinstalled Zeus service.

## Check out the repository

```sh
git clone https://github.com/nnayz/zeus.git
cd zeus
```

Most development commands run from `zeus/`, the Rust workspace. Repository
scripts under `scripts/` (root) and `zeus/scripts/` are run from their
respective directories unless a script says otherwise.

## First build

```sh
cd zeus
cargo build
```

Expect the first build to take a while: GPUI is compiled from Zeus's pinned
Zed revision. The exact revision and toolchain are recorded in
[`zeus/README.md`](https://github.com/nnayz/zeus/blob/main/zeus/README.md);
upgrade them deliberately and update that record.

If the build succeeds, continue to [Build and run](build-and-run.md). If you
only want to run the checks, start with
[Required checks](required-checks.md).

## Working in a worktree

Zeus itself is developed with Git worktrees. Create one per task so parallel
builds and checks do not fight over `zeus/target/`:

```sh
git worktree add ../zeus-my-change -b my-change
cd ../zeus-my-change/zeus
cargo build
```

Cargo caches are per-worktree, so the first build in a new worktree is again
the slow one. Reuse a worktree for related changes instead of creating one per
commit.
