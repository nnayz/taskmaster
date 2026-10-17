# Build and run

## Prerequisites

- macOS 15 or newer for the desktop app. The Remote Helper also builds for
  Linux x86_64 and aarch64; macOS x86_64 and Rosetta are not Helper targets.
- Rust from [`taskmaster/rust-toolchain.toml`](https://github.com/nnayz/taskmaster/blob/main/taskmaster/rust-toolchain.toml).
  The pin is currently 1.99.0, with `clippy` and `rustfmt`. `rustup` installs
  that toolchain when you build inside `taskmaster/`.
- Xcode command-line tools, for the macOS app.
- A working `cargo` on `PATH`. The first build compiles GPUI from Taskmaster's
  pinned Zed revision and takes longer than a typical crate.

Product install of a released DMG is in the
[user guide](../../src/getting-started.md). This page is the contributor path.

## Checkout

```sh
git clone https://github.com/nnayz/taskmaster.git
cd taskmaster
```

Commands below assume the repository root unless they say `taskmaster/`.

## Build

```sh
(cd taskmaster && cargo build)
```

Run a development bundle from `taskmaster/`. `scripts/dev.sh` builds a throwaway
app with a commit-specific name, window title, Dock icon, and in-window
build marker. The bundle id stays stable so macOS folder grants survive
rebuilds. Engine, Holder, and CLI helpers run from that bundle.

```sh
(cd taskmaster && ./scripts/dev.sh)
```

`./scripts/dev.sh --watch` rebuilds on save (install `watchexec` first).
`./scripts/dev.sh --release` and `./scripts/dev.sh --settings remote` are
the other everyday switches. Details, including
`TASKMASTER_DEV_SIGN_IDENTITY` for Desktop and Documents access, are in
[`taskmaster/README.md`](https://github.com/nnayz/taskmaster/blob/main/taskmaster/README.md).

The dev app and an installed Taskmaster share the daemon, socket, sessions, and
Application Support directory. Do not focus the same session in both apps
at different terminal sizes: each client can resize the shared PTY.

`cargo run -p taskmaster-app` from `taskmaster/` also launches a development build. Prefer
`dev.sh` when you need the signed bundle identity.

## Required checks

From the repository root, the CI-equivalent script is:

```sh
./scripts/check.sh
```

That runs the shell and release-publishing guards, then from `taskmaster/`:

```sh
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

Before a release-oriented handoff, also build the workspace in release mode:

```sh
(cd taskmaster && cargo build --workspace --release)
```

Remote Holder acceptance (`taskmaster/scripts/remote-acceptance.sh`) and the
disposable OpenSSH soak are release gates exercised in CI. They do not need
your personal SSH config. Real-host tests stay opt-in and must document
their environment variables and cleanup. See [Tests](testing.md).

## Website preview

The user guide and the playbooks are one static site under `/docs/`. Pages in
this directory stay Markdown on GitHub; they are not published.

```sh
cd website
npm test
npm run dev
```

User guide: <http://127.0.0.1:4177/docs/>. Playbooks:
<http://127.0.0.1:4177/docs/playbooks/>. `npm test` checks that every chapter
in `docs/src/SUMMARY.md` is published, that playbooks stay under that same
`/docs/` base, and that these developer pages are not emitted as site pages.
See [Documentation](documentation.md).
