# Companion clients

People pairing a phone and driving a session should follow the User Guide
[iOS Companion](../../src/ios-companion.md) page. The trust decision and external
API shape are [Companion architecture and trust model](companion-architecture.md)
in this book. Do not fork that decision into a client README.

## What a client is allowed to be

A Companion client talks to the Engine-launched Rust gateway over HTTPS.
It does not embed an Engine, open SSH, attach to a Holder, or ship a Swift
daemon or CLI. `remote_pty` is the Engine-to-Helper protocol. Phones do not
speak it.

| Piece | Role | Start at |
|-------|------|----------|
| Gateway | Opt-in Engine child. Device credentials, HTTP admission, curated DTOs | [`taskmaster/COMPANION_GATEWAY.md`](https://github.com/nnayz/taskmaster/blob/main/taskmaster/COMPANION_GATEWAY.md) |
| Terminal v1 | Read-only snapshots and explicit commands. Not a raw mobile PTY | [`taskmaster/COMPANION_TERMINAL.md`](https://github.com/nnayz/taskmaster/blob/main/taskmaster/COMPANION_TERMINAL.md) |
| External types | Versioned API crate | `taskmaster/crates/taskmaster-companion-api` |
| iOS app | SwiftUI client in this repo | [`ios/TaskmasterCompanion/README.md`](https://github.com/nnayz/taskmaster/blob/main/ios/TaskmasterCompanion/README.md) |
| Web prototype | Synthetic loopback fixture for the curated API. Not the gateway | [`prototypes/companion-web/README.md`](https://github.com/nnayz/taskmaster/blob/main/prototypes/companion-web/README.md) |

The iOS README's local testing gateway is `./scripts/companion-dev.sh` from
`ios/TaskmasterCompanion/`. It is a development stand-in. It is not the production
listener policy in the architecture page.

The web prototype's `npm test` is a CI job (`companion-web` in
`.github/workflows/ci.yml`). Those tests do not start Taskmaster.

Native iOS stores the bearer token in Keychain. Do not put tokens in URLs,
logs, UserDefaults, or WebSocket query parameters. The in-repo web prototype
keeps tokens in memory and re-pairs after reload.
