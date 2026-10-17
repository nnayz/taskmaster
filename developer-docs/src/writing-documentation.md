# Writing documentation

Zeus has two documentation books and one rule: classify content by its
purpose.

| Guide | Source | Audience | Covers |
|-------|--------|----------|--------|
| User Guide | `docs/` | People using Zeus | Installing and using the product: workbench, agents, worktrees, orchestration, remote execution, Companion pairing, settings, privacy, support |
| Developer Guide | `developer-docs/` | People building or maintaining Zeus | Setup, checks, crate map, architecture pointers, manifests, MCP/hooks, testing, packaging, releases |

Canonical engineering documents (`zeus/REMOTE_PORT.md`,
`zeus/PACKAGING.md`, `zeus/UPDATING.md`, the Companion records) stay in their
repository locations. Both books link to them; neither keeps a second copy.
[Engineering documents](engineering-documents.md) is the index.

## Where new content goes

| Content | Belongs in |
|---------|------------|
| Installing, shortcuts, UI workflows, settings | User Guide |
| Task-oriented workflows and lessons from using Zeus | User Guide → Playbooks |
| CLI commands as used by operators and scripts | User Guide |
| Build, test, debug, and packaging instructions | Developer Guide |
| Crate and repository map, internal data flow | Developer Guide |
| Manifest schema, MCP bridge, hook wiring | Developer Guide |
| Architecture decisions and protocol contracts | The canonical repository document; link from the Developer Guide |
| Deferred or experimental features | Nowhere as a shipped feature; document them only where their gates live, and say what is not available |

A page that mixes audiences should be split, not duplicated: keep the
practical instructions where the audience already is, and move the technical
detail to the other guide with a deliberate cross-link in both directions.

Playbook pages state when the workflow is useful, prerequisites, concrete
steps, expected results, and common pitfalls, then link to the reference
pages. Keep tips in the workflow they belong to. Never describe unshipped
behavior as available.

## Building and previewing

```sh
mdbook serve docs --open             # User Guide  → http://localhost:3000
mdbook serve developer-docs --open   # Developer Guide
mdbook build docs
mdbook build developer-docs
```

Do not run `mdbook serve docs` from inside `docs/` or `docs/book/`; that
looks for `docs/src/SUMMARY.md` under the current directory and fails.

The published layout puts the User Guide at `/docs/` and the Developer Guide
at `/docs/dev/` on the same origin.

## Cross-guide links

Links between the books are relative paths between the published books:

- From the User Guide to the Developer Guide: `dev/<page>.html` — for
  example `dev/companion-architecture.html`.
- From the Developer Guide to the User Guide: `../<page>.html` — for example
  `../worktrees.html`.

Within a book, always use mdBook links (`page.md`, optionally with an anchor).
A single-book local preview cannot resolve the other guide's pages; the link
checker and the assembled Pages build verify them.

## Moving or renaming a page

1. Move the file and update `SUMMARY.md` and every inbound link (both books,
   the root README, repository documents, and the website).
2. If the page lived in the User Guide, leave a compatibility file at the old
   path — a small HTML page with a meta refresh and a visible link to the new
   location — so existing URLs keep working. `docs/src/companion-architecture.html`
   and `docs/src/screenshot-soak.html` are the current examples.
3. Run the link checker.

```sh
python3 scripts/check-docs-links.py                 # both book sources
python3 scripts/check-docs-links.py --site-build site/build   # assembled output
```

The checker validates that every internal link and asset resolves, that
fragments exist, and that compatibility redirects point at real pages.
Pages workflow runs it on the assembled site before upload.

## Website navigation

The marketing site links both guides through constants in
`site/src/lib/releases.ts` (`DOCS`, `DEVELOPER_DOCS`) and the header
navigation. Keep the labels "User Guide" and "Developer Guide" in sync with
this page when adding entries.
