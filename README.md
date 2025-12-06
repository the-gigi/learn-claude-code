# learn-claude-code

A curated learning resource for mastering Claude Code - practical guides, examples, and tools for effective AI-assisted development.

## Overview

This repository contains:
- **Documentation** - Comprehensive guides and tutorials in `/docs`
- **Study Guide** - Structured learning path with checkboxes
- **Example Agents** - Custom Claude Code agents in `/agents`
- **Example Commands** - Custom slash commands in `/commands`
- **Example Skills** - Reusable skills in `/skills`

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/learn-claude-code.git
   cd learn-claude-code
   ```

2. **Run the setup script:**
   ```bash
   ./scripts/setup-claude.sh
   ```

3. **Start exploring:**
   - Read `docs/basics.md` for fundamentals
   - Follow `docs/study-guide.md` for a structured learning path
   - Try the example agents with `@agent-name` in Claude Code

## Setup Script Explained

The `setup-claude.sh` script creates **symlinks** from the example directories to your local `.claude/` directory:

```
/agents     -> .claude/agents
/commands   -> .claude/commands
/skills     -> .claude/skills
```

**Why symlinks?**

- ✅ **Version controlled examples** - Teaching materials stay in the repo
- ✅ **Instantly active** - Claude Code finds them in `.claude/`
- ✅ **Single source of truth** - No duplication or sync issues
- ✅ **Live updates** - Edits to examples are immediately available
- ✅ **Easy contribution** - Add examples to `/agents` and they work instantly

**What happens:**
1. Creates `.claude/` directory if it doesn't exist
2. Removes any existing directories (preserves existing symlinks)
3. Creates symlinks to `/agents`, `/commands`, `/skills`
4. Verifies setup and shows you what was linked

This means you can add new teaching examples to the repo directories and they're automatically available in Claude Code - perfect for a learning repository!

## Repository Structure

```
/
├── README.md                      # You are here
├── CLAUDE.md                      # Project instructions for Claude Code
├── docs/                          # Documentation
│   ├── basics.md                  # Fundamentals and setup
│   ├── study-guide.md             # Structured learning path
│   ├── army-of-claudes.md         # Managing multiple sessions
│   ├── claude-md.md               # Guide to CLAUDE.md files
│   └── slash-commands.md          # Slash commands guide
├── agents/                        # Example custom agents
│   └── claude-code-expert.md      # Claude Code configuration expert
├── commands/                      # Example custom commands
├── skills/                        # Example custom skills
├── scripts/                       # Utility scripts
│   └── setup-claude.sh            # Setup script for symlinks
└── .claude/                       # Local Claude Code settings (gitignored)
    ├── agents -> ../agents        # Symlink to examples
    ├── commands -> ../commands    # Symlink to examples
    └── skills -> ../skills        # Symlink to examples
```

## Learning Path

1. **Start with basics** - Read `docs/basics.md`
2. **Follow the guide** - Work through `docs/study-guide.md`
3. **Explore examples** - Try the agents, commands, and skills
4. **Setup parallel sessions** - Learn from `docs/army-of-claudes.md`
5. **Contribute** - Add your own examples and improvements

## Using Example Agents

After running setup, example agents are available:

```bash
# In Claude Code:
@claude-code-expert help me set up CLAUDE.md for my project
```

## Contributing

Contributions welcome! To add examples:

1. Add agents to `/agents/agent-name.md`
2. Add commands to `/commands/command-name.md`
3. Add skills to `/skills/skill-name.md`
4. They're instantly available via the symlinks

See `CLAUDE.md` for style guidelines and contribution details.

## Resources

- [Official Claude Code Docs](https://code.claude.com/docs)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Study Guide](docs/study-guide.md) - Comprehensive learning path

## License

MIT License - See [LICENSE](LICENSE) for details.
