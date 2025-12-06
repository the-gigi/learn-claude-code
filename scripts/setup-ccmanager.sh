#!/bin/bash
# CCManager Setup Script
# Installs and configures CCManager for managing multiple Claude Code instances

set -e

echo "=================================="
echo "CCManager Setup Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration - not needed, CCManager is interactive

echo "Step 1: Checking prerequisites..."
echo ""

# Check if npm/node is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    echo "Install Node.js from: https://nodejs.org"
    echo "Or use Homebrew: brew install node"
    exit 1
fi
echo -e "${GREEN}✓ npm found ($(npm --version))${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ git found${NC}"

# Check if claude is installed
if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}⚠ Warning: claude command not found${NC}"
    echo "CCManager will work, but you'll need Claude Code installed to use it"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ claude found${NC}"
fi

echo ""
echo "Step 2: Installing CCManager..."
echo ""

# Check if already installed
if command -v ccmanager &> /dev/null; then
    CURRENT_VERSION=$(ccmanager --version 2>&1 || echo "unknown")
    echo -e "${YELLOW}CCManager is already installed${NC}"
    read -p "Reinstall/upgrade? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping installation..."
    else
        npm install -g ccmanager
    fi
else
    # Install via npm
    echo "Installing via npm..."
    npm install -g ccmanager
fi

# Verify installation
if command -v ccmanager &> /dev/null; then
    echo -e "${GREEN}✓ CCManager installed successfully${NC}"
    echo "Version: $(ccmanager --version 2>&1 || echo 'installed')"
else
    echo -e "${RED}✗ CCManager installation failed${NC}"
    exit 1
fi

echo ""
echo "Step 3: Testing installation..."
echo ""

# Test ccmanager
if ccmanager --help > /dev/null 2>&1; then
    echo -e "${GREEN}✓ CCManager is working${NC}"
else
    echo -e "${RED}✗ CCManager test failed${NC}"
    exit 1
fi

echo ""
echo "=================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=================================="
echo ""
echo "CCManager is an interactive TUI application."
echo ""
echo "Basic Usage:"
echo ""
echo "  # Launch the interactive interface"
echo "  ccmanager"
echo ""
echo "  # Or run without installing"
echo "  npx ccmanager"
echo ""
echo "Inside CCManager, you can:"
echo "  • Create new worktrees for different branches"
echo "  • Launch Claude Code in each worktree"
echo "  • See real-time status of each session (busy/waiting/idle)"
echo "  • Copy conversation history between worktrees"
echo "  • Manage multiple projects from one interface"
echo ""
echo "Keyboard shortcuts:"
echo "  • Arrow keys: Navigate"
echo "  • Enter: Select/Execute"
echo "  • Ctrl+E: Return to menu"
echo "  • Ctrl+C: Exit"
echo ""
echo "Next steps:"
echo "  1. cd to your git repo: cd /Users/gigi/git/learn-claude-code"
echo "  2. Run: ccmanager"
echo "  3. Use the interactive menu to create worktrees and launch Claude"
echo ""
echo "More info: https://github.com/kbwo/ccmanager"
echo ""
