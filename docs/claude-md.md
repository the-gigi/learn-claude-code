
# CLAUDE.md Files

## Overview

CLAUDE.md files are instruction files that tell Claude Code how to work with your project. They're automatically loaded into the context when you run Claude Code.

## File Discovery

Claude Code automatically discovers and loads CLAUDE.md files in this hierarchy:

1. `~/.claude/CLAUDE.md` - Global settings for all projects
2. Project root `CLAUDE.md` - Project-wide instructions
3. Project root `CLAUDE.local.md` - ⚠️ **Superseded by imports** (see below)
4. Subdirectory `CLAUDE.md` files - Directory-specific instructions
5. Subdirectory `CLAUDE.local.md` files - ⚠️ **Superseded by imports** (see below)

**How files are combined:**
Claude Code combines all CLAUDE.md files from your current directory and parent directories up to the home directory, automatically adding them to the prompt. When working with files in subdirectories, any CLAUDE.md files in those subdirectories are also pulled into the context.

### CLAUDE.local.md → Imports Migration

**`CLAUDE.local.md` files still work but are no longer recommended.** Use `@` imports instead for better git worktree compatibility.

**Problem with CLAUDE.local.md:**
- Git worktrees DON'T copy `.local.md` files (they're gitignored), so you must manually recreate them in each worktree
- When running parallel Claude Code sessions across worktrees, maintaining identical personal settings becomes tedious

**Recommended approach:**
```markdown
# In your project's CLAUDE.md
@~/.claude/the-project/CLAUDE.md
```

This keeps personal settings in your home directory, making them work seamlessly across all git worktrees.

[Official documentation on imports](https://code.claude.com/docs/en/memory#claude-md-imports) | [Git worktrees workflow](https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)

## Best Practices

### Keep It Concise

CLAUDE.md files become part of the prompt. Be concise and relevant:

```markdown
# Good
- Run `npm test` before commits
- Use TypeScript strict mode
- API docs: https://api.example.com

# Too Verbose
- Please make sure to always run the test suite using npm test before making any commits to ensure code quality and prevent regressions...
```

### Structure Your Instructions

Use clear sections:

```markdown
# Project Overview
Brief description of what this project does.

# Commands
- Build: `npm run build`
- Test: `npm test`
- Deploy: `./scripts/deploy.sh`

# Style Guide
- 2 space indentation
- Single quotes for strings
- Add JSDoc comments for public APIs

# Testing
Run tests with `pytest tests/` before submitting PRs.
```

### Document Custom Tools

If you have custom CLI tools, document them:

```markdown
# Custom Tools

## db-migrate
Database migration tool.
Usage: `db-migrate up|down|status`
Config: `config/database.yml`

## gen-api
API code generator.
Usage: `gen-api spec.yaml output/`
```

### Add Context Inline

Use the `#` directive to add context on the fly:

```
# claude, remember we're using Python 3.11 and mypy strict mode
```

This adds temporary context without editing CLAUDE.md.

## Hierarchy Example

**~/.claude/CLAUDE.md** (global):
```markdown
# Global Preferences
- Don't use emojis unless requested
- Run mypy on Python changes
- Always show git diff before commits
```

**project/CLAUDE.md** (project):
```markdown
# The App Project
Web application using React + FastAPI.

# Commands
- Dev: `npm run dev` (frontend) + `uvicorn main:app` (backend)
- Test: `npm test && pytest`
- Lint: `npm run lint && ruff check .`

# Architecture
- Backend: api/
- Web Frontend: src/components/
- Console Frontend: cli/
- Shared types: types/

# Personal Preferences
@~/.claude/projects/the-app/CLAUDE.md
```

**~/.claude/projects/the-app/CLAUDE.md** (personal, in home directory):
```markdown
# MyApp Local Settings
- Database: postgresql://localhost/the_app_dev
- Test with --verbose flag
- Deploy to staging with approval
```

## Common Patterns

### Commit Guidelines

```markdown
# Git Workflow
- Branch naming: feature/description or fix/description
- Run tests before commit
- Keep commits atomic and well-described
- Never force push to main
```

### Tool Configuration

```markdown
# Development Setup
- Python 3.11+ required
- Install: `poetry install`
- Activate: `poetry shell`
- Environment: Copy `.env.example` to `.env`
```

### Project Map

```markdown
# Project Structure
- `src/` - Main application code
- `tests/` - Test suite
- `docs/` - Documentation
- `scripts/` - Build and deployment scripts
- `config/` - Configuration files
```

## Anti-Patterns

### Don't Include

❌ Large documentation dumps
❌ Full API references (link instead)
❌ Obvious information ("use git for version control")
❌ Outdated instructions

### Do Include

✅ Project-specific commands
✅ Non-standard workflows
✅ Custom tool documentation
✅ Team conventions
✅ Links to external docs

## Maintenance

Review and update your CLAUDE.md files regularly:

- Remove outdated instructions
- Add new tools and commands
- Update links
- Refine based on what Claude asks repeatedly
- Use the inline `#` directive to test new instructions before adding them permanently
- Keep files concise - they become part of the prompt, so avoid overwhelming detail

Think of CLAUDE.md files as living documentation that evolves with your project.

## Command-Line Tools

Claude Code has access to the shell environment that launched it, including all installed command-line tools like `git`, `curl`, `ls`, etc. For custom tools specific to your project, document them in your CLAUDE.md files so Claude understands how to use them (see "Document Custom Tools" section above).
