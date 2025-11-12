#!/usr/bin/env python3
"""
Update Notion configuration in ~/.claude/deep-code-reader/notion_config.json

This script ONLY updates the deep-code-reader project configuration,
NOT Claude Code's MCP server configuration (~/.claude.json).

The Notion MCP server configuration in Claude Code should be set up
during installation via install.sh and should not be modified afterward.
"""

import json
import os
import sys
from pathlib import Path

def update_notion_config(api_key):
    """Update Notion API key in deep-code-reader configuration"""
    config_path = Path.home() / ".claude/deep-code-reader/notion_config.json"

    # Create config directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Read existing config or create new
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "api_key": "",
            "workspace_page_id": "",
            "oss_database_id": "",
            "auto_export": False,
            "setup_complete": False
        }

    # Update API key
    config['api_key'] = api_key

    # Write back
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    return True

def main():
    api_key = None

    # Try to get API key from command line argument
    if len(sys.argv) >= 2:
        api_key = sys.argv[1]

    if not api_key or api_key == "":
        print("Error: No API key provided", file=sys.stderr)
        print("Usage: update_notion_mcp.py <notion_api_key>", file=sys.stderr)
        print("", file=sys.stderr)
        print("This script updates ~/.claude/deep-code-reader/notion_config.json", file=sys.stderr)
        print("", file=sys.stderr)
        print("Note: To update Claude Code's MCP server configuration,", file=sys.stderr)
        print("      please run install.sh instead.", file=sys.stderr)
        sys.exit(1)

    try:
        config_path = Path.home() / ".claude/deep-code-reader/notion_config.json"

        print("Updating Notion API key in deep-code-reader configuration...")
        print("")

        if update_notion_config(api_key):
            print(f"✓ Updated: {config_path}")
            print("")
            print("✅ Successfully updated Notion configuration")
            print("")
            print("📝 Next Steps:")
            print("  1. Run Claude Code: claude-code")
            print("  2. Run: /setup-notion")
            print("  3. Complete the setup wizard")
            print("")
            return 0
        else:
            print("❌ Failed to update configuration", file=sys.stderr)
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
