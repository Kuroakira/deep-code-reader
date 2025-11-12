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

### Step 4: Create Notion Page in OSSリスト

**IMPORTANT**: Create the OSS page FIRST, then create the Commits & PRs database inside it.

Create entry in "OSSリスト" database:

**Properties**:
- **Name** (title): Project name (e.g., "Express.js")
- **GitHub URL** (url): Repository URL
- **Description** (rich_text): Repository description
- **Language** (select): Primary language
- **Stars** (number): Star count

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

### Step 5: Create Commits & PRs Database INSIDE the OSS Page

**CRITICAL**: Use the page ID from Step 4 as the parent!

Create an **inline database** inside the OSS page:

Use Notion MCP `create_database`:
```json
{
  "parent": {
    "type": "page_id",
    "page_id": "<oss_page_id_from_step_4>"
  },
  "is_inline": true,
  "title": [{"type": "text", "text": {"content": "{OSS Name} - Commits & PRs"}}],
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

**Note**: The database will appear inline on the OSS page, not as a separate full-page database.

Save the database ID for later use.

### Step 6: Clone Repository Locally

**IMPORTANT**: Clone the repository for deep code analysis with Serena MCP.

```python
import os
import subprocess
from pathlib import Path

# Determine clone directory
home = Path.home()
repos_dir = home / ".claude" / "deep-code-reader" / "repos"
local_repo_path = repos_dir / owner / repo

# Create repos directory if it doesn't exist
repos_dir.mkdir(parents=True, exist_ok=True)

