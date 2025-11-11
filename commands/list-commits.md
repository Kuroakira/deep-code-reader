---
name: list-commits
description: List recent commits from current OSS project for easy discovery
---

# List Recent Commits

Display recent commits from the currently registered OSS project, making it easy to find commits to analyze.

## Usage

```
/list-commits
/list-commits --limit 20
/list-commits --branch develop
/list-commits --author username
```

**Examples**:
```
# List 10 most recent commits (default)
/list-commits

# List 50 recent commits
/list-commits --limit 50

# List commits from specific branch
/list-commits --branch develop

# List commits by specific author
/list-commits --author octocat
```

## Workflow

### Step 1: Get Current Project

```python
# Read current OSS from memory
current_oss = serena_mcp.read_memory("current_oss")

if not current_oss:
    print("⚠️  No project set. Run: /register-oss <url>")
    return

owner = current_oss["owner"]
repo = current_oss["repo"]
```

### Step 2: Fetch Commits (use GitHub MCP)

```python
# Get recent commits
commits = github_mcp.list_commits(
    owner=owner,
    repo=repo,
    branch=branch or "main",
    per_page=limit or 10
)
```

### Step 3: Check Analysis Status (optional)

```python
# Check which commits have been analyzed
analyzed_commits = serena_mcp.read_memory("analyzed_commits") or []

for commit in commits:
    commit["analyzed"] = commit["sha"] in analyzed_commits
```

### Step 4: Display List

```markdown
📋 Recent Commits: {owner}/{repo}

Branch: {branch}
Showing: {count} commits

{index}. {status} {short_sha} - {message_first_line}
   👤 {author} • 📅 {date} • ✏️ {files_changed} files

   Quick analyze:
   /analyze-commit {short_sha}

---

💡 Tips:
- Use /analyze-commit <hash> to analyze any commit
- Analyzed commits marked with ✅
- Fresh commits marked with 🆕
```

## Output Format

### Default List (10 commits)

```markdown
📋 Recent Commits: expressjs/express

Branch: main
Showing: 10 most recent commits

1. 🆕 abc1234 - Fix security vulnerability in auth middleware
   👤 johndoe • 📅 2025-01-15 • ✏️ 3 files

   Quick analyze:
   /analyze-commit abc1234

2. ✅ def5678 - Add rate limiting to API endpoints
   👤 janedoe • 📅 2025-01-14 • ✏️ 5 files

   Already analyzed: https://notion.so/commit-def5678

3. 🆕 ghi9012 - Update dependencies to latest versions
   👤 maintainer • 📅 2025-01-13 • ✏️ 1 file

   Quick analyze:
   /analyze-commit ghi9012

4. 🆕 jkl3456 - Refactor authentication module
   👤 contributor • 📅 2025-01-12 • ✏️ 8 files

   Quick analyze:
   /analyze-commit jkl3456

[... 6 more commits ...]

---

💡 Next actions:
- Analyze fresh commit: /analyze-commit abc1234
- See more commits: /list-commits --limit 20
- Filter by author: /list-commits --author johndoe
- Switch branch: /list-commits --branch develop
```

### With Filters

```markdown
📋 Recent Commits: expressjs/express

Branch: develop
Author: johndoe
Showing: 5 commits

1. 🆕 xyz7890 - Implement new caching strategy
   👤 johndoe • 📅 2025-01-16 • ✏️ 4 files

   Quick analyze:
   /analyze-commit xyz7890

2. 🆕 uvw4567 - Add tests for auth module
   👤 johndoe • 📅 2025-01-14 • ✏️ 2 files

   Quick analyze:
   /analyze-commit uvw4567

[... 3 more commits ...]

---

💡 Commands:
- Remove author filter: /list-commits --branch develop
- Back to main branch: /list-commits
```

## Status Indicators

- **🆕** - Not yet analyzed (fresh commit)
- **✅** - Already analyzed and in Notion
- **🔄** - Analysis in progress
- **⚠️** - Large commit (>20 files changed)

## Error Handling

### No Project Set

```
⚠️  No OSS Project Set

Please register a project first:
  /register-oss <github-url>

Then list commits:
  /list-commits
```

### Branch Not Found

```
❌ Branch not found: develop

Available branches:
- main (default)
- staging
- feature/new-api

Usage:
  /list-commits --branch main
```

### No Commits Found

```
ℹ️  No Commits Found

Repository: expressjs/express
Branch: main
Author filter: nonexistent-user

Possible reasons:
- No commits from this author
- Branch is empty
- Repository is new

Try:
  /list-commits  # Remove filters
```

### API Rate Limit

```
⚠️  GitHub API Rate Limit

Remaining: 0 requests
Resets at: 2025-01-15 14:30:00

Options:
1. Wait 15 minutes for rate limit reset
2. Set GITHUB_TOKEN for higher limits (5000/hour)

Set token:
  export GITHUB_TOKEN=your_token
```

## Advanced Options

### Limit Number of Commits

```
/list-commits --limit 50
```

Shows up to 50 recent commits (default: 10, max: 100)

### Filter by Branch

```
/list-commits --branch develop
```

Shows commits from specific branch

### Filter by Author

```
/list-commits --author johndoe
```

Shows commits only from specific author

### Combine Filters

```
/list-commits --branch develop --author johndoe --limit 20
```

Shows 20 commits from johndoe on develop branch

### Show File Changes

```
/list-commits --show-files
```

Display list of changed files for each commit

## Tips

1. **Start with list-commits**: Browse commits before analyzing
2. **Check status icons**: See which commits are already analyzed
3. **Copy-paste hashes**: Easy /analyze-commit execution
4. **Filter strategically**: Use --author to focus on specific contributors
5. **Explore branches**: Use --branch to discover feature development
6. **Track progress**: ✅ marks help avoid duplicate analysis

## Integration with Analysis Workflow

### Typical Usage Pattern

```bash
# Step 1: Register project
/register-oss https://github.com/expressjs/express

# Step 2: Browse recent commits
/list-commits

# Step 3: Analyze interesting commits
/analyze-commit abc1234
/analyze-commit def5678

# Step 4: Check progress
/list-commits  # See what's been analyzed (✅)

# Step 5: Continue with fresh commits
/analyze-commit ghi9012
```

### Finding First Commit

```bash
# Get recent commits
/list-commits --limit 100

# Oldest commit will be at the bottom
# Or use GitHub directly for repository's first commit
```

### Systematic Analysis

```bash
# Analyze commits chronologically
/list-commits --limit 50

# Start from oldest to newest
/analyze-commit <oldest-hash>
# ... work your way up

# Or start from newest
/analyze-commit <newest-hash>
# ... work your way down
```
