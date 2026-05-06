---
name: cmux-close-browser-surfaces
description: Bulk-close cmux browser surfaces. Default scope is the caller's current workspace (across all panes); `--workspace <ref>` targets a specific workspace; `--all` covers every workspace in the current cmux window. `--list` previews matches without closing; `--exclude <ref>...` keeps specified surfaces around. Use whenever the user asks to "close the browser surface(s)", "close the cmux browser tab(s)", or otherwise tidy up cmux browser surfaces left behind by prior work. Terminal surfaces are never touched. cmux is a tmux-like multiplexer with terminal and browser surfaces; this skill is unrelated to web-browser tabs or OS-level browser windows.
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

For closing one specific surface, prefer `cmux close-surface --surface <ref>` directly. This skill exists for the bulk case.

## Scope semantics

cmux has windows → workspaces → panes → surfaces. The skill operates on **surfaces**, never panes or workspaces themselves. Within whatever scope is selected, every pane's surfaces are inspected and only those with `type == "browser"` are closed.

| Flag                          | What gets considered                                              |
| ----------------------------- | ----------------------------------------------------------------- |
| _(none)_                      | Caller's current workspace, across all its panes.                 |
| `--workspace <id\|ref\|index>`| One specific workspace, across all its panes.                     |
| `--all`                       | Every workspace in the **current cmux window** (does not cross to other windows). |

`--workspace` and `--all` are mutually exclusive. Cross-window scope is not currently supported — switch to the target window first or invoke per-workspace.

## Selection

| Flag                                | Behavior                                                                |
| ----------------------------------- | ----------------------------------------------------------------------- |
| `--list`                            | Print browser surfaces in scope and exit. No surfaces are closed. Use this to discover refs before deciding what to close or exclude. |
| `--exclude <ref>[,<ref>...]`        | Skip the listed surface refs. Repeatable; values are unioned. Refs can be UUIDs, `surface:N` refs, or per-workspace indexes — same forms `cmux` itself accepts. |

## Usage

```bash
# Default: caller's workspace, all browser surfaces.
./scripts/close-browser-surfaces.sh

# Specific workspace.
./scripts/close-browser-surfaces.sh --workspace workspace:28

# Every workspace in the current window.
./scripts/close-browser-surfaces.sh --all

# Discover refs first.
./scripts/close-browser-surfaces.sh --list
./scripts/close-browser-surfaces.sh --all --list

# Close all browser surfaces except one.
./scripts/close-browser-surfaces.sh --exclude surface:107

# Close all browser surfaces except two (either form works).
./scripts/close-browser-surfaces.sh --exclude surface:107,surface:113
./scripts/close-browser-surfaces.sh --exclude surface:107 --exclude surface:113

# Close a single specific surface — use cmux directly, not this skill.
cmux close-surface --surface surface:107
```

## Output

Each non-list run prints one line per surface processed:

- `closed <surface> in <workspace> — <title>\t<url>` on success.
- `skipped <surface> in <workspace> — <title>\t<url>` for `--exclude`'d surfaces.
- `FAILED to close ...` (to stderr) if a `cmux close-surface` call returns non-zero.

`--list` prints `<workspace>\t<surface>\t<title>\t<url>` per row, with a trailing `(excluded)` column when the surface matches `--exclude`.

Exit codes: `0` if everything went cleanly (including "no browser surfaces in scope"); non-zero only if a `close-surface` call actually failed.

## Requirements

- `cmux` CLI on `PATH`.
- `jq` on `PATH`.
- Bash 3.2+ (works on macOS system bash; no `mapfile`).
