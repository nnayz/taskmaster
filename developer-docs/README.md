# Developer Guide

Developer-facing documentation for Zeus. Built with
[mdBook](https://rust-lang.github.io/mdBook/) and published alongside the
[User Guide](../docs/) at `/docs/dev/` on the documentation site.

The User Guide (source: `docs/`) is for people using Zeus. This guide is for
people building, extending, or maintaining it. The full placement rules are in
[Writing documentation](src/writing-documentation.md).

```sh
# from the repository root
mdbook serve developer-docs --open   # http://localhost:3000
mdbook build developer-docs          # output in developer-docs/book/

# verify both guides and their cross-links
mdbook build docs
mdbook build developer-docs
python3 scripts/check-docs-links.py
```

Do not run `mdbook serve developer-docs` from inside `developer-docs/`; that
looks for `src/SUMMARY.md` under the current directory and fails.

## Contents

| Section | Source |
|---------|--------|
| Introduction | [`src/introduction.md`](src/introduction.md) |
| Development setup | [`src/setup.md`](src/setup.md) |
| Build and run | [`src/build-and-run.md`](src/build-and-run.md) |
| Required checks | [`src/required-checks.md`](src/required-checks.md) |
| Repository layout | [`src/repository-layout.md`](src/repository-layout.md) |
| How Zeus fits together | [`src/architecture.md`](src/architecture.md) |
| Remote transport | [`src/remote-transport.md`](src/remote-transport.md) |
| Companion architecture and trust model | [`src/companion-architecture.md`](src/companion-architecture.md) |
| Companion clients and prototypes | [`src/companion-clients.md`](src/companion-clients.md) |
| Agent manifests | [`src/agent-manifests.md`](src/agent-manifests.md) |
| MCP, hooks, and automation | [`src/mcp-and-hooks.md`](src/mcp-and-hooks.md) |
| Tests and fixtures | [`src/testing.md`](src/testing.md) |
| Screenshot soak test | [`src/screenshot-soak.md`](src/screenshot-soak.md) |
| Packaging | [`src/packaging.md`](src/packaging.md) |
| Releases and updates | [`src/releases-and-updates.md`](src/releases-and-updates.md) |
| Engineering documents | [`src/engineering-documents.md`](src/engineering-documents.md) |
| Writing documentation | [`src/writing-documentation.md`](src/writing-documentation.md) |

Canonical engineering documents remain authoritative in their repository
locations (`zeus/REMOTE_PORT.md`, `zeus/PACKAGING.md`, `zeus/UPDATING.md`, the
Companion records). This book links to them instead of copying them.
