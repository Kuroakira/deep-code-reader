# OSS学習プラットフォーム

**Claude CodeとMCPサーバーを活用した、OSSコードベースの自動分析と賢い洞察、Notion統合**

こんな開発者に最適：
- 🚀 コミットとPRを深く理解したい
- 📚 Notionで知識ベースを構築したい
- 🎯 「何が」変わったかだけでなく「なぜ」変わったかを学びたい
- 🤝 コンテキストを理解してコントリビューションに備えたい

## ✨ 機能

### 🔍 コミットレベルの詳細分析
- **Why（変更の意図）** - 変更の背景と動機を理解
- **What（変更内容）** - 何が変更されたのかを正確に把握
- **Impact（影響範囲）** - どのモジュールが影響を受けるかを知る
- **Design（設計意図）** - 設計判断とトレードオフを学ぶ
- **Context（コンテキスト）** - 関連するissue、PR、周辺コミットの把握

### 🤖 インテリジェントな自動化
- **ワンコマンドインストール** - `./install.sh`で全てセットアップ
- **プロジェクトコンテキストメモリ** - 一度登録すれば、URLの再入力なしで多くのコミットを分析
- **戦略的分析** - Sequential ThinkingによるAI駆動の分析計画
- **シンボルレベルの理解** - Serena MCPによる意味的なコード理解
- **フレームワーク専門知識** - Context7 MCPによる公式ドキュメントパターン

### 📝 Notion統合
- **自動エクスポート** - 分析結果をNotionワークスペースに自動保存
- **構造化ドキュメント** - 一貫性があり検索可能な分析ページ
- **チームコラボレーション** - チームで洞察を共有
- **ナレッジベース** - 分析したプロジェクトのライブラリを構築

## 🚀 クイックスタート

### インストール（2分）

```bash
# リポジトリをクローン
git clone https://github.com/Kuroakira/deep-code-reader.git
cd deep-code-reader

# インストーラーを実行
./install.sh
```

インストーラーが実行すること：
1. ✅ 依存関係のチェック（Node.js、Python、npm）
2. 📦 MCPサーバーのインストール（既存のインストールを自動検出）
   - 必須：GitHub、Notion
   - オプション：追加のMCPサーバー（対話的に選択）
3. ⚙️  Claude Codeの設定
4. 🎯 スキルとコマンドのインストール
5. 🔐 Notion統合のセットアップ
   - インストール中にNotion APIキーを入力
   - MCP設定が自動更新
   - インストール後にデータベース作成ウィザードが利用可能

### アンインストール

全てのインストールコンポーネントを安全に削除するには：

```bash
./uninstall.sh
```

アンインストーラーが実行すること：
- 🔍 インストール済みコンポーネントをスキャン
- 📋 削除されるものを表示
- ⚠️  確認を求める
- 🎯 削除するMCPサーバーを選択可能
- 🔄 設定バックアップの復元オプション
- 💾 Notion設定の保持（オプション）
- 🗑️  全てのファイルをクリーンアップ

### Notionセットアップ（インストール中）

**`./install.sh`実行中：**

「Setup Notion integration now? (y/n)」と表示されたら：
1. **yesと回答**（Notion統合が必要な場合）
2. **APIキーを取得** - https://www.notion.so/profile/integrations にアクセス
   - "Deep Code Reader"という名前のインテグレーションを作成
   - Internal Integration Secretをコピー
3. **APIキーを貼り付け** - インストーラーが自動的にMCPを設定
4. **アクセス権限を付与** - インテグレーション設定に移動：
   - https://www.notion.so/profile/integrations にアクセス
   - インテグレーションをクリック
   - 「アクセス」タブをクリック
   - 「アクセス権限を編集」をクリック
   - ワークスペースページを選択
5. **完了！** - Notion MCPが使用可能に

**インストール後：**

```bash
# Claude Codeを起動
claude-code

# Notionセットアップを完了
/setup-notion
```

ウィザードが実行すること：
1. **ワークスペースページURLを尋ねる** - アクセスを付与したページを入力
2. **OSSリストデータベースを自動作成** - 全リポジトリのマスターデータベース
3. **完了！** - OSSリポジトリの登録準備完了

**注意**: 個別の「Commits & PRs」データベースは、`/register-oss`で各OSSを登録する際に自動的に作成されます。

**インストール中にスキップした場合：**
```bash
# NotionからAPIキーを取得
# 更新スクリプトを実行
python3 ~/.claude/deep-code-reader/scripts/update_notion_mcp.py <api_key>

# Claude Codeを再起動
# 次に /setup-notion を実行
```

### 初回分析（30秒）

```bash
# ステップ1: OSSリポジトリを登録（一度だけ）
/register-oss https://github.com/expressjs/express

# ステップ2: コミットを分析 - URLは不要！
/analyze-commit abc1234567          # コミットハッシュだけ
/analyze-commit def5678             # URLは不要！
/analyze-pr 5234                    # PR番号だけ

# 現在のプロジェクトを確認
/current-oss
```

