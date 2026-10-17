# Reviewing an agent's changes and opening a pull request

**When this is useful.** An agent says it is done. Before you accept the work,
read the diff in the same window you used to watch it, then publish the change
as a pull request when it stands up.

**Prerequisites.**

- The session is a local session whose working directory is the repository or
  worktree you want to review. A worktree session reviews *that* branch, not
  `main`.
- For pull requests: the repository has a remote, and either the agent can
  push (`git` credentials available) or you have `gh` configured.

## Steps

1. **Confirm you are on the right tree.** Select the session, press `⌘⇧D` if
   the panel is closed, and open the **Review** tab. The header names the
   repository and branch; the diff is bound to the session's working
   directory.
2. **Read the change.** Stage nothing yet: **Stage** and **Commit** apply to
   the working tree when you decide. Use **Files** to browse or open files,
   and **Branches…** to compare against another ref without checking it out.
3. **Check the surrounding context in a shell.** `⌘J` opens an auxiliary
   login shell under the session — run tests, `git log`, or `git diff --stat`
   there without stealing the agent's PTY.
4. **If a pull request already exists**, use **Go to Pull Request…** (Review
   header or `⌘K`) and paste `#123` or a URL. Opening a PR head uses an
   isolated worktree.
5. **If it does not**, ask the agent to open one, or do it yourself in the
   `⌘J` shell:

   ```sh
   git status
   git add -A && git commit -m "auth rewrite"
   git push -u origin HEAD
   gh pr create --fill
   ```

6. **Record the outcome.** The **Details** tab keeps the session briefing
   (kind, host, lifecycle, links to pull requests) without mutating the
   repository; the Review tab is where changes actually happen.
7. **Archive when done.** `⌘⇧W` archives the session as history, and `⌥⌘W`
   lets you clean up the worktree once the change is merged.

## Expected results

- Review shows exactly the working tree you picked, with staged, unstaged,
  rename, conflict, and untracked status.
- Committing from Review or the auxiliary shell leaves the agent's session
  running; the agent can continue from the new commit.
- A PR opened from the branch is visible through **Go to Pull Request…**, and
  Details can summarize it.

## Pitfalls

- **Reviewing the wrong worktree.** If the session's cwd is a worktree, the
  diff is that branch. Use **Branches…** deliberately instead of assuming
  `main`.
- **Remote sessions are view-only in Files.** Their files are not browsed
  through the local filesystem, and Quick Open does not index them.
- **Details does not mutate anything.** It summarizes; do not look for
  stage/commit there.
- **Closing an edited file asks you to save or revert.** Terminal tabs stay
  running when closed, but file tabs do not silently drop changes.
- **Do not merge from a confused state.** If the diff does not match what the
  agent described, ask it to explain before committing.

## Related

- [The workbench](../workbench.md)
- [Worktrees](../worktrees.md)
- [Command line](../cli.md)
- [Keyboard](../keyboard.md)
