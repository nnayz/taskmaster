# Agent manifests

Agent behavior is catalog data, not Engine code. Each CLI gets one JSON
manifest under `zeus/crates/zeus-engine/manifests/` describing how to spawn
it, how to resume it, which keys approve or deny a prompt, and the screen
rules that decide whether it is working, waiting, or done.

A missing manifest does not error at runtime — it silently downgrades that
agent to a bare login shell. **Never shrink the catalog.** The Engine test
suite loads the shipped directory and fails if any manifest stops decoding,
so a broken manifest is caught by `cargo test -p zeus-engine`.

## Schema

The authoritative schema is [`zeus/crates/zeus-engine/src/detect/manifest.rs`](https://github.com/nnayz/zeus/blob/main/zeus/crates/zeus-engine/src/detect/manifest.rs);
the field list here is orientation. Manifests are camelCase JSON, current
`schemaVersion` is `2`.

| Field | Meaning |
|-------|---------|
| `schemaVersion`, `id`, `version` | Identity and manifest revision. |
| `statusModel` | `full` (screen/hook rules produce the richest state) or `processOnly` (running/exited only). |
| `agent` | Launch descriptor: `binary`, `displayName`, `shortLabel`, `glyph`, `aliases`, `firstClass`, `setup` hints, `statusAuthority` (`hooks` or screen), `resume`, `env`, `envScrubPrefixes`, `approve`/`deny` keys, `attachments`, `injection` (`claudeHooks`/`claudeMCP`), `returnToLoginShell`. |
| `rules` | Detection rules, evaluated in descending `priority`; ties keep file order, and evaluation stops at the first match. |

A rule declares an `id`, the `state` it produces, a `priority`, the terminal
`region` it reads, a `when` predicate, optional `flags`, and an optional
`capture` for preserving prompt text.

- **States**: `working`, `idle`, `blockedPermission`, `blockedQuestion`, and
  `skip` (the screen shows a transient view; hold the current state instead of
  transitioning).
- **Regions**: `osc_title`, `osc_progress`, `whole_recent`, `prompt_box_body`,
  `bottom_non_empty_lines`.
- **Predicates**: case-insensitive `contains`, `regex`, `lineRegex`, OSC
  `progress`, and recursive `any` / `all` / `not`.
- **Capture**: pulls a bounded excerpt (default 400 characters) from a named
  region so the UI can show the actual blocker text.

Patterns compile once at load. If a predicate cannot name a blocker, Zeus does
not invent one: a lying spinner is worse than a quiet row.

## Adding an agent

1. Copy the closest existing manifest under
   `zeus/crates/zeus-engine/manifests/` and change `id`, `version`, and the
   `agent` descriptor.
2. Declare the launch contract: `binary`, package-install hint, sign-in hint,
   `resume` style, approval/denial keys, and whether the CLI needs the login
   shell wrapper.
3. Add the smallest set of detection rules that produces honest states. Prefer
   high-priority `skip` rules for transient screens over guessing.
4. Run `cargo test -p zeus-engine` (the whole catalog is decoded) and launch
   the CLI from the app to verify status transitions.
5. You do not need Engine code for a new catalog entry, and you never remove
   an existing one.

`injection` decides whether Zeus writes a per-session MCP overlay and Claude
hook configuration for the CLI. See [MCP, hooks, and automation](mcp-and-hooks.md).

## User-facing reference

The status vocabulary users see (`Working`, `Needs input`, `Done`, `Idle`,
`Hibernated`, `Ended`) and what each means is documented once in the User
Guide: [Agents and status](../agents.html). Keep that page and the manifests
consistent when you change detection behavior.
