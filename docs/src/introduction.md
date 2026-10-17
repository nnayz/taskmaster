# Zeus

<img src="images/zeus-logo.svg" alt="Zeus" width="160">

Native macOS control plane for coding agents. Run Claude Code, Codex, Cursor,
Grok, OpenCode, Gemini, and a catalog of other CLIs in parallel, locally or
over SSH. Each session is a real PTY with a live status (working, needs you,
done). Closing the window never kills an agent. A daemon restart brings the
conversations back.

Zeus is not an IDE and not a model. It is the place you watch a fleet, jump
to the session that is stuck, and accept the work.

## Install

Zeus requires macOS 15 or newer. Download the current universal DMG from
[Releases](https://github.com/nnayz/zeus/releases/latest), drag Zeus to
Applications, then complete the one-time Gatekeeper exception. The current
release is ad-hoc signed and is not available through Homebrew.

See [Getting started](getting-started.md) or the
[illustrated macOS install guide](https://nnayz.github.io/zeus/install/) for
the complete installation flow.

## In this book

| Section | What it covers |
|---------|----------------|
| [Getting started](getting-started.md) | First project, first session, first quit |
| [The workbench](workbench.md) | Sidebar, panel tabs, terminal, overview |
| [Keyboard](keyboard.md) | Every shortcut that matters |
| [Agents and status](agents.md) | Catalog, resume, what the colors mean |
| [Worktrees](worktrees.md) | Isolated checkouts for parallel edits |
| [Orchestration](orchestration.md) | MCP spawn, wait, prompt, read |
| [Fleet patterns](fleet.md) | Ways to run more agents than you can watch |
| [Settings](settings.md) | Defaults, layout, hibernate, hosts |
| [Command line](cli.md) | `zeus session`, worktrees, doctor |
| [Remote hosts](remote-hosts.md) | SSH machines in Settings → Remote |
| [Remote nodes](remote-nodes.md) | First-party `zeus-node` on a VPS |
| [Updates](updates.md) | How auto-update works |
| [Playbooks](playbooks/parallel-agents-worktrees.md) | Concrete workflows: parallel worktrees, delegation, review, local vs remote, blocked sessions, resources |
| [Security model](security-model.md) | Trust boundaries |
| [Privacy](privacy.md) | Local data and network activity |
| [Support](support.md) | Diagnostics and logs |
| [Roadmap](roadmap.md) | Product direction |

## This book and the Developer Guide

This is the **User Guide**: how to install, run, and operate Zeus. Building
Zeus from source, the crate map, agent manifests, protocols, tests, packaging,
and release engineering are covered separately in the
[Developer Guide](dev/introduction.html). Content moves between the two guides
by audience, so links to moved pages continue to work.