# Check if already cloned
if (local_repo_path / ".git").exists():
    print(f"✅ Repository already cloned: {local_repo_path}")

    # Optional: Pull latest changes
    try:
        result = subprocess.run(
            ["git", "fetch", "--all"],
            cwd=local_repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        print(f"📥 Fetched latest changes")
    except Exception as e:
        print(f"⚠️  Could not fetch updates: {e}")

else:
    # Clone the repository
    print(f"📥 Cloning repository to: {local_repo_path}")

    try:
        # Create owner directory
        (repos_dir / owner).mkdir(parents=True, exist_ok=True)

        # Clone with progress
        result = subprocess.run(
            ["git", "clone", repo_url, str(local_repo_path)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            print(f"✅ Successfully cloned repository")
            print(f"📁 Location: {local_repo_path}")
        else:
            print(f"❌ Clone failed: {result.stderr}")
            # Continue without local clone - analysis will use GitHub API only
            local_repo_path = None

    except subprocess.TimeoutExpired:
        print(f"⚠️  Clone timeout (large repository)")
        print(f"   You can manually clone to: {local_repo_path}")
        local_repo_path = None

    except Exception as e:
        print(f"❌ Clone error: {e}")
        local_repo_path = None

# Store the path (even if None - indicates clone failed)
local_repo_path_str = str(local_repo_path) if local_repo_path else None
```

**Clone Benefits**:
- Enables deep code analysis with Serena MCP
- Line-by-line code reading in analyze-commit
- Symbol-level dependency tracking
- Full file content access without API limits

**If Clone Fails**:
- Analysis will still work using GitHub API
- Some features may be limited
- Manual clone recommended for deep analysis

### Step 7: Save to Memory

Save current OSS project information to memory, including the commits database ID and local clone path:

```python
# Save current OSS context including commits database info AND local clone path
serena_mcp.write_memory("current_oss", {
    "repo_url": repo_url,
    "owner": owner,
    "repo": repo_name,
    "notion_page_id": notion_page_id,
    "commits_database_id": commits_db_id,
    "commits_database_url": commits_db_url,
    "local_repo_path": local_repo_path_str,  # NEW: Path to local clone
    "registered_at": current_timestamp
})
```

Also save to JSON file for persistence:

```python
import json
from pathlib import Path

# Save to ~/.claude/deep-code-reader/current_oss.json
config_dir = Path.home() / ".claude" / "deep-code-reader"
config_file = config_dir / "current_oss.json"

current_oss_data = {
    "repo_url": repo_url,
    "owner": owner,
    "repo": repo_name,
    "notion_page_id": notion_page_id,
    "notion_page_url": notion_page_url,
    "commits_database_id": commits_db_id,
    "commits_database_url": commits_db_url,
    "local_repo_path": local_repo_path_str,
    "project_name": project_name,
    "description": description,
    "language": primary_language,
    "stars": stars_count,
    "last_updated": last_commit_date,
    "registered_at": current_timestamp,
    "status": "active"
}

with open(config_file, 'w') as f:
    json.dump(current_oss_data, f, indent=2)

print(f"💾 Saved configuration to: {config_file}")
```

This allows users to omit URLs in subsequent commands:
- `/analyze-commit <hash>` - Uses local clone for deep analysis
- `/analyze-pr <number>` - Uses local clone for PR analysis

### Step 8: Get Initial Commit and First PR

Find the repository's initial commit and first PR to guide the user:

```python
# Get the initial commit (oldest commit in the repository)
try:
    # Use git log to get the very first commit
    result = subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"],
        cwd=local_repo_path,
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0 and result.stdout.strip():
        initial_commit_sha = result.stdout.strip().split('\n')[0]
        initial_commit_short = initial_commit_sha[:7]

        # Get commit message for better context
        result = subprocess.run(
            ["git", "log", "-1", "--format=%s", initial_commit_sha],
            cwd=local_repo_path,
            capture_output=True,
            text=True
        )
        initial_commit_msg = result.stdout.strip() if result.returncode == 0 else ""
    else:
        initial_commit_short = None
        initial_commit_msg = ""
except Exception as e:
    print(f"⚠️  Could not fetch initial commit: {e}")
    initial_commit_short = None
    initial_commit_msg = ""

# Get the first PR (PR #1)
try:
    first_pr = github_mcp.get_pull_request(
        owner=owner,
        repo=repo,
        pull_number=1
    )
    first_pr_exists = True
    first_pr_title = first_pr.get("title", "")
except Exception:
    first_pr_exists = False
    first_pr_title = ""
```

### Step 9: Confirm Success with Next Steps

Return to user with specific next actions:

```markdown
✅ OSS Repository Registered!

📦 Project: Express.js
🔗 GitHub: https://github.com/expressjs/express
📄 Notion Page: https://notion.so/Express-js-abc123
💾 Commits & PRs Database: Created inline on the OSS page
📁 Local Clone: ~/.claude/deep-code-reader/repos/expressjs/express

🎯 Ready for Deep Code Analysis!

The repository has been cloned locally, enabling:
- Line-by-line code analysis with Serena MCP
- Symbol-level dependency tracking
- Full file content access without API limits

---

🚀 **Start Your Learning Journey!**

**Option 1: Analyze from the very first commit**
```
/analyze-commit {initial_commit_short}
```
📝 Initial commit: {initial_commit_msg}

**Option 2: Analyze from the first PR**
```
/analyze-pr 1
```
{first_pr_title if first_pr_exists else "ℹ️  Check /list-prs to find the first available PR"}

**Browse available content:**
- List oldest commits: `/list-commits`
- List oldest PRs: `/list-prs`
- Check current project: `/current-oss`

💡 Recommended: Start with the initial commit to understand how the project began!

📄 View in Notion: {notion_page_url}
```

**Example output**:
```markdown
✅ OSS Repository Registered!

📦 Project: NestJS
🔗 GitHub: https://github.com/nestjs/nest
📄 Notion Page: https://www.notion.so/NestJS-2a9c3130714381d89a34d421343ab43b
💾 Commits & PRs Database: Created inline on the OSS page
📁 Local Clone: ~/.claude/deep-code-reader/repos/nestjs/nest

🎯 Ready for Deep Code Analysis!

The repository has been cloned locally, enabling:
- Line-by-line code analysis with Serena MCP
- Symbol-level dependency tracking
- Full file content access without API limits

---

🚀 **Start Your Learning Journey!**

**Option 1: Analyze from the very first commit**
```
/analyze-commit f7c8d10
```
📝 Initial commit: feat(core): initial commit

**Option 2: Analyze from the first PR**
```
/analyze-pr 1
```
📝 Add middleware support and error handling

**Browse available content:**
- List oldest commits: `/list-commits`
- List oldest PRs: `/list-prs`
- Check current project: `/current-oss`

💡 Recommended: Start with the initial commit to understand how the project began!

📄 View in Notion: https://www.notion.so/NestJS-2a9c3130714381d89a34d421343ab43b
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
💾 **Commits & PRs Database**: Inline on the OSS page

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
(Open the page to see the inline Commits & PRs database)
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
