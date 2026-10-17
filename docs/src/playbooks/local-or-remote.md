# Choosing local or remote execution

**When this is useful.** You are deciding where a session should run, or you
came back to the laptop and want to know whether the work survived. The short
rule: run agents where they should outlive your window; review where the glass
is best.

**Prerequisites.**

- **Local:** macOS 15 or newer.
- **Remote:** an SSH-reachable machine you can log in to, ideally with a
  dedicated non-admin account, and an entry under Settings → Remote.

## Steps

### Run locally

1. `⌘T` starts your default agent in the current project; `⌘N` picks a
   different kind. Local is the best default for tight edit/review loops.
2. Sessions belong to the background Engine, not the window: `⌘Q` and reopen
   keeps the process and its scrollback alive.

### Run on a host

1. Press `⌘,` → **Remote** and add the host: name, SSH destination (or an
   `~/.ssh/config` alias), and a default working directory. Save.
2. Open `⌘K` and type the host name — **New Codex on Forge**, or whichever
   agent you want — to spawn there. Status, hibernate, Review, and grouping
   behave like local sessions.
3. The first connection bootstraps a small Helper on the host; there is no
   `tmux`, Node.js, Python, or preinstalled Zeus service to maintain.
4. To move an existing **Claude** session between hosts, use **Move Session
   to …** in the palette. It is Claude-only in this version because resume has
   to be trustworthy.

### Reconnect

1. Reopen Zeus after quitting — local and remote sessions are still listed
   with their state.
2. Select the session. Local sessions replay their holder's PTY. Remote
   sessions reconnect to the remote Helper that owns the PTY.
3. Open **Details** to see the session briefing, including whether a remote
   process can survive disconnect.

## Expected results

- Local and remote sessions share the same sidebar, status vocabulary, and
  review surfaces.
- A remote session keeps running when your window or connection drops, as
  long as the host's persistence situation allows it; Details reports what it
  knows.
- A failed or unverifiable Helper never silently falls back to another
  transport: Zeus reports a structured error instead.

## Pitfalls

- **Do not treat remote as a sandbox.** Sessions run under a real account
  with that machine's credentials. Prefer a non-admin user and narrowly
  scoped keys.
- **A laptop lead cannot MCP-spawn onto a host yet.** Start remote workers
  from the palette or `zeus session spawn --host`, then orchestrate children
  on that machine.
- **SSH prompts**: password and host-key prompts appear through Zeus's
  askpass helper; they are not scraped from the protocol.
- **Host unreachable?** Local sessions and local numbers never block on it.
  Check the host entry and try again.
- **Remote files are not indexed locally.** Quick Open and the Files tab do
  not browse a remote filesystem; review happens through the terminal and the
  Review surface.

## Related

- [Remote hosts](../remote-hosts.md)
- [Remote nodes](../remote-nodes.md)
- [Settings](../settings.md)
- [Agents and status](../agents.md)
