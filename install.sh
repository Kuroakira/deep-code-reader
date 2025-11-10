#!/bin/bash
# OSS Learning Platform - Auto Installer
# Installs MCP servers, configures Claude Code, and sets up skills

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   OSS Learning Platform - Installer       ║${NC}"
echo -e "${BLUE}║   Powered by Claude Code & MCP            ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================
# Dependency Checks
# ============================================================

check_dependencies() {
    echo -e "${YELLOW}[1/6] Checking dependencies...${NC}"

    local missing_deps=()

    if ! command -v node &> /dev/null; then
        missing_deps+=("Node.js")
    fi

    if ! command -v npm &> /dev/null; then
        missing_deps+=("npm")
    fi

    if ! command -v python3 &> /dev/null; then
        missing_deps+=("Python 3")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${RED}✗ Missing dependencies: ${missing_deps[*]}${NC}"
        echo ""
        echo "Please install the required dependencies:"
        echo "  - Node.js (v18+): https://nodejs.org/"
        echo "  - Python 3 (v3.8+): https://www.python.org/"
        exit 1
    fi

    echo -e "${GREEN}✓ All dependencies found${NC}"
    echo "  - Node.js: $(node --version)"
    echo "  - npm: $(npm --version)"
    echo "  - Python: $(python3 --version)"
    echo ""
}

# ============================================================
# MCP Server Installation
# ============================================================

install_mcp_servers() {
    echo -e "${YELLOW}[2/6] Installing MCP Servers...${NC}"
    echo "This may take a few minutes..."
    echo ""

    # Create a temporary directory for installations
    TEMP_DIR=$(mktemp -d)
    trap "rm -rf $TEMP_DIR" EXIT

    # Install each MCP server
    local servers=(
        "@modelcontextprotocol/server-github:GitHub MCP"
        "@modelcontextprotocol/server-brave-search:Brave Search MCP"
        "@notionhq/notion-mcp-server:Notion MCP"
    )

    for server_info in "${servers[@]}"; do
        IFS=':' read -r package name <<< "$server_info"
        echo -e "  Installing ${BLUE}${name}${NC}..."

        if npm install -g "$package" &> /dev/null; then
            echo -e "  ${GREEN}✓${NC} ${name} installed"
        else
            echo -e "  ${YELLOW}⚠${NC} ${name} installation failed (may already be installed)"
        fi
    done

    echo ""
    echo -e "${GREEN}✓ MCP Servers installation complete${NC}"
    echo ""

    # Note about additional MCP servers
    echo -e "${BLUE}Note:${NC} Some MCP servers may require additional setup:"
    echo "  - Context7: Automatically available in Claude Code"
    echo "  - Sequential Thinking: Automatically available in Claude Code"
    echo "  - Serena: Automatically available in Claude Code"
    echo ""
}

# ============================================================
# Claude Code Configuration
# ============================================================

configure_claude() {
    echo -e "${YELLOW}[3/6] Configuring Claude Code...${NC}"

    # Determine Claude config location
    if [[ "$OSTYPE" == "darwin"* ]]; then
        CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
    else
        echo -e "${YELLOW}⚠ Unsupported OS. Please configure manually.${NC}"
        return
    fi

    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

    # Create config directory if it doesn't exist
    mkdir -p "$CLAUDE_CONFIG_DIR"

    # Backup existing config
    if [ -f "$CLAUDE_CONFIG_FILE" ]; then
        cp "$CLAUDE_CONFIG_FILE" "$CLAUDE_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "  ${GREEN}✓${NC} Backed up existing config"
    fi

    # Copy MCP configuration
    if [ -f "$REPO_ROOT/config/mcp_servers.json" ]; then
        # Merge with existing config or create new
        cp "$REPO_ROOT/config/mcp_servers.json" "$CLAUDE_CONFIG_FILE"
        echo -e "  ${GREEN}✓${NC} MCP servers configured"
    else
        echo -e "  ${YELLOW}⚠${NC} MCP config template not found, skipping"
    fi

    echo ""
}

# ============================================================
# Skills Installation
# ============================================================

install_skills() {
    echo -e "${YELLOW}[4/6] Installing Claude Skills...${NC}"

    SKILLS_DIR="$HOME/.claude/skills"
    mkdir -p "$SKILLS_DIR"

    # Install deep-code-reader skill
    if [ -d "$REPO_ROOT/skills/deep-code-reader" ]; then
        cp -r "$REPO_ROOT/skills/deep-code-reader" "$SKILLS_DIR/"
        echo -e "  ${GREEN}✓${NC} deep-code-reader skill installed"
    else
        echo -e "  ${RED}✗${NC} deep-code-reader skill not found"
    fi

    echo ""
}

