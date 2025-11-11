#!/bin/bash
# OSS Learning Platform - Uninstaller
# Safely removes all installed components

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Track what will be removed
ITEMS_TO_REMOVE=()
TOTAL_SIZE=0

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   OSS Learning Platform - Uninstaller     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================
# Safety Checks
# ============================================================

check_installed_components() {
    echo -e "${YELLOW}Scanning for installed components...${NC}"
    echo ""

    local found_items=0

    # Check Claude Skills
    if [ -d "$HOME/.claude/skills/deep-code-reader" ]; then
        local size=$(du -sh "$HOME/.claude/skills/deep-code-reader" 2>/dev/null | cut -f1)
        ITEMS_TO_REMOVE+=("skill:$HOME/.claude/skills/deep-code-reader:$size")
        echo -e "  ${GREEN}✓${NC} Claude Skill: deep-code-reader ($size)"
        ((found_items++))
    fi

    # Check Slash Commands
    if [ -d "$HOME/.claude/commands" ]; then
        local cmd_count=$(find "$HOME/.claude/commands" -name "*.md" -path "*/deep-code-reader/*" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$cmd_count" -gt 0 ]; then
            local size=$(du -sh "$HOME/.claude/commands" 2>/dev/null | cut -f1)
            ITEMS_TO_REMOVE+=("commands:$HOME/.claude/commands:$size")
            echo -e "  ${GREEN}✓${NC} Slash Commands: $cmd_count commands ($size)"
            ((found_items++))
        fi
    fi

    # Check MCP Servers
    local mcp_servers=(
        "@modelcontextprotocol/server-github"
        "@notionhq/notion-mcp-server"
    )

    for package in "${mcp_servers[@]}"; do
        if npm list -g "$package" &>/dev/null; then
            ITEMS_TO_REMOVE+=("mcp:$package:npm")
            echo -e "  ${GREEN}✓${NC} MCP Server: $package"
            ((found_items++))
        fi
    done

    # Check Claude Desktop Config
    if [[ "$OSTYPE" == "darwin"* ]]; then
        CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
    fi

    CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

    if [ -f "$CLAUDE_CONFIG_FILE" ]; then
        local size=$(du -sh "$CLAUDE_CONFIG_FILE" 2>/dev/null | cut -f1)

        # Check for backups
        local backup_count=$(find "$CLAUDE_CONFIG_DIR" -name "claude_desktop_config.json.backup.*" 2>/dev/null | wc -l | tr -d ' ')

        ITEMS_TO_REMOVE+=("config:$CLAUDE_CONFIG_FILE:$size")
        echo -e "  ${GREEN}✓${NC} Claude Config: claude_desktop_config.json ($size)"

        if [ "$backup_count" -gt 0 ]; then
            echo -e "  ${BLUE}ℹ${NC} Found $backup_count backup(s) of config file"
        fi

        ((found_items++))
    fi

    # Check Notion Config
    if [ -f "$REPO_ROOT/config/notion_config.json" ]; then
        if ! grep -q "YOUR_NOTION_API_KEY" "$REPO_ROOT/config/notion_config.json" 2>/dev/null; then
            ITEMS_TO_REMOVE+=("notion:$REPO_ROOT/config/notion_config.json:configured")
            echo -e "  ${GREEN}✓${NC} Notion Config: configured (will preserve by default)"
            ((found_items++))
        fi
    fi

    echo ""

    if [ "$found_items" -eq 0 ]; then
        echo -e "${YELLOW}No installed components found.${NC}"
        echo "The platform may not be installed, or was already uninstalled."
        echo ""
        exit 0
    fi

    echo -e "Found ${GREEN}$found_items${NC} component(s) to remove."
    echo ""
}

# ============================================================
# Uninstall Functions
# ============================================================

remove_skills() {
    echo -e "${YELLOW}Removing Claude Skills...${NC}"

    if [ -d "$HOME/.claude/skills/deep-code-reader" ]; then
        rm -rf "$HOME/.claude/skills/deep-code-reader"
        echo -e "  ${GREEN}✓${NC} Removed deep-code-reader skill"
    fi

    echo ""
}

remove_commands() {
    echo -e "${YELLOW}Removing Slash Commands...${NC}"

    if [ -d "$HOME/.claude/commands" ]; then
        # List of deep-code-reader commands
        local dcr_commands=(
            "analyze-commit.md"
            "analyze-pr.md"
            "current-oss.md"
            "export-analysis.md"
            "list-commits.md"
            "list-prs.md"
            "register-oss.md"
            "setup-notion.md"
        )

        local removed_count=0
        for cmd in "${dcr_commands[@]}"; do
            if [ -f "$HOME/.claude/commands/$cmd" ]; then
                rm "$HOME/.claude/commands/$cmd"
                ((removed_count++))
            fi
        done

        if [ $removed_count -gt 0 ]; then
            echo -e "  ${GREEN}✓${NC} Removed $removed_count deep-code-reader commands"
        else
            echo -e "  ${BLUE}ℹ${NC} No deep-code-reader commands found"
        fi

        # Count remaining commands
        local remaining=$(find "$HOME/.claude/commands" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$remaining" -eq 0 ]; then
            rm -rf "$HOME/.claude/commands"
            echo -e "  ${GREEN}✓${NC} Removed empty commands directory"
        fi
    else
        echo -e "  ${BLUE}ℹ${NC} No commands directory found"
    fi

    echo ""
}

remove_mcp_servers() {
    echo -e "${YELLOW}MCP Server Removal...${NC}"
    echo ""
    echo -e "${BLUE}MCP servers may be used by other projects or workflows.${NC}"
    echo "Select which MCP servers you want to remove:"
    echo ""

    local servers=(
        "@modelcontextprotocol/server-github:GitHub MCP"
        "@notionhq/notion-mcp-server:Notion MCP"
    )

    local to_remove=()
    local found_count=0

    # Show installed servers and ask for each
    for server_info in "${servers[@]}"; do
        IFS=':' read -r package name <<< "$server_info"

        if npm list -g "$package" &>/dev/null; then
            ((found_count++))
            echo -e "  ${GREEN}✓${NC} ${name} is installed"
            echo -e "    ${BLUE}Remove ${name}? (y/n)${NC}"
            read -r remove_this

            if [[ "$remove_this" =~ ^[Yy]$ ]]; then
                to_remove+=("$package:$name")
                echo -e "    ${YELLOW}→${NC} Marked for removal"
            else
                echo -e "    ${GREEN}→${NC} Will keep installed"
            fi
            echo ""
        fi
    done

    if [ "$found_count" -eq 0 ]; then
        echo -e "  ${BLUE}ℹ${NC} No MCP servers from this platform are installed"
        echo ""
        return
    fi

    # Remove selected servers
    if [ ${#to_remove[@]} -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}Removing ${#to_remove[@]} MCP server(s)...${NC}"
        echo ""

        for server_info in "${to_remove[@]}"; do
            IFS=':' read -r package name <<< "$server_info"
            echo -e "  Uninstalling ${BLUE}${name}${NC}..."

            if npm uninstall -g "$package" &>/dev/null; then
                echo -e "  ${GREEN}✓${NC} Removed $name"
            else
                echo -e "  ${RED}✗${NC} Failed to remove $name (may need sudo)"
            fi
        done
    else
        echo -e "${GREEN}✓ Keeping all MCP servers installed${NC}"
    fi

    echo ""
}

restore_claude_config() {
    echo -e "${YELLOW}Handling Claude Config...${NC}"

    if [ -f "$CLAUDE_CONFIG_FILE" ]; then
        # Find most recent backup
        local latest_backup=$(find "$CLAUDE_CONFIG_DIR" -name "claude_desktop_config.json.backup.*" 2>/dev/null | sort -r | head -n1)

        if [ -n "$latest_backup" ]; then
            echo -e "  ${BLUE}Found backup:${NC} $(basename "$latest_backup")"
            echo -e "  ${BLUE}Restore backup? (y/n)${NC}"
            read -r restore_backup

            if [[ "$restore_backup" =~ ^[Yy]$ ]]; then
                cp "$latest_backup" "$CLAUDE_CONFIG_FILE"
                echo -e "  ${GREEN}✓${NC} Restored config from backup"

                # Ask if we should clean up other backups
                local backup_count=$(find "$CLAUDE_CONFIG_DIR" -name "claude_desktop_config.json.backup.*" 2>/dev/null | wc -l | tr -d ' ')
                if [ "$backup_count" -gt 1 ]; then
                    echo -e "  ${BLUE}Remove all backups? (y/n)${NC}"
                    read -r remove_backups
                    if [[ "$remove_backups" =~ ^[Yy]$ ]]; then
                        find "$CLAUDE_CONFIG_DIR" -name "claude_desktop_config.json.backup.*" -delete
                        echo -e "  ${GREEN}✓${NC} Removed all backup files"
                    fi
                fi
            else
                echo -e "  ${YELLOW}⚠${NC} Keeping current config (backup preserved)"
            fi
        else
            echo -e "  ${YELLOW}⚠${NC} No backup found"
            echo -e "  ${BLUE}Remove current config? (y/n)${NC}"
            read -r remove_config

            if [[ "$remove_config" =~ ^[Yy]$ ]]; then
                rm "$CLAUDE_CONFIG_FILE"
                echo -e "  ${GREEN}✓${NC} Removed Claude config"
            else
                echo -e "  ${YELLOW}⚠${NC} Keeping current config"
            fi
        fi
    fi

    echo ""
}

handle_notion_config() {
    echo -e "${YELLOW}Handling Deep Code Reader Data...${NC}"

    # Check deep-code-reader directory
    DEEP_CODE_READER_DIR="$HOME/.claude/deep-code-reader"
    if [ -d "$DEEP_CODE_READER_DIR" ]; then
        echo -e "  ${BLUE}Found deep-code-reader directory${NC}"
        echo -e "  ${YELLOW}Contains: config, scripts, and cloned repositories${NC}"
        echo -e "  ${BLUE}Remove entire deep-code-reader directory? (y/n)${NC}"
        read -r remove_dcr

        if [[ "$remove_dcr" =~ ^[Yy]$ ]]; then
            rm -rf "$DEEP_CODE_READER_DIR"
            echo -e "  ${GREEN}✓${NC} Removed ~/.claude/deep-code-reader/"
        else
            echo -e "  ${YELLOW}⚠${NC} Keeping deep-code-reader data"
        fi
    else
        echo -e "  ${BLUE}ℹ${NC} No deep-code-reader directory found"
    fi

    # Also check old project-local config location (for backwards compatibility)
    if [ -f "$REPO_ROOT/config/notion_config.json" ]; then
        echo -e "  ${YELLOW}⚠${NC} Found old config at $REPO_ROOT/config/notion_config.json"
        echo -e "  ${BLUE}Remove old config? (y/n)${NC}"
        read -r remove_old

        if [[ "$remove_old" =~ ^[Yy]$ ]]; then
            rm "$REPO_ROOT/config/notion_config.json"
            echo -e "  ${GREEN}✓${NC} Removed old Notion config"
        fi
    fi

    echo ""
}

# ============================================================
# Main Uninstall Flow
# ============================================================

main() {
    check_installed_components

    echo -e "${RED}╔════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║   WARNING: This will remove components    ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════╝${NC}"
    echo ""
    echo "This will remove:"
    echo "  • Claude Skills (deep-code-reader)"
    echo "  • Slash Commands"
    echo "  • MCP Servers (you'll choose which ones to remove)"
    echo "  • Claude Desktop Config (with option to restore from backup)"
    echo ""
    echo -e "${YELLOW}Your Notion data will NOT be affected.${NC}"
    echo -e "${BLUE}You'll be asked to confirm removal of each MCP server.${NC}"
    echo ""
    echo -e "${RED}Are you sure you want to continue? (yes/no)${NC}"
    read -r confirm

    if [[ ! "$confirm" =~ ^[Yy][Ee][Ss]$ ]]; then
        echo -e "${BLUE}Uninstall cancelled.${NC}"
        exit 0
    fi

    echo ""
    echo -e "${YELLOW}Starting uninstallation...${NC}"
    echo ""

    # Remove components
    remove_skills
    remove_commands
    remove_mcp_servers
    restore_claude_config
    handle_notion_config

    # Summary
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Uninstallation Complete!                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    echo ""
    echo "🗑️  Removed Components:"
    echo "  ✓ Claude Skills"
    echo "  ✓ Slash Commands"
    echo "  ✓ MCP Servers"
    echo ""
    echo "📋 Next Steps:"
    echo "  1. Restart Claude Code to apply changes"
    echo "  2. (Optional) Remove this directory: $REPO_ROOT"
    echo ""
    echo "💡 To reinstall:"
    echo "  Run: ./install.sh"
    echo ""
    echo -e "${BLUE}Thank you for trying OSS Learning Platform!${NC}"
    echo ""
}

# Run uninstallation
main
