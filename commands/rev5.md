Run an autonomous codex review loop, up to 5 iterations, self-paced.

Each invocation executes **one** iteration and — if actionable findings remain and the cap isn't reached — calls `ScheduleWakeup` to continue in a subsequent response. This ensures each iteration's report is the final text of its response, so focus mode surfaces every round as it happens instead of swallowing intermediate output.

## Parsing the iteration counter

The skill is invoked as `/rev5` or `/rev5 --iter N`:
- Empty args → iteration **1**
- `--iter N` → iteration **N** (1 ≤ N ≤ 5)

Treat anything else as iteration 1.

## Iteration steps

1. **Run codex**, capturing the full output:
   - If the working tree has uncommitted changes (staged, unstaged, or untracked): `codex review --uncommitted`
   - Otherwise: `codex review --base main`
2. **Read findings critically** — not every suggestion is worth acting on. Weigh each against the codebase's conventions and the change's intent. Decide which are genuine bugs, logic errors, missing edge cases, or real quality issues.
3. **Apply any actionable fixes.** Non-actionable findings are acknowledged with a one-line reason.
4. **Decide whether to continue**:
   - **Clean** (no findings, or all non-actionable) → stop.
   - **N == 5** → stop (cap reached).
   - Otherwise → call `ScheduleWakeup` with `delaySeconds: 60`, `prompt: "/rev5 --iter <N+1>"`, `reason: "rev5 iter <N+1>/5"`. This fires as a new user message when the delay elapses and re-enters the skill.

## End-of-response report

**The last thing in every response must be the iteration report.** In focus mode this is the only text the user sees, so make it load-bearing.

Use this shape:

```
## /rev5 — iter N/5

Codex findings
- [P1|P2|P3] path:line — one-line summary
- ...

Assessment
- <finding>: actionable — reason / not actionable — reason
- ...

Fixes applied
- <file>: what changed
(or: "none — review is clean")

Next: scheduled iter <N+1>/5 in 60s   |   stopping — clean   |   stopping — cap reached
```

## Notes

- 60s is the ScheduleWakeup minimum; shorter isn't possible. Expect ~60s + codex runtime between iteration reports.
- Do NOT loop inside a single response. One invocation = one iteration + (optionally) one ScheduleWakeup for the next.
- Do NOT call ScheduleWakeup after a clean pass or at iter 5 — that wastes a wakeup and confuses the user.
- If the user wants to manually pace iterations, they can just re-invoke `/rev5` themselves; the skill works either way.