**それだけです！** Claudeが実行すること：
- 💾 プロジェクトコンテキストを記憶（URLの繰り返し入力不要！）
- 🔄 コミット情報を取得
- 🎯 変更が行われた理由を理解
- 🏗️ アーキテクチャへの影響を分析
- 📊 コンソールに詳細な分析を表示
- 📤 全てを自動的にNotionにエクスポート

## 📁 プロジェクト構造

```
deep-code-reader/
├── install.sh                    # ワンコマンドインストーラー
├── uninstall.sh                  # クリーンアンインストーラー
├── commands/                     # スラッシュコマンド
│   ├── register-oss.md          # OSSリポジトリ登録
│   ├── current-oss.md           # 現在のプロジェクト表示
│   ├── analyze-commit.md        # 単一コミット分析
│   ├── analyze-pr.md            # プルリクエスト分析
│   └── setup-notion.md          # Notion設定
├── config/                       # 設定ファイル
│   ├── mcp_servers.json         # MCPサーバー設定
│   └── notion_template.json     # Notionページテンプレート
├── scripts/                      # ユーティリティスクリプト
│   ├── update_notion_mcp.py     # Notion設定更新
│   └── utils/                   # ヘルパーユーティリティ
├── skills/                       # Claudeスキル
│   └── deep-code-reader/        # コード分析スキル
└── docs/                         # ドキュメント
```

## 📦 インストールされるファイル

`./install.sh`実行後、ホームディレクトリに以下のファイルが作成されます：

```
~/.claude/
├── deep-code-reader/            # プロジェクト固有ファイル
│   ├── notion_config.json       # Notion統合設定
│   │                            # - APIキー
│   │                            # - ワークスペースページID
│   │                            # - データベースID
│   │                            # - 自動エクスポート設定
│   └── scripts/                 # ユーティリティスクリプト
│       ├── update_notion_mcp.py # Notion設定更新
│       └── utils/               # ヘルパーモジュール
│
├── commands/                    # スラッシュコマンド（リポジトリからコピー）
│   ├── register-oss.md
│   ├── current-oss.md
│   ├── analyze-commit.md
│   ├── analyze-pr.md
│   ├── list-commits.md
│   ├── list-prs.md
│   ├── setup-notion.md
│   └── export-analysis.md
│
└── skills/                      # Claudeスキル（リポジトリからコピー）
    └── deep-code-reader/        # 分析スキル

~/.claude.json                   # Claude Code CLI設定
                                 # - MCPサーバー設定（GitHub、Notion）
                                 # - Notion APIトークン
```

**重要な注意点：**
- `~/.claude/deep-code-reader/` - **このプロジェクトのみが変更**
  - バックアップ/復元が安全
  - 全てのプロジェクト固有設定を含む
  - `/setup-notion`とユーティリティスクリプトで更新

- `~/.claude.json` - **全てのClaude Codeプロジェクトで共有**
  - インストール中に変更（Notion MCPサーバーを追加）
  - 変更前に自動バックアップ
  - アンインストール時に復元（オプション）

- `~/.claude/commands/`と`~/.claude/skills/` - **共有リソース**
  - 他のプロジェクトのコマンド/スキルが含まれる可能性
  - アンインストーラーはこのプロジェクトのファイルのみ削除

**バックアップの推奨：**
```bash
# インストール前
cp ~/.claude.json ~/.claude.json.backup

# またはアンインストール時の組み込みバックアップを使用
./uninstall.sh  # バックアップの復元を提供
```

## 🎯 使用例

### OSSリポジトリの登録

```bash
# プロジェクトごとに一度登録
/register-oss https://github.com/expressjs/express

# OSSリストデータベースにエントリを作成
# メモリに現在のプロジェクトとして保存
```

### 現在のプロジェクトを確認

```bash
# 現在アクティブなプロジェクトを表示
/current-oss

# 表示内容：リポジトリ情報、Notionページ、利用可能なコマンド
```

### コミットの分析

```bash
# 登録後 - URLは不要！
/analyze-commit abc1234
/analyze-commit def5678

# または明示的にURL指定（オプション）
/analyze-commit https://github.com/expressjs/express abc1234

# コンソールに詳細な分析を表示 + Notionにエクスポート
```

### プルリクエストの分析

```bash
# PR番号だけ！
/analyze-pr 5234

# または完全なURL（オプション）
/analyze-pr https://github.com/expressjs/express/pull/5234

# 質問：全てのコミットを分析するか、特定のものを選択するか
```

### プロジェクト間の切り替え

```bash
# 別のプロジェクトに切り替え
/register-oss https://github.com/facebook/react
/analyze-commit xyz9012          # 現在はreactリポジトリを使用

# 元に戻す
/register-oss https://github.com/expressjs/express
/analyze-commit abc1234          # expressに戻る
```

### Notionセットアップ

```bash
# Notion統合を設定（初回のみ）
/setup-notion

# または手動で編集：~/.claude/deep-code-reader/notion_config.json
```

## 💡 得られるもの

コミット分析後、以下が得られます：

### 📊 Claude Code上

