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

### Step 4: Create Notion Page

Create entry in "OSSリスト" database:

**Properties**:
- **Name** (title): Project name (e.g., "Express.js")
- **GitHub URL** (url): Repository URL

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

### Step 5: Confirm Success

Return to user:
```markdown
✅ OSS Repository Registered!

📦 Project: Express.js
🔗 GitHub: https://github.com/expressjs/express
📄 Notion: https://notion.so/your-oss-page-id

💡 Next steps:
- Analyze commits: /analyze-commit <url> <commit-hash>
- Analyze PR: /analyze-pr <pr-url>
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
❌ Error: Notion not configured

Please configure Notion integration first:
  1. Run: /setup-notion
  2. Provide API key and database IDs
  3. Retry registration

Current config: config/notion_config.json
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
4. Update: config/notion_config.json
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

## Quick Start

Analyze a commit:
/analyze-commit https://github.com/expressjs/express abc1234

Analyze a PR:
/analyze-pr https://github.com/expressjs/express/pull/5234

View in Notion:
https://notion.so/Express-js-abc123
```

### Success (Already Exists)

```markdown
ℹ️  Repository Already in Notion

📦 **Project**: Express.js
📄 **Notion Page**: https://notion.so/Express-js-abc123
📅 **Registered**: 2025-01-10

✅ Ready to analyze!

Examples:
  /analyze-commit <url> <commit>
  /analyze-pr <pr-url>
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
