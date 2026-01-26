Construct a git commit message and run the commit command.

Note: `gcm` uses `git commit -a` which automatically stages modified/deleted tracked files.
New (untracked) files still need to be added manually with `git add`.

## Instructions

1. Run `git diff --stat` to see changes (both staged and unstaged).

2. Run `git diff` to see the actual changes.

3. Find the project prefix by looking at recent commits in the affected directories:
   ```
   git log --oneline -10 -- <affected-paths>
   ```
   Look for the `[project]` pattern in those commits. Use the most common prefix found.

4. Generate a concise one-liner commit message:
    - Start with lowercase after the `[project]` prefix
    - Focus on the "what" and "why", not the "how"
    - No issue numbers (those go in PR descriptions)
    - Keep it under 72 characters total

5. Run the commit command immediately:
   ```
   gcm "[<project>] <message>"
   ```