```markdown
📊 Commit Analysis: abc1234

## 🎯 変更の意図（Why）
認証ミドルウェアのセキュリティ脆弱性を修正（CVE-2024-1234）

関連Issue：#1234、#1235

## 📝 変更内容（What）
変更されたファイル（3件）：
- src/auth/middleware.js (+45, -12)
- src/auth/validator.js (+23, -5)
- test/auth.test.js (+67, -0)

## 🏗️ 影響範囲（Impact）
影響を受けるモジュール：
- api/routes/* (10ファイル)
- middleware/session.js
✅ 破壊的変更なし

## 🎨 設計意図（Design）
パターン：Chain of Responsibility
トレードオフ：メモリ+2MBでセキュリティ10倍向上

## 🔗 コンテキスト
前：abc0123 - 認証モジュールのリファクタ
後：abc1235 - ドキュメント更新
PR：#5234（5件の承認レビュー）

💾 Notionにエクスポート済み：https://notion.so/commit-page
```

### 📝 Notion上

構造化された分析ページ：
- 🎯 変更の意図 - なぜこの変更が行われたか
- 📝 変更内容 - 何が変更されたか（コード差分付き）
- 🏗️ 影響範囲 - コードベースへの影響
- 🎨 設計意図 - 設計判断とトレードオフ
- 🔗 コンテキスト - 関連するissue、コミット、PR
- 📋 完全な差分（トグル内）
- 📝 メモフィールド（あなたのメモ用）

## 🛠️ 使用するMCPサーバー

このプラットフォームは強力なMCPサーバーを活用：

### ビルトイン（Claude Code）
- **Serena** - 意味的なコード理解とプロジェクトメモリ
- **Context7** - 公式フレームワークドキュメント
- **Sequential Thinking** - 戦略的分析計画

### 外部（自動インストール）
- **GitHub MCP** - リポジトリメタデータとアクセス
- **Notion MCP** - Notionへの自動エクスポート

## 📚 ドキュメント

- **[QUICKSTART_ja.md](QUICKSTART_ja.md)** - 5分で始める
- **[REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md)** - プロジェクト構成
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - コントリビューションガイドライン
- **[docs/MCP_SETUP.md](docs/MCP_SETUP.md)** - MCPサーバー設定
- **[docs/NOTION_INTEGRATION.md](docs/NOTION_INTEGRATION.md)** - Notionセットアップガイド

## 🧪 サポート言語とフレームワーク

### 現在のサポート
- **Python** - 完全サポート（Django、Flask、FastAPI）
- **JavaScript/TypeScript** - 完全サポート（React、Vue、Express、Next.js）

### 計画中のサポート
- **Go** - 近日公開
- **Rust** - 近日公開
- **Java** - 近日公開
- **Ruby** - 近日公開

## 🔧 要件

- **Node.js** v18+（MCPサーバー用）
- **Claude Code**（CLIまたはデスクトップ）
- **Notionアカウント**（オプション、エクスポート用）
- **GitHubアカウント**（プライベートリポジトリ分析用）

## 🎓 ユースケース

### オープンソースコントリビューター向け
```
1. コントリビュートする新しいプロジェクトを発見
2. 最初のPR前にコードベースを理解
3. 「good first issues」を特定
4. アーキテクチャパターンを学習
```

### 開発チーム向け
```
1. 新しいチームメンバーのオンボーディングを加速
2. レガシーコードベースをドキュメント化
3. リファクタリング計画を立案
4. アーキテクチャ知識を共有
```

### テクニカルリード向け
```
1. 潜在的な依存関係を評価
2. コード品質とアーキテクチャを査定
3. 情報に基づいた技術判断
4. 技術ドキュメントを構築
```

### 学習者向け
```
1. 実世界のコードアーキテクチャを研究
2. 確立されたプロジェクトから学習
3. 個人的なナレッジベースを構築
4. ベストプラクティスを理解
```

## 🤝 コントリビューション

コントリビューションを歓迎します！[CONTRIBUTING.md](CONTRIBUTING.md)を参照：
- 開発環境のセットアップ
- コードスタイルガイドライン
- テスト要件
- プルリクエストプロセス

コントリビューションのアイデア：
- 追加言語のサポート
- 新しい分析機能
- 代替エクスポート形式
- パフォーマンス最適化

## 📄 ライセンス

MITライセンス - 詳細は[LICENSE](LICENSE)を参照

## 🙏 謝辞

構築に使用：
- [Claude Code](https://claude.com/claude-code) by Anthropic
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Notion API](https://developers.notion.com/)
- [GitHub API](https://docs.github.com/en/rest)

オープンソースプロジェクトを理解し、コントリビュートするためのより良いツールの必要性に触発されました。

## 🔗 リンク

- **GitHubリポジトリ**：https://github.com/Kuroakira/deep-code-reader
- **Issue & フィードバック**：https://github.com/Kuroakira/deep-code-reader/issues
- **ディスカッション**：https://github.com/Kuroakira/deep-code-reader/discussions
- **Anthropic Skills**：https://docs.anthropic.com/en/docs/build-with-claude/skills
- **MCPドキュメント**：https://modelcontextprotocol.io/

---

**OSSコミュニティのために ❤️ を込めて構築**

*一度に一つの分析で、オープンソースをより身近に。*
