---
name: register-oss
description: Register an OSS repository with your Notion database
---

# Register OSS Repository

Register a GitHub repository to start tracking commits. You provide your own Notion database.

## Prerequisites

1. **Create a Notion Database** with these properties:
   - `Title` (title) - Commit title
   - `Commit ID / PR No` (text) - Full commit hash
   - `Type` (select) - "Commit" or "PR"
   - `GitHub URL` (url) - Link to commit
   - `Comment` (text) - Commit message
   - `Memo` (text) - Your notes

2. **Share database with integration**:
   - Open database in Notion
   - Click "..." → "Connections" → Add your integration

3. **Copy database ID** from URL:
   - URL: `https://notion.so/abc123def456?v=...`
   - Database ID: `abc123def456`

## Usage

```
/register-oss <github-url> --database <database-id>
```

**Examples**:
```
/register-oss https://github.com/nestjs/nest --database abc123def456
/register-oss https://github.com/expressjs/express --database 294c3130714380eab9a9ee8cd897e09e
```

## Workflow

### Step 1: Validate Inputs

```python
# Parse GitHub URL
github_url = args["github_url"]
database_id = args["database"]

# Extract owner and repo
# https://github.com/owner/repo -> owner, repo
parts = github_url.replace("https://github.com/", "").split("/")
owner = parts[0]
repo = parts[1].replace(".git", "")

print(f"Repository: {owner}/{repo}")
print(f"Database: {database_id}")
```

### Step 2: Verify Database Access (use Notion MCP)

```python
# Check database is accessible
try:
    db_info = notion_mcp.retrieve_database(database_id=database_id)
    db_title = db_info.get("title", [{}])[0].get("plain_text", "Untitled")
    print(f"Database found: {db_title}")
except Exception as e:
    print(f"Error: Cannot access database")
    print(f"Please ensure:")
    print(f"  1. Database ID is correct")
    print(f"  2. Integration is connected to the database")
    return
```

### Step 3: Fetch Repository Info (use GitHub MCP)

```python
# Get repository metadata
repo_info = github_mcp.get_repository(owner, repo)

project_name = repo_info.get("name", repo)
description = repo_info.get("description", "")
language = repo_info.get("language", "")
stars = repo_info.get("stargazers_count", 0)

print(f"Project: {project_name}")
print(f"Language: {language}")
print(f"Stars: {stars}")
```

### Step 4: Clone Repository Locally

```python
import subprocess
from pathlib import Path

# Clone to ~/.claude/deep-code-reader/repos/{owner}/{repo}
home = Path.home()
repos_dir = home / ".claude" / "deep-code-reader" / "repos"
local_repo_path = repos_dir / owner / repo

if (local_repo_path / ".git").exists():
    print(f"Repository already cloned: {local_repo_path}")
    # Fetch latest
    subprocess.run(["git", "fetch", "--all"], cwd=local_repo_path, capture_output=True)
else:
    print(f"Cloning repository...")
    (repos_dir / owner).mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["git", "clone", github_url, str(local_repo_path)],
        capture_output=True,
        text=True,
        timeout=300
    )
    if result.returncode == 0:
        print(f"Cloned to: {local_repo_path}")
    else:
        print(f"Clone failed: {result.stderr}")
        local_repo_path = None
```

### Step 5: Get Initial Commit

```python
if local_repo_path:
    result = subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"],
        cwd=local_repo_path,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        initial_commit = result.stdout.strip().split('\n')[0][:7]
    else:
        initial_commit = None

    # Get total commit count
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=local_repo_path,
        capture_output=True,
        text=True
    )
    total_commits = int(result.stdout.strip()) if result.returncode == 0 else 0
```

### Step 6: Save to Memory (use Serena MCP)

```python
import json
from datetime import datetime

current_oss = {
    "repo_url": github_url,
    "owner": owner,
    "repo": repo,
    "database_id": database_id,
    "local_repo_path": str(local_repo_path) if local_repo_path else None,
    "project_name": project_name,
    "description": description,
    "language": language,
    "stars": stars,
    "total_commits": total_commits,
    "registered_at": datetime.now().isoformat()
}

# Save to Serena memory
serena_mcp.write_memory("current_oss", json.dumps(current_oss))

# Also save to config file for persistence
config_dir = Path.home() / ".claude" / "deep-code-reader"
config_dir.mkdir(parents=True, exist_ok=True)
config_file = config_dir / "current_oss.json"

with open(config_file, 'w') as f:
    json.dump(current_oss, f, indent=2)

print(f"Configuration saved")
```

### Step 7: Display Success

```python
print(f"""
{'='*50}
OSS Repository Registered
{'='*50}

Project: {project_name}
GitHub: {github_url}
Database: {database_id}
Local Clone: {local_repo_path or 'Not available'}

Total Commits: {total_commits}
Initial Commit: {initial_commit or 'Unknown'}

{'='*50}

Next Steps:

1. Add first batch of commits:
   /add-commits 1 100

2. Check current project:
   /current-oss

3. List available commits:
   /list-commits

{'='*50}
""")
```

## Output Example

```markdown
==================================================
OSS Repository Registered
==================================================

Project: nest
GitHub: https://github.com/nestjs/nest
Database: abc123def456
Local Clone: ~/.claude/deep-code-reader/repos/nestjs/nest

Total Commits: 5432
Initial Commit: f7c8d10

==================================================

Next Steps:

1. Add first batch of commits:
   /add-commits 1 100

2. Check current project:
   /current-oss

3. List available commits:
   /list-commits

==================================================
```

## Error Handling

### Invalid GitHub URL

```
Error: Invalid GitHub URL

Expected: https://github.com/owner/repo
Got: invalid-url

Please provide a valid GitHub repository URL.
```

### Database Not Accessible

```
Error: Cannot access database

Database ID: abc123

Please ensure:
1. Database ID is correct (from Notion URL)
2. Integration is connected to the database
   - Open database in Notion
   - Click "..." → "Connections"
   - Add your integration
```

### Repository Not Found

```
Error: Repository not found

URL: https://github.com/owner/nonexistent

The repository may be:
- Private (without access token)
- Deleted or renamed
- Typo in URL
```

### Clone Failed

```
Warning: Could not clone repository

Error: timeout

The repository will be registered without local clone.
Some features may be limited.

You can manually clone to:
  ~/.claude/deep-code-reader/repos/owner/repo
```

## Tips

1. **Database ID**: Found in Notion URL after `notion.so/`
2. **Integration setup**: Create at https://www.notion.so/my-integrations
3. **One database per project**: Use separate databases for different projects
4. **Re-register**: Run again to update project info or change database
