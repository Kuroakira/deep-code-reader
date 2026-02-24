---
name: status
description: Show reading progress for current and all registered deep-code-reader projects. Use when user asks about progress or wants an overview.
---

# Deep Code Reader - Status

Show reading progress for current and all registered projects.

## Arguments

No arguments. If no project configured:
```
No projects registered. Run /deep-code-reader to set up a project.
```

## Flow

1. **Load state**: Read `~/.claude/deep-code-reader/current.json` → `projects/{name}.json`
2. **Calculate progress**: `current_index / total_commits`
3. **Recent history**: Get details of last few `analyzed_commits` via git log
4. **Display**

## Output format

```
📊 Progress

expressjs/express
████████░░░░░░░░ 156 / 5,432 (2.9%)

Recently read:
  156. abc1234 - Add query parsing (2024-02-10)
  155. xyz9876 - Initial routing (2024-02-09)
  154. rst5432 - Setup project (2024-02-08)

Output: ~/obsidian-vault/deep-code-reading/expressjs-express/

/deep-code-reader:next   - Continue reading
/deep-code-reader:list   - Commit list
```

## Multiple projects

```
📊 All Projects

  expressjs/express    ████████░░░░░░░░ 156 / 5,432 (2.9%)  ← active
  facebook/react       ██░░░░░░░░░░░░░░  45 / 18,234 (0.2%)

Switch project → /deep-code-reader
```
