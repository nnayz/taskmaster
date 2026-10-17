# Packaging

[`zeus/PACKAGING.md`](https://github.com/nnayz/zeus/blob/main/zeus/PACKAGING.md)
is the authoritative packaging reference. This page summarizes what it covers
so you know when to go read it.

`zeus/scripts/package.sh` builds the desktop app for Apple silicon and Intel,
combines the slices with `lipo`, asks cargo-packager to assemble
`dist/zeus.app`, and signs the result. The bundle identifier is
`com.zeus.zeus`, the deployment target is macOS 15.0, and the app does not use
App Sandbox.

## One-time setup

```sh
rustup target add aarch64-apple-darwin x86_64-apple-darwin \
    aarch64-unknown-linux-musl x86_64-unknown-linux-musl
cargo install cargo-packager --locked
brew install zig
cargo install cargo-zigbuild --locked
```

The universal targets must be installed for the toolchain that `zeus/` pins,
not the runner default; the bundle CI job repeats this explicitly.

## What the bundle carries

The app is self-contained. CI verifies that a packaged `zeus.app` contains the
executables, resources, and helper layout the runtime expects (see the
Package zeus.app job in [Required checks](required-checks.md)):

- `zeus`, `zeus-mcp`, `zeusd-rs`, `zeus-holder`, and `zeus-ssh-askpass`
  binaries, universal.
- The agent manifest catalog under `Contents/Resources/bin/manifests/`.
- Remote Helper artifacts (`remote-helpers/manifest.json` plus the exact
  per-target binaries).
- The inert power-helper scaffold: present and signed, but reporting
  `power_helper_unavailable` until the issue #70 release gates pass.

## Icons and assets

The app uses a layered Icon Composer icon with an ICNS fallback. See
[`zeus/assets/icon-assets/README.md`](https://github.com/nnayz/zeus/blob/main/zeus/assets/icon-assets/README.md)
when changing artwork; release and development bundles install their matching
icon resources before signing. The committed `assets/icon.icns` is rasterized
from `docs/src/images/zeus-logo.svg`.

## Local install

```sh
zeus/scripts/package.sh          # assemble the application bundle
zeus/scripts/install-local.sh    # install that local bundle
```

Release assembly, signing, notarization, and publishing live in
`zeus/scripts/release.sh` and the publish scripts; see
[Releases and updates](releases-and-updates.md).
