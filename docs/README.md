# Documentation

Zeus documentation is split by audience into two [mdBook](https://rust-lang.github.io/mdBook/)
sources, published together on the documentation site:

| Guide | Source | Audience | Published at |
|-------|--------|----------|--------------|
| User Guide | `docs/` | People using Zeus | `/docs/` |
| Developer Guide | [`developer-docs/`](../developer-docs/) | People building, extending, or maintaining Zeus | `/docs/dev/` |

Canonical engineering documents (`zeus/REMOTE_PORT.md`, `zeus/PACKAGING.md`,
`zeus/UPDATING.md`, the Companion records) stay next to the code and are
linked from the Developer Guide's
[Engineering documents](../developer-docs/src/engineering-documents.md) index.
Neither book keeps a competing copy.

## Build and preview

```sh
# from the repository root
mdbook serve docs --open             # User Guide  → http://localhost:3000
mdbook serve developer-docs --open   # Developer Guide
mdbook build docs                    # output in docs/book/
mdbook build developer-docs          # output in developer-docs/book/
```

Install mdBook with `cargo install mdbook --locked` or `brew install mdbook`.

If your shell is already in a book directory, drop the extra path:

```sh
cd docs
mdbook serve --open
```

Do not run `mdbook serve docs` from `docs/` or `docs/book/`. That looks for
`docs/src/SUMMARY.md` under the current directory and fails.

## Check links and assets

```sh
python3 scripts/check-docs-links.py                  # both sources
mdbook build docs && mdbook build developer-docs
python3 scripts/check-docs-links.py --site-build site/build   # assembled output
```

The checker validates internal links, anchors, images, and the compatibility
redirects. The Pages workflow runs it on the assembled site before upload.

## User Guide contents

| Book page | Source |
|-----------|--------|
| Introduction | [`src/introduction.md`](src/introduction.md) |
| Getting started | [`src/getting-started.md`](src/getting-started.md) |
| The workbench | [`src/workbench.md`](src/workbench.md) |
| Keyboard | [`src/keyboard.md`](src/keyboard.md) |
| Agents and status | [`src/agents.md`](src/agents.md) |
| Worktrees | [`src/worktrees.md`](src/worktrees.md) |
| Orchestration | [`src/orchestration.md`](src/orchestration.md) |
| Fleet patterns | [`src/fleet.md`](src/fleet.md) |
| Settings | [`src/settings.md`](src/settings.md) |
| Command line | [`src/cli.md`](src/cli.md) |
| Remote hosts | [`src/remote-hosts.md`](src/remote-hosts.md) |
| Remote nodes | [`src/remote-nodes.md`](src/remote-nodes.md) |
| iOS Companion | [`src/ios-companion.md`](src/ios-companion.md) |
| Updates | [`src/updates.md`](src/updates.md) |
| Playbooks | [`src/playbooks/`](src/playbooks/) |
| Security model | [`src/security-model.md`](src/security-model.md) |
| Security policy | [`src/security-policy.md`](src/security-policy.md) |
| Privacy | [`src/privacy.md`](src/privacy.md) |
| Support | [`src/support.md`](src/support.md) |
| Roadmap | [`src/roadmap.md`](src/roadmap.md) |

## Where new documentation goes

- **Using Zeus** → User Guide. Task-oriented workflows belong in the
  [Playbooks](src/playbooks/) section.
- **Building or maintaining Zeus** → Developer Guide, whose
  [Writing documentation](../developer-docs/src/writing-documentation.md)
  page has the full placement rules, cross-guide link convention, and the
  page-move/redirect policy.
- **Architecture decisions and protocol contracts** → their canonical
  repository location next to the code; link them from the Developer Guide.

## Moved pages

Pages that moved from the User Guide to the Developer Guide leave a
compatibility file at the old path (a meta refresh plus a visible link), so
existing URLs keep working:

- `src/companion-architecture.html` → Developer Guide
- `src/screenshot-soak.html` → Developer Guide
