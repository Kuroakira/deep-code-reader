#!/usr/bin/env python3
"""
Update Notion MCP server configuration in Claude Desktop config
"""

import json
import os
import sys
from pathlib import Path

def get_claude_config_paths():
    """Get both Claude Desktop and Claude Code CLI config file paths"""
    paths = []

    # Claude Desktop config
    if sys.platform == "darwin":
        paths.append(Path.home() / "Library/Application Support/Claude/claude_desktop_config.json")
    elif sys.platform == "linux":
        paths.append(Path.home() / ".config/Claude/claude_desktop_config.json")

    # Claude Code CLI config
    claude_cli_config = Path.home() / ".claude/.mcp.json"
    if claude_cli_config.parent.exists():
        paths.append(claude_cli_config)

    return paths

def update_notion_api_key(config_path, api_key):
    """Update Notion API key in a config file"""
    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing config or create new
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    # Ensure mcpServers exists
    if 'mcpServers' not in config:
        config['mcpServers'] = {}

    # Ensure notion server exists with proper structure
    if 'notion' not in config['mcpServers']:
        # Check if this is Claude CLI config (has 'type' field)
        is_cli_config = any('type' in server for server in config.get('mcpServers', {}).values())

        if is_cli_config:
            # Claude Code CLI format
            config['mcpServers']['notion'] = {
                "type": "stdio",
                "command": "npx",
                "args": ["-y", "@notionhq/notion-mcp-server"],
                "env": {
                    "NOTION_TOKEN": api_key
                }
            }
        else:
            # Claude Desktop format
            config['mcpServers']['notion'] = {
                "command": "npx",
                "args": ["-y", "@notionhq/notion-mcp-server"],
                "env": {
                    "NOTION_TOKEN": api_key
                }
            }
    else:
        # Update existing notion server
        # Check if this is Claude CLI config and add type if missing
        is_cli_config = any('type' in server for server in config.get('mcpServers', {}).values())
        if is_cli_config and 'type' not in config['mcpServers']['notion']:
            config['mcpServers']['notion']['type'] = 'stdio'

        if 'env' not in config['mcpServers']['notion']:
            config['mcpServers']['notion']['env'] = {}
        config['mcpServers']['notion']['env']['NOTION_TOKEN'] = api_key

    # Write back
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    return True

def main():
    api_key = None

    # Try to get API key from command line argument
    if len(sys.argv) >= 2:
        api_key = sys.argv[1]

    # If no argument, try to read from deep-code-reader config
    if not api_key:
        config_path = Path.home() / ".claude/deep-code-reader/notion_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key')
                    if api_key:
                        print(f"Using API key from {config_path}")
                        print("")
            except Exception as e:
                print(f"Warning: Could not read config from {config_path}: {e}", file=sys.stderr)

    if not api_key or api_key == "":
        print("Error: No API key provided", file=sys.stderr)
        print("Usage: update_notion_mcp.py [notion_api_key]", file=sys.stderr)
        print("  Or configure ~/.claude/deep-code-reader/notion_config.json first", file=sys.stderr)
        sys.exit(1)

    try:
        config_paths = get_claude_config_paths()
        updated_count = 0

        print("Updating Notion API key in Claude configurations...")
        print("")

        for config_path in config_paths:
            try:
                if update_notion_api_key(config_path, api_key):
                    print(f"✓ Updated: {config_path}")
                    updated_count += 1
            except Exception as e:
                print(f"⚠ Skipped {config_path}: {e}")

        print("")

        if updated_count == 0:
            print("❌ No configurations were updated", file=sys.stderr)
            return 1

        print(f"✅ Successfully updated {updated_count} configuration(s)")
        print("")
        print("⚠️  IMPORTANT: Restart Claude Code for changes to take effect")
        print("")

        # Show which configs were updated
        print("Updated configurations:")
        for config_path in config_paths:
            if config_path.exists():
                if ".mcp.json" in str(config_path):
                    print(f"  • Claude Code CLI: {config_path}")
                else:
                    print(f"  • Claude Desktop: {config_path}")
        print("")

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
