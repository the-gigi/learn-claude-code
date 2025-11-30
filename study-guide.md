Here is a lightweight study guide you can drop into a markdown file (e.g., `claude-code-study-guide.md`) and tick off as you go.[1][2]

***

## Track 1 – Core Claude Code

- [x] Skim official [Claude Code overview - Claude Code Docs](https://code.claude.com/docs/en/overview) to understand core concepts, how it runs in your terminal, and the mental model (agent in your repo, not in the cloud).[2]
- [x] Watch [Claude Code Tutorial #1 - Introduction & Setup - YouTube](https://www.youtube.com/watch?v=SUysp3sJHbA) and follow along to install Claude Code, run it in a small test repo, and complete at least one "fix a bug" flow.[4]
- [x] Read [Claude Code](https://www.anthropic.com/engineering/claude-code-best-practices) and create or update a `CLAUDE.md` for your lab repo (document commands, tests, style, project map).[3]
- [ ] Skim [Claude Code Documentation](https://www.claudecode.pro/docs/) sections for "Commands" and "Best Practices"; write down 3 CLI flags or commands you want to experiment with next session.[5]
- [ ] Create a personal “first session” script in your `CLAUDE.md` (how you want Claude to start: inspect repo, build mental model, run tests, etc.).[3]

***

## Track 2 – Skills, Slash Commands, Subagents

- [ ] Read [Understanding Claude Code's Full Stack](https://alexop.dev/posts/understanding-claude-code-full-stack/) focusing on the conceptual differences between skills, commands, and subagents.[1]
- [ ] Read [Understanding Claude Code](https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins) and write a 3‑line "When to use each" summary in your own words inside this study guide.[6]
- [ ] Skim [Claude Code Skills vs MCP vs Sub-agents vs Commands vs Hooks](https://www.linkedin.com/posts/lewisowain_claude-code-simplified-activity-7388911764161122304-7j7U) infographic/post and adjust your summary if it changes your mental model.[7]
- [ ] Read [How I Use Every Claude Code Feature - by Shrivu Shankar](https://blog.sshh.io/p/how-i-use-every-claude-code-feature) and note 2–3 patterns you want to copy (e.g., a specific subagent role or reusable slash command).[8]
- [ ] Study [Subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) and configure at least one subagent in your lab repo (e.g., "Test Runner" or "Security Reviewer").[9]
- [ ] Install or create at least one custom skill following [Claude Skills Tutorial](https://www.siddharthbharath.com/claude-skills/); document in `CLAUDE.md` when/how you want it used.[10]
- [ ] Read [Slash Commands vs Subagents](https://jxnl.co/writing/2025/08/29/context-engineering-slash-commands-subagents/) and refactor at least one workflow into a slash command and one into a subagent, based on those guidelines.[11]
- [ ] Explore [VoltAgent/awesome-claude-code-subagents - GitHub](https://github.com/VoltAgent/awesome-claude-code-subagents) and adapt one existing subagent idea to your lab repo.[12]
- [ ] Read the Reddit thread [When should I use a Skill, a Slash Command, or a Sub-Agent in ...](https://www.reddit.com/r/ClaudeAI/comments/1orozs4/when_should_i_use_a_skill_a_slash_command_or_a/) and add 2 "rules of thumb" you like into this guide.[13]

***

## Track 3 – MCP Servers and Extensions

- [ ] Read official [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) docs to understand the lifecycle: discovery, `tools/list`, `tools/call`, error modes.[14]
- [ ] Follow [How to Quickly Build a MCP Server for Claude Code - Apidog](https://apidog.com/blog/how-to-quickly-build-a-mcp-server-for-claude-code/) to build a minimal "Hello World" MCP server locally and see it inside Claude Code.[15]
- [ ] Work through [Build an MCP Server](https://www.codecademy.com/article/build-an-mcp-server) and add at least one real function you'd actually use (e.g., querying a local service or reading docs).[16]
- [ ] Watch [Claude Code Tutorial #7 - MCP Servers - YouTube](https://www.youtube.com/watch?v=X7lgIa6guKg) and compare the video workflow to your own; note any missing safety or logging considerations in your server.[17]
- [ ] Read [Understanding Skills, Agents, Subagents, and MCP in Claude Code](https://colinmcnamara.com/blog/understanding-skills-agents-and-mcp-in-claude-code) and sketch how you'd structure: Skills, Subagents, and one MCP server for a real project you care about.[18]
- [ ] Pick one external system you use often (e.g., docs, DB, CI) and design an MCP‑backed flow for it, even if you do not fully implement it yet.[19]

***

## Track 4 – GitHub Integration

- [ ] Ensure the Claude Code GitHub app is installed on a sandbox repo you control; verify it can read issues and PRs.[20][14]
- [ ] Watch [Claude Code Tutorial #9 - Claude Code with GitHub - YouTube](https://www.youtube.com/watch?v=7pKN_pjPW04) and perform the same steps: trigger Claude on a PR, request changes, let it push commits.[21]
- [ ] Watch [Claude Code + GitHub WORKFLOW for Complex Apps - YouTube](https://www.youtube.com/watch?v=FjHtZnjNEBU) and write a short note on how you want Claude Code to participate in your own review/branch model.[22]
- [ ] In your lab repo, practice a full loop: open issue → let Claude propose plan → create branch → implement via Claude Code → open PR → have Claude review the diff.[21][22]
- [ ] Add a section to `CLAUDE.md` describing your Git workflow rules for Claude (branch naming, tests to run before pushing, when to open vs update a PR).[3]

***

## Track 5 – Power‑user Patterns & Reference

- [ ] Read [How I Turned Claude Code Into My Personal AI Agent Operating ...](https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide) and note 2–3 "operating system" ideas (e.g., global planner, review subagent) to try later.[23]
- [ ] Watch [9 months of Claude Code Lessons in 19 minutes - YouTube](https://www.youtube.com/watch?v=wxFt2d7xN44) and list 5 mistakes to avoid in your own usage.[24]
- [ ] Study [Ultimate guide to extending Claude Code with skills, agents ...](https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935) and pick one advanced pattern (hooks, meta‑commands, or plugins) to experiment with.[25]
- [ ] Read [Claude Code Cheat Sheet](https://devoriales.com/post/400/claude-code-cheat-sheet-the-reference-guide) and copy the subset of commands/flags that match your workflow into this guide as your personal cheatsheet.[26]
- [ ] Read [Cooking with Claude Code](https://www.siddharthbharath.com/claude-code-the-complete-guide/) or a similar "complete guide" and compare its recommended workflows with your current habits.[27]
- [ ] Optionally, skim [claude_code_docs_map.md - Simon Willison](https://simonwillison.net/2025/Oct/24/claude-code-docs-map/) and bookmark/docs sections you haven't touched yet for future deep dives.[28]

***

## Optional – Project and Indexing Aids

- [ ] Add [ericbuess/claude-code-project-index](https://github.com/ericbuess/claude-code-project-index) to your lab repo and generate a `PROJECT_INDEX.json` once to see how it changes Claude's navigation.[29]
- [ ] Read the Reddit post [A checklist that saves me from endless back-and-forth with Claude ...](https://www.reddit.com/r/ClaudeCode/comments/1mwzk3v/a_checklist_that_saves_me_from_endless/) and adapt at least 3 checklist items into a slash command you run before big tasks.[30]
- [ ] Skim [A checklist that saves me from endless back-and-forth with Claude ...](https://www.reddit.com/r/ClaudeCode/comments/1mwzk3v/a_checklist_that_saves_me_from_endless/) once more after a week and refine your own pre‑flight checklist based on lived experience.[30]

If you like, the next step can be a version tailored to one concrete repo (e.g., your Kubernetes tooling) where each unit is “do X *in this repo*,” not just “read/watch.”

Sources
[1] Understanding Claude Code's Full Stack: MCP, Skills, Subagents ... https://alexop.dev/posts/understanding-claude-code-full-stack/
[2] Claude Code overview - Claude Code Docs https://code.claude.com/docs/en/overview
[3] Claude Code: Best practices for agentic coding - Anthropic https://www.anthropic.com/engineering/claude-code-best-practices
[4] Claude Code Tutorial #1 - Introduction & Setup - YouTube https://www.youtube.com/watch?v=SUysp3sJHbA
[5] Claude Code Documentation https://www.claudecode.pro/docs/
[6] Understanding Claude Code: Skills vs Commands vs Subagents vs ... https://www.youngleaders.tech/p/claude-skills-commands-subagents-plugins
[7] Claude Code Skills vs MCP vs Sub-agents vs Commands vs Hooks https://www.linkedin.com/posts/lewisowain_claude-code-simplified-activity-7388911764161122304-7j7U
[8] How I Use Every Claude Code Feature - by Shrivu Shankar https://blog.sshh.io/p/how-i-use-every-claude-code-feature
[9] Subagents - Claude Code Docs https://code.claude.com/docs/en/sub-agents
[10] Claude Skills Tutorial: Give your AI Superpowers - Sid Bharath https://www.siddharthbharath.com/claude-skills/
[11] Slash Commands vs Subagents: How to Keep AI Tools Focused https://jxnl.co/writing/2025/08/29/context-engineering-slash-commands-subagents/
[12] VoltAgent/awesome-claude-code-subagents - GitHub https://github.com/VoltAgent/awesome-claude-code-subagents
[13] When should I use a Skill, a Slash Command, or a Sub-Agent in ... https://www.reddit.com/r/ClaudeAI/comments/1orozs4/when_should_i_use_a_skill_a_slash_command_or_a/
[14] Connect Claude Code to tools via MCP https://code.claude.com/docs/en/mcp
[15] How to Quickly Build a MCP Server for Claude Code - Apidog https://apidog.com/blog/how-to-quickly-build-a-mcp-server-for-claude-code/
[16] Build an MCP Server: Complete MCP Tutorial for Beginners https://www.codecademy.com/article/build-an-mcp-server
[17] Claude Code Tutorial #7 - MCP Servers - YouTube https://www.youtube.com/watch?v=X7lgIa6guKg
[18] Understanding Skills, Agents, Subagents, and MCP in Claude Code https://colinmcnamara.com/blog/understanding-skills-agents-and-mcp-in-claude-code
[19] Adding Document Understanding to Claude Code - LlamaIndex https://www.llamaindex.ai/blog/adding-document-understanding-to-claude-code
[20] tell me about claude code gothub app https://www.perplexity.ai/search/cf89e3fd-a299-41c2-b38c-c361e84e1137
[21] Claude Code Tutorial #9 - Claude Code with GitHub - YouTube https://www.youtube.com/watch?v=7pKN_pjPW04
[22] Claude Code + GitHub WORKFLOW for Complex Apps - YouTube https://www.youtube.com/watch?v=FjHtZnjNEBU
[23] How I Turned Claude Code Into My Personal AI Agent Operating ... https://aimaker.substack.com/p/how-i-turned-claude-code-into-personal-ai-agent-operating-system-for-writing-research-complete-guide
[24] 9 months of Claude Code Lessons in 19 minutes - YouTube https://www.youtube.com/watch?v=wxFt2d7xN44
[25] Ultimate guide to extending Claude Code with skills, agents ... https://gist.github.com/alirezarezvani/a0f6e0a984d4a4adc4842bbe124c5935
[26] Claude Code Cheat Sheet: The Reference Guide - Devoriales https://devoriales.com/post/400/claude-code-cheat-sheet-the-reference-guide
[27] Cooking with Claude Code: The Complete Guide - Sid Bharath https://www.siddharthbharath.com/claude-code-the-complete-guide/
[28] claude_code_docs_map.md - Simon Willison https://simonwillison.net/2025/Oct/24/claude-code-docs-map/
[29] ericbuess/claude-code-project-index: PROJECT_INDEX system for ... https://github.com/ericbuess/claude-code-project-index
[30] A checklist that saves me from endless back-and-forth with Claude ... https://www.reddit.com/r/ClaudeCode/comments/1mwzk3v/a_checklist_that_saves_me_from_endless/
[31] How Skills compares to prompts, Projects, MCP, and subagents https://www.claude.com/blog/skills-explained
[32] Created 24 Claude Code learning units (beginner → power user) https://www.reddit.com/r/ClaudeAI/comments/1p62e3o/created_24_claude_code_learning_units_beginner/
[33] 20 Tips to Master Claude Code in 35 Minutes (Build a Real App) https://creatoreconomy.so/p/20-tips-to-master-claude-code-in-35-min-build-an-app
[34] Claude Code not really indexing the codebase, and I am suspicious ... https://www.reddit.com/r/ClaudeAI/comments/1l7i3xy/claude_code_not_really_indexing_the_codebase_and/
[35] The Complete Beginner's Guide to Claude Code (Even If You're Not ... https://www.youtube.com/watch?v=A0SV-DExypQ
[36] Claude Code https://www.claude.com/product/claude-code
[37] The awesome collection of Claude Skills and resources. https://github.com/VoltAgent/awesome-claude-skills
[38] Claude Code Tutorial: Build Full-Stack Apps Without ... https://blogs.pageon.ai/claude-code-tutorial-build-full-stack-apps-without-programming-experience
[39] AI Can't Read Your Docs - by Shrivu Shankar https://blog.sshh.io/p/ai-cant-read-your-docs
[40] Danny Hucke - Skills vs Slash Commands vs Subagents https://www.linkedin.com/posts/danny-hucke-a24a0a1aa_claude-code-skills-vs-slash-commands-vs-activity-7385277219922784256-8EJC
[41] MCP server learning resources - .NET https://learn.microsoft.com/en-us/dotnet/ai/resources/mcp-servers
[42] A Complete Guide to Claude Code - Here are ALL the Best ... https://www.youtube.com/watch?v=amEUIuBKwvg
[43] How I Turned Claude Code Into My Personal Assistant... You ... https://www.youtube.com/watch?v=aYAVSG4Ra40
[44] 800+ hours of Learning Claude Code in 8 minutes (2026 ... https://www.youtube.com/watch?v=Ffh9OeJ7yxw
[45] Njengah/claude-code-cheat-sheet https://github.com/Njengah/claude-code-cheat-sheet
[46] anthropics/claude-cookbooks https://github.com/anthropics/claude-cookbooks
[47] Simon Willison on claude-code https://simonwillison.net/tags/claude-code/
[48] hesreallyhim/awesome-claude-code: A curated list ... https://github.com/hesreallyhim/awesome-claude-code
[49] The Ultimate Guide to Turn Claude Into Your Brain's Most ... https://aimaker.substack.com/p/the-ultimate-guide-to-turn-claude-project-knowledge-into-your-brain-most-valuable-coworker
