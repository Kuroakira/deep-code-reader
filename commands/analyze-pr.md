---
name: analyze-pr
description: Analyze all commits in a Pull Request with context and export to Notion
---

# Analyze Pull Request

Analyze all commits within a PR, understanding the collective changes and their purpose.

## Usage

```
/analyze-pr <pr-number>
/analyze-pr <pr-url>
/analyze-pr <github-url>/pull/<number>
```

**Examples**:
```
# After /register-oss - just PR number!
/analyze-pr 5234

# Or with full URL
/analyze-pr https://github.com/expressjs/express/pull/5234
/analyze-pr https://github.com/expressjs/express 5234
```

## Workflow

### Step 0: Repository URL Resolution

Determine the repository URL and PR number:

```python
# Parse input - could be just number, full URL, or URL + number
if input_is_number_only(input):
    # Just PR number provided, read from memory
    pr_number = input
    current_oss = serena_mcp.read_memory("current_oss")

    if not current_oss:
        print("⚠️  No repository set. Please:")
        print("  1. Register: /register-oss <github-url>")
        print("  2. Or specify full URL: /analyze-pr <pr-url>")
        return

    owner = current_oss["owner"]
    repo = current_oss["repo"]
    github_url = current_oss["repo_url"]
    notion_oss_page_id = current_oss["notion_page_id"]

    print(f"📦 Using current project: {owner}/{repo}")
else:
    # Full URL or URL + number provided
    owner, repo, pr_number = parse_pr_url(input)
```

### Step 1: PR Information Gathering

```python
# Get PR details
pr_data = github_mcp.get_pr(owner, repo, pr_number)

Extract:
- PR title & description
- All commits in PR
- Reviews & comments
- Labels & milestones
- Merge status
```

### Step 2: User Choice

```markdown
📋 Pull Request #5234: "Security hardening for auth"

Found: 5 commits

Options:
1. Analyze all commits (recommended)
2. Analyze specific commits (select)
3. PR summary only (skip individual commits)

> _
```

### Step 3: Batch Analysis

For each commit:
1. Run `/analyze-commit` workflow
2. Show progress: `Analyzing commit 1/5...`
3. Export to Notion individually
4. Continue to next

### Step 4: PR Summary

Create additional summary entry in Notion:

```markdown
## PR Summary

Title: Security hardening for auth
Status: Merged
Commits: 5
Files Changed: 12
Lines: +450, -120

### Overview
[Synthesized analysis of all commits]

### Key Changes
- Feature 1
- Feature 2
- Bug fixes

### Impact
[Combined impact assessment]

### Review Notes
- 5 approving reviews
- 2 change requests (resolved)
- Security team approved
```

## Output Format

```markdown
📊 PR Analysis Complete

PR #5234: Security hardening for auth
Status: Merged (2025-01-10)

Analyzed Commits:
✅ abc1234: Add input validation
✅ abc1235: Implement rate limiting
✅ abc1236: Add test coverage
✅ abc1237: Update documentation
✅ abc1238: Fix edge case

🔗 Notion:
- PR Summary: https://notion.so/pr-summary-id
- Individual commits: 5 pages created

💡 View all in Notion under: [OSS → Express.js → PR #5234]
```

### Next PR Suggestions

After successful analysis, suggest next PRs to analyze:

```python
# Get recent merged PRs
recent_prs = github_mcp.list_pull_requests(
    owner=owner,
    repo=repo,
    state="merged",
    per_page=5
)

# Filter out already analyzed PRs
analyzed_prs = serena_mcp.read_memory("analyzed_prs") or []
unanalyzed = [pr for pr in recent_prs if pr["number"] not in analyzed_prs]

# Mark current PR as analyzed
analyzed_prs.append(pr_number)
serena_mcp.write_memory("analyzed_prs", analyzed_prs)
```

Display suggestions:

```markdown
---

🔍 Next Suggestions

Recent merged PRs from this project:

1. 🆕 #5235 - Add TypeScript definitions
   📅 Merged: 2025-01-16 • 💬 8 comments • 🔢 4 commits
   /analyze-pr 5235

2. 🆕 #5233 - Performance optimization for routing
   📅 Merged: 2025-01-14 • 💬 12 comments • 🔢 6 commits
   /analyze-pr 5233

3. ✅ #5232 - Fix memory leak (already analyzed)

💡 Commands:
  /list-prs              # Browse all PRs
  /list-prs --state open # See open PRs
  /list-commits          # Browse individual commits
  /current-oss           # Check current project

Continue exploring! 🚀
```

## Tips

- Use PR analysis for understanding feature additions
- Use commit analysis for detailed change inspection
- Check PR description for context before diving into commits
