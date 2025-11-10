---
name: setup-notion
description: Configure Notion integration for automated analysis export
---

# Notion Integration Setup

Guide the user through setting up Notion integration for automated code analysis export.

## Setup Steps

### Step 1: Create Notion Integration

1. Guide user to Notion integrations page:
   ```
   Visit: https://www.notion.so/my-integrations
   ```

2. Walk through integration creation:
   ```
   1. Click "New integration"
   2. Name: "OSS Learning Platform" (or user's choice)
   3. Associated workspace: [Select workspace]
   4. Capabilities:
      ✓ Read content
      ✓ Update content
      ✓ Insert content
   5. Click "Submit"
   ```

3. Copy integration token:
   ```
   📋 Copy "Internal Integration Token"
   (Starts with "secret_")
   ```

### Step 2: Create Analysis Database

1. Guide database creation:
   ```
   1. Open Notion
   2. Create new page: "Code Analyses" (or user's choice)
   3. Type: /database → "Table - Inline"
   4. Add properties:
      - Repository (URL)
      - Commit (Text)
      - Analysis Date (Date)
      - Status (Select: Completed, In Progress, Failed)
      - Architecture Pattern (Multi-select)
   ```

2. Share database with integration:
   ```
   1. Click "Share" in top-right
   2. Click "Invite"
   3. Search for integration name: "OSS Learning Platform"
   4. Click "Invite"
   ```

3. Get database ID:
   ```
   1. Open database as full page
   2. Copy URL: https://notion.so/workspace/DATABASE_ID?v=...
   3. Extract DATABASE_ID (32-character string)
   ```

### Step 3: Configure Platform

Save configuration to file:

```json
{
  "api_key": "secret_xxxxxxxxxxxxxxxxxxxxx",
  "database_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "auto_export": true,
  "page_template": "analysis"
}
```

Write this to: `config/notion_config.json`

### Step 4: Verify Setup

Test the connection:

```bash
# Verify configuration file
cat config/notion_config.json

# Test Notion MCP connection
# (This will be tested when you run /analyze-oss)
```

## Interactive Setup

Ask the user for each piece of information step by step:

1. **Integration Token**:
   ```
   🔑 Notion Integration Token

   Please enter your Notion integration token:
   (Starts with "secret_")

   > _
   ```

2. **Database ID**:
   ```
   📋 Notion Database ID

   Please enter your database ID:
   (32-character string from URL)

   > _
   ```

3. **Auto-export preference**:
   ```
   ⚙️  Auto-export Setting

   Automatically export to Notion after analysis? (yes/no)

   > _
   ```

4. **Confirmation**:
   ```
   ✅ Configuration Summary:

   - Integration: Connected
   - Database: [database_id]
   - Auto-export: [enabled/disabled]

   Save this configuration? (yes/no)

   > _
   ```

## Troubleshooting

### Invalid Token
```
❌ Error: Invalid Notion token

The token should:
- Start with "secret_"
- Be about 50 characters long
- Come from https://www.notion.so/my-integrations

Please verify and try again.
```

### Database Not Found
```
❌ Error: Database not accessible

Possible issues:
1. Database ID is incorrect
2. Integration not invited to database
3. Database was deleted

Steps to fix:
1. Verify database ID from URL
2. Share database with integration:
   - Open database
   - Click "Share"
   - Invite "OSS Learning Platform"
```

### Permission Denied
```
❌ Error: Insufficient permissions

The integration needs these capabilities:
✓ Read content
✓ Update content
✓ Insert content

To fix:
1. Go to: https://www.notion.so/my-integrations
2. Select your integration
3. Check all required capabilities
4. Save changes
```

## Output Format

After successful setup:

```markdown
✅ Notion Integration Configured!

📋 Configuration saved to: config/notion_config.json

🔗 Database: https://notion.so/workspace/[database_id]

📝 Next steps:
1. Run analysis: /analyze-oss <github-url>
2. Results will automatically export to Notion
3. View in database: [Notion database URL]

💡 Tip: You can disable auto-export by setting
    "auto_export": false in config/notion_config.json
```

## Security Notes

Remind user about security:

```
🔒 Security Reminder:

- config/notion_config.json is gitignored
- Never commit your Notion token
- Keep your integration token secret
- You can regenerate tokens at any time

⚠️  If token is compromised:
1. Visit: https://www.notion.so/my-integrations
2. Select integration
3. Click "Regenerate token"
4. Update config/notion_config.json
```
