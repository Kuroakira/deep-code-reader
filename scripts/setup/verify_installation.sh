#!/bin/bash
# Installation Verification Script
# Checks if all components are properly installed

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 Verifying OSS Learning Platform Installation"
echo "================================================"
echo ""

check_command() {
    local cmd=$1
    local name=$2

    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $name: $(command -v $cmd)"
        return 0
    else
        echo -e "${RED}✗${NC} $name: Not found"
        return 1
    fi
}

check_file() {
    local file=$1
    local name=$2

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $name: $file"
        return 0
    else
        echo -e "${RED}✗${NC} $name: Not found"
        return 1
    fi
}

check_directory() {
    local dir=$1
    local name=$2

    if [ -d "$dir" ]; then
        local count=$(find "$dir" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')
        echo -e "${GREEN}✓${NC} $name: $dir ($count items)"
        return 0
    else
        echo -e "${RED}✗${NC} $name: Not found"
        return 1
    fi
}

# Check dependencies
echo "Dependencies:"
check_command "node" "Node.js"
check_command "npm" "npm"
check_command "python3" "Python 3"
echo ""

# Check MCP servers
echo "MCP Servers:"
if npm list -g @modelcontextprotocol/server-github &> /dev/null; then
    echo -e "${GREEN}✓${NC} GitHub MCP"
else
    echo -e "${YELLOW}⚠${NC} GitHub MCP (not installed globally)"
fi

if npm list -g @notionhq/notion-mcp-server &> /dev/null; then
    echo -e "${GREEN}✓${NC} Notion MCP"
else
    echo -e "${YELLOW}⚠${NC} Notion MCP (not installed globally)"
fi
echo ""

# Check Claude configuration
echo "Claude Configuration:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    CLAUDE_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CLAUDE_CONFIG="$HOME/.config/Claude/claude_desktop_config.json"
fi

check_file "$CLAUDE_CONFIG" "Claude Config"
echo ""

# Check skills
echo "Skills:"
check_directory "$HOME/.claude/skills/deep-code-reader" "deep-code-reader"
echo ""

# Check commands
echo "Slash Commands:"
check_directory "$HOME/.claude/commands" "Commands Directory"
echo ""

# Check configuration files
echo "Configuration:"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
check_file "$REPO_ROOT/config/mcp_servers.json" "MCP Config"
check_file "$REPO_ROOT/config/notion_template.json" "Notion Template"
check_file "$REPO_ROOT/config/default_settings.json" "Default Settings"
echo ""

echo "================================================"
echo "Verification complete!"
echo ""
echo "If any items are missing, run: ./install.sh"
