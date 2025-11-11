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

check_mcp_installed() {
    local package=$1
    if npm list -g "$package" &>/dev/null; then
        return 0  # Already installed
    else
        return 1  # Not installed
    fi
}

install_mcp_servers() {
    echo -e "${YELLOW}[2/6] Installing MCP Servers...${NC}"
    echo ""

    # Required MCP servers for this platform
    echo -e "${BLUE}Required MCP Servers:${NC}"
    local required_servers=(
        "@modelcontextprotocol/server-github:GitHub MCP:required"
        "@modelcontextprotocol/server-brave-search:Brave Search MCP:required"
        "@notionhq/notion-mcp-server:Notion MCP:required"
    )

    local to_install=()
    local already_installed=()

    # Check which servers are already installed
    for server_info in "${required_servers[@]}"; do
        IFS=':' read -r package name type <<< "$server_info"

        if check_mcp_installed "$package"; then
            already_installed+=("$name")
            echo -e "  ${GREEN}✓${NC} ${name} (already installed)"
        else
            to_install+=("$package:$name:$type")
            echo -e "  ${YELLOW}○${NC} ${name} (will install)"
        fi
    done

    echo ""

    # Optional MCP servers
    echo -e "${BLUE}Optional MCP Servers:${NC}"
    echo "Additional MCP servers can enhance functionality."
    echo ""
    echo "Would you like to install optional MCP servers? (y/n)"
    echo -e "${YELLOW}Note: Context7, Sequential Thinking, and Serena are built into Claude Code${NC}"

    read -r install_optional

    if [[ "$install_optional" =~ ^[Yy]$ ]]; then
        local optional_servers=(
            # Add any optional npm-based MCP servers here
            # Example: "@someorg/some-mcp-server:Some MCP:optional"
        )

        if [ ${#optional_servers[@]} -eq 0 ]; then
            echo -e "  ${BLUE}ℹ${NC} No additional optional servers available at this time"
        else
            for server_info in "${optional_servers[@]}"; do
                IFS=':' read -r package name type <<< "$server_info"

                if check_mcp_installed "$package"; then
                    already_installed+=("$name")
                    echo -e "  ${GREEN}✓${NC} ${name} (already installed)"
                else
                    echo -e "  ${BLUE}Install ${name}? (y/n)${NC}"
                    read -r install_this
                    if [[ "$install_this" =~ ^[Yy]$ ]]; then
                        to_install+=("$package:$name:$type")
                        echo -e "  ${YELLOW}○${NC} ${name} (will install)"
                    else
                        echo -e "  ${YELLOW}⊘${NC} ${name} (skipped)"
                    fi
                fi
            done
        fi
    fi

    echo ""

    # Install selected servers
    if [ ${#to_install[@]} -gt 0 ]; then
        echo -e "${YELLOW}Installing ${#to_install[@]} MCP server(s)...${NC}"
        echo "This may take a few minutes..."
        echo ""

        for server_info in "${to_install[@]}"; do
            IFS=':' read -r package name type <<< "$server_info"
            echo -e "  Installing ${BLUE}${name}${NC}..."

            if npm install -g "$package" &> /dev/null; then
                echo -e "  ${GREEN}✓${NC} ${name} installed successfully"
            else
                echo -e "  ${RED}✗${NC} ${name} installation failed"
            fi
        done
        echo ""
    else
        echo -e "${GREEN}All required MCP servers already installed!${NC}"
        echo ""
    fi

    # Summary
    if [ ${#already_installed[@]} -gt 0 ]; then
        echo -e "${GREEN}✓ Already installed (${#already_installed[@]}):${NC}"
        for name in "${already_installed[@]}"; do
            echo "  - $name"
        done
        echo ""
    fi

    echo -e "${GREEN}✓ MCP Servers setup complete${NC}"
    echo ""

    # Note about built-in MCP servers
    echo -e "${BLUE}Built-in Claude Code MCP Servers:${NC}"
    echo "  ✓ Context7 - Official library documentation"
    echo "  ✓ Sequential Thinking - Multi-step reasoning"
    echo "  ✓ Serena - Semantic code understanding"
    echo "  ${YELLOW}(No installation needed - automatically available)${NC}"
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

    # Note: Notion API key will be set by setup_notion() function later
    # This function only sets up the MCP server structure

    # Create or merge MCP configuration
    if [ -f "$CLAUDE_CONFIG_FILE" ]; then
        # Merge with existing config using Python
        python3 << EOF
import json
import sys

try:
    # Read existing config
    with open('$CLAUDE_CONFIG_FILE', 'r') as f:
        existing = json.load(f)
except:
    existing = {}

# Ensure mcpServers exists
if 'mcpServers' not in existing:
    existing['mcpServers'] = {}

# Add MCP servers
mcp_servers = {
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {
            "GITHUB_PERSONAL_ACCESS_TOKEN": ""
        }
    },
    "brave-search": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-brave-search"],
        "env": {
            "BRAVE_API_KEY": ""
        }
    },
    "notion": {
        "command": "npx",
        "args": ["-y", "@notionhq/notion-mcp-server"],
        "env": {
            "NOTION_API_KEY": ""
        }
    }
}

# Merge servers (preserve existing tokens if present)
for server_name, server_config in mcp_servers.items():
    if server_name not in existing['mcpServers']:
        existing['mcpServers'][server_name] = server_config
    else:
        # Preserve existing environment variables
        if 'env' in existing['mcpServers'][server_name]:
            for key, value in server_config['env'].items():
                if key not in existing['mcpServers'][server_name]['env'] or not existing['mcpServers'][server_name]['env'][key]:
                    existing['mcpServers'][server_name]['env'][key] = value

# Write back
with open('$CLAUDE_CONFIG_FILE', 'w') as f:
    json.dump(existing, f, indent=2)

print("success")
EOF

        if [ $? -eq 0 ]; then
            echo -e "  ${GREEN}✓${NC} MCP servers configured (merged with existing)"
        else
            echo -e "  ${RED}✗${NC} Failed to merge MCP config"
        fi
    else
        # Create new config
        if [ -f "$REPO_ROOT/config/mcp_servers.json" ]; then
            # Use template and inject Notion API key
            python3 << EOF
import json

with open('$REPO_ROOT/config/mcp_servers.json', 'r') as f:
    config = json.load(f)

# Notion API key will be set by setup_notion() function

with open('$CLAUDE_CONFIG_FILE', 'w') as f:
    json.dump(config, f, indent=2)
EOF
            echo -e "  ${GREEN}✓${NC} MCP servers configured (new)"
        else
            echo -e "  ${YELLOW}⚠${NC} MCP config template not found, skipping"
        fi
    fi

    echo ""
    echo -e "${BLUE}ℹ${NC} MCP Server Notes:"
    echo "  • MCP servers configured in: $CLAUDE_CONFIG_FILE"
    echo "  • Notion API key will be set in next step"
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
# Scripts Installation
# ============================================================

install_scripts() {
    echo -e "${YELLOW}[6/7] Installing Scripts...${NC}"

    SCRIPTS_DIR="$HOME/.claude/deep-code-reader/scripts"
    mkdir -p "$SCRIPTS_DIR/utils"

    # Copy scripts
    if [ -d "$REPO_ROOT/scripts" ]; then
        cp "$REPO_ROOT/scripts/update_notion_mcp.py" "$SCRIPTS_DIR/" 2>/dev/null || true
        cp -r "$REPO_ROOT/scripts/utils"/* "$SCRIPTS_DIR/utils/" 2>/dev/null || true

        echo -e "  ${GREEN}✓${NC} Installed scripts to ~/.claude/deep-code-reader/scripts/"
    else
        echo -e "  ${YELLOW}⚠${NC} No scripts directory found"
    fi

    echo ""
}

# ============================================================
# Notion Setup
# ============================================================

setup_notion() {
    echo -e "${YELLOW}[7/7] Notion Integration Setup...${NC}"
    echo ""
    echo -e "${BLUE}Notion Integration (Optional but Recommended)${NC}"
    echo ""
    echo "Notion integration enables:"
    echo "  • Automatic export of code analysis results"
    echo "  • Organized repository and commit tracking"
    echo "  • Team collaboration and knowledge sharing"
    echo ""
    echo -e "${BLUE}Setup Notion integration now? (y/n)${NC}"
    read -r setup_notion_now

    if [[ "$setup_notion_now" =~ ^[Yy]$ ]]; then
        echo ""
        echo "╔════════════════════════════════════════════╗"
        echo "║   Notion Integration Setup                ║"
        echo "╚════════════════════════════════════════════╝"
        echo ""
        echo "📝 Step 1: Create Notion Integration"
        echo ""
        echo "1. Open in browser: https://www.notion.so/profile/integrations"
        echo "2. Click 'New integration' or '+ Create new integration'"
        echo "3. Name it: 'Deep Code Reader' (or your choice)"
        echo "4. Select your workspace"
        echo "5. Capabilities needed:"
        echo "   ✓ Read content"
        echo "   ✓ Update content"
        echo "   ✓ Insert content"
        echo "6. Click 'Submit'"
        echo "7. Copy the 'Internal Integration Secret'"
        echo ""
        echo "The token should start with 'secret_' or 'ntn_'"
        echo ""
        read -p "Enter your Notion API Key: " NOTION_KEY

        # Validate API key format
        if [[ ! "$NOTION_KEY" =~ ^(secret_|ntn_) ]]; then
            echo ""
            echo -e "${YELLOW}⚠ Warning: API key doesn't match expected format${NC}"
            echo "Expected: secret_xxx... or ntn_xxx..."
            echo "Got: ${NOTION_KEY:0:10}..."
            echo ""
            echo -e "${BLUE}Continue anyway? (y/n)${NC}"
            read -r continue_anyway
            if [[ ! "$continue_anyway" =~ ^[Yy]$ ]]; then
                echo -e "${YELLOW}⚠ Skipping Notion setup${NC}"
                NOTION_KEY=""
            fi
        fi

        if [ -n "$NOTION_KEY" ]; then
            # Save config to deep-code-reader directory
            mkdir -p "$HOME/.claude/deep-code-reader"
            cat > "$HOME/.claude/deep-code-reader/notion_config.json" <<EOF
{
  "api_key": "$NOTION_KEY",
  "workspace_page_id": "",
  "oss_database_id": "",
  "auto_export": false,
  "setup_complete": false
}
EOF

            echo ""
            echo -e "${GREEN}✓${NC} Notion API key saved to ~/.claude/deep-code-reader/notion_config.json"
            echo ""

            # Update MCP configurations
            echo "📝 Step 2: Configuring MCP Servers..."
            echo ""

            if python3 "$HOME/.claude/deep-code-reader/scripts/update_notion_mcp.py" "$NOTION_KEY"; then
                echo ""
                echo -e "${GREEN}✓${NC} MCP configurations updated successfully"
                echo ""
                echo "╔════════════════════════════════════════════╗"
                echo "║   Initial Setup Complete!                 ║"
                echo "╚════════════════════════════════════════════╝"
                echo ""
                echo -e "${GREEN}✅ What's been configured:${NC}"
                echo "  ✓ Notion API key saved"
                echo "  ✓ Claude Desktop MCP configured"
                echo "  ✓ Claude Code CLI MCP configured"
                echo ""
                echo -e "${YELLOW}📝 Next Steps (after installation):${NC}"
                echo "  1. Grant integration access to a workspace page:"
                echo "     • Go to: https://www.notion.so/profile/integrations"
                echo "     • Click on your integration"
                echo "     • Click 'アクセス' (Access) tab"
                echo "     • Click 'アクセス権限を編集'"
                echo "     • Select a page to use as workspace"
                echo ""
                echo "  2. Start Claude Code: claude-code"
                echo "  3. Run: /setup-notion"
                echo "  4. The wizard will:"
                echo "     • Ask for workspace page URL"
                echo "     • Automatically create databases"
                echo "     • Complete the setup"
                echo ""
            else
                echo ""
                echo -e "${RED}✗${NC} Failed to update MCP configurations"
                echo ""
                echo -e "${YELLOW}You can update manually later by running:${NC}"
                echo "  python3 ~/.claude/deep-code-reader/scripts/update_notion_mcp.py \"$NOTION_KEY\""
                echo ""
            fi
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} Skipping Notion setup"

        # Create empty config in deep-code-reader directory
        mkdir -p "$HOME/.claude/deep-code-reader"
        cat > "$HOME/.claude/deep-code-reader/notion_config.json" <<EOF
{
  "api_key": "",
  "workspace_page_id": "",
  "oss_database_id": "",
  "auto_export": false,
  "setup_complete": false
}
EOF

        echo ""
        echo -e "${BLUE}ℹ${NC} To set up Notion later:"
        echo "  1. Get API key: https://www.notion.so/my-integrations"
        echo "  2. Run: python3 ~/.claude/deep-code-reader/scripts/update_notion_mcp.py <api_key>"
        echo "  3. Restart Claude Code"
        echo "  4. Run: /setup-notion"
        echo ""
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
    echo "  1. Start Claude Code: claude-code"

    # Check Notion setup status
    NOTION_CONFIGURED=false
    if [ -f "$HOME/.claude/deep-code-reader/notion_config.json" ]; then
        NOTION_API_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.claude/deep-code-reader/notion_config.json')).get('api_key', ''))" 2>/dev/null || echo "")
        if [ -n "$NOTION_API_KEY" ]; then
            NOTION_CONFIGURED=true
        fi
    fi

    if [ "$NOTION_CONFIGURED" = true ]; then
        echo "  2. Complete Notion setup: /setup-notion"
        echo "     (Notion API key already configured)"
        echo ""
        echo -e "${GREEN}✓ Notion MCP ready!${NC}"
        echo "  The /setup-notion wizard will:"
        echo "  • Ask for workspace page URL"
        echo "  • Automatically create databases"
        echo "  • Complete integration"
    else
        echo "  2. (Optional) Set up Notion later:"
        echo "     - Get API key: https://www.notion.so/my-integrations"
        echo "     - Run: python3 ~/.claude/deep-code-reader/scripts/update_notion_mcp.py <api_key>"
        echo "     - Restart Claude Code"
        echo "     - Run: /setup-notion"
    fi

    echo ""
    echo "📚 Documentation:"
    echo "  - README.md: Overview and features"
    echo "  - QUICKSTART.md: Quick start guide"
    echo "  - docs/: Detailed documentation"
    echo ""
    echo "💡 Quick Start:"
    if [ "$NOTION_CONFIGURED" = true ]; then
        echo -e "  ${BLUE}# Complete Notion setup${NC}"
        echo -e "  ${BLUE}/setup-notion${NC}"
        echo ""
    fi
    echo -e "  ${BLUE}# Register repository${NC}"
    echo -e "  ${BLUE}/register-oss https://github.com/user/repo${NC}"
    echo ""
    echo -e "  ${BLUE}# Analyze commits${NC}"
    echo -e "  ${BLUE}/analyze-commit abc1234${NC}"
    echo ""
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
    install_scripts
    setup_notion
    verify_installation
}

# Run installation
main
