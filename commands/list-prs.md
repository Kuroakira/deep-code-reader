---
name: list-prs
description: List pull requests from current OSS project for easy discovery
---

# List Pull Requests

Display pull requests from the currently registered OSS project, making it easy to find PRs to analyze.

**Deep Code Reader Philosophy**: Start from the beginning! By default, this command shows the **oldest PRs first** to help you understand the project's evolution chronologically.

## Usage

```
/list-prs
/list-prs --order newest
/list-prs --state merged
/list-prs --state open
/list-prs --limit 20
```

**Examples**:
```
# List 10 oldest merged PRs (default - recommended for learning!)
/list-prs

# List 10 newest merged PRs
/list-prs --order newest

# List oldest open PRs
/list-prs --state open

# List oldest closed PRs
/list-prs --state closed

# List 30 oldest PRs
/list-prs --limit 30

# Combine filters
/list-prs --state merged --limit 20 --order newest
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
# Parse order option (default: oldest first)
order = "oldest"  # Default to chronological learning
if args.get("order") == "newest":
    order = "newest"

# Get pull requests
prs = github_mcp.list_pull_requests(
    owner=owner,
    repo=repo,
    state=state or "merged",  # open, closed, merged, all
    per_page=limit or 10,
    sort="created",  # Always sort by creation date for chronological order
    direction="asc" if order == "oldest" else "desc"  # Ascending = oldest first
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
Order: {order} (oldest first / newest first)
Showing: {count} PRs

{index}. {status} #{pr_number} - {title}
   👤 {author} • 📅 {merged_date} • 💬 {comments} comments
   🔢 {commits} commits • ✏️ {files_changed} files • +{additions}/-{deletions}

   Quick analyze:
   /analyze-pr {pr_number}

---

💡 Tips:
- Default shows oldest PRs (start from the beginning!)
- Use --order newest for recent PRs
- Analyzed PRs marked with ✅
- Fresh PRs marked with 🆕
```

## Output Format

### Default List (Oldest Merged PRs First)

```markdown
🔀 Pull Requests: expressjs/express

State: Merged
Order: oldest first
Showing: 10 oldest PRs

1. 🆕 #1 - Initial project structure and basic routing
   👤 tj • 📅 2009-07-15 • 💬 2 comments
   🔢 1 commit • ✏️ 8 files • +250/-0 lines

   Quick analyze:
   /analyze-pr 1

2. ✅ #2 - Add middleware support
   👤 tj • 📅 2009-07-16 • 💬 1 comment
   🔢 2 commits • ✏️ 4 files • +120/-5 lines

   Already analyzed: https://notion.so/pr-2

3. 🆕 #3 - Implement template engine integration
   👤 contributor1 • 📅 2009-07-20 • 💬 5 comments
   🔢 3 commits • ✏️ 6 files • +180/-12 lines

   Quick analyze:
   /analyze-pr 3

4. 🆕 #4 - Add request/response helpers
   👤 contributor2 • 📅 2009-07-25 • 💬 3 comments
   🔢 1 commit • ✏️ 3 files • +95/-8 lines

   Quick analyze:
   /analyze-pr 4

[... 6 more early PRs ...]

---

💡 Next actions:
- Start learning from the first PR: /analyze-pr 1
- See more early PRs: /list-prs --limit 20
- Jump to recent PRs: /list-prs --order newest
- View open PRs: /list-prs --state open
```

### Newest First Option

```markdown
🔀 Pull Requests: expressjs/express

State: Merged
Order: newest first
Showing: 10 newest PRs

1. 🆕 #5234 - Security hardening for authentication
   👤 security-team • 📅 2025-01-15 • 💬 12 comments
   🔢 5 commits • ✏️ 12 files • +450/-120 lines

   Quick analyze:
   /analyze-pr 5234

2. ✅ #5233 - Add support for async middleware
   👤 core-contributor • 📅 2025-01-14 • 💬 8 comments
   🔢 3 commits • ✏️ 6 files • +230/-45 lines

   Already analyzed: https://notion.so/pr-5233

[... 8 more recent PRs ...]

---

💡 Commands:
- Back to chronological learning: /list-prs
- View all PRs: /list-prs --state all
```

### Open PRs (Oldest First)

