#!/bin/bash
#
# Setup script for learn-claude-code repository
#
# This script creates symlinks from the repo's example agents, commands, and skills
# to your local .claude directory, making them immediately available in Claude Code.
#
# Why symlinks?
# - Keeps examples version controlled in /agents, /commands, /skills
# - Makes them active in .claude/ where Claude Code expects them
# - Single source of truth - no duplication or sync issues
# - Any updates to examples are instantly available
#

set -e

echo "🚀 Setting up Claude Code environment..."

# Create .claude directory if it doesn't exist
mkdir -p .claude

# Remove existing directories if they exist (but not if they're already symlinks)
for dir in agents commands skills; do
    if [ -d ".claude/$dir" ] && [ ! -L ".claude/$dir" ]; then
        echo "⚠️  Removing existing .claude/$dir directory..."
        rm -rf ".claude/$dir"
    fi
done

# Create symlinks
echo "🔗 Creating symlinks..."
ln -sf ../agents .claude/agents
ln -sf ../commands .claude/commands
ln -sf ../skills .claude/skills

# Verify setup
echo ""
echo "✅ Setup complete!"
echo ""
echo "Symlinks created:"
ls -la .claude/ | grep -E "agents|commands|skills"

echo ""
echo "📚 Example agents, commands, and skills are now active in Claude Code."
echo ""
echo "To use an agent: @agent-name"
echo "To use a command: /command-name"
echo ""
echo "Add new examples to /agents, /commands, or /skills and they'll be instantly available!"
