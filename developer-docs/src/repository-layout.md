# Repository layout

Zeus is a monorepo. One checkout contains the Rust workspace, the iOS client,
both documentation books, the website, and the release automation.

| Path | Contents |
|------|----------|
| `zeus/` | The Rust workspace: desktop app, Engine, holders, CLI, transports, and tooling. Most development happens here. |
| `ios/ZeusCompanion/` | Native SwiftUI Companion client. A client of the versioned HTTPS API — it never embeds an Engine, executes SSH, or owns sessions. |
| `docs/` | User Guide source (mdBook). Entry point for people using Zeus. |
| `developer-docs/` | Developer Guide source (mdBook) — this book. |
| `site/` | SvelteKit marketing site. Serves the install guide, release notes, and links to both books. |
| `prototypes/companion-web/` | Browser prototype for the Companion API. Development tooling, never shipped. |
| `sidecar/` | Browser-automation sidecar used by the browser panel. |
| `scripts/` | Repository-wide scripts: `check.sh`, the docs link checker, the dev signing helper, `companion-dev.sh`. |
| `Casks/` | The monorepo Homebrew tap (`zeus.rb`). |
| `.github/workflows/` | CI, CodeQL, dependency review, and Pages publishing. |
| Root documents | Repository instructions (`AGENTS.md`/`.rules`), `SECURITY.md`, `PRIVACY.md`, `SUPPORT.md`, `DESIGN.md`, `LICENSE`, `NOTICE`. |

## Rust workspace map

All crates live under `zeus/crates/`. The Engine's workspace is authoritative;
this table is orientation, not a dependency specification.

| Crate | Responsibility |
|-------|----------------|
| `zeus-app` | GPUI desktop UI: workbench, terminal, sidebar, inspector, palette, review surfaces. Requests remote actions through the local Engine. |
| `zeus-engine` | Authoritative local session engine: PTY/holder lifecycle, status reduction, host orchestration, remote bootstrap/SSH seam. Also ships the [agent manifest catalog](#agent-catalog). |
| `zeus-client` | Local app-to-engine client. Does not execute SSH directly. |
| `zeus-proto` | Shared data models and wire codecs. `remote_pty` is the authoritative versioned Remote Helper protocol. |
| `zeus-remote` | Minimal remote Helper binary. Independent of GPUI, `zeus-app`, `zeus-client`, and `zeus-node`. One Holder per remote session. |
| `zeus-terminal-state` | Headless terminal parser, grid, snapshot, and diff shared by the local Engine and the remote Holder. |
| `zeus-term` | GPUI terminal renderer and client-side terminal interaction. |
| `zeus-pty` | Cross-process PTY ownership shared by local and remote holders. Children receive an exact argv/environment/cwd tuple; the parent environment is never inherited implicitly. |
| `zeus-cli` | The shipped `zeus` automation CLI: hooks, notifications, MCP backend, session and worktree commands. |
| `zeus-mcp` | MCP server and bridge used to expose Zeus tools to hosted agents. |
| `zeus-node` | Optional enhanced node mode: per-node accounts, usage, and handoff. Not a dependency of the default SSH bootstrap path. |
| `zeus-ui` | Shared GPUI design system: tokens, brand marks, status behavior. |
| `zeus-usage` | Shared API-equivalent pricing and usage accounting. Estimates, never authoritative provider billing. |
| `zeus-updater` | The self-updater: download, verify, stage, and relaunch. |
| `zeus-companion` | Engine-launched Rust Companion gateway sidecar. |
| `zeus-companion-api` | Curated external v1 DTOs. No dependency on the Engine wire model. |
| `zeus-companion-client` | Typed, bounded Companion reference client. |
| `zeus-power` / `zeus-power-helper` | Platform-neutral policy core and the inert package contract for the gated closed-lid power exploration (#70). Ordinary builds report the helper unavailable. |

Two pins matter when you touch builds:

- **Toolchain**: [`zeus/rust-toolchain.toml`](https://github.com/nnayz/zeus/blob/main/zeus/rust-toolchain.toml)
  pins the channel and components. The workspace declares `edition = "2024"`.
- **GPUI**: compiled from an exact Zed revision recorded in
  [`zeus/README.md`](https://github.com/nnayz/zeus/blob/main/zeus/README.md).
  Upgrade it deliberately and update the record.

## Agent catalog

`zeus/crates/zeus-engine/manifests/` is the Agent catalog: one JSON manifest
per CLI. A missing manifest does not error at runtime — it silently downgrades
that agent to a bare login shell, so **never shrink the catalog**. Supporting
an agent is a data change; see [Agent manifests](agent-manifests.md).

## Tests

Rust tests live beside the crates (`#[cfg(test)]`) and in `zeus/crates/*/tests/`
integration targets. Repository-wide scripts under `zeus/scripts/` exercise the
remote transport, packaging, and release guards. The documentation checker is
`scripts/check-docs-links.py`. See [Tests and fixtures](testing.md).

## Repository instructions

[`AGENTS.md`](https://github.com/nnayz/zeus/blob/main/AGENTS.md) (and `.rules`)
is the binding instruction set for the whole repository: remote architecture
invariants, security rules, build commands, and change discipline. Read it
before changing remote behavior, packaging, or anything privileged.
