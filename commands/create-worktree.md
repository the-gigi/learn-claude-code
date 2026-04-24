# Create Worktree from Linear Issue

Creates a new git worktree from a Linear issue, then opens it in iTerm2 with horizontal split panes.

**Argument:** `<linear-issue> --repo <repo>`

- `linear-issue`: Linear issue ID (e.g., `AI2-992`, `IN-2705`)
- `--repo`: Target repo — `agi`, `infra`, or `inference-monorepo` (REQUIRED)

## Instructions

1. Parse `$ARGUMENTS` to extract the Linear issue ID and `--repo` value. If `--repo` is missing, ask the user which repo.
2. Fetch the Linear issue using the `mcp__linear__get_issue` tool
3. Extract the issue identifier (e.g., `AI2-992`) and title
4. Generate a slug from the title:
   - Lowercase
   - Replace spaces and special chars with hyphens
   - Remove consecutive hyphens
   - Max 50 characters
   - Example: "Investigate duplicate alerts due to env ambiguity" → "investigate-duplicate-alerts-due-to-env-ambiguity"
5. Run: `~/.local/bin/create-worktree <issue-id> <slug> --repo <repo>`

Example:
```bash
~/.local/bin/create-worktree AI2-992 investigate-duplicate-alerts-due-to-env-ambiguity --repo agi
~/.local/bin/create-worktree IN-2705 upgrade-sandbox-tailscale-operator --repo agi
```
