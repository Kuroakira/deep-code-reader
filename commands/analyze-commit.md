---
name: analyze-commit
description: Deep analysis of a single commit with context gathering and Notion export
---

# Analyze Single Commit

Perform comprehensive analysis of a single commit, understanding the **Why**, **What**, **Impact**, and **Design** behind the changes.

## Usage

```
/analyze-commit <commit-hash>
/analyze-commit <github-url> <commit-hash>  # URL optional if project registered
```

**Examples**:
```
# After /register-oss - URL not needed!
/analyze-commit abc1234567
/analyze-commit abc1234  # Short hash OK

# Or with explicit URL
/analyze-commit https://github.com/expressjs/express abc1234567
```

## Analysis Workflow

### Phase 0: Repository URL Resolution

Determine the repository URL to use:

```python
# If URL not provided, read from memory
if not github_url:
    current_oss = serena_mcp.read_memory("current_oss")

    if not current_oss:
        print("⚠️  No repository specified and no current project set")
        print("Please either:")
        print("  1. Register a project: /register-oss <github-url>")
        print("  2. Or specify URL: /analyze-commit <github-url> <commit-hash>")
        return

    github_url = current_oss["repo_url"]
    owner = current_oss["owner"]
    repo = current_oss["repo"]
    notion_oss_page_id = current_oss["notion_page_id"]

    print(f"📦 Using current project: {owner}/{repo}")
else:
    # URL provided, parse it
    owner, repo = parse_github_url(github_url)
```

### Phase 1: Commit Data Gathering (use GitHub MCP)

Fetch commit information:

```python
# Get commit details
commit_info = github_mcp.get_commit(owner, repo, commit_hash)

Required data:
- Commit hash (full & short)
- Commit message
- Author & date
- Changed files
- Diff content
- Parent commits
```

### Phase 2: Context Gathering (use GitHub MCP + Sequential Thinking)

#### 2.1 Related Issues

Extract issue references from:
- Commit message: `#123`, `fixes #456`, `closes #789`
- PR associations: If commit is part of a PR

```python
# Find related issues
issues = extract_issue_numbers(commit_message)
for issue_num in issues:
    issue_data = github_mcp.get_issue(owner, repo, issue_num)
    # Store: issue title, description, labels
```

#### 2.2 Before & After Context

Get surrounding commits:

```python
# Get commit timeline
before_commits = git log --oneline {commit}~3..{commit}~1
after_commits = git log --oneline {commit}..{commit}+2

Context includes:
- 1-2 commits before
- 1-2 commits after
- Brief description of each
```

#### 2.3 Pull Request Context (if applicable)

```python
# Find associated PR
prs = github_mcp.search_prs(query=f"commit:{commit_hash}")
if prs:
    pr_data = github_mcp.get_pr(owner, repo, pr.number)
    # Store: PR title, description, reviews, comments
```

### Phase 3: Change Analysis (use Serena MCP + Sequential Thinking)

#### 3.1 変更の意図 (Why)

Analyze **why** this change was made:

```markdown
- 問題: What problem does this solve?
- 動機: Why was this approach chosen?
- 背景: What's the business/technical context?

Sources:
- Commit message
- Related issue descriptions
- PR discussions
- Code comments
```

#### 3.2 変更内容 (What)

Document **what** was changed:

```markdown
変更されたファイル:
- file1.js: Added authentication middleware
- file2.js: Updated route handler
- test/file1.test.js: Added tests

主な変更点:
[Code diff summary with key changes highlighted]
```

#### 3.3 影響範囲 (Impact)

Assess **impact** on the codebase:

Use Serena MCP to analyze:
- Which modules depend on changed code
- Breaking changes
- API compatibility
- Performance implications

```markdown
影響を受けるモジュール:
- auth/ - Direct usage
- api/routes/ - Indirect dependency
- middleware/ - Configuration change

リスク:
- 破壊的変更: No
- パフォーマンス: +10% faster (from benchmarks)
- セキュリティ: Improved (CVE-2024-1234 fixed)
```

