# Delegating a task and following parent/child sessions

**When this is useful.** You want one agent to coordinate work instead of
typing every prompt yourself: a lead that spawns an implementer and a
reviewer, waits for them, and reports back. Delegated sessions appear in the
sidebar as real Zeus sessions nested under their parent, each with its own
terminal and Review diff.

**Prerequisites.**

- A hosted agent session — Claude Code, Codex, Grok, OpenCode, Gemini, or
  Cursor launched from Zeus. Hosted sessions get the `zeus` MCP server
  automatically; a plain shell (`⌥⌘T`) does not.
- The agent and its account are set up. See [Agents and status](../agents.md).

## Steps

1. **Start the lead.** `⌘T` launches your default agent; `⌘N` lets you pick a
   different kind and name it (`lead`) with an opening prompt.
2. **Describe the outcome, the constraints, and the stopping point.** Ask it
   to spawn specialists in worktrees rather than touching `main`, and to stop
   at a reviewable point instead of merging:

   > Spawn a Codex in a fresh worktree on the auth rewrite. Wait until it is
   > done or needs me. If it asks for a destructive permission, ping me
   > instead of approving. Then spawn a second Codex to review the diff and
   > stop at a PR description. Do not merge.

3. **Watch the sidebar.** Each child appears nested under the lead as soon as
   it is created. Expand or collapse a lead to control the noise.
4. **Let the lead wait and collect.** It can wait for a child to finish or
   need input, read its output, and summarize; the assignment is delivered
   once the child can accept text.
5. **Answer whoever is blocked.** `⌘⇧J` lands on the next session that needs
   input. You can answer in that child's terminal directly, or tell the lead
   to forward the answer with MCP.
6. **Read the briefing, then review.** When the lead reports done, open
   **Review** on the implementing session's worktree before accepting
   anything.

## Expected results

- Child sessions have their own sidebar rows, terminals, status, and Review
  diffs; lineage stays visible after the parent goes idle.
- The lead can pause on children with a timeout, then read output and report
  what actually happened.
- Children survive like any other session: quitting Zeus does not kill them.

## Pitfalls

- **Codex's built-in subagents stay inside one PTY.** While Zeus hosts Codex,
  its own multi-agent spawn is turned off on purpose; only Zeus-spawned
  children get sidebar rows and review surfaces.
- **A local lead cannot MCP-spawn onto a remote host yet.** Start remote
  sessions from the palette or `zeus session spawn --host`, and orchestrate
  children on that same machine.
- **Do not approve destructive permissions on autopilot.** Tell the lead to
  escalate instead.
- **Read before you trust.** A quiet PTY is not a passing test; ask the lead
  to read a child's output and report evidence.
- **Do not skip Review.** Orchestration without an accept step is just more
  unmerged branches.

## Related

- [Orchestration](../orchestration.md)
- [Fleet patterns](../fleet.md)
- [Worktrees](../worktrees.md)
- [Command line](../cli.md)
