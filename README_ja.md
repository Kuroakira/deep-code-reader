# OSS学習プラットフォーム

**Claude CodeとMCPサーバーを活用した、OSSコードベースの自動分析とNotion統合**

こんな開発者に最適：
- 🚀 コミットを体系的に追跡・理解したい
- 📚 Notionで知識ベースを構築したい
- 🎯 オープンソースプロジェクトを時系列で学びたい
- 🤝 コンテキストを理解してコントリビューションに備えたい

## ✨ 機能

### 🔍 バッチコミット追跡
- **範囲指定で追加** - 1-100、101-200などでコミットを追加
- **重複検出** - 既存エントリを自動スキップ
- **スキーマ自動検出** - Notionデータベース構造に適応
- **シンプルな情報** - コミットID、メッセージ、著者、日付、変更ファイル数

### 🤖 インテリジェントな自動化
- **ワンコマンドインストール** - `./install.sh`で全てセットアップ
- **プロジェクトコンテキストメモリ** - 一度登録すれば、URLの再入力なしでコミット追加
- **ローカルクローンサポート** - ローカルgitリポジトリで高速アクセス
- **シンボルレベルの理解** - Serena MCPによる意味的なコード理解

### 📝 Notion統合
- **自分のデータベース** - データベース構造は自分で作成・管理
- **バッチエクスポート** - 数百のコミットを効率的に追加
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
2. 📦 MCPサーバーのインストール（GitHub、Notion）
3. ⚙️  Claude Codeの設定
4. 🎯 スキルとコマンドのインストール

### Notionデータベースのセットアップ（手動）

**プラットフォームを使用する前に、Notionデータベースを作成：**

1. **Notionインテグレーションを作成**
   - https://www.notion.so/my-integrations にアクセス
   - "Deep Code Reader"という名前のインテグレーションを作成
   - Internal Integration Secretをコピー

2. **データベースを作成**（以下のプロパティで）：
   - `Title` (タイトル) - コミットタイトル
   - `Commit ID / PR No` (テキスト) - 完全なコミットハッシュ
   - `Type` (セレクト) - "Commit"オプション
   - `GitHub URL` (URL) - コミットへのリンク
   - `Comment` (テキスト) - コミットメッセージ
   - `Memo` (テキスト) - あなたのメモ

3. **データベースをインテグレーションと共有**
   - Notionでデータベースを開く
   - 「...」→「コネクト」→インテグレーションを追加

4. **URLからデータベースIDをコピー**：
   - URL: `https://notion.so/abc123def456?v=...`
   - データベースID: `abc123def456`

### 初回使用（1分）

```bash
# ステップ1：OSSリポジトリをデータベースと共に登録
/register-oss https://github.com/expressjs/express --database abc123def456

# ステップ2：コミットをバッチで追加
/add-commits 1 100      # 最初の100コミット（古い順）
/add-commits 101 200    # 次の100コミット
/add-commits 201 300    # 続き...

# 進捗確認
/current-oss
/list-commits
```

**それだけです！** Claudeが実行すること：
- 💾 リポジトリをローカルにクローン
- 🔄 コミット情報を取得
- 📊 Notionデータベースにコミットを追加
- ⏭️ 重複を自動スキップ

## 📁 プロジェクト構造

```
deep-code-reader/
├── install.sh                    # ワンコマンドインストーラー
├── uninstall.sh                  # クリーンアンインストーラー
├── commands/                     # スラッシュコマンド
│   ├── register-oss.md          # OSSリポジトリ登録
│   ├── add-commits.md           # バッチでコミット追加
│   ├── current-oss.md           # 現在のプロジェクト表示
│   └── list-commits.md          # コミット一覧
├── config/                       # 設定ファイル
│   └── mcp_servers.json         # MCPサーバー設定
├── scripts/                      # ユーティリティスクリプト
│   └── utils/                   # ヘルパーユーティリティ
└── skills/                       # Claudeスキル
    └── deep-code-reader/        # コード分析スキル
```

## 📦 インストールされるファイル

`./install.sh`実行後：

