---
name: knowledge
description: Shared context for Deep Code Reader — state management, output configuration, analysis methodology. Auto-loaded when any /deep-code-reader command runs.
user-invocable: false
---

# Deep Code Reader — Shared Knowledge

Background knowledge for all `/deep-code-reader:*` skills. Not directly invocable — Claude loads this automatically when needed.

## State management

### Directory structure

```
~/.claude/deep-code-reader/
├── current.json              # Active project pointer
├── projects/
│   ├── expressjs-express.json
│   └── facebook-react.json
└── repos/
    ├── expressjs/express/    # git clone
    └── facebook/react/
```

### current.json

```json
{
  "active_project": "expressjs-express"
}
```

### Project state (projects/{name}.json)

```json
{
  "owner": "expressjs",
  "repo": "express",
  "github_url": "https://github.com/expressjs/express",
  "local_path": "~/.claude/deep-code-reader/repos/expressjs/express",
  "output_path": "~/obsidian-vault/deep-code-reading/expressjs-express",
  "total_commits": 5432,
  "current_index": 156,
  "analyzed_commits": ["abc1234", "def5678"],
  "initialized_at": "2025-02-10T12:00:00Z",
  "last_analyzed_at": "2025-02-10T15:30:00Z"
}
```

## Output configuration

### Default output path

```
~/obsidian-vault/deep-code-reading/{owner}-{repo}/
```

Users can specify a custom output path during initialization. The `output_path` field in the project state stores the configured path.

### Output directory structure

```
{output_path}/
├── _index.md              # Project overview
└── commits/
    ├── 0001-abc1234.md    # Each commit analysis
    ├── 0002-def5678.md
    └── ...
```

## Analysis methodology

### Template

Use `templates/analysis.md` in the `knowledge` skill directory.

### Full analysis (default)

Apply when any of:
- +100 lines changed
- New pattern or architecture introduced
- Active PR discussion
- Multi-file structural changes

Use all sections from the template.

### Brief analysis

Apply when all of:
- Small bug fix, docs-only, dependency update, or formatting/lint fix
- Minimal discussion

Use only: basic info + summary (1-2 sentences) + file list.

## Required tools

### For commit analysis (next, read)
- Read: state files, template
- Write: Markdown (output), JSON (state)
- Bash: git show, git diff, git log
- GitHub MCP:
  - `mcp__github__search_issues` (commit → PR lookup)
  - `mcp__github__get_pull_request`
  - `mcp__github__get_pull_request_comments`
  - `mcp__github__get_pull_request_reviews`

### For browsing (list, status)
- Read: state files
- Bash: git log
- Glob: list project JSON files

### For initialization
- Read: state files
- Write: JSON, Markdown
- Bash: git clone, git log
- GitHub MCP: `mcp__github__search_repositories`

## Error handling

### Repository not found
Suggest similar names. Ask user for correction.

### PR info unavailable
Continue analysis from commit info only. Skip PR discussion section.

### No project configured
Guide user to run `/deep-code-reader` first.
