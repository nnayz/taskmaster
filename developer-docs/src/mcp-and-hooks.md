# MCP, hooks, and automation

Hosted agent sessions — the ones Zeus launches from a manifest — receive a
per-session MCP overlay and (for CLIs that support them) hook configuration.
The agent sees a `zeus` server and can create child sessions, observe them,
answer prompts, and wait for results. A plain login shell started with `⌥⌘T`
does not get this server.

You do not configure MCP by hand for the default path. The manifest's
`injection` flags (`claudeHooks`, `claudeMCP`, and equivalents) decide what the
Engine writes for each launch. See [Agent manifests](agent-manifests.md).

The user-facing description of orchestration — what a lead can do, how to ask
for it, and what not to do — lives once in the User Guide:
[Orchestration](../orchestration.html) and
[Fleet patterns](../fleet.html).

## Where the pieces live

| Piece | Location |
|-------|----------|
| MCP server binary | `zeus/crates/zeus-mcp` — packaged beside the CLI as `zeus-mcp` |
| CLI bridge | `zeus/crates/zeus-cli/src/mcp.rs` — `zeus mcp-stdio` proxies stdio to the server binary |
| One-shot tool access | `zeus mcp-tools`, `zeus mcp-call --tool <name>` — same Engine control socket |
| Session injection | `zeus/crates/zeus-engine` writes the overlay at launch, honoring manifest `injection` |
| Hooks | `zeus hook <event>` (Claude hooks) and `zeus notify` (Codex notify), fail-open forwarders so those CLIs can poke Zeus |

Hook events are a status authority: manifests built on them trust the event
stream rather than screen scraping, while screen rules still provide the
fallback vocabulary. A hook or notify failure must never block the agent.

Tests covering the bridge and injection live in
`zeus/crates/zeus-engine/tests/mcp_tools.rs` and
`zeus/crates/zeus-engine/tests/inject_prompt.rs`. The opt-in live smoke test in
[Build and run](build-and-run.md#live-agent-smoke-test) exercises delegation
through a real hosted agent.

## Automation CLI

The `zeus` CLI exposes the same control surface to scripts: sessions,
worktrees, artifacts, ports, events, doctor, and the MCP commands above. The
command reference users see is documented once in the User Guide:
[Command line](../cli.html). Treat `zeus/crates/zeus-cli/src/args.rs` as the
authoritative command list, and `zeus/crates/zeus-cli/src/commands.rs` as the
implementation.
