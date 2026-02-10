# Deep Code Reader

**Learn OSS codebases commit by commit with AI-powered explanations**

A conversational Claude Code skill for systematic deep code reading. Analyze commits chronologically, understand the evolution of open source projects, and build your knowledge base in Obsidian.

## Quick Start

```
/deep-code-reader

📚 Deep Code Reader
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

何を読みますか？

> expressを読みたい

✅ expressjs/express を設定しました
📊 総コミット数: 5,432

最初のコミットから読み始めますか？

> はい

[詳細な解説が表示される]

> なぜこのパターンを使ってるの？

[質問に回答、Q&Aに保存]

> 次

[次のコミット解説...]
```

## Features

- **会話型インターフェース** - コマンドを覚える必要なし
- **詳細な解説** - Mermaid図、設計パターン、Before/After比較
- **PR情報統合** - ディスカッション、レビューコメントも翻訳・解説
- **Q&A蓄積** - 質問と回答を自動保存
- **Obsidian連携** - ナレッジベースとして蓄積・検索

## How It Works

```
┌─────────────────┐     ┌─────────────────┐
│   Claude Code   │────▶│    Obsidian     │
│  (操作・解説)    │     │  (閲覧・メモ)    │
└─────────────────┘     └─────────────────┘
```

**Claude Code**: スキルを起動して会話
**Obsidian**: 生成されたMarkdownを閲覧・検索・メモ追記

## What You Say

| やりたいこと | 言い方の例 |
|------------|-----------|
| 始める | 「expressを読みたい」「reactを分析」 |
| 次へ進む | 「次」「続き」 |
| 質問する | 「なぜこうなってる？」「このパターンは？」 |
| 一覧を見る | 「コミット一覧」「リスト」 |
| 進捗確認 | 「進捗」「どこまで読んだ？」 |
| 特定のを読む | 「abc1234を解説して」「PR #298を読む」 |

## Output Structure

```
~/obsidian-vault/deep-code-reading/
└── expressjs-express/
    ├── _index.md              # プロジェクト概要
    └── commits/
        ├── 0001-abc1234.md
        ├── 0002-def5678.md
        └── ...
```

### Each Analysis Contains

- 📋 **基本情報** - PR番号、作成者、変更規模
- 🎯 **変更の要約** - 核心コンセプト、Before/After
- 🏗️ **アーキテクチャ** - Mermaid図で可視化
- 💻 **コード解説** - 設計ポイント付き
- 💬 **PRやり取り** - 英語原文 + 日本語訳 + 背景解説
- 🎓 **設計パターン** - 使われているパターンと原則
- 🔄 **Before/After** - 改善点の比較
- 📚 **学習ポイント** - このPRから学べること

## Requirements

- Claude Code CLI
- Git
- GitHub MCP server (for PR information)
- Obsidian (recommended) or any markdown editor

## Installation

### Via Plugin Marketplace (Recommended)

1. Open **Manage Plugins** (Claude Code settings)
2. Go to the **Marketplaces** tab
3. Enter `Kuroakira/deep-code-reader` and click **Add**
4. Switch to the **Plugins** tab and install `deep-code-reader`

To update or uninstall, use the same **Plugins** tab.

### Manual Installation (Alternative)

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
- Vault: `~/obsidian-vault/deep-code-reading/`

## License

MIT