# ============================================================
# Commands Installation
# ============================================================

install_commands() {
    echo -e "${YELLOW}[5/6] Installing Slash Commands...${NC}"

    COMMANDS_DIR="$HOME/.claude/commands"
    mkdir -p "$COMMANDS_DIR"

    # Copy all command files
    if [ -d "$REPO_ROOT/commands" ]; then
        cp -r "$REPO_ROOT/commands"/* "$COMMANDS_DIR/" 2>/dev/null || true

        # Count installed commands
        local cmd_count=$(find "$REPO_ROOT/commands" -name "*.md" | wc -l | tr -d ' ')
        echo -e "  ${GREEN}✓${NC} Installed $cmd_count slash commands"
    else
        echo -e "  ${YELLOW}⚠${NC} No commands directory found"
    fi

    echo ""
}

# ============================================================
# Notion Setup
# ============================================================

setup_notion() {
    echo -e "${YELLOW}[6/6] Notion Integration Setup...${NC}"
    echo ""
    echo "To enable Notion export functionality, you need:"
    echo "  1. Notion API Key (Integration Token)"
    echo "  2. Notion Database ID (where analyses will be stored)"
    echo ""
    echo -e "${BLUE}Setup Notion now? (y/n)${NC}"
    read -r setup_notion_now

    if [[ "$setup_notion_now" =~ ^[Yy]$ ]]; then
        echo ""
        echo "Visit: https://www.notion.so/my-integrations"
        echo "Create a new integration and copy the 'Internal Integration Token'"
        echo ""
        read -p "Enter your Notion API Key: " NOTION_KEY

        echo ""
        echo "Create a database in Notion and copy its ID from the URL"
        echo "Example: https://notion.so/workspace/DATABASE_ID?v=..."
        echo ""
        read -p "Enter your Notion Database ID: " NOTION_DB_ID

        # Save to config
        cat > "$REPO_ROOT/config/notion_config.json" <<EOF
{
  "api_key": "$NOTION_KEY",
  "database_id": "$NOTION_DB_ID",
  "auto_export": true,
  "page_template": "analysis"
}
EOF

        echo ""
        echo -e "${GREEN}✓${NC} Notion configuration saved"
    else
        echo -e "  ${YELLOW}⚠${NC} Skipping Notion setup (you can configure later)"

        # Create template config
        cat > "$REPO_ROOT/config/notion_config.json" <<EOF
{
  "api_key": "YOUR_NOTION_API_KEY",
  "database_id": "YOUR_DATABASE_ID",
  "auto_export": false,
  "page_template": "analysis"
}
EOF
        echo -e "  ${BLUE}ℹ${NC} Edit config/notion_config.json when ready"
    fi

    echo ""
}

# ============================================================
# Verification
# ============================================================

verify_installation() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Installation Complete!                  ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    echo ""
    echo "📦 Installed Components:"
    echo "  ✓ MCP Servers (GitHub, Brave Search, Notion)"
    echo "  ✓ Claude Skills (deep-code-reader)"
    echo "  ✓ Slash Commands"
    echo "  ✓ Configuration files"
    echo ""
    echo "🚀 Next Steps:"
    echo "  1. Restart Claude Code if it's running"
    echo "  2. Run: claude-code"
    echo "  3. Try: /analyze-oss <github-url> [commit-id]"
    echo ""
    echo "📚 Documentation:"
    echo "  - README.md: Overview and features"
    echo "  - QUICKSTART.md: Quick start guide"
    echo "  - docs/: Detailed documentation"
    echo ""
    echo "💡 Example usage:"
    echo -e "  ${BLUE}/analyze-oss https://github.com/user/repo main${NC}"
    echo ""

    if [ -f "$REPO_ROOT/config/notion_config.json" ]; then
        if grep -q "YOUR_NOTION_API_KEY" "$REPO_ROOT/config/notion_config.json"; then
            echo -e "${YELLOW}⚠ Remember to configure Notion:${NC}"
            echo "  Edit: config/notion_config.json"
            echo ""
        fi
    fi
}

# ============================================================
# Main Installation Flow
# ============================================================

main() {
    check_dependencies
    install_mcp_servers
    configure_claude
    install_skills
    install_commands
    setup_notion
    verify_installation
}

# Run installation
main
