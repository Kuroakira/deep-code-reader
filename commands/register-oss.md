---
name: register-oss
description: Register an OSS repository in Notion database for tracking
---

# Register OSS Repository

Register a GitHub repository in your Notion "OSSリスト" database to start tracking commits and PRs.

## Usage

```
/register-oss <github-url>
```

**Example**:
```
/register-oss https://github.com/expressjs/express
```

## Workflow

### Step 1: Validate GitHub URL

Extract repository information:
- Owner: e.g., "expressjs"
- Repository name: e.g., "express"
- Full URL validation

### Step 2: Check for Existing Entry

Search Notion "OSSリスト" database:
1. Query by GitHub URL
2. If found → Return existing page ID
3. If not found → Proceed to create

### Step 3: Fetch Repository Metadata (use GitHub MCP)

Get repository information:
- Project name
- Description
- Primary language
- Stars count
- Last commit date
- Topics/tags

```python
# Use GitHub MCP to fetch repo info
repo_info = github_mcp.get_repository(owner, repo_name)
```

### Step 4: Create Commits & PRs Database for this OSS

Create a dedicated database for this OSS repository's commits and PRs:

Use Notion MCP `create_database`:
```json
{
  "parent_page_id": "<workspace_page_id>",
  "title": "{OSS Name} - Commits & PRs",
  "properties": {
    "Title": {"title": {}},
    "Type": {
      "select": {
        "options": [
          {"name": "Commit", "color": "blue"},
          {"name": "PR", "color": "green"}
        ]
      }
    },
    "Commit ID / PR No": {"rich_text": {}},
    "GitHub URL": {"url": {}},
    "Comment": {"rich_text": {}},
    "Created": {"created_time": {}},
    "Analyzed Date": {"date": {}},
    "Memo": {"rich_text": {}}
  }
}
```

Save the database ID and URL for later use.

### Step 5: Create Notion Page in OSSリスト

Create entry in "OSSリスト" database:

**Properties**:
- **Name** (title): Project name (e.g., "Express.js")
- **GitHub URL** (url): Repository URL
- **Commits DB** (url): URL to the Commits & PRs database created in Step 4

**Content** (optional):
```markdown
# {Project Name}

{Description}

## Repository Info
- Language: {primary_language}
- Stars: {stars_count}
- Last Updated: {last_commit_date}

## Registered
- Date: {today}
- Status: Ready for analysis
```

### Step 6: Save to Memory (use Serena MCP)

Save current OSS project information to memory, including the commits database ID:

```python
# Save current OSS context including commits database info
serena_mcp.write_memory("current_oss", {
    "repo_url": repo_url,
    "owner": owner,
    "repo": repo_name,
    "notion_page_id": notion_page_id,
    "commits_database_id": commits_db_id,  # NEW: OSS-specific commits DB
    "commits_database_url": commits_db_url,  # NEW: For easy access
    "registered_at": current_timestamp
})
```

This allows users to omit URLs in subsequent commands:
- `/analyze-commit <hash>` instead of `/analyze-commit <url> <hash>`
- `/analyze-pr <number>` instead of `/analyze-pr <url>/pull/<number>`

### Step 7: Confirm Success

Return to user:
```markdown
✅ OSS Repository Registered!

📦 Project: Express.js
🔗 GitHub: https://github.com/expressjs/express
📄 Notion Page: https://notion.so/your-oss-page-id
💾 Commits DB: https://notion.so/your-commits-db-id

💡 Next steps:
- Check current project: /current-oss
- Analyze commits: /analyze-commit <commit-hash>  ⬅️ URL not needed!
- Commits will be saved to the dedicated "Express.js - Commits & PRs" database
- Analyze PR: /analyze-pr <pr-number>
- View in Notion: [link]
```

## Error Handling

### Invalid GitHub URL

```
❌ Error: Invalid GitHub URL

Expected format:
  ✓ https://github.com/owner/repo
  ✓ github.com/owner/repo
  ✗ gitlab.com/owner/repo (not supported)

Please provide a valid GitHub repository URL.
```

### Private Repository

