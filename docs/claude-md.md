# CLAUDE.md Files

## Overview

CLAUDE.md files are instruction files that tell Claude Code how to work with your project. They're automatically loaded into the context when you run Claude Code.

## File Discovery

Claude Code automatically discovers and loads CLAUDE.md files in this hierarchy:

1. `~/.claude/CLAUDE.md` - Global settings for all projects
2. Project root `CLAUDE.md` - Project-wide instructions
3. Project root `CLAUDE.local.md` - Personal project settings (add to .gitignore)
4. Subdirectory `CLAUDE.md` files - Directory-specific instructions
5. Subdirectory `CLAUDE.local.md` files - Personal directory settings (add to .gitignore)

Both `CLAUDE.md` and `CLAUDE.local.md` work at any level (root or subdirectory). The `.local.md` variant is for personal settings you don't want to commit.

All discovered files are combined into Claude's context when working in that directory.

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
# MyApp Project
Web application using React + FastAPI.

# Commands
- Dev: `npm run dev` (frontend) + `uvicorn main:app` (backend)
- Test: `npm test && pytest`
- Lint: `npm run lint && ruff check .`

# Architecture
- Frontend: src/components/
- Backend: api/
- Shared types: types/
```

**project/CLAUDE.local.md** (personal, gitignored):
```markdown
# Local Settings
- Database: postgresql://localhost/myapp_dev
- Test with --verbose flag
- Deploy to staging before asking
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

Think of CLAUDE.md as living documentation that evolves with your project.