```
~/.claude/
├── deep-code-reader/            # プロジェクト固有ファイル
│   ├── repos/                   # クローンされたリポジトリ
│   │   └── {owner}/{repo}/      # ローカルgitクローン
│   └── current_oss.json         # 現在のプロジェクト設定
│
├── commands/                    # スラッシュコマンド
│   ├── register-oss.md
│   ├── add-commits.md
│   ├── current-oss.md
│   └── list-commits.md
│
└── skills/                      # Claudeスキル
    └── deep-code-reader/

~/.claude.json                   # Claude Code CLI設定
```

## 🎯 使用例

### OSSリポジトリの登録

```bash
# Notionデータベースと共に登録
/register-oss https://github.com/nestjs/nest --database abc123def456

# 出力：
# ✅ OSSリポジトリが登録されました
# プロジェクト：nest
# データベース：abc123def456
# 総コミット数：5432
```

### コミットをバッチで追加

```bash
# 最古の100コミットを追加
/add-commits 1 100

# 次のバッチを追加
/add-commits 101 200

# 特定の範囲を追加
/add-commits 301 400
```

### 現在のプロジェクトを確認

```bash
/current-oss

# 表示：リポジトリ情報、データベース、コミット数
```

### 利用可能なコミットを一覧

```bash
# 最古のコミットを一覧（デフォルト）
/list-commits

# 件数を指定
/list-commits --limit 50

# 最新順で表示
/list-commits --order newest
```

### プロジェクト間の切り替え

```bash
# 別のプロジェクトに切り替え
/register-oss https://github.com/facebook/react --database def456abc789

# 新しいプロジェクトにコミットを追加
/add-commits 1 100
```

## 💡 得られるもの

コミット追加後、Notionデータベースには：

| Title | Type | Commit ID | GitHub URL | Comment |
|-------|------|-----------|------------|---------|
| f7c8d10: 初期コミット | Commit | f7c8d10... | https://... | 初期コミットメッセージ |
| a3b4c5d: ルーティング追加 | Commit | a3b4c5d... | https://... | 基本的なルーティング... |
| ... | ... | ... | ... | ... |

各ページには：
- コミットメタデータ（著者、日付、変更ファイル数）
- 完全なコミットメッセージ
- GitHubへのリンク
- メモフィールド（あなたのメモ用）

## 🛠️ 使用するMCPサーバー

### ビルトイン（Claude Code）
- **Serena** - 意味的なコード理解とプロジェクトメモリ

### 外部（自動インストール）
- **GitHub MCP** - リポジトリメタデータとアクセス
- **Notion MCP** - データベース操作

## 🔧 要件

- **Node.js** v18+（MCPサーバー用）
- **Claude Code**（CLIまたはデスクトップ）
- **Notionアカウント**（データベース用）
- **GitHubアカウント**（APIアクセス用）

## 🎓 ユースケース

### オープンソースコントリビューター向け
```
1. 興味のあるプロジェクトを登録
2. コミットを時系列で追加
3. プロジェクトの進化を研究
4. コントリビューションへの理解を構築
```

### 開発チーム向け
```
1. チームプロジェクトのコミットを追跡
2. 検索可能なコミット履歴を構築
3. メモとコンテキストを追加
4. ナレッジベースを共有
```

### 学習者向け
```
1. 最初のコミットからプロジェクトの進化を研究
2. 機能がどのように構築されたかを理解
3. 経験豊富な開発者からパターンを学ぶ
4. 個人的なナレッジベースを構築
```

## 📋 利用可能なコマンド

| コマンド | 説明 |
|---------|------|
| `/register-oss` | OSSリポジトリをデータベースと共に登録 |
| `/add-commits` | コミットをバッチでNotionに追加 |
| `/current-oss` | 現在のプロジェクト情報を表示 |
| `/list-commits` | 利用可能なコミットを一覧 |

## 🤝 コントリビューション

コントリビューションを歓迎します！ガイドラインは[CONTRIBUTING.md](CONTRIBUTING.md)を参照してください。

## 📄 ライセンス

MITライセンス - 詳細は[LICENSE](LICENSE)を参照

## 🔗 リンク

- **GitHubリポジトリ**：https://github.com/Kuroakira/deep-code-reader
- **Issue & フィードバック**：https://github.com/Kuroakira/deep-code-reader/issues

---

**OSSコミュニティのために ❤️ を込めて構築**

*一度に一つのコミットで、オープンソースをより身近に。*
