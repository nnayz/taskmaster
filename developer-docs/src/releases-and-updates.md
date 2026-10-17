# Releases and updates

Two documents own this area:

- [`zeus/UPDATING.md`](https://github.com/nnayz/zeus/blob/main/zeus/UPDATING.md)
  — the release packaging and updater implementation reference.
- [`zeus/PACKAGING.md`](https://github.com/nnayz/zeus/blob/main/zeus/PACKAGING.md)
  — bundle assembly and signing.

What users see is documented once in the User Guide:
[Updates](../updates.html).

## The updater

Zeus updates itself without Sparkle. The Rust
[`zeus-updater`](https://github.com/nnayz/zeus/tree/main/zeus/crates/zeus-updater)
crate reads a JSON feed published with each GitHub Release and stages a
verified bundle under `~/Library/Caches/zeus/updates/<version>/`. A download is
accepted only when the code signature verifies, the Team ID and bundle
identifier match the running app, notarization is accepted without a network
round trip, and the version is strictly newer. Checks are automatic; applying
an update always waits for a click.

The feed URL is stable and versioned by the release host, not by the app.
Changes to the feed shape, verification order, or staging layout belong in
`zeus/UPDATING.md` first.

## Release automation

| Script | Purpose |
|--------|---------|
| `zeus/scripts/release.sh` | Assemble, sign, notarize, and publish a release |
| `zeus/scripts/publish-github-release.sh` | Upload release assets and the appcast feed |
| `zeus/scripts/publish-homebrew-cask.sh` | Update the monorepo cask |
| `zeus/scripts/test-publish-github-release.sh`, `test-publish-homebrew-cask.sh` | Guard tests for the publishing path, run in CI |

The Homebrew cask lives at `Casks/zeus.rb` in this repository (a monorepo tap)
and declares `auto_updates true`: Homebrew installs Zeus once and the app
updates itself afterwards.

Published release assets are treated as immutable. Only release operators with
the GitHub and Apple credentials can publish; protect those credentials as
production secrets, and never log credentials, signatures, or full
authentication responses from the release path.

## Release gates

Signing, notarization, and the update feed are release gates, not
conveniences. The same applies to the remote Helper artifacts: CI must
execute `zeus-remote probe` on every supported target and produce the exact
nested-code layout for the packaged helpers before a release is valid.
