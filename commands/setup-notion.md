---
name: setup-notion
description: Configure Notion integration with automatic database creation
---

# Notion Integration Setup Wizard

This command guides you through setting up Notion integration with automatic database creation.

## Overview

The setup process:
1. **Get Notion API Key** - Create integration and get token
2. **Share Workspace Page** - Share a Notion page with your integration
3. **Auto-create Databases** - Automatically create OSSリスト and Commit & PRリスト databases
4. **Configure Platform** - Save configuration for automated export

## Setup Flow

### Step 1: Check Existing Configuration

First, check if configuration already exists:

```javascript
const fs = require('fs');
const path = require('path');
const configPath = path.join(require('os').homedir(), '.claude/deep-code-reader/notion_config.json');

if (fs.existsSync(configPath)) {
  const config = JSON.parse(fs.readFileSync(configPath));

  if (config.setup_complete) {
    // Ask if user wants to reconfigure
    console.log('⚠️  Notion is already configured.');
    console.log('Do you want to reconfigure? (y/n)');
    // If no, exit
  }
}
```

### Step 2: Get Notion API Key

Guide user to create integration:

```markdown
📝 Step 1: Create Notion Integration

1. Visit: https://www.notion.so/profile/integrations
2. Click "New integration"
3. Name: "Deep Code Reader" (or your choice)
4. Select workspace
5. Capabilities needed:
   ✓ Read content
   ✓ Update content
   ✓ Insert content
6. Click "Submit"
7. Copy the "Internal Integration Token"

Please enter your Notion API Key:
(Should start with "secret_")
```

Validate the API key:
- Must start with "secret_" or "ntn_"
- Should be around 50 characters
- Save to config and update Claude Code configuration

**Note: Notion MCP Server Configuration**

The Notion MCP server should already be configured in Claude Code during installation (`install.sh`).
This setup wizard only configures the **workspace and database settings** specific to deep-code-reader.

If you need to update the Notion API key in your project configuration:

```bash
python3 ~/.claude/deep-code-reader/scripts/update_notion_mcp.py "<notion_api_key>"
```

This will update: `~/.claude/deep-code-reader/notion_config.json`

**Expected output:**
```
Updating Notion API key in deep-code-reader configuration...

✓ Updated: /Users/.../. claude/deep-code-reader/notion_config.json

✅ Successfully updated Notion configuration

📝 Next Steps:
  1. Run Claude Code: claude-code
  2. Run: /setup-notion
  3. Complete the setup wizard
```

**No Restart Required**
- The Notion MCP server is already running (configured via install.sh)
- This wizard only updates project-specific settings
- Changes take effect immediately

### Step 3: Grant Integration Access

Guide user to grant access to a workspace page:

```markdown
📄 Step 2: Grant Integration Access to Workspace

1. Go to: https://www.notion.so/profile/integrations

2. Click on your integration (e.g., "MCP接続用" or "Deep Code Reader")

3. Click the "アクセス" (Access) tab

4. Click "アクセス権限を編集" (Edit access permissions)

5. Select or create a workspace page:
   - Choose existing page, or
   - Create new page: "Code Analysis Workspace"

6. Click "保存" (Save) to grant access

7. Copy the page URL:

Please enter the Notion page URL:
(Example: https://notion.so/workspace/abc123...)
```

Extract page ID from URL:
- Format: `https://notion.so/workspace/PAGE_ID?v=...`
- Or: `https://notion.so/PAGE_ID`
- Extract the 32-character ID

**Note**: The new method (via Integration settings) is much simpler than the old "Share button" method.

### Step 4: Create OSSリスト Database

Use Notion MCP to create the master OSS database:

```markdown
🔨 Step 3: Creating OSSリスト Database

Creating master database for OSS repositories...
```

**OSSリスト Database** (Master Database)

Use Notion MCP `create_database` with:
```json
{
  "parent_page_id": "<workspace_page_id>",
  "title": "OSSリスト",
  "properties": {
    "Name": {
      "title": {}
    },
    "GitHub URL": {
      "url": {}
    },
    "Description": {
      "rich_text": {}
    },
    "Language": {
      "select": {
        "options": [
          {"name": "Python", "color": "blue"},
          {"name": "JavaScript", "color": "yellow"},
          {"name": "TypeScript", "color": "blue"},
          {"name": "Go", "color": "green"},
          {"name": "Rust", "color": "orange"},
          {"name": "Other", "color": "gray"}
        ]
      }
    },
    "Stars": {
      "number": {}
    },
    "Commits DB": {
      "url": {}
    },
    "Created": {
      "created_time": {}
    }
  }
}
```

**Note**: Individual "Commits & PRs" databases will be created automatically when you register each OSS repository using `/register-oss`.

Show progress:
```markdown
  ✓ Created "OSSリスト" database

💡 Next: Run /register-oss to add OSS repositories
   Each OSS will get its own "Commits & PRs" database
```

