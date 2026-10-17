# Running parallel agents in separate worktrees

**When this is useful.** You want two or more agents writing code in the same
project at the same time — an implementer and a reviewer, or three competing
approaches. Giving each writer its own Git worktree keeps them from
overwriting each other.

**Prerequisites.**

- A local project open in Zeus (`⌘O` or `⌘P`).
- The project is a Git repository.
- The agent CLIs you want are installed and signed in; Zeus does not install
  them. See [Agents and status](../agents.md).

## Steps

1. **Create the session with a worktree.** Press `⌘N` to open the New Agent
   composer, pick the agent, then toggle the folder control from **Checkout**
   to **Worktree** and optionally name the branch. The toggle is unavailable
   for remote hosts: worktrees are local only.
2. **Name the session after the bet** (`auth-rewrite`, `reviewer`, `spike-cache`)
   so the sidebar reads like a board instead of a list of "Claude Code".
3. **Send the assignment.** Two agents in the same checkout will fight over
   files; two worktrees will not. If a child only needs to read the parent's
   files (a shell running tests), share the checkout instead.
4. **Launch the second writer the same way.** Each session row in the sidebar
   is bound to its own directory.
5. **Watch the fleet, not the terminals.** `⌘⇧J` jumps to the next session
   blocked on input, `⌘⇧O` shows the session overview, and the menu bar extra
   counts who needs you.
6. **Review each tree separately.** Select a session and open **Review**
   (`⌘⇧D`): it is bound to that session's working directory, so you are
   looking at that agent's branch, not `main`.
7. **Clean up deliberately.** `⌥⌘W` opens the worktrees sheet. Zeus suggests
   cleanup only for trees it believes are stale (old, merged, clean, not
   `main`), and always asks for confirmation.

You can also create worktrees without the UI:

```sh
zeus worktree create --repo ~/src/mldrills --branch spike-auth
zeus session spawn claude-code --cwd ~/src/mldrills --worktree \
  --prompt "own the auth rewrite"
```

## Expected results

- The worktrees sheet (`⌥⌘W`) lists one tree per writing session, with path,
  branch, owner, and dirty state.
- Each session's **Review** tab shows the diff for its own tree.
- Deleting a tree from the sheet is blocked while it is dirty, unmerged, or
  on `main`.

## Pitfalls

- **A worktree is not a sandbox.** It prevents edit collisions, not access.
  Agents still run with your user account and credentials.
- **Commit or move changes before deleting a tree.** Cleanup is destructive;
  the sheet will not force-remove a dirty tree, and the CLI's `--force` is for
  when you know exactly what you are doing.
- **Do not create a worktree per prompt.** Reuse a tree for related work;
  every new tree is a new branch to babysit.
- **Remote sessions do not get local worktrees.** Spawn remote workers from
  the palette or `zeus session spawn --host`, then orchestrate children on
  that machine.

## Related

- [Worktrees](../worktrees.md)
- [Fleet patterns](../fleet.md)
- [Orchestration](../orchestration.md)
- [Command line](../cli.md)
