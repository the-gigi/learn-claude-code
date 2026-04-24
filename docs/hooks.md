# Hooks

Hooks are shell commands (or LLM prompts) that fire automatically at specific points during a Claude Code
session. Unlike CLAUDE.md instructions that Claude might forget or skip, hooks execute **deterministically**
every time.

Official docs: [Hooks reference](https://code.claude.com/docs/en/hooks) |
[Hooks guide](https://code.claude.com/docs/en/hooks-guide)

## Why Hooks?

Here is an example session where CLAUDE.md + subagents failed. The instructions were clear, Claude had them in
context, and it still didn't follow them:

```
  The instructions in CLAUDE.md are clear - I should have used the comet-cloud-test-runner agent immediately
  after making changes instead of manually running a single test. I'll follow this workflow going forward.

✻ Sautéed for 1m 50s

❯ let's double click on this. why did you fail to follow the instructions this time? what gives you confidence
  you'll follow the instructions next time?

⏺ Good question. Let me be honest:

  Why I failed:

  1. I didn't actively consult CLAUDE.md at the completion checkpoint. I read it at the session start (it was
     in context), but when finishing the task, I defaulted to my generic pattern: "build passes, one test
     passes, done."
  2. I didn't include the verification step in my todo list. My todos ended with "Run build to verify" instead
     of "Run tests with comet-cloud-test-runner agent" which is what CLAUDE.md actually specifies.
  3. Rushing through the finish line. I was focused on the code changes and treated verification as a formality
     rather than following the documented process.

  What gives me confidence for next time?

  Honestly - not much. I can say I'll "be more careful" but that's weak. What would actually help:

  1. Add the CLAUDE.md verification steps explicitly to my todo list when I create it - not just "run tests"
     but the specific agent/command the project requires.
  2. Re-read the relevant CLAUDE.md section before marking work complete - treat it as a checklist, not
     background context.

  But I recognize this is a pattern issue. The instructions were clear, I had them in context, and I still
  didn't follow them. That's on me.
```

This is why hooks exist. CLAUDE.md says "run tests before committing." Claude reads it, nods, and sometimes...
doesn't. A hook on
`PreToolUse` matching the Bash tool that detects `git commit` will block the commit if tests haven't passed.
Every time. No exceptions.

## Configuration

Hooks live in settings files. Three levels of scope:

| Scope | File | Shared via git? |
|-------|------|-----------------|
| User (global) | `~/.claude/settings.json` | No |
| Project (shared) | `.claude/settings.json` | Yes |
| Project (local) | `.claude/settings.local.json` | No |

You can also define hooks in plugin `hooks/hooks.json` files and in skill/agent YAML frontmatter.

The `/hooks` slash command opens an interactive menu for viewing and editing hooks.

**Important:** Hooks are snapshotted at session startup. If you edit settings files directly, restart the
session or use `/hooks` to reload.

### Structure

Three levels of nesting: event → matcher group → hook handler(s).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

## Hook Events

| Event | When it fires | Can block? |
|-------|---------------|------------|
| `SessionStart` | Session begins, resumes, or compacts | No (injects context) |
| `UserPromptSubmit` | User submits a prompt, before Claude sees it | Yes |
| `PreToolUse` | Before a tool call executes | Yes |
| `PermissionRequest` | Permission dialog appears | Yes |
| `PostToolUse` | After a tool call succeeds | No (already ran) |
| `PostToolUseFailure` | After a tool call fails | No (already failed) |
| `Notification` | Claude sends a notification | No |
| `SubagentStart` | Subagent spawns | No (injects context) |
| `SubagentStop` | Subagent finishes | Yes |
| `Stop` | Claude finishes responding | Yes |
| `TeammateIdle` | Agent team teammate about to idle | Yes |
| `TaskCompleted` | Task being marked complete | Yes |
| `PreCompact` | Before context compaction | No |
| `SessionEnd` | Session terminates | No |

The typical flow: `SessionStart` → `UserPromptSubmit` → [`PreToolUse` → tool runs → `PostToolUse`] (repeating)
→ `Stop` → back to waiting for user input, or `SessionEnd`.

## Matchers

Matchers filter which tool calls (or events) trigger the hook. They use regex patterns:

| Pattern | Matches |
|---------|---------|
| `"Bash"` | Exact: only the Bash tool |
| `"Edit\|Write"` | Either Edit or Write |
| `"Notebook.*"` | Anything starting with "Notebook" |
| `"mcp__.*"` | All MCP tools |
| `"mcp__linear__.*"` | All tools from the Linear MCP server |
| `""` or `"*"` or omitted | Everything |

**What matchers match on depends on the event:**

- `PreToolUse`, `PostToolUse`, `PermissionRequest` → tool name
- `SessionStart` → session source (`startup`, `resume`, `clear`, `compact`)
- `SessionEnd` → exit reason
- `Notification` → notification type
- `SubagentStart/Stop` → agent type
- `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted` → no matcher support (always fires)

## Hook Types

### Command Hooks

Run a shell command. The event's JSON data arrives on stdin.

```json
{
  "type": "command",
  "command": ".claude/hooks/my-script.sh",
  "timeout": 600,
  "async": false,
  "statusMessage": "Running security check..."
}
```

- `timeout`: seconds before kill (default: 600)
- `async`: run in background, Claude continues working (only `systemMessage` delivered later)
- `statusMessage`: spinner text while running

### Prompt Hooks

Send the hook input + your prompt to a fast LLM (Haiku) for a single-turn yes/no decision.

```json
{
  "type": "prompt",
  "prompt": "Check if all tasks are complete. Respond with {\"ok\": false, \"reason\": \"what remains\"} if not.",
  "timeout": 30
}
```

Returns `{"ok": true}` or `{"ok": false, "reason": "..."}`.

### Agent Hooks

Like prompt hooks but the LLM gets tool access (Read, Grep, Glob, etc.) and can do multi-turn work — up to 50
tool calls.

```json
{
  "type": "agent",
  "prompt": "Run the test suite and verify all tests pass. $ARGUMENTS",
  "timeout": 60
}
```

Same response schema as prompt hooks.

**When to use which:** Use command hooks for deterministic checks (file existence, pattern matching). Use prompt
hooks when the input data alone is enough for a judgment call. Use agent hooks when you need to inspect the
codebase to verify something.

## Input & Output

### Input (stdin)

Every hook receives JSON on stdin with common fields:

```json
{
  "session_id": "abc123",
  "cwd": "/Users/me/project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run tests"
  }
}
```

The `tool_input` schema varies by tool — Bash gets `command`, Edit gets `file_path`/`old_string`/`new_string`,
etc.

### Output

Hooks communicate back via **exit codes** and **stdout/stderr**:

| Exit code | Meaning | stdout | stderr |
|-----------|---------|--------|--------|
| 0 | Success, proceed | Parsed for JSON or added as context | Verbose mode only |
| 2 | **Block the action** | Ignored | Fed back to Claude as error |
| Other | Non-blocking error | Ignored | Verbose mode only |

**Exit code 2** is the key mechanism. For blocking events (`PreToolUse`, `UserPromptSubmit`, `Stop`, etc.),
exit 2 prevents the action and sends stderr to Claude so it can adjust.

### Structured JSON Output

On exit 0, you can print JSON to stdout for fine-grained control:

```json
{
  "continue": true,
  "systemMessage": "Warning: approaching rate limit",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "File is protected",
    "updatedInput": { "command": "safe-alternative" }
  }
}
```

- `continue: false` + `stopReason` → force Claude to stop
- `permissionDecision`: `"allow"`, `"deny"`, or `"ask"`
- `updatedInput`: rewrite the tool's input before execution

## Environment Variables

- `$CLAUDE_PROJECT_DIR` — project root (use for portable paths in shared hooks)
- `$CLAUDE_ENV_FILE` — write `export VAR=value` lines here (SessionStart) to persist env vars

## Practical Examples

### Auto-format after edits

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
        }]
      }
    ]
  }
}
```

### Protect sensitive files

`.claude/hooks/protect-files.sh`:
```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

