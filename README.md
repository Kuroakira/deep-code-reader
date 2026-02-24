# Deep Code Reader

**Learn OSS codebases commit by commit — build a knowledge base with AI-powered explanations**

A Claude Code skill for systematic deep code reading. Analyze commits chronologically, understand how open source projects evolved, and automatically generate rich Markdown documentation.

## Why?

Deep Code Reader doesn't just explain code — it **builds a searchable knowledge base**. Every commit analysis is saved as a Markdown file with Mermaid diagrams, design pattern breakdowns, and your own Q&A. Over time, you accumulate a structured library of architectural knowledge that you can browse, search, and annotate.

```mermaid
graph LR
    CC["Claude Code<br/>(analyze & explain)"]
    OD["Output Directory<br/>(browse, search, & note)"]
    CC -->|"generates Markdown"| OD

    subgraph "Output Structure"
        IDX["_index.md<br/>Project overview"]
        C1["0001-abc1234.md"]
        C2["0002-def5678.md"]
        C3["..."]
    end

    OD --- IDX
    OD --- C1
    OD --- C2
    OD --- C3
```

## Quick Start

```
/deep-code-reader

📚 Deep Code Reader
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to read?

> I want to read express

✅ Set up expressjs/express
📊 Total commits: 5,432

Start from the first commit?

> Yes

[Detailed analysis is displayed and saved]

> Why is this pattern used here?

[Answers your question, saves Q&A to the Markdown file]

> Next

[Next commit analysis...]
```

## Features

- **Conversational interface** — No commands to memorize; just talk naturally
- **Rich analysis output** — Mermaid diagrams, design patterns, Before/After comparisons
- **PR context included** — Discussion threads and review comments, translated and explained
- **Q&A accumulation** — Your questions and answers are auto-saved to each commit's file
- **Flexible output** — Defaults to Obsidian vault, configurable to any directory
- **Session hooks** — Auto-detects active projects on session start

## Commands

All operations require explicit command invocation:

| Command | Purpose |
|---------|---------|
| `/deep-code-reader` | Initialize or resume a project |
| `/deep-code-reader:next` | Analyze the next commit |
| `/deep-code-reader:read abc1234` | Analyze a specific commit by hash |
| `/deep-code-reader:read #298` | Analyze a specific PR by number |
| `/deep-code-reader:list` | Show commit list |
| `/deep-code-reader:status` | Show reading progress |

## What Each Analysis Contains

Every commit generates a Markdown file with:

- **Basic info** — PR number, author, change size
- **Change summary** — Core concept, Before/After
- **Architecture** — Visualized with Mermaid diagrams
- **Code walkthrough** — With design rationale
- **PR discussions** — Original English + Japanese translation + context
- **Design patterns** — Patterns and principles applied
- **Before/After** — Comparison of improvements
- **Learning points** — Key takeaways from this commit

## Output Structure

```
{output_path}/
├── _index.md              # Project overview
└── commits/
    ├── 0001-abc1234.md    # Each commit analysis
    ├── 0002-def5678.md
    └── ...
```

Default output path: `~/obsidian-vault/deep-code-reading/{owner}-{repo}/`

Custom output path:
```
/deep-code-reader expressjs/express --output ~/my-notes/express/
```

## Requirements

- Claude Code CLI
- Git
- GitHub MCP server (for PR information)
- Obsidian (recommended) or any Markdown editor

## Installation

### Via Plugin Marketplace (Recommended)

1. Open **Manage Plugins** (Claude Code settings)
2. Go to the **Marketplaces** tab
3. Enter `Kuroakira/deep-code-reader` and click **Add**
4. Switch to the **Plugins** tab and install `deep-code-reader`

To update or uninstall, use the same **Plugins** tab.

### Manual Installation

```bash
git clone https://github.com/Kuroakira/deep-code-reader.git
cd deep-code-reader
mkdir -p ~/.claude/skills
ln -s $(pwd) ~/.claude/skills/deep-code-reader

# To uninstall:
rm ~/.claude/skills/deep-code-reader
```

## Configuration

Default paths:
- Repos: `~/.claude/deep-code-reader/repos/`
- Projects: `~/.claude/deep-code-reader/projects/`
- Output: `~/obsidian-vault/deep-code-reading/` (configurable)

## License

MIT
