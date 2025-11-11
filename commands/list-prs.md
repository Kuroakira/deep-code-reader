---
name: list-prs
description: List pull requests from current OSS project for easy discovery
---

# List Pull Requests

Display pull requests from the currently registered OSS project, making it easy to find PRs to analyze.

## Usage

```
/list-prs
/list-prs --state merged
/list-prs --state open
/list-prs --limit 20
```

**Examples**:
```
# List 10 most recent merged PRs (default)
/list-prs

# List open PRs
/list-prs --state open

# List closed PRs
/list-prs --state closed

# List 30 recent PRs
/list-prs --limit 30

# Combine filters
/list-prs --state merged --limit 20
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

### Step 2: Fetch PRs (use GitHub MCP)

```python
# Get pull requests
prs = github_mcp.list_pull_requests(
    owner=owner,
    repo=repo,
    state=state or "merged",  # open, closed, merged, all
    per_page=limit or 10
)
```

### Step 3: Check Analysis Status

```python
# Check which PRs have been analyzed
analyzed_prs = serena_mcp.read_memory("analyzed_prs") or []

for pr in prs:
    pr["analyzed"] = pr["number"] in analyzed_prs
```

### Step 4: Display List

```markdown
🔀 Pull Requests: {owner}/{repo}

State: {state}
Showing: {count} PRs

{index}. {status} #{pr_number} - {title}
   👤 {author} • 📅 {merged_date} • 💬 {comments} comments
   🔢 {commits} commits • ✏️ {files_changed} files • +{additions}/-{deletions}

   Quick analyze:
   /analyze-pr {pr_number}

---

💡 Tips:
- Use /analyze-pr <number> to analyze any PR
- Analyzed PRs marked with ✅
- Fresh PRs marked with 🆕
```

## Output Format

### Default List (Merged PRs)

```markdown
🔀 Pull Requests: expressjs/express

State: Merged
Showing: 10 most recent PRs

1. 🆕 #5234 - Security hardening for authentication
   👤 security-team • 📅 2025-01-15 • 💬 12 comments
   🔢 5 commits • ✏️ 12 files • +450/-120 lines

   Quick analyze:
   /analyze-pr 5234

2. ✅ #5233 - Add support for async middleware
   👤 core-contributor • 📅 2025-01-14 • 💬 8 comments
   🔢 3 commits • ✏️ 6 files • +230/-45 lines

   Already analyzed: https://notion.so/pr-5233

3. 🆕 #5232 - Fix memory leak in session handling
   👤 bug-hunter • 📅 2025-01-13 • 💬 15 comments
   🔢 2 commits • ✏️ 4 files • +67/-89 lines

   Quick analyze:
   /analyze-pr 5232

4. 🆕 #5231 - Update documentation for v5.0
   👤 docs-team • 📅 2025-01-12 • 💬 5 comments
   🔢 1 commit • ✏️ 25 files • +1200/-300 lines

   Quick analyze:
   /analyze-pr 5231

[... 6 more PRs ...]

---

💡 Next actions:
- Analyze fresh PR: /analyze-pr 5234
- See more PRs: /list-prs --limit 20
- View open PRs: /list-prs --state open
- View all PRs: /list-prs --state all
```

### Open PRs

```markdown
🔀 Pull Requests: expressjs/express

State: Open
Showing: 5 PRs

1. 🆕 #5240 - Add TypeScript definitions
   👤 typescript-hero • 📅 Opened: 2025-01-16 • 💬 3 comments
   🔢 4 commits • ✏️ 15 files • +890/-0 lines
   ✅ All checks passed • 🔍 2 approving reviews

   Quick analyze:
   /analyze-pr 5240

2. 🆕 #5239 - Refactor router implementation
   👤 refactor-expert • 📅 Opened: 2025-01-15 • 💬 7 comments
   🔢 8 commits • ✏️ 20 files • +345/-456 lines
   ⚠️ Some checks failed • 🔍 1 review pending

   Quick analyze:
   /analyze-pr 5239

[... 3 more PRs ...]

---

💡 Commands:
- View merged PRs: /list-prs --state merged
- View all states: /list-prs --state all
```

## Status Indicators

### Analysis Status
- **🆕** - Not yet analyzed (fresh PR)
- **✅** - Already analyzed and in Notion
- **🔄** - Analysis in progress

### PR State Icons
- **✅** - All checks passed
- **⚠️** - Some checks failed
- **❌** - Checks failed
- **⏳** - Checks in progress
- **🔍** - Review status

### Size Indicators
- **🟢** - Small PR (<100 lines)
- **🟡** - Medium PR (100-500 lines)
- **🟠** - Large PR (500-1000 lines)
- **🔴** - Huge PR (>1000 lines)

## Error Handling

### No Project Set

```
⚠️  No OSS Project Set

