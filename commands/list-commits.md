---
name: list-commits
description: List commits from current OSS project for easy discovery
---

# List Commits

Display commits from the currently registered OSS project, making it easy to find commits to analyze.

**Deep Code Reader Philosophy**: Start from the beginning! By default, this command shows the **oldest commits first** to help you understand the project's evolution chronologically.

## Usage

```
/list-commits
/list-commits --order newest
/list-commits --limit 20
/list-commits --branch develop
/list-commits --author username
```

**Examples**:
```
# List 10 oldest commits (default - recommended for learning!)
/list-commits

# List 10 newest commits
/list-commits --order newest

# List 50 oldest commits
/list-commits --limit 50

# List newest commits
/list-commits --order newest --limit 20

# List commits from specific branch (oldest first)
/list-commits --branch develop

# List commits by specific author (oldest first)
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
# Parse order option (default: oldest first)
order = "oldest"  # Default to chronological learning
if args.get("order") == "newest":
    order = "newest"

# Get commits
commits = github_mcp.list_commits(
    owner=owner,
    repo=repo,
    branch=branch or "main",
    per_page=limit or 10
)

# Reverse to show oldest first (GitHub API returns newest first)
if order == "oldest":
    commits = list(reversed(commits))
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
📋 Commits: {owner}/{repo}

Branch: {branch}
Order: {order} (oldest first / newest first)
Showing: {count} commits

{index}. {status} {short_sha} - {message_first_line}
   👤 {author} • 📅 {date} • ✏️ {files_changed} files

   Quick analyze:
   /analyze-commit {short_sha}

---

💡 Tips:
- Default shows oldest commits (start from the beginning!)
- Use --order newest for recent commits
- Analyzed commits marked with ✅
- Fresh commits marked with 🆕
```

## Output Format

### Default List (10 commits - Oldest First)

```markdown
📋 Commits: expressjs/express

Branch: main
Order: oldest first
Showing: 10 oldest commits

1. 🆕 f7c8d10 - Initial commit
   👤 tj • 📅 2009-06-26 • ✏️ 12 files

   Quick analyze:
   /analyze-commit f7c8d10

2. ✅ a3b4c5d - Add basic routing functionality
   👤 tj • 📅 2009-06-27 • ✏️ 3 files

   Already analyzed: https://notion.so/commit-a3b4c5d

3. 🆕 e6f7g8h - Implement middleware support
   👤 tj • 📅 2009-06-28 • ✏️ 5 files

   Quick analyze:
   /analyze-commit e6f7g8h

4. 🆕 i9j0k1l - Add template engine integration
   👤 contributor • 📅 2009-07-01 • ✏️ 8 files

   Quick analyze:
   /analyze-commit i9j0k1l

[... 6 more commits from early development ...]

---

💡 Next actions:
- Start learning from the beginning: /analyze-commit f7c8d10
- See more early commits: /list-commits --limit 20
- Jump to recent commits: /list-commits --order newest
- Filter by author: /list-commits --author tj
```

### With Newest First Option

```markdown
📋 Commits: expressjs/express

Branch: main
Order: newest first
Showing: 10 newest commits

1. 🆕 abc1234 - Fix security vulnerability in auth middleware
   👤 johndoe • 📅 2025-01-15 • ✏️ 3 files

   Quick analyze:
   /analyze-commit abc1234

2. ✅ def5678 - Add rate limiting to API endpoints
   👤 janedoe • 📅 2025-01-14 • ✏️ 5 files

   Already analyzed: https://notion.so/commit-def5678

[... 8 more recent commits ...]

---

💡 Commands:
- Back to chronological learning: /list-commits
- See older commits: /list-commits --limit 50
```

### With Filters (Oldest First by Default)

```markdown
📋 Commits: expressjs/express

Branch: develop
Author: johndoe
Order: oldest first
Showing: 5 commits from johndoe

1. 🆕 m2n3o4p - First contribution: Add error handling
   👤 johndoe • 📅 2015-03-20 • ✏️ 4 files

   Quick analyze:
   /analyze-commit m2n3o4p

2. 🆕 q5r6s7t - Improve middleware logging
   👤 johndoe • 📅 2015-04-12 • ✏️ 2 files

   Quick analyze:
   /analyze-commit q5r6s7t

[... 3 more commits ...]

---

💡 Commands:
- Remove author filter: /list-commits --branch develop
- Back to main branch: /list-commits
- See newest from this author: /list-commits --author johndoe --order newest
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

### Change Sort Order

```
/list-commits --order newest
```

Show newest commits first (default is oldest first for chronological learning)

### Limit Number of Commits

```
/list-commits --limit 50
```

Shows up to 50 commits (default: 10, max: 100). Always in chronological order (oldest first) unless --order newest is specified.

### Filter by Branch

```
/list-commits --branch develop
```

Shows commits from specific branch (oldest first by default)

### Filter by Author

```
/list-commits --author johndoe
```

Shows commits only from specific author (oldest first by default)

### Combine Filters

```
/list-commits --branch develop --author johndoe --limit 20 --order newest
```

Shows 20 newest commits from johndoe on develop branch

### Show File Changes

```
/list-commits --show-files
```

Display list of changed files for each commit

## Tips

1. **Start from the beginning**: Default shows oldest commits for chronological learning
2. **Check status icons**: See which commits are already analyzed (✅)
3. **Copy-paste hashes**: Easy /analyze-commit execution
4. **Follow chronological order**: Understand project evolution from first commit
5. **Use --order newest when needed**: Quick check of recent changes
6. **Filter strategically**: Use --author to follow a contributor's journey
7. **Explore branches**: Use --branch to discover feature development
8. **Track progress**: ✅ marks help avoid duplicate analysis

## Integration with Analysis Workflow

### Typical Usage Pattern (Chronological Learning)

```bash
# Step 1: Register project
/register-oss https://github.com/expressjs/express

# Step 2: Browse oldest commits (default behavior)
/list-commits

# Step 3: Start analyzing from the very first commit
/analyze-commit f7c8d10  # Initial commit

# Step 4: Continue chronologically
/analyze-commit a3b4c5d  # Second commit
/analyze-commit e6f7g8h  # Third commit

# Step 5: Check progress
/list-commits  # See what's been analyzed (✅)

# Step 6: Continue systematic learning
/list-commits --limit 20  # Get next batch of old commits
```

### Finding First Commit (Now Default!)

```bash
# The very first commit is now shown by default!
/list-commits

# First result will be the initial commit
# No need for special commands or GitHub search

# Want to see more early commits?
/list-commits --limit 50
```

### Systematic Chronological Analysis (Recommended)

```bash
# Step 1: Get oldest commits (default)
/list-commits --limit 20

# Step 2: Analyze from the beginning
/analyze-commit <first-commit-hash>
/analyze-commit <second-commit-hash>
# ... work chronologically forward

# Step 3: Track progress with icons (✅)
/list-commits --limit 20  # Check what's analyzed

# Step 4: Continue with next batch
/list-commits --limit 20  # Still shows oldest unanalyzed commits

# Alternative: If you need to check recent changes
/list-commits --order newest --limit 10
```
