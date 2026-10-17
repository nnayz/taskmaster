# Diagnosing a session that is waiting for permission or a response

**When this is useful.** A session looks stuck. It may be genuinely working,
or it may be blocked on a permission prompt, a question, or a confirm — which
is exactly what Zeus's status vocabulary is for.

**Prerequisites.**

- Know the status vocabulary: **Working**, **Needs input** (blocked on you),
  **Done**, **Idle**, **Hibernated**, **Ended**. See
  [Agents and status](../agents.md).
- Claude Code and Codex have the richest blocker detection (permission,
  question, captured prompt text). Other catalog agents report what their
  manifest can name; if Zeus cannot name a blocker it will not invent one.

## Steps

1. **Find who needs you.** The sidebar row shows the state; the menu bar
   extra counts sessions that need input without stealing focus; optional
   chimes (Settings → General) stay quiet on mere token activity.
   `⌘⇧J` jumps to the next blocked session.
2. **Read the blocker before touching it.** The row and the session briefing
   tell you whether it is a permission, a question, or a confirmation.
   Destructive permission prompts get a sharper color.
3. **Open the session and answer in its terminal.** That is the source of
   truth: read the actual prompt text and reply there (for example `1` to
   approve, `Esc` to deny for Claude-style prompts). Do not approve a
   destructive action you have not read.
4. **Check line endings of the situation first**: is the PTY waiting for
   input, or is the agent still working? A spinner that lies is worse than a
   quiet row, so if the state looks wrong for a while, read the terminal
   yourself before retrying.
5. **For children, use the tree.** A blocked child nests under its lead.
   Answer it directly, or tell the lead to forward the answer.
6. **Scripted checks.** Outside the app:

   ```sh
   zeus session list --all        # status including needs-input detail
   zeus session read <id> --source scrollback --lines 80
   zeus session send <id> "yes, run the tests"
   ```

   An MCP-driven lead can do the same with `get_status`, `read_output`, and
   `send_prompt`.

## Expected results

- Answering the prompt clears the blocker: the row returns to **Working** and
  the blocking state disappears.
- If the agent exits instead, the row shows **Ended** and (for agents that
  support it) offers a resume path.
- Nothing is auto-approved on your behalf. Automated flows (`⌘⇧J`, chimes,
  MCP) route to the session; they do not answer for you.

## Pitfalls

- **Do not paste answers into the wrong session.** `⌘⇧J` changes selection;
  confirm the title before typing.
- **Never approve a destructive prompt just to clear the queue.** Deny and
  ask the agent for a safer plan.
- **Plain shells only report running/exited.** A `⌥⌘T` terminal does not have
  agent status rules, so its silence means nothing about a blocked prompt.
- **A missing manifest silently downgrades an agent to a plain shell.** If an
  agent never reports blockers, check that its catalog entry exists.
- **Resume is agent-specific.** Trust Claude Code and Codex resume; others
  may come back as a fresh CLI in the same folder.

## Related

- [Agents and status](../agents.md)
- [Keyboard](../keyboard.md)
- [Orchestration](../orchestration.md)
- [Command line](../cli.md)
