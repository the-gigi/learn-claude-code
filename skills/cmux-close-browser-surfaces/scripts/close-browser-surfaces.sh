#!/usr/bin/env bash
# Close every cmux browser surface in scope. Terminal surfaces are never
# touched. By default, scope is the caller's current workspace (across all
# panes in that workspace).

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: close-browser-surfaces.sh [--workspace <id|ref|index>] [--all]
                                 [--list] [--exclude <ref>[,<ref>...]]...

Close cmux browser surfaces in bulk. Terminal surfaces are left alone.

Scope (mutually exclusive):
  (default)                    All panes in the caller's current workspace.
  --workspace <id|ref|index>   All panes in the given workspace.
  --all                        All workspaces in the current cmux window
                               (does not cross to other windows).

Selection:
  --list                       Print browser surfaces in scope and exit;
                               do not close anything. Use this to discover
                               refs before passing them to --exclude or to
                               `cmux close-surface --surface <ref>` for a
                               single-target close.
  --exclude <ref>[,<ref>...]   Skip these surface refs (UUIDs, `surface:N`
                               refs, or per-workspace indexes). May be
                               passed multiple times; values are unioned.

Other:
  -h, --help                   Show this help.
EOF
}

workspace=""
all=0
list_only=0
exclude_csv=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --workspace)
      [[ $# -ge 2 ]] || { echo "error: --workspace requires a value" >&2; exit 2; }
      workspace="$2"
      shift 2
      ;;
    --all)
      all=1
      shift
      ;;
    --list)
      list_only=1
      shift
      ;;
    --exclude)
      [[ $# -ge 2 ]] || { echo "error: --exclude requires a value" >&2; exit 2; }
      if [[ -z "$exclude_csv" ]]; then
        exclude_csv="$2"
      else
        exclude_csv="$exclude_csv,$2"
      fi
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -n "$workspace" && "$all" -eq 1 ]]; then
  echo "error: --workspace and --all are mutually exclusive" >&2
  exit 2
fi

command -v cmux >/dev/null 2>&1 || { echo "error: cmux not on PATH" >&2; exit 1; }
command -v jq   >/dev/null 2>&1 || { echo "error: jq not on PATH"   >&2; exit 1; }

if [[ "$all" -eq 1 ]]; then
  tree_json=$(cmux tree --json)
elif [[ -n "$workspace" ]]; then
  tree_json=$(cmux tree --workspace "$workspace" --json)
else
  caller_ws=$(cmux identify 2>/dev/null | jq -r '.caller.workspace_ref // empty')
  if [[ -z "$caller_ws" ]]; then
    echo "error: could not determine caller's workspace from 'cmux identify'" >&2
    exit 1
  fi
  tree_json=$(cmux tree --workspace "$caller_ws" --json)
fi

# Build a newline-list of excluded refs (trim whitespace, drop empties).
exclude_list=$(printf '%s' "$exclude_csv" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v '^$' || true)

is_excluded() {
  local needle="$1"
  [[ -z "$exclude_list" ]] && return 1
  printf '%s\n' "$exclude_list" | grep -Fxq -- "$needle"
}

# Emit "<workspace_ref>\t<surface_ref>\t<title>\t<url>" for every browser surface.
# Use `while read` (works on macOS bash 3.2) instead of `mapfile`.
rows=$(jq -r '
  .windows[]?.workspaces[]? as $ws
  | $ws.panes[]?.surfaces[]?
  | select(.type == "browser")
  | [$ws.ref, .ref, (.title // ""), (.url // "")]
  | @tsv
' <<<"$tree_json")

if [[ -z "$rows" ]]; then
  echo "no browser surfaces in scope"
  exit 0
fi

if [[ "$list_only" -eq 1 ]]; then
  while IFS=$'\t' read -r ws_ref surface_ref title url; do
    [[ -z "$surface_ref" ]] && continue
    if is_excluded "$surface_ref"; then
      printf '%s\t%s\t%s\t%s\t(excluded)\n' "$ws_ref" "$surface_ref" "$title" "$url"
    else
      printf '%s\t%s\t%s\t%s\n' "$ws_ref" "$surface_ref" "$title" "$url"
    fi
  done <<<"$rows"
  exit 0
fi

failed=0
matched=0
skipped=0
while IFS=$'\t' read -r ws_ref surface_ref title url; do
  [[ -z "$surface_ref" ]] && continue
  if is_excluded "$surface_ref"; then
    printf 'skipped %s in %s — %s\t%s\n' "$surface_ref" "$ws_ref" "$title" "$url"
    skipped=$((skipped + 1))
    continue
  fi
  matched=$((matched + 1))
  if cmux close-surface --surface "$surface_ref" --workspace "$ws_ref" >/dev/null 2>&1; then
    printf 'closed %s in %s — %s\t%s\n' "$surface_ref" "$ws_ref" "$title" "$url"
  else
    printf 'FAILED to close %s in %s — %s\t%s\n' "$surface_ref" "$ws_ref" "$title" "$url" >&2
    failed=$((failed + 1))
  fi
done <<<"$rows"

if [[ "$matched" -eq 0 && "$skipped" -eq 0 ]]; then
  echo "no browser surfaces in scope"
  exit 0
fi

exit $(( failed > 0 ? 1 : 0 ))
