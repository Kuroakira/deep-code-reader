---
name: analyze-pr
description: Analyze all commits in a Pull Request with context and export to Notion
---

# Analyze Pull Request

Analyze all commits within a PR, understanding the collective changes and their purpose.

## Usage

```
/analyze-pr <pr-url>
/analyze-pr <github-url>/pull/<number>
```

**Examples**:
```
/analyze-pr https://github.com/expressjs/express/pull/5234
/analyze-pr https://github.com/expressjs/express 5234
```

## Workflow

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

## Tips

- Use PR analysis for understanding feature additions
- Use commit analysis for detailed change inspection
- Check PR description for context before diving into commits
