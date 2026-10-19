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

## The worktree's devbox

A merged PR's devbox is no longer needed, and the script does not know about
devboxes — so after it succeeds, reap the box this workspace owned. It is the
most expensive thing a worktree holds and the only one that keeps costing after
the branch is gone:

```bash
cd <agi-checkout> && ./bin/devbox list          # find the box carrying this worktree's PLA id
cd <agi-checkout> && ./bin/devbox delete <name>
```

Rules:
- **Only a box you can attribute to this worktree** — the naming convention is
  `pla<NNNN>-<slug>` with no hyphen after `pla` (see the `smoke` command and
  `/finalize` step 11), so match on that prefix, not on "looks unused". A box
  you cannot attribute is someone else's.
- The script having succeeded *is* the merge check; it bails out otherwise, so
  reaching this step means the PR merged.
- If no box carries this worktree's id, there is nothing to do — say so rather
  than hunting for a candidate.
- Shared, long-lived boxes (`hale-dove-mist`, `pale-leaf`) are never reaped
  here. They are not worktree-scoped and other sessions are on them.

## Workspace groups

The workspace it closes may be a member of an umbrella's cmux workspace group
(named `<PLA-id> <issue title>`, anchored on the umbrella workspace). The script
needs no extra flags either way, but the outcome differs:

- **A sub-issue worktree** is a plain member — the close drops it from the group
  and leaves the group's name, colour, pin and siblings intact.
- **An umbrella that is itself a worktree** (e.g. `wt-pla-6103-…-umbrella`) is
  the group **anchor**. Closing it closes only that workspace and promotes the
  next member to anchor, so the group keeps the umbrella's name while being
  headed by a sub-issue row. Run `cmux workspace-group ungroup <group-ref>`
  first when the whole family is done; otherwise say which sub-issue inherited
  the header.

Check with `cmux workspace-group list --json` before deleting an umbrella
worktree. Never use `workspace-group delete --close-workspaces` to tidy up after
this script — it would close every sibling sub-issue's live session.