for pattern in ".env" "secrets" ".git/"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh" }]
      }
    ]
  }
}
```

### Notifications (macOS)

Getting notified when Claude needs attention is surprisingly annoying on macOS. Here are three approaches that
actually work, from simplest to most visible.

**Option 1: System sound** — no dependencies, non-blocking, always works:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{
          "type": "command",
          "command": "afplay /System/Library/Sounds/Glass.aiff &"
        }]
      }
    ]
  }
}
```

Other sounds in `/System/Library/Sounds/`: `Basso`, `Blow`, `Bottle`, `Frog`, `Funk`, `Hero`, `Morse`,
`Ping`, `Pop`, `Purr`, `Sosumi`, `Submarine`, `Tink`.

**Option 2: iTerm2 tab flash + dock bounce** — no dependencies, but only works in iTerm2:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{
          "type": "command",
          "command": "if [ \"$TERM_PROGRAM\" = \"iTerm.app\" ]; then printf '\\a'; printf '\\033]1337;RequestAttention=yes\\007'; fi"
        }]
      }
    ]
  }
}
```

`\a` (BEL character) flashes the tab. `RequestAttention` is an iTerm2 proprietary escape sequence that bounces
the dock icon until you switch to it. Requires iTerm2 Settings → Profiles → Terminal → Notifications →
enable "Flash bell" and "Bounce dock icon".

**Option 3: Modal dialog** — impossible to miss, but blocks the hook until you click OK:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{
          "type": "command",
          "command": "osascript -e 'display alert \"Claude Code\" message \"Claude needs attention\"'"
        }]
      }
    ]
  }
}
```