Please register a project first:
  /register-oss <github-url>

Then list PRs:
  /list-prs
```

### No PRs Found

```
ℹ️  No Pull Requests Found

Repository: expressjs/express
State: merged
Limit: 10

This repository might:
- Be new with no PRs yet
- Have PRs in different state (try --state open)
- Have older PRs (try --limit 50)

Try:
  /list-prs --state all
  /list-prs --limit 50
```

### API Rate Limit

```
⚠️  GitHub API Rate Limit

Remaining: 0 requests
Resets at: 2025-01-15 14:30:00

Options:
1. Wait for rate limit reset
2. Set GITHUB_TOKEN for higher limits

Set token:
  export GITHUB_TOKEN=your_token
```

## Advanced Options

### Filter by State

```bash
# Open PRs (not merged yet)
/list-prs --state open

# Closed PRs (closed without merging)
/list-prs --state closed

# Merged PRs (default)
/list-prs --state merged

# All PRs (any state)
/list-prs --state all
```

### Limit Number of PRs

```bash
# Show 30 PRs
/list-prs --limit 30

# Show 50 PRs
/list-prs --limit 50
```

### Sort Options

```bash
# By recently updated (default)
/list-prs --sort updated

# By creation date
/list-prs --sort created

# By popularity (comments + reactions)
/list-prs --sort popularity
```

### Filter by Label

```bash
# PRs with specific label
/list-prs --label bug
/list-prs --label feature
/list-prs --label security
```

## Tips

1. **Start with merged PRs**: See completed features and fixes
2. **Explore open PRs**: Understand ongoing development
3. **Check PR size**: 🟢 Small PRs are easier to start with
4. **Review status**: ✅ means PR passed all checks
5. **Comment count**: High 💬 count indicates important discussions
6. **Track progress**: ✅ marks show analyzed PRs

## Integration with Analysis Workflow

### Typical Usage Pattern

```bash
# Step 1: Register project
/register-oss https://github.com/expressjs/express

# Step 2: Browse recent PRs
/list-prs

# Step 3: Analyze interesting PRs
/analyze-pr 5234
/analyze-pr 5233

# Step 4: Check progress
/list-prs  # See what's been analyzed (✅)

# Step 5: Explore open PRs
/list-prs --state open
/analyze-pr 5240
```

### Finding Important PRs

```bash
# Step 1: List all merged PRs
/list-prs --limit 50

# Step 2: Look for:
- 🔴 Large PRs (major features)
- High 💬 comment count (controversial/important)
- Security-related PRs
- Breaking changes

# Step 3: Analyze in order of importance
/analyze-pr <important-pr>
```

### Systematic PR Analysis

```bash
# Strategy 1: Chronological (oldest to newest)
/list-prs --limit 100 --sort created
# Start from bottom (oldest)

# Strategy 2: By size (small to large)
/list-prs --limit 50
# Start with 🟢 small PRs, progress to 🔴 large

# Strategy 3: By importance
/list-prs --sort popularity
# High comment/reaction count = important
```

## PR Analysis Priority Guide

### High Priority PRs (Analyze First)
- **Security fixes**: Labeled "security" or CVE mentioned
- **Breaking changes**: Major version bumps or API changes
- **Core features**: Fundamental functionality additions
- **Bug fixes with high impact**: Critical bugs affecting many users

### Medium Priority PRs
- **Performance improvements**: Speed or memory optimizations
- **Refactoring**: Code quality improvements
- **New features**: Additional functionality
- **Documentation updates**: Major doc improvements

### Low Priority PRs (Optional)
- **Minor bug fixes**: Edge case fixes
- **Style changes**: Formatting, linting
- **Test additions**: Additional test coverage only
- **Minor docs**: Typo fixes, small clarifications

## Example Workflow: Finding First PR

```bash
# Step 1: List oldest PRs
/list-prs --state merged --sort created --limit 100

# Step 2: Scroll to bottom for earliest PRs

# Step 3: Start analyzing from PR #1 or earliest significant PR
/analyze-pr 1

# Step 4: Continue chronologically
/analyze-pr 2
/analyze-pr 3
```
