---
name: close-browser-surfaces
description: Close all cmux browser surfaces in the current workspace (or a specific workspace, or every workspace in the current window). Use whenever the user asks to "close the browser surface(s)", "close the cmux browser tab(s)", or otherwise tidy up browser surfaces left behind by prior work. Terminal surfaces are never touched.
---

# Close cmux Browser Surfaces

Close every browser surface in scope using the `cmux` CLI. Terminal surfaces are left alone.

## When to use

Trigger this skill when the user asks anything like:

- "close the browser surface(s) in this workspace"
- "close the cmux browser tab(s)"
- "kill the browser panes"
- "tidy up the browser surfaces"

The cmux CLI is the only supported control plane — do not try to close surfaces by killing processes or manipulating windows directly.

## Usage

```bash
# Default: close browser surfaces in the caller's current workspace.
./scripts/close-browser-surfaces.sh

# Specific workspace (UUID, ref like `workspace:28`, or index).
./scripts/close-browser-surfaces.sh --workspace workspace:28

# Every workspace in the current cmux window.
./scripts/close-browser-surfaces.sh --all
```

The script:

1. Calls `cmux tree --json` (scoped to the chosen workspace, or `--all` for every workspace in the window).
2. Filters surfaces where `type == "browser"`.
3. Calls `cmux close-surface --surface <ref>` for each match.
4. Prints one line per closed surface (`workspace_ref`, `surface_ref`, `title`, `url`).
5. Exits 0 if any surfaces matched and all closed cleanly, 0 with a "no browser surfaces" notice if none matched, and non-zero if any close call failed.

## Scope

- Closes **browser** surfaces only. Terminal surfaces are never touched.
- Operates on the current cmux window. Use `--all` to fan out across every workspace in that window; for other windows, switch focus first or pass an explicit workspace ref.
- Requires `cmux` (the `cmux` binary, reachable on `PATH`) and `jq`.
