# Prune Worktrees

Cleans up bazel cache entries for worktrees that no longer exist, freeing disk space.

## Instructions

1. First, run with `--dry-run` to see what would be deleted:
   ```bash
   ~/.local/bin/prune-worktrees --dry-run
   ```

2. If the output looks correct, run without `--dry-run` to actually clean up:
   ```bash
   ~/.local/bin/prune-worktrees
   ```

3. Report the amount of disk space freed.
