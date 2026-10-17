# Zeus Developer Guide

This guide is for people who build, extend, or maintain Zeus: the Rust
workspace under `zeus/`, the macOS app it ships, the bootstrapped remote
Helper, and the Companion clients.

If you want to *use* Zeus — install it, run agents, review their work, use
remote hosts — read the [User Guide](../introduction.html) instead. The two
guides are published together: the User Guide covers the product, this guide
covers the codebase.

## Start here

1. [Development setup](setup.md) — prerequisites and a first checkout.
2. [Build and run](build-and-run.md) — development builds, previews, and
   watch mode.
3. [Required checks](required-checks.md) — the commands CI enforces and how
   to run them locally.
4. [Repository layout](repository-layout.md) — what lives where, including
   the crate map.

Then pick the area you are changing: [architecture](architecture.md),
[remote transport](remote-transport.md), the
[Companion](companion-architecture.md), or
[agent manifests](agent-manifests.md). [Engineering documents](engineering-documents.md)
indexes every canonical design record in the repository, including the ones
that are historical.

## What is in this guide

| Section | Covers |
|---------|--------|
| Getting started | Prerequisites, build, run, checks, repository map |
| Architecture | How the app, Engine, holders, and transports fit together |
| Agent integration | The manifest catalog, MCP, and hooks |
| Testing | The test suites, fixtures, and opt-in runs |
| Release engineering | Packaging, releases, and the updater |
| Reference | Canonical documents and documentation conventions |

## Ground rules

- The repository instructions in [`AGENTS.md`](https://github.com/nnayz/zeus/blob/main/AGENTS.md)
  (`.rules`) are binding for all changes. Read them before touching remote
  behavior, packaging, or the power tooling.
- Architecture decisions live in their canonical repository locations, not
  in this book. Pages here summarize and link; they do not define competing
  decisions. When implementation and `zeus/REMOTE_PORT.md` disagree, stop and
  resolve the mismatch instead of picking one silently.
- Never describe deferred or experimental work as shipped. Features under a
  release gate stay marked as such.
- Keep unrelated user changes intact.

## Working on this guide

The source for this book is [`developer-docs/`](https://github.com/nnayz/zeus/tree/main/developer-docs).
Build it with mdBook:

```sh
mdbook serve developer-docs --open
mdbook build developer-docs
```

See [Writing documentation](writing-documentation.md) for where future user
documentation and developer documentation belong, how cross-guide links work,
and how both books are checked in CI.