### Step 5: Save Configuration

Save complete configuration:

```json
{
  "api_key": "secret_xxxxxxxxxxxxx",
  "workspace_page_id": "abc123...",
  "oss_database_id": "def456...",
  "auto_export": true,
  "setup_complete": true
}
```

**Note**: `commits_database_id` is no longer stored globally. Each OSS repository will have its own commits database, referenced in the OSSリスト entries.

Write to `~/.claude/deep-code-reader/notion_config.json`.

### Step 6: Verify Setup

Test the configuration:

```markdown
🧪 Step 4: Verifying Setup

Testing Notion connection...
  ✓ API key valid
  ✓ Workspace page accessible
  ✓ OSSリスト database accessible

✅ Notion Integration Complete!
```

## Success Output

After successful setup:

```markdown
╔════════════════════════════════════════════╗
║   Notion Integration Configured!          ║
╚════════════════════════════════════════════╝

📋 Configuration Details:
  • Workspace: [page_name]
  • OSSリスト: https://notion.so/workspace/[oss_db_id]
  • Auto-export: Enabled

🚀 Next Steps:
  1. Register an OSS repository:
     /register-oss https://github.com/user/repo
     (This will create a Commits & PRs database for that OSS)

  2. Analyze commits:
     /analyze-commit abc1234

  3. View results in Notion:
     Check the "Commits DB" link in OSSリスト

💡 Tips:
  • Each OSS gets its own Commits & PRs database
  • Results automatically export to the correct database
  • Use /current-oss to check active project
```

## Error Handling

### Invalid API Key

```markdown
❌ Invalid Notion API Key

The API key should:
  • Start with "secret_"
  • Be about 50 characters long
  • Come from https://www.notion.so/profile/integrations

Please try again with a valid key.
```

### Page Not Accessible

```markdown
❌ Cannot Access Workspace Page

Possible issues:
  1. Page URL is incorrect
  2. Integration not granted access to page
  3. Page was deleted

To fix:
  1. Verify page URL
  2. Grant integration access to page:
     - Go to: https://www.notion.so/profile/integrations
     - Click on your integration
     - Click "アクセス" (Access) tab
     - Click "アクセス権限を編集" (Edit access permissions)
     - Select the page
     - Click "保存" (Save)
```

### Database Creation Failed

```markdown
❌ Failed to Create Database

Error: [error message]

Troubleshooting:
  1. Verify integration has required permissions:
     ✓ Read content
     ✓ Update content
     ✓ Insert content

  2. Check workspace page is shared with integration

  3. Try again or create databases manually:
     /setup-notion --manual
```

## Manual Setup Mode

If automatic setup fails, provide manual instructions:

```markdown
📝 Manual Setup Instructions

Follow these steps to set up manually:

Step 1: Create OSSリスト Database
  1. Open your workspace page
  2. Type: /database
  3. Select "Table - Inline"
  4. Name: "OSSリスト"
  5. Add properties:
     - Name (title)
     - GitHub URL (url)
     - Description (text)
     - Language (select)
     - Stars (number)

Step 2: Create Commit & PRリスト Database
  1. On same page, add another database
  2. Name: "Commit & PRリスト"
  3. Add properties:
     - Title (title)
     - Type (select: Commit, PR)
     - Commit ID / PR No (text)
     - GitHub URL (url)
     - Comment (text)
     - OSS (relation to OSSリスト)
     - Analyzed Date (date)
     - Memo (text)

Step 3: Grant Integration Access
  1. Go to: https://www.notion.so/profile/integrations
  2. Click on your integration
  3. Click "アクセス" tab
  4. Click "アクセス権限を編集"
  5. Ensure the workspace page is selected (databases inherit access)

Step 4: Get Database IDs
  1. Open each database as full page
  2. Copy ID from URL
  3. Run: /setup-notion --manual-config

I'll ask for the IDs to complete setup.
```

## Configuration Check Command

Also support checking current configuration:

```markdown
/setup-notion --check

Current Notion Configuration:
  ✓ API Key: Configured
  ✓ Workspace Page: [page_name]
  ✓ OSSリスト Database: Connected
  ✓ Commit & PRリスト Database: Connected
  ✓ Auto-export: Enabled
  ✓ Setup Complete: Yes

Last verified: [timestamp]

To reconfigure: /setup-notion --reset
```

## Security Notes

```markdown
🔒 Security Reminders:

✓ Configuration saved to: ~/.claude/deep-code-reader/notion_config.json
✓ File is in your home directory (not in project)
✓ Never share your Notion API key
✓ You can regenerate token anytime

⚠️  If token is compromised:
  1. Visit: https://www.notion.so/profile/integrations
  2. Select "Deep Code Reader"
  3. Click "Regenerate token"
  4. Run: /setup-notion --update-token
```
