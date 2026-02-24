---
name: read
description: Analyze a specific commit or PR by hash or number.
disable-model-invocation: true
argument-hint: "[commit-hash or #PR-number]"
---

# Deep Code Reader - Read

Analyze a specific commit or PR.

## Arguments

- If `$ARGUMENTS` provided: use as commit hash or PR number
- If no argument and no context: ask user

```
Which commit or PR would you like to read?
(e.g. "abc1234" or "#298")
```

## Flow

### By commit hash

1. **Load state**: Read `~/.claude/deep-code-reader/current.json` → `projects/{name}.json`
2. **Validate commit**: `git show {hash} --quiet`
3. **Get commit info**: `git show {hash} --stat` and `git diff {hash}~1 {hash}`
4. **Get PR info**: Search related PR via GitHub MCP
5. **Generate analysis**: Follow `templates/analysis.md` in the `knowledge` skill directory
6. **Save to output**: Write `{output_path}/commits/{index}-{short_hash}.md`
7. **Update state**: Add to `analyzed_commits`, update `current_index` if sequential
8. **Display**: Show analysis

### By PR number

1. Fetch PR via `mcp__github__get_pull_request`
2. Identify merge commit
3. Continue with commit hash flow above

## After displaying analysis

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Saved to: {output_path}/commits/0157-def5678.md

/deep-code-reader:next   - Next commit
/deep-code-reader:list   - Commit list
/deep-code-reader:status - Progress
```
