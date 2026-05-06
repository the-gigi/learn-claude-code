#!/usr/bin/env bash
# Close every cmux browser surface in scope. Terminal surfaces are never
# touched. By default, scope is the caller's current workspace.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage: close-browser-surfaces.sh [--workspace <id|ref|index>] [--all]

Close cmux browser surfaces. Terminal surfaces are left alone.

Flags:
  --workspace <id|ref|index>   Restrict to one workspace (default: caller's workspace).
  --all                        Close browser surfaces across every workspace in
                               the current cmux window. Mutually exclusive with
                               --workspace.
  -h, --help                   Show this help.
EOF
}

workspace=""
all=0

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

failed=0
matched=0
while IFS=$'\t' read -r ws_ref surface_ref title url; do
  [[ -z "$surface_ref" ]] && continue
  matched=$((matched + 1))
  if cmux close-surface --surface "$surface_ref" --workspace "$ws_ref" >/dev/null 2>&1; then
    printf 'closed %s in %s — %s\t%s\n' "$surface_ref" "$ws_ref" "$title" "$url"
  else
    printf 'FAILED to close %s in %s — %s\t%s\n' "$surface_ref" "$ws_ref" "$title" "$url" >&2
    failed=$((failed + 1))
  fi
done <<<"$rows"

if [[ "$matched" -eq 0 ]]; then
  echo "no browser surfaces in scope"
  exit 0
fi

exit $(( failed > 0 ? 1 : 0 ))
