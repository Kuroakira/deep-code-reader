---
name: current-oss
description: Display currently active OSS project for analysis
---

# Current OSS Project

Display the currently active OSS project that will be used for commit and PR analysis.

## Usage

```
/current-oss
```

## Workflow

### Step 1: Check Memory

```python
# Read current OSS from project memory
current_oss = serena_mcp.read_memory("current_oss")

if not current_oss:
    print("⚠️  No OSS project currently set")
    return
```

### Step 2: Parse Stored Data

The memory contains:
```json
{
  "repo_url": "https://github.com/owner/repo",
  "owner": "owner",
  "repo": "repo",
  "notion_page_id": "abc123...",
  "commits_database_id": "def456...",
  "local_repo_path": "~/.claude/deep-code-reader/repos/owner/repo",
  "registered_at": "2025-01-15T10:30:00Z"
}
```

### Step 3: Fetch Additional Info (optional)

```python
# Get repository metadata from GitHub
repo_info = github_mcp.get_repository(owner, repo)

# Get Notion page details
notion_page = notion_mcp.get_page(notion_page_id)
```

### Step 4: Display Information

```markdown
📦 Current OSS Project

Repository: {owner}/{repo}
GitHub: {repo_url}
Notion: {notion_page_url}
Local Clone: {local_repo_path}

Description: {repo_description}
Language: {primary_language}
Stars: {stargazers_count} ⭐
Last Updated: {updated_at}

Registered: {registered_at}

🎯 Deep Analysis Features:
  ✅ Line-by-line code analysis (Serena MCP)
  ✅ Symbol-level dependency tracking
  ✅ Full file content access

💡 Commands available:
  /list-commits           # List oldest commits first
  /analyze-commit <hash>  # Deep analysis with Serena
  /analyze-pr <number>    # PR analysis with context

To switch projects:
  /register-oss <new-url>
```

## Output Format

### When Project is Set

```markdown
📦 Current OSS Project

Repository: expressjs/express
GitHub: https://github.com/expressjs/express
Notion: https://notion.so/Express-js-abc123
Local Clone: ~/.claude/deep-code-reader/repos/expressjs/express

Description: Fast, unopinionated, minimalist web framework
Language: JavaScript
Stars: 65,432 ⭐
Last Updated: 2025-01-15

Registered: 2025-01-10 10:30

🎯 Deep Analysis Features:
  ✅ Line-by-line code analysis (Serena MCP)
  ✅ Symbol-level dependency tracking
  ✅ Full file content access

💡 You can now analyze commits without specifying the URL:
  /list-commits           # Browse from the beginning
  /analyze-commit abc1234 # Deep analysis enabled
  /analyze-pr 5234        # Full PR context

To switch to a different project:
  /register-oss <new-url>
```

### When No Project is Set

```markdown
⚠️  No OSS Project Currently Set

You haven't registered any OSS project yet.

To start analyzing commits:
  1. Register a project: /register-oss <github-url>
  2. Then analyze: /analyze-commit <commit-hash>

Example:
  /register-oss https://github.com/expressjs/express
  /analyze-commit abc1234567
```

## Error Handling

### Memory Read Error

```markdown
❌ Error reading project memory

Please try registering the project again:
  /register-oss <github-url>
```

### Notion Page Not Found

```markdown
⚠️  Project registered but Notion page not found

Repository: {repo_url}
Status: Registered in memory but not in Notion

Please re-register:
  /register-oss {repo_url}
```

### GitHub API Error

```markdown
📦 Current OSS Project

Repository: expressjs/express
GitHub: https://github.com/expressjs/express
Notion: https://notion.so/Express-js-abc123

⚠️  Could not fetch latest repository info from GitHub
    (Registered info shown above)

💡 Commands available:
  /analyze-commit <commit-hash>
  /analyze-pr <pr-number>
```

## Tips

- Use this command to verify which project you're working on
- Helps avoid accidentally analyzing commits from the wrong repository
- Shows Notion page URL for quick access to your analysis database
- Check this before running `/analyze-commit` if you're unsure