```
⚠️  Private Repository Detected

This repository requires authentication.

Options:
1. Set GITHUB_TOKEN environment variable
2. Make repository public
3. Use GitHub App with proper permissions

Current token status: [Not set / Invalid / Valid]
```

### Repository Not Found

```
❌ Error: Repository not found

URL: https://github.com/owner/repo

Possible reasons:
- Repository deleted
- Owner/name changed
- Typo in URL
- Private repository without access

Please verify the URL and try again.
```

### Already Registered

```
ℹ️  Repository Already Registered

📦 Project: Express.js
📄 Notion: https://notion.so/existing-page-id

This repository was registered on: 2025-01-10

✅ You can start analyzing commits:
   /analyze-commit <url> <commit-hash>
```

### Notion Not Configured

```
⚠️  Notion Integration Not Set Up

This command requires Notion integration to store repository data.

Quick Setup:
  1. Run: /setup-notion
  2. The wizard will:
     • Guide you through creating Notion integration
     • Help you share a workspace page
     • Automatically create OSSリスト database
     • Automatically create Commit & PRリスト database
     • Configure everything for you

  3. Come back and run this command again

Alternatively, you can:
  • Skip Notion integration (analyze without saving to Notion)
  • Set up manually (see: commands/setup-notion.md)

Would you like to continue without Notion? (y/n)
```

If user chooses to continue without Notion:
```
✅ Repository Info Saved to Memory (Local Only)

📦 Project: Express.js
🔗 GitHub: https://github.com/expressjs/express
💾 Saved as current project

⚠️  Note: Results won't be saved to Notion
   Run /setup-notion to enable Notion integration

You can still analyze:
  /analyze-commit abc1234
  /analyze-pr 5234
```

### Notion Database Not Found

```
❌ Error: OSSリスト database not accessible

Database ID: 294c3130714380eab9a9ee8cd897e09e

Possible issues:
1. Database ID is incorrect
2. Integration not invited to database
3. Database was deleted

Steps to fix:
1. Open Notion database
2. Click "Share" → Invite integration
3. Verify database ID in URL
4. Update: ~/.claude/deep-code-reader/notion_config.json
```

## Output Format

### Success (New Registration)

```markdown
✅ OSS Repository Registered Successfully!

📦 **Project**: Express.js
📝 **Description**: Fast, unopinionated, minimalist web framework
🌐 **GitHub**: https://github.com/expressjs/express
⭐ **Stars**: 65,234
💻 **Language**: JavaScript
📄 **Notion Page**: https://notion.so/Express-js-abc123

💾 **Saved as current project** - URL no longer needed for analysis!

## Quick Start

Check current project:
/current-oss

Analyze a commit (URL optional!):
/analyze-commit abc1234

Analyze a PR (URL optional!):
/analyze-pr 5234

View in Notion:
https://notion.so/Express-js-abc123
```

### Success (Already Exists)

```markdown
ℹ️  Repository Already in Notion

📦 **Project**: Express.js
📄 **Notion Page**: https://notion.so/Express-js-abc123
📅 **Registered**: 2025-01-10

💾 **Set as current project** - URL no longer needed for analysis!

✅ Ready to analyze!

Examples:
  /current-oss
  /analyze-commit <commit-hash>
  /analyze-pr <pr-number>
```

## Advanced Options

### Re-sync Metadata

```
/register-oss <url> --sync
```

Updates existing entry with latest GitHub metadata:
- Stars count
- Description
- Last commit date

### Batch Registration

```
/register-oss --batch <file>
```

Register multiple repositories from a file:
```
# repos.txt
https://github.com/expressjs/express
https://github.com/koajs/koa
https://github.com/nestjs/nest
```

Result:
```
📦 Batch Registration

✅ expressjs/express → Registered
✅ koajs/koa → Already exists
✅ nestjs/nest → Registered

Summary: 3 total, 2 new, 1 existing
```

## Tips

1. **Register once, analyze many**: You only need to register a repository once
2. **Check before analyzing**: Always register before running commit/PR analysis
3. **Update metadata**: Use `--sync` flag to refresh repository information
4. **Organize in Notion**: Add custom properties in Notion after registration
5. **Share with team**: Notion pages are shareable for collaboration
