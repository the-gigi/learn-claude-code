# learn-claude-code

A learning resource repository for mastering Claude Code.

## Project Purpose

This repo contains curated documentation, guides, and references to help developers work effectively with Claude Code. It's designed to be practical, hands-on, and focused on real-world usage patterns.

## Repository Structure

```
/
├── README.md           - Project overview
├── CLAUDE.md           - Project instructions for Claude Code
├── docs/               - Documentation files
│   ├── basics.md           - Fundamental Claude Code concepts and setup
│   ├── study-guide.md      - Comprehensive learning path with checkboxes
│   ├── army-of-claudes.md  - Guide for managing multiple Claude Code sessions
│   ├── claude-md.md        - Documentation about CLAUDE.md files
│   └── slash-commands.md   - Guide to slash commands
├── agents/             - Example custom agents (teaching materials)
├── commands/           - Example custom commands (teaching materials)
├── skills/             - Example custom skills (teaching materials)
└── .claude/            - Personal local Claude Code settings (gitignored)
```

## File Editing Guidelines

### Writing Style

- **Concise and practical** - Focus on actionable information
- **No fluff** - Avoid marketing speak or unnecessary elaboration
- **Code examples** - Show concrete commands and configurations
- **External links** - Link to official docs rather than duplicating content
- **Personal notes welcome** - "YMMV", "I prefer X" are fine

### Format

- Use standard Markdown
- Code blocks with appropriate language tags
- Clear section headers (# and ##)
- Links in markdown format: `[text](url)`
- Checkboxes for study-guide.md: `- [ ]` and `- [x]`

### Study Guide Structure

Each track in `study-guide.md` follows this pattern:

```markdown
## Track N – Topic Name

- [ ] Action item with [linked resource](url) and brief context.
- [ ] Another action with specific deliverable or outcome.
```

Keep items:
- **Single line** - One checkbox, one link, minimal description
- **Actionable** - Clear what to do
- **Linked** - Always include relevant URL
- **Consistent** - Follow existing formatting

## Git Workflow

- Branch naming: `feature/description` or `fix/description`
- This is a documentation repo - no tests to run
- Keep commits focused and well-described
- No need to ask permission for documentation improvements

## Working with This Repo

### Adding New Resources

When adding tutorials or tools to `docs/study-guide.md`:
1. Verify the link works and has actual content
2. Ensure it has step-by-step instructions (not just discussion)
3. Add to the appropriate Track
4. Keep descriptions brief

### Updating docs/army-of-claudes.md

Focus on:
- Practical setup instructions
- Tool comparisons with real use cases
- Command examples
- Workflow patterns

### Adding Example Agents/Commands/Skills

The `/agents`, `/commands`, and `/skills` directories contain teaching examples:
- Add well-commented examples that demonstrate best practices
- Include documentation headers explaining what they do
- These are study materials, not production configs

### Maintenance

- Check for broken links periodically
- Update with new Claude Code features
- Remove outdated information
- Keep file sizes reasonable (CLAUDE.md context matters)

## Custom Tools

None yet - this is a documentation project.

## References

- [Official Claude Code Docs](https://code.claude.com/docs)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
