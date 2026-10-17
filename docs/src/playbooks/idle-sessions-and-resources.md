# Managing idle sessions and resource limits

**When this is useful.** You keep a large fleet open, run overnight, or notice
the laptop getting warm. Zeus does not require killing sessions to save
memory, and archiving is for history, not for freeing a process.

**Prerequisites.**

- Access to Settings → Resources (`⌘,`).
- A rough sense of which sessions are finished and which might resume later.

## Steps

1. **Choose a hibernate policy.** Settings → **Resources** → **Hibernate idle
   sessions**: Off, 5 minutes, 15 (default), 30, or 1 hour. An idle session
   is frozen, not killed.
2. **Set a memory limit.** The same tab caps each session at 2, 4, 6
   (default), or 8 GB. Crossing the limit freezes that session the same way.
   Gentle status chimes (Settings → General) include memory pauses.
3. **Wake a frozen session by opening it.** It comes back as the same process
   at the same screen — hibernation is not a restart.
4. **Archive what you are done with.** `⌘⇧W` moves a session row into its
   project's archive group. Archived rows stay as history; they are not the
   resume path.
5. **Release a process you really want ended.** Use the session's release or
   close action (with the confirm setting respected), or the CLI:

   ```sh
   zeus session archive <id>            # history, row kept
   zeus session release <id>            # kill the process tree, keep the row
   zeus session release <id> --remove   # kill and remove the row
   ```

6. **Clean the apartments, not the residents.** `⌥⌘W` opens the worktrees
   sheet; remove stale trees after committing or moving changes. Zeus only
   suggests stale, clean, non-`main` trees through the UI.
7. **Check usage where it lives.** Installation-level usage is in the account
   menu at the sidebar footer; Details only shows usage Zeus can attribute to
   the selected session.

## Expected results

- Frozen sessions stop consuming their memory budget but keep their process
  and screen; their rows show **Hibernated** until opened.
- Archived sessions remain searchable history without appearing in the
  active list.
- The fleet stays responsive at a smaller memory footprint, including
  overnight with the app closed.

## Pitfalls

- **Hibernation is not termination.** If you need the process gone, release
  it; if you need it later, do not release it.
- **Archive is not delete, and not resume.** Do not archive something you
  intend to continue; select it and keep working instead.
- **Session limits are per session**, not a fleet-wide budget. A dozen
  sessions each under the cap can still add up.
- **Freezing is not a checkpoint.** Checkpoints stay a cache; the same
  process is what wakes.
- **Do not force-remove a dirty worktree.** Commit or move the changes first;
  the CLI's `--force` is a last resort.

## Related

- [Settings](../settings.md)
- [The workbench](../workbench.md)
- [Agents and status](../agents.md)
- [Command line](../cli.md)
