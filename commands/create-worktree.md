# Create Worktree from Linear Issue

Creates a new git worktree from a Linear issue, then opens it in iTerm2 with horizontal split panes.

**Argument:** Linear issue ID (e.g., `AI2-992`)

## Instructions

1. Fetch the Linear issue `$ARGUMENTS` using the `mcp__linear__get_issue` tool
2. Extract the issue identifier (e.g., `AI2-992`) and title
3. Generate a slug from the title:
   - Lowercase
   - Replace spaces and special chars with hyphens
   - Remove consecutive hyphens
   - Max 50 characters
   - Example: "Investigate duplicate alerts due to env ambiguity" → "investigate-duplicate-alerts-due-to-env-ambiguity"
4. Run: `~/.local/bin/create-worktree <issue-id> <slug>`

Example:
```bash
~/.local/bin/create-worktree AI2-992 investigate-duplicate-alerts-due-to-env-ambiguity
```
