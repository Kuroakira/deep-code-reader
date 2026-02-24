---
name: deep-code-reader
description: Initialize or resume an OSS code reading project.
disable-model-invocation: true
argument-hint: "[owner/repo or URL]"
---

# Deep Code Reader

Entry point. Initialize a new project or show resume info for an existing one.

## Commands

| Command | Purpose |
|---------|---------|
| `/deep-code-reader` | Initialize or resume project (this command) |
| `/deep-code-reader:next` | Analyze next commit |
| `/deep-code-reader:read` | Analyze a specific commit/PR |
| `/deep-code-reader:list` | Show commit list |
| `/deep-code-reader:status` | Show progress |

## Behavior

### 1. Parse arguments

- If `$ARGUMENTS` provided: use as target repository
- If no argument: read state to check for existing project

### 2. Read state

Read `~/.claude/deep-code-reader/current.json`.

### 3a. Argument provided → Initialize project

1. Resolve `$ARGUMENTS` to owner/repo format
2. Clone to `~/.claude/deep-code-reader/repos/{owner}/{repo}`
3. Create output directory structure (see below for path resolution)
4. Initialize state file (see knowledge skill for format)
5. Show setup summary — do NOT auto-proceed to first commit

#### Output path resolution

- Default: `~/obsidian-vault/deep-code-reading/{owner}-{repo}/`
- If `--output <path>` is provided in `$ARGUMENTS`, use that path instead
- Store resolved path as `output_path` in project state JSON

Response:
```
✅ Set up expressjs/express

📁 Output: ~/obsidian-vault/deep-code-reading/expressjs-express/
📊 Total commits: 5,432

Run /deep-code-reader:next to start reading.
```

### 3b. No argument + project configured → Resume

```
📚 Deep Code Reader
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current: expressjs/express
Progress: ████████░░░░░░░░ 156 / 5,432 (2.9%)

Last: abc1234 - Add query parsing (2014-03-16)
Next: def5678 - Implement middleware (2014-03-17)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/deep-code-reader:next     - Continue reading
/deep-code-reader:read     - Read specific commit/PR
/deep-code-reader:list     - Commit list
/deep-code-reader:status   - Full progress details
```

Do NOT auto-proceed. Wait for explicit command.

### 3c. No argument + no project → Ask user

```
📚 Deep Code Reader
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

No project configured.

Which repository would you like to read?
(e.g. "expressjs/express" or "https://github.com/facebook/react")
```

Wait for user response, then proceed with initialization.

## Project switching

Only when user provides a different repo name:
1. Show registered projects
2. Initialize if new, switch if existing

## Error handling

### Repository not found
```
❌ expressjs/expres was not found.

Did you mean:
  - expressjs/express
  - express/express

Please provide the correct repository name.
```
