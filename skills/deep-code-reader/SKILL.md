---
name: deep-code-reader
description: OSSコードベースをコミットごとに学ぶ。「expressを読みたい」「次」「進捗」などの自然な会話で操作。
---

# Deep Code Reader

OSSコードベースをコミットごとに学ぶための会話型スキル。

## 起動トリガー

- `/deep-code-reader` または `/dcr`
- 「OSSを読みたい」「コードリーディングしたい」
- 「expressを読みたい」「reactを分析」など具体的なリポジトリ名

## 起動時の振る舞い

### 初回起動（プロジェクト未設定）

```
📚 Deep Code Reader
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OSSコードベースをコミットごとに深く理解しましょう。

始め方:
  「expressを読みたい」
  「facebook/reactを読む」
  「https://github.com/excalidraw/excalidraw を分析」

何を読みますか？
```

### プロジェクト設定済みの場合

```
📚 Deep Code Reader
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

現在: expressjs/express
進捗: ████████░░░░░░░░ 156 / 5,432 (2.9%)

前回: abc1234 - Add query parsing (2014-03-16)
次: def5678 - Implement middleware (2014-03-17)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

続きを読む → 「次」「続き」
別のを読む → 「reactを読みたい」
特定commit → 「abc1234を解説して」
一覧を見る → 「コミット一覧」
```

## 会話フロー

### プロジェクト初期化

ユーザー入力の例:
- 「expressを読みたい」
- 「excalidraw/excalidrawを読む」
- 「https://github.com/expressjs/express」

処理:
1. リポジトリを特定（owner/repo形式に正規化）
2. ローカルにクローン: `~/.claude/deep-code-reader/repos/{owner}/{repo}`
3. Obsidian vault構造を作成
4. 状態ファイルを初期化
5. 最初のcommit解説へ自動進行（または確認）

応答例:
```
✅ expressjs/express を設定しました

📁 保存先: ~/obsidian-vault/deep-code-reading/expressjs-express/
📊 総コミット数: 5,432

最初のコミットから読み始めますか？
```

### 次のコミットを読む

ユーザー入力の例:
- 「次」「続き」「next」
- 「次のコミットを読む」
- 「進む」

処理:
1. 次の未解析commitを特定
2. commit情報を取得（git show）
3. 関連PR情報を取得（GitHub MCP）
4. 詳細解説を生成
5. Obsidian vaultに保存
6. 解説を表示

### 特定のコミットを読む

ユーザー入力の例:
- 「abc1234を解説して」
- 「このコミットを読みたい: def5678」
- 「PR #298を解説」

処理:
1. commit hashまたはPR番号を抽出
2. 該当commitを解析
3. 詳細解説を生成・保存

### 質問への対応

解説表示後、ユーザーは自由に質問できる:
- 「なぜこのパターンを使ってる？」
- 「changePropertyって何してるの？」
- 「このアーキテクチャのメリットは？」

処理:
1. 現在のcommit/PRコンテキストを保持
2. 質問に詳細回答
3. 回答をMarkdownファイルのQ&Aセクションに追記

応答後:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💾 Q&Aを保存しました

他に質問があれば聞いてください。
次に進むなら「次」と言ってください。
```

### コミット一覧を見る

ユーザー入力の例:
- 「一覧」「リスト」「list」
- 「コミット一覧を見せて」
- 「次の10件」

処理:
1. current_index周辺のcommitを表示
2. 番号またはhashで選択可能に

応答例:
```
📋 コミット一覧 (156-165 / 5,432)

  156 ✅ abc1234 - Add query parsing
  157    def5678 - Implement middleware  ← 次
  158    ghi9012 - Fix routing bug
  159    jkl3456 - Add body parser
  160    mno7890 - Refactor utils
  ...

「def5678を読む」または番号で選択できます。
```

### 進捗確認

ユーザー入力の例:
- 「進捗」「status」
- 「どこまで読んだ？」

応答:
```
📊 進捗状況

expressjs/express
████████░░░░░░░░ 156 / 5,432 (2.9%)

最近読んだコミット:
  156. abc1234 - Add query parsing (2024-02-10)
  155. xyz9876 - Initial routing (2024-02-09)
  154. ...

Obsidian: ~/obsidian-vault/deep-code-reading/expressjs-express/
```

### プロジェクト切り替え

ユーザー入力の例:
- 「reactに切り替え」
- 「別のプロジェクトを読みたい」

処理:
1. 登録済みプロジェクトを表示
2. 選択または新規登録

## 解説テンプレート

詳細は `templates/analysis.md` を参照。

主要セクション:
- 📋 基本情報
- 🎯 変更の要約
- 🏗️ アーキテクチャ設計（Mermaid図）
- 💻 主要コード解説
- 💬 PRでのやり取り（翻訳+背景解説）
- 🎓 設計パターン・クリーンコード解説
- 🔄 Before/After比較
- 📚 学習ポイント

## 状態管理

### ディレクトリ構造

```
~/.claude/deep-code-reader/
├── current.json              # 現在のプロジェクト
├── projects/
│   ├── expressjs-express.json
│   └── facebook-react.json
└── repos/
    ├── expressjs/express/    # git clone
    └── facebook/react/
```

### プロジェクト状態 (projects/{name}.json)

```json
{
  "owner": "expressjs",
  "repo": "express",
  "github_url": "https://github.com/expressjs/express",
  "local_path": "~/.claude/deep-code-reader/repos/expressjs/express",
  "vault_path": "~/obsidian-vault/deep-code-reading/expressjs-express",
  "total_commits": 5432,
  "current_index": 156,
  "analyzed_commits": ["abc1234", "def5678", ...],
  "initialized_at": "2025-02-10T12:00:00Z",
  "last_analyzed_at": "2025-02-10T15:30:00Z"
}
```

## Obsidian出力構造

```
~/obsidian-vault/deep-code-reading/
└── expressjs-express/
    ├── _index.md              # プロジェクト概要
    └── commits/
        ├── 0001-abc1234.md    # 各コミット解説
        ├── 0002-def5678.md
        └── ...
```

## 必要なツール

- Read: 状態ファイル読み込み
- Write: Markdown・JSON書き込み
- Bash: git clone, git show, git log
- GitHub MCP:
  - `mcp__github__search_issues` (commit→PR検索)
  - `mcp__github__get_pull_request`
  - `mcp__github__get_pull_request_comments`
  - `mcp__github__get_pull_request_reviews`

## エラー時の振る舞い

### リポジトリが見つからない
```
❌ expressjs/expres が見つかりませんでした。

もしかして:
  - expressjs/express
  - express/express

正しいリポジトリ名を教えてください。
```

### PR情報取得失敗
```
⚠️ PR情報を取得できませんでした（API制限の可能性）。
コミット情報のみで解説を生成します。

(解説を続行)
```

### 全コミット完了
```
🎉 おめでとうございます！

expressjs/express の全 5,432 コミットを読破しました。

次のプロジェクトを読みますか？
```