Downside: `display alert` is modal — the hook hangs until you dismiss it. This means Claude is paused waiting
for you to click OK. Fine if you're AFK and want to know when to come back, annoying if you're watching.

**What about desktop notifications?** `osascript display notification` is unreliable from background processes
on macOS 15+. `terminal-notifier` (the classic recommendation) is unmaintained and broken on modern macOS. If
you find a maintained alternative, please share. For now, combine options 1 + 2 for the best result.

### Re-inject context after compaction

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [{
          "type": "command",
          "command": "echo 'Reminder: use bun not npm. Current sprint: auth refactor.'"
        }]
      }
    ]
  }
}
```

### Log all Bash commands

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
        }]
      }
    ]
  }
}
```

## The Ralph Wiggum Loop

The Ralph Wiggum loop is the most famous hook-based pattern in the Claude Code ecosystem. It creates an
**autonomous, self-iterating development loop** — Claude works on a task, tries to stop, gets told to keep
going, and iterates until the job is actually done.

Named after the Simpsons character (persistent despite setbacks), it was created by
[Geoffrey Huntley](https://ghuntley.com/loop/), who famously ran a 3-month Ralph loop that built an entire
programming language.

**Source code:**
[anthropics/claude-code/plugins/ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)

### How It Works

Ralph is a Claude Code **plugin** that installs a `Stop` hook and two slash commands (`/ralph-loop` and
`/cancel-ralph`).

1. You invoke `/ralph-loop "Build a REST API with full test coverage" --completion-promise "DONE"`
2. The command runs a setup script that writes `.claude/ralph-loop.local.md` — a state file containing YAML
   frontmatter (iteration count, max iterations, completion promise) and the user's prompt. Crucially, the
   setup script **injects explicit instructions** into this file telling Claude the exact exit syntax:
   *"To complete this loop, output this EXACT text: `<promise>DONE</promise>`"* along with guardrails:
   *"The statement MUST be completely and unequivocally TRUE. Do NOT output false statements to exit the loop."*
3. Claude works on the task normally — it knows about the `<promise>` tags because it was told in step 2
4. When Claude tries to stop, the **Stop hook** fires:
   - It reads the state file and the session transcript
   - It checks termination conditions (see below)
   - If not done: blocks the exit (exit code 0 with `"decision": "block"`) and feeds the **original prompt**
     back as the reason — Claude sees its own previous work in context and starts the next iteration
   - The iteration counter increments atomically

### Termination Conditions

The loop ends when **any** of these are true:

1. **Completion promise detected.** If `--completion-promise "DONE"` was set, the stop hook scans Claude's
   latest output for `<promise>DONE</promise>`. It does **literal string comparison** — no regex, no fuzzy
   matching. Claude must output the exact promise text wrapped in `<promise>` tags. When found, the state file
   is removed and Claude is allowed to stop.

2. **Max iterations reached.** If `--max-iterations N` was set and the counter hits N, the loop exits. This is
   your safety net for tasks that might be impossible or get stuck.

3. **Manual cancellation.** Run `/cancel-ralph` to kill the loop immediately.

4. **State file missing.** If `.claude/ralph-loop.local.md` doesn't exist (deleted manually or never created),
   the hook exits normally and Claude stops.

### Why It Works

The key insight: **files and git history persist between iterations.** Each time Claude restarts, it sees the
code it wrote in the previous iteration. Combined with a well-structured prompt (especially TDD-style: write
tests first, then implement until they pass), Claude can incrementally converge on a working solution.

### Usage

```
/ralph-loop "Your task description" --max-iterations 10 --completion-promise "DONE"
```

Best practices from the community:
- Always set `--max-iterations` as a safety net
- Use TDD-style prompts: "Write failing tests first, then implement until all pass"
- Include clear completion criteria in the prompt
- The completion promise should be something Claude would naturally say when done
- Check `git log` after to see the iteration history

## Debugging Hooks

- Run `claude --debug` to see which hooks matched, their exit codes, and output
- Press `Ctrl+O` in Claude Code for verbose mode (shows hook progress in transcript)
- Test command hooks manually: `echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh; echo $?`

## Gotcha: Shell Profile Pollution

If your `~/.zshrc` or `~/.bashrc` has unconditional `echo` statements, they'll prepend text to your hook's
JSON output and break parsing. Wrap them:

```bash
if [[ $- == *i* ]]; then
  echo "Welcome back!"
fi
```

`$-` contains shell flags; `i` means interactive.