#### 3.4 設計意図 (Design)

Understand **design** decisions:

Use Sequential Thinking to analyze:
- Architectural patterns used
- Design trade-offs
- Alternative approaches
- Future extensibility

```markdown
設計パターン:
- Middleware pattern for separation of concerns
- Dependency injection for testability

トレードオフ:
- Added complexity vs improved security
- Memory +2MB vs 10x faster

将来の拡張性:
- Can add more auth providers
- Backward compatible with v1.x
```

### Phase 4: Console Output

Display analysis in console:

```markdown
📊 Commit Analysis: abc1234

## 🎯 変更の意図 (Why)
Fix security vulnerability in authentication middleware (CVE-2024-1234)

Related Issues:
- #1234: Security: Auth bypass in edge case
- #1235: Enhancement: Add rate limiting

## 📝 変更内容 (What)

Changed Files (3):
- src/auth/middleware.js (+45, -12)
- src/auth/validator.js (+23, -5)
- test/auth.test.js (+67, -0)

Key Changes:
- Add input validation for auth tokens
- Implement rate limiting (100 req/min)
- Add comprehensive test coverage

## 🏗️ 影響範囲 (Impact)

Affected Modules:
- api/routes/* (10 files) - All routes using auth
- middleware/session.js - Session handling logic
- config/security.js - Security configuration

Risk Assessment:
✅ No breaking changes
✅ Backward compatible
⚠️  Requires config update in production

## 🎨 設計意図 (Design)

Pattern: Chain of Responsibility for validation
Trade-off: +2MB memory for 10x security improvement
Extensibility: Can add custom validators via plugin

## 🔗 コンテキスト

Before this commit:
- abc0123: Refactor auth module structure
- abc0122: Add auth logging

After this commit:
- abc1235: Update documentation
- abc1236: Deploy to staging

Related PR: #5234 "Security hardening"
- 5 approving reviews
- Passed all CI checks
- Merged 2 days ago

---

💾 Exporting to Notion...
```

### Phase 5: Notion Export (use Notion MCP)

#### 5.1 Find OSS Page

```python
# Query OSSリスト database
oss_pages = notion_mcp.query_database(
    database_id=oss_database_id,
    filter={"property": "GitHub URL", "url": {"equals": repo_url}}
)

if not oss_pages:
    print("⚠️  Repository not registered. Run: /register-oss <url>")
    return

oss_page_id = oss_pages[0]["id"]
```

#### 5.2 Get Commits Database ID from Memory

```python
# Get OSS-specific commits database ID from current_oss memory
current_oss = serena_mcp.read_memory("current_oss")
commits_database_id = current_oss["commits_database_id"]
```

**Important**: Each OSS has its own Commits & PRs database. The database ID is stored in Serena memory when the OSS is registered.

#### 5.3 Create Commit Entry

```python
# Create page in OSS-specific Commits & PRs database
commit_page = notion_mcp.create_page(
    parent={"database_id": commits_database_id},
    properties={
        "Title": f"{commit_hash_short}: {commit_message_first_line}",
        "Commit ID / PR No": commit_hash,
        "Comment": commit_message,
        "Created Date": commit_date,
        "GitHub URL": f"{repo_url}/commit/{commit_hash}",
        "Memo": "",  # Empty for user to fill
    },
    children=[
        # ... all content blocks from template
    ]
)
```

**Note**: No OSS relation property needed since each database is OSS-specific.

#### 5.4 Confirm Export

```markdown
✅ Exported to Notion!

📄 Notion Page: https://notion.so/commit-page-id
🔗 View commit: [link to OSS page] → [link to this commit]

💡 Tip: Add personal notes in the "Memo" field
```

### Phase 6: Next Commit Suggestions

After successful analysis, suggest next commits to analyze:

```python
# Get surrounding commits for context
timeline_commits = github_mcp.list_commits(
    owner=owner,
    repo=repo,
    per_page=5
)

# Filter out already analyzed commits
analyzed_commits = serena_mcp.read_memory("analyzed_commits") or []
unanalyzed = [c for c in timeline_commits if c["sha"] not in analyzed_commits]

# Mark current commit as analyzed
analyzed_commits.append(commit_hash)
serena_mcp.write_memory("analyzed_commits", analyzed_commits)
```

Display suggestions:

```markdown
---

🔍 Next Suggestions

Recent commits from this project:

1. 🆕 def5678 - Add rate limiting to API endpoints
   📅 2025-01-14 • 👤 janedoe • ✏️ 5 files
   /analyze-commit def5678

2. 🆕 ghi9012 - Update dependencies
   📅 2025-01-13 • 👤 maintainer • ✏️ 1 file
   /analyze-commit ghi9012

3. ✅ xyz3456 - Refactor auth module (already analyzed)

💡 Commands:
  /list-commits           # Browse all recent commits
  /list-prs              # Browse pull requests
  /current-oss           # Check current project

Continue your learning journey! 🚀
```

## Error Handling

### Repository Not Set

```
⚠️  No Repository Specified

You haven't specified a repository URL and no current project is set.

Options:
1. Register a project first:
   /register-oss https://github.com/expressjs/express
   /analyze-commit abc1234

2. Or specify URL directly:
   /analyze-commit https://github.com/expressjs/express abc1234

Check current project:
   /current-oss
```

### Commit Not Found

```
❌ Error: Commit not found

Commit: abc1234
Repository: expressjs/express

Possible reasons:
- Commit hash is incorrect
- Commit was force-pushed/deleted
- Private repository without access

Please verify the commit hash.
```

### Repository Not Registered

```
⚠️  Repository Not Registered

Before analyzing commits, register the repository:

  /register-oss https://github.com/expressjs/express

This creates a parent entry in your OSSリスト database.
```

### Large Diff

```
⚠️  Large Commit Detected

This commit changes 150+ files (12,000 lines).

Options:
1. Continue with full analysis (~5min)
2. Summary only (skip detailed analysis)
3. Cancel

> _
```

### Related Issue Not Found

```
ℹ️  Context Gathering

Found issue references: #1234, #5678

✅ #1234: Security vulnerability (loaded)
❌ #5678: Issue not found or private

Continuing with available context...
```

## Output Format

### Console (always shown)

```markdown
📊 Commit Analysis Complete

## Summary
- Changed: 3 files
- Added: 135 lines
- Removed: 17 lines
- Impact: Medium (10 dependent modules)

## Key Insights
🎯 Why: Security fix for CVE-2024-1234
📝 What: Auth middleware validation
🏗️ Impact: All API routes (backward compatible)
🎨 Design: Chain of Responsibility pattern

🔗 Full analysis: https://notion.so/commit-page-id
```

### Notion (complete analysis)

Full detailed page with:
- 🎯 変更の意図
- 📝 変更内容 (with code diff)
- 🏗️ 影響範囲
- 🎨 設計意図
- 🔗 コンテキスト (issues, commits, PR)
- 📋 Complete diff (in toggle)

## Advanced Features

### Compare Mode

```
/analyze-commit <url> <commit1>..<commit2>
```

Analyze changes between two commits.

### Focus Analysis

```
/analyze-commit <url> <commit> --focus security
```

Focus on specific aspects:
- `security`: Security implications
- `performance`: Performance impact
- `api`: API changes
- `breaking`: Breaking changes

### Skip Export

```
/analyze-commit <url> <commit> --no-export
```

Analyze only, don't export to Notion.

## Tips

1. **Start with context**: Always check related issues first
2. **Think in layers**: Why → What → Impact → Design
3. **Use your notes**: Fill the "Memo" field in Notion
4. **Compare commits**: Use before/after commits for better understanding
5. **Focus on intent**: Understand why, not just what changed
