---
name: next
description: Analyze the next unread commit and save to output directory.
disable-model-invocation: true
---

# Deep Code Reader - Next

Analyze the next unread commit, generate explanation, and save to output directory.

## Arguments

No arguments. Uses state to determine the next commit.

If no project configured:
```
No project configured. Run /deep-code-reader first to set up a project.
```

## Flow

1. **Load state**: Read `~/.claude/deep-code-reader/current.json` → `projects/{name}.json`
2. **Identify next commit**: Get commit at `current_index + 1` via `git log --reverse --format="%H %s"`
3. **Get commit info**: `git show {hash} --stat` and `git diff {hash}~1 {hash}`
4. **Get PR info**: Search for related PR via GitHub MCP, fetch discussion and review comments
5. **Generate analysis**: Follow `templates/analysis.md` in the `knowledge` skill directory
6. **Save to output**: Write to `{output_path}/commits/{index}-{short_hash}.md`
7. **Update state**: Increment `current_index`, append to `analyzed_commits`, update `last_analyzed_at`
8. **Display**: Show the generated analysis to the user

## After displaying analysis

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Saved to: {output_path}/commits/0157-def5678.md

/deep-code-reader:next   - Next commit
/deep-code-reader:list   - Commit list
/deep-code-reader:status - Progress
```

Do NOT auto-proceed. Wait for explicit command.

## All commits completed

```
🎉 Congratulations!

You've read all 5,432 commits of expressjs/express.

Run /deep-code-reader to start a new project.
```

## Error handling

### PR info unavailable
```
⚠️ Could not fetch PR info (possible API rate limit).
Generating analysis from commit info only.
```
Continue analysis, skip PR discussion section.