```markdown
🔀 Pull Requests: expressjs/express

State: Open
Order: oldest first
Showing: 5 oldest open PRs

1. 🆕 #4850 - Add HTTP/2 support (long-standing discussion)
   👤 http2-champion • 📅 Opened: 2018-03-10 • 💬 156 comments
   🔢 12 commits • ✏️ 25 files • +1200/-50 lines
   ⚠️ Needs rebase • 🔍 Multiple reviews over years

   Quick analyze:
   /analyze-pr 4850

2. 🆕 #5105 - Refactor core middleware system
   👤 refactor-expert • 📅 Opened: 2020-09-15 • 💬 45 comments
   🔢 8 commits • ✏️ 20 files • +345/-456 lines
   ⚠️ Some checks failed • 🔍 1 review pending

   Quick analyze:
   /analyze-pr 5105

[... 3 more oldest open PRs ...]

---

💡 Commands:
- View newest open PRs: /list-prs --state open --order newest
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

### Change Sort Order

```bash
# Oldest PRs first (default - chronological learning)
/list-prs

# Newest PRs first
/list-prs --order newest
```

### Filter by State

```bash
# Open PRs (not merged yet) - oldest first
/list-prs --state open

# Closed PRs (closed without merging) - oldest first
/list-prs --state closed

# Merged PRs (default) - oldest first
/list-prs --state merged

# All PRs (any state) - oldest first
/list-prs --state all
```

### Limit Number of PRs

```bash
# Show 30 oldest PRs
/list-prs --limit 30

# Show 50 oldest PRs
/list-prs --limit 50

# Show 30 newest PRs
/list-prs --limit 30 --order newest
```

### Filter by Label

```bash
# PRs with specific label (oldest first)
/list-prs --label bug
/list-prs --label feature
/list-prs --label security

# Combine with newest first
/list-prs --label security --order newest
```

## Tips

1. **Start from the beginning**: Default shows oldest PRs for chronological learning
2. **Follow project evolution**: Understand how features were introduced over time
3. **Check status icons**: ✅ shows analyzed PRs
4. **Check PR size**: 🟢 Small PRs are easier to start with for beginners
5. **Comment count**: High 💬 count indicates important discussions
6. **Use --order newest when needed**: Quick check of recent development
7. **Track progress**: ✅ marks help avoid duplicate analysis
8. **Explore open PRs**: See long-standing discussions and proposals

## Integration with Analysis Workflow

### Typical Usage Pattern (Chronological Learning)

```bash
# Step 1: Register project
/register-oss https://github.com/expressjs/express

# Step 2: Browse oldest PRs (default behavior)
/list-prs

# Step 3: Start analyzing from the very first PR
/analyze-pr 1  # Initial PR

# Step 4: Continue chronologically
/analyze-pr 2  # Second PR
/analyze-pr 3  # Third PR

# Step 5: Check progress
/list-prs  # See what's been analyzed (✅)

# Step 6: Continue systematic learning
/list-prs --limit 20  # Get next batch of old PRs

# Step 7: Explore open PRs when ready
/list-prs --state open
```

### Finding First PRs (Now Default!)

```bash
# The very first PRs are now shown by default!
/list-prs

# First result will be PR #1 or the earliest merged PR
# No need for special sorting or commands

# Want to see more early PRs?
/list-prs --limit 50
```

### Systematic Chronological Analysis (Recommended)

```bash
# Step 1: Get oldest PRs (default)
/list-prs --limit 20

# Step 2: Analyze from the beginning
/analyze-pr 1
/analyze-pr 2
# ... work chronologically forward

# Step 3: Track progress with icons (✅)
/list-prs --limit 20  # Check what's analyzed

# Step 4: Continue with next batch
/list-prs --limit 20  # Still shows oldest unanalyzed PRs

# Alternative: If you need to check recent changes
/list-prs --order newest --limit 10
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

## Example Workflow: Chronological PR Analysis

```bash
# Step 1: List oldest PRs (default behavior!)
/list-prs --state merged --limit 20

# Step 2: First result is the earliest PR - start there!
/analyze-pr 1  # Or whatever the first PR number is

# Step 3: Continue chronologically from the beginning
/analyze-pr 2
/analyze-pr 3
/analyze-pr 4

# Step 4: Get next batch of old PRs
/list-prs --limit 20  # Continues showing oldest unanalyzed

# Step 5: Track your progress
/list-prs --limit 50  # ✅ marks show what you've analyzed

# Alternative: Jump to recent PRs if needed
/list-prs --order newest --limit 10
```
