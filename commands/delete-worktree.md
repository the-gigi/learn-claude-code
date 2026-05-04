# Delete Worktree

Deletes a git worktree along with its branch and associated bazel cache after verifying the PR was merged.

**Argument:** Worktree path or name (e.g., `wt-feature-name` or `fix-testing-env`)

## Instructions

1. Run: `~/.local/bin/delete-worktree $ARGUMENTS`

Example:
```bash
~/.local/bin/delete-worktree fix-testing-env
```

The script will:
- Check if the PR for the branch was merged (fails if not merged)
- Remove the bazel workspace cache (freeing disk space)
- Remove the git worktree
- Delete the branch
- Checkout main and pull latest with rebase
- Close the matching cmux workspace if one is open (closes panes' surfaces first to avoid the hang that happens when `close-workspace` is invoked with live panes)

Bails out if PR wasn't merged or doesn't exist.
