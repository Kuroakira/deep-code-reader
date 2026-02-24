---
name: list
description: Show commit list with analyzed/unanalyzed status around current reading position. Use when user wants to see what commits are available or browse commit history.
argument-hint: "[index or range]"
---

# Deep Code Reader - List

Show commit list around current reading position.

## Arguments

- If `$ARGUMENTS` provided: use as index or range (e.g. `200`, `200-220`)
- If no argument: show around `current_index`
- If no project configured: ask user to run `/deep-code-reader` first

## Flow

1. **Load state**: Read `~/.claude/deep-code-reader/current.json` → `projects/{name}.json`
2. **Get commits**: `git log --reverse --format="%h %s" --skip={offset} -n 20`
3. **Display**: Show with analyzed markers

## Output format

```
📋 Commits (156-175 / 5,432)

  156 ✅ abc1234 - Add query parsing
  157    def5678 - Implement middleware  ← next
  158    ghi9012 - Fix routing bug
  159    jkl3456 - Add body parser
  160    mno7890 - Refactor utils
  ...

/deep-code-reader:read {hash}  - Read specific commit
/deep-code-reader:next         - Analyze next
```
