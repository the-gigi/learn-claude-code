Here is a lightweight study guide you can drop into a markdown file (e.g., `claude-code-study-guide.md`) and tick off as you go.

***

## Track 1 – Core Claude Code

- [x] Skim official [Claude Code overview - Claude Code Docs](https://code.claude.com/docs/en/overview) to understand core concepts, how it runs in your terminal, and the mental model (agent in your repo, not in the cloud).
- [x] Watch [Claude Code Tutorial #1 - Introduction & Setup - YouTube](https://www.youtube.com/watch?v=SUysp3sJHbA) and follow along to install Claude Code, run it in a small test repo, and complete at least one "fix a bug" flow.
- [x] Read [Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) and create or update a `CLAUDE.md` for your lab repo (document commands, tests, style, project map).
***

## Track 2 – Skills, Slash Commands, Subagents

- [x] Read [Understanding Claude Code's Full Stack](https://alexop.dev/posts/understanding-claude-code-full-stack/) focusing on the conceptual differences between skills, commands, and subagents.
- [x] Read [How I Use Every Claude Code Feature - by Shrivu Shankar](https://blog.sshh.io/p/how-i-use-every-claude-code-feature) and note 2–3 patterns you want to copy (e.g., a specific subagent role or reusable slash command).
- [ ] Study [Subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) and configure at least one subagent in your lab repo (e.g., "Test Runner" or "Security Reviewer").
- [ ] Install or create at least one custom skill following [Claude Skills Tutorial](https://www.siddharthbharath.com/claude-skills/); document in `CLAUDE.md` when/how you want it used.
- [ ] Read [Slash Commands vs Subagents](https://jxnl.co/writing/2025/08/29/context-engineering-slash-commands-subagents/) and refactor at least one workflow into a slash command and one into a subagent, based on those guidelines.
- [ ] Explore [VoltAgent/awesome-claude-code-subagents - GitHub](https://github.com/VoltAgent/awesome-claude-code-subagents) and adapt one existing subagent idea to your lab repo.
- [ ] Read the Reddit thread [When should I use a Skill, a Slash Command, or a Sub-Agent in ...](https://www.reddit.com/r/ClaudeAI/comments/1orozs4/when_should_i_use_a_skill_a_slash_command_or_a/) and add 2 "rules of thumb" you like into this guide.

***

## Track 3 – MCP Servers and Extensions

- [ ] Read official [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) docs to understand the lifecycle: discovery, `tools/list`, `tools/call`, error modes.
- [ ] Follow [How to Quickly Build a MCP Server for Claude Code - Apidog](https://apidog.com/blog/how-to-quickly-build-a-mcp-server-for-claude-code/) to build a minimal "Hello World" MCP server locally and see it inside Claude Code.
- [ ] Work through [Build an MCP Server](https://www.codecademy.com/article/build-an-mcp-server) and add at least one real function you'd actually use (e.g., querying a local service or reading docs).
- [ ] Watch [Claude Code Tutorial #7 - MCP Servers - YouTube](https://www.youtube.com/watch?v=X7lgIa6guKg) and compare the video workflow to your own; note any missing safety or logging considerations in your server.
- [ ] Read [Understanding Skills, Agents, Subagents, and MCP in Claude Code](https://colinmcnamara.com/blog/understanding-skills-agents-and-mcp-in-claude-code) and sketch how you'd structure: Skills, Subagents, and one MCP server for a real project you care about.
- [ ] Pick one external system you use often (e.g., docs, DB, CI) and design an MCP‑backed flow for it, even if you do not fully implement it yet.

***

## Track 4 – GitHub Integration

- [ ] Ensure the Claude Code GitHub app is installed on a sandbox repo you control; verify it can read issues and PRs.
- [ ] Watch [Claude Code Tutorial #9 - Claude Code with GitHub - YouTube](https://www.youtube.com/watch?v=7pKN_pjPW04) and perform the same steps: trigger Claude on a PR, request changes, let it push commits.
- [ ] Watch [Claude Code + GitHub WORKFLOW for Complex Apps - YouTube](https://www.youtube.com/watch?v=FjHtZnjNEBU) and write a short note on how you want Claude Code to participate in your own review/branch model.
- [ ] In your lab repo, practice a full loop: open issue → let Claude propose plan → create branch → implement via Claude Code → open PR → have Claude review the diff.
- [ ] Add a section to `CLAUDE.md` describing your Git workflow rules for Claude (branch naming, tests to run before pushing, when to open vs update a PR).

***

## Track 5 – Power‑user Patterns & Reference

- [ ] Read [How I Turned Claude Code Into My Personal AI Agent Operating ...](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) and note 2–3 "operating system" ideas (e.g., global planner, review subagent) to try later.
- [ ] Watch [9 months of Claude Code Lessons in 19 minutes - YouTube](https://www.youtube.com/watch?v=wxFt2d7xN44) and list 5 mistakes to avoid in your own usage.
- [ ] Study [Ultimate guide to extending Claude Code with skills, agents ...](https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935) and pick one advanced pattern (hooks, meta‑commands, or plugins) to experiment with.
- [ ] Read [Claude Code Cheat Sheet](https://devoriales.com/post/400/claude-code-cheat-sheet-the-reference-guide) and copy the subset of commands/flags that match your workflow into this guide as your personal cheatsheet.
- [ ] Read [Cooking with Claude Code](https://www.siddharthbharath.com/claude-code-the-complete-guide/) or a similar "complete guide" and compare its recommended workflows with your current habits.
- [ ] Optionally, skim [claude_code_docs_map.md - Simon Willison](https://simonwillison.net/2025/Oct/24/claude-code-docs-map/) and bookmark/docs sections you haven't touched yet for future deep dives.

***

## Track 6 – Army of Claudes

- [ ] Set up parallel Claude Code sessions with Git Worktrees using [tree-me](https://haacked.com/archive/2025/11/21/tree-me/) bash wrapper.
- [ ] Run Claude Code in isolated Docker containers with [ClaudeBox](https://github.com/RchGrav/claudebox) for multi-instance support.
- [ ] Use [Claude Code on the Web](https://docs.claude.com/en/docs/claude-code/claude-code-on-the-web) to run multiple coding tasks in parallel via browser.
- [ ] Install [CCManager](https://github.com/kbwo/ccmanager) to monitor and switch between multiple AI coding sessions with real-time status indicators.
- [ ] Try [Claude Squad](https://github.com/smtg-ai/claude-squad) for tmux-based orchestration of multiple AI agents with background task execution.
- [ ] Explore [agenttools/worktree](https://github.com/agenttools/worktree) for GitHub issue integration with multi-worker Claude coordination.
- [ ] Explore [Claude 007 Agents](https://github.com/avivl/claude-007-agents) orchestration system with 14 categories of specialized agents.

***

## Track 7 – Advanced Features & Customization

- [ ] Read [Plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins) and install at least one plugin to extend Claude Code's capabilities.
- [ ] Study [Hooks Guide - Claude Code Docs](https://code.claude.com/docs/en/hooks-guide) and create a startup hook for your workflow (e.g., auto-run tests, set environment).
- [ ] Read [Output styles - Claude Code Docs](https://code.claude.com/docs/en/output-styles) and customize how Claude presents information (compact, verbose, etc.).
- [ ] Read [Headless mode - Claude Code Docs](https://code.claude.com/docs/en/headless) to understand automation and CI/CD integration use cases.
- [ ] Experiment with combining hooks + plugins to create a personalized Claude Code startup sequence.

