---
name: analyze-commit
description: Deep analysis of a single commit with context gathering and Notion export
---

# Analyze Single Commit

Perform comprehensive analysis of a single commit, understanding the **Why**, **What**, **Impact**, and **Design** behind the changes.

## Usage

```
/analyze-commit <commit-hash>
/analyze-commit <github-url> <commit-hash>  # URL optional if project registered
```

**Examples**:
```
# After /register-oss - URL not needed!
/analyze-commit abc1234567
/analyze-commit abc1234  # Short hash OK

# Or with explicit URL
/analyze-commit https://github.com/expressjs/express abc1234567
```

## Analysis Workflow

### Phase 0: Repository Setup and Local Clone

**IMPORTANT**: This command requires a local clone of the repository for deep code analysis.

#### Step 0.1: Repository URL Resolution

```python
# If URL not provided, read from memory
if not github_url:
    current_oss = serena_mcp.read_memory("current_oss")

    if not current_oss:
        print("⚠️  No repository specified and no current project set")
        print("Please either:")
        print("  1. Register a project: /register-oss <github-url>")
        print("  2. Or specify URL: /analyze-commit <github-url> <commit-hash>")
        return

    github_url = current_oss["repo_url"]
    owner = current_oss["owner"]
    repo = current_oss["repo"]
    notion_oss_page_id = current_oss["notion_page_id"]
    local_repo_path = current_oss.get("local_repo_path")  # May be None

    print(f"📦 Using current project: {owner}/{repo}")
else:
    # URL provided, parse it
    owner, repo = parse_github_url(github_url)
    local_repo_path = None
```

#### Step 0.2: Local Clone Verification

Check if repository is cloned locally:

```python
import os
from pathlib import Path

# Determine expected clone location
if not local_repo_path:
    # Default location: ~/.claude/deep-code-reader/repos/{owner}/{repo}
    home = Path.home()
    local_repo_path = home / ".claude" / "deep-code-reader" / "repos" / owner / repo

# Check if clone exists
if not os.path.exists(local_repo_path / ".git"):
    print(f"⚠️  Repository not cloned locally")
    print(f"")
    print(f"This repository needs to be registered first for deep code analysis:")
    print(f"")
    print(f"  /register-oss {github_url}")
    print(f"")
    print(f"The /register-oss command will:")
    print(f"  • Clone the repository to ~/.claude/deep-code-reader/repos/{owner}/{repo}")
    print(f"  • Set up Notion database for tracking")
    print(f"  • Enable deep code analysis features")
    print(f"")
    print(f"After registration, run this command again.")
    return

print(f"✅ Repository found: {local_repo_path}")

# Activate project in Serena MCP for symbol analysis
serena_mcp.activate_project(str(local_repo_path))
print(f"🔍 Serena MCP activated for deep analysis")
```

#### Step 0.3: Checkout Commit

```python
# Checkout the specific commit for analysis
import subprocess

try:
    # Save current branch
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=local_repo_path,
        capture_output=True,
        text=True
    )
    original_branch = result.stdout.strip()

    # Checkout the commit
    subprocess.run(
        ["git", "checkout", commit_hash],
        cwd=local_repo_path,
        check=True,
        capture_output=True
    )

    print(f"📍 Checked out commit: {commit_hash}")

    # Store for cleanup later
    cleanup_info = {
        "repo_path": local_repo_path,
        "original_branch": original_branch,
        "commit_hash": commit_hash
    }

except subprocess.CalledProcessError as e:
    print(f"❌ Error checking out commit: {e}")
    return
```

### Phase 1: Commit Data Gathering (use GitHub MCP)

Fetch commit information:

```python
# Get commit details
commit_info = github_mcp.get_commit(owner, repo, commit_hash)

Required data:
- Commit hash (full & short)
- Commit message
- Author & date
- Changed files
- Diff content
- Parent commits
```

### Phase 2: Context Gathering (use GitHub MCP + Sequential Thinking)

#### 2.1 Related Issues

Extract issue references from:
- Commit message: `#123`, `fixes #456`, `closes #789`
- PR associations: If commit is part of a PR

```python
# Find related issues
issues = extract_issue_numbers(commit_message)
for issue_num in issues:
    issue_data = github_mcp.get_issue(owner, repo, issue_num)
    # Store: issue title, description, labels
```

#### 2.2 Before & After Context

Get surrounding commits:

```python
# Get commit timeline
before_commits = git log --oneline {commit}~3..{commit}~1
after_commits = git log --oneline {commit}..{commit}+2

Context includes:
- 1-2 commits before
- 1-2 commits after
- Brief description of each
```

#### 2.3 Pull Request Context (if applicable)

```python
# Find associated PR
prs = github_mcp.search_prs(query=f"commit:{commit_hash}")
if prs:
    pr_data = github_mcp.get_pr(owner, repo, pr.number)
    # Store: PR title, description, reviews, comments
```

### Phase 3: Deep Code Analysis (use GitHub MCP + Sequential Thinking + Serena MCP)

**IMPORTANT**: This phase performs **line-by-line code analysis** for deep understanding.

#### 3.1 ファイルの完全な内容取得 (from Local Clone + Serena MCP)

For each changed file, get the full file content from local clone:

```python
# Get commit details from GitHub API
commit_data = github_mcp.get_commit(owner, repo, commit_hash)

files_analysis = []

for file in commit_data["files"]:
    file_path = file["filename"]
    full_path = local_repo_path / file_path

    # Get the FULL file content AFTER the change (currently checked out)
    if file["status"] != "deleted":
        file_content_after = serena_mcp.read_file(
            relative_path=file_path,
            max_answer_chars=-1  # Read entire file
        )
    else:
        file_content_after = None

    # Get the file content BEFORE the change
    if file["status"] != "added":
        # Checkout parent commit temporarily to read old content
        parent_sha = commit_data["parents"][0]["sha"]

        subprocess.run(
            ["git", "checkout", parent_sha, "--", file_path],
            cwd=local_repo_path,
            capture_output=True
        )

        file_content_before = serena_mcp.read_file(
            relative_path=file_path,
            max_answer_chars=-1
        )

        # Restore to current commit
        subprocess.run(
            ["git", "checkout", commit_hash, "--", file_path],
            cwd=local_repo_path,
            capture_output=True
        )
    else:
        file_content_before = None

    # Get the patch/diff from GitHub
    diff = file["patch"]

    # Use Serena MCP to get symbol information
    symbols_info = None
    if is_code_file(file_path) and file["status"] != "deleted":
        try:
            # Get overview of symbols in this file
            symbols_info = serena_mcp.get_symbols_overview(
                relative_path=file_path,
                max_answer_chars=-1
            )
        except Exception as e:
            print(f"⚠️  Could not analyze symbols in {file_path}: {e}")

    # Store all for detailed analysis
    files_analysis.append({
        "path": file_path,
        "status": file["status"],  # added, modified, deleted
        "content_after": file_content_after,
        "content_before": file_content_before,
        "diff": diff,
        "additions": file["additions"],
        "deletions": file["deletions"],
        "symbols": symbols_info  # NEW: Symbol-level information
    })

print(f"✅ Loaded {len(files_analysis)} files for deep analysis")
```

#### 3.2 変更の意図 (Why)

Analyze **why** this change was made:

```markdown
- 問題: What problem does this solve?
- 動機: Why was this approach chosen?
- 背景: What's the business/technical context?

Sources:
- Commit message
- Related issue descriptions
- PR discussions
- Code comments in changed files
```

#### 3.3 ファイルごとの詳細解析 (Detailed File Analysis)

**For EACH changed file**, perform deep analysis:

```python
for file_info in files_analysis:
    file_analysis = {
        "file_path": file_info["path"],
        "file_role": "",  # このファイルの役割
        "change_summary": "",  # 変更の概要
        "detailed_explanation": "",  # 詳細な説明
        "code_walkthrough": []  # コードの行ごとの解説
    }

    # Step 1: ファイルの役割を理解
    file_analysis["file_role"] = analyze_file_role(
        file_path=file_info["path"],
        content=file_info["content_after"],
        project_context=commit_data
    )

    # Step 2: 変更の概要
    file_analysis["change_summary"] = f"""
    - 変更タイプ: {file_info["status"]} ({file_info["additions"]}行追加, {file_info["deletions"]}行削除)
    - 主な変更内容: [AIが分析]
    """

    # Step 3: 詳細な解説 (LINE-BY-LINE)
    # Parse the diff to identify changed sections
    changed_sections = parse_diff(file_info["diff"])

    for section in changed_sections:
        section_analysis = {
            "line_range": section["line_range"],
            "change_type": section["type"],  # addition, deletion, modification
            "code_before": section["code_before"],
            "code_after": section["code_after"],
            "explanation": ""
        }

        # DEEP ANALYSIS: Explain what this code does LINE BY LINE
        section_analysis["explanation"] = analyze_code_section(
            code=section["code_after"],
            context={
                "file_path": file_info["path"],
                "file_role": file_analysis["file_role"],
                "full_content": file_info["content_after"],
                "change_intent": commit_message
            }
        )

        file_analysis["code_walkthrough"].append(section_analysis)
```

**Example of detailed analysis output**:

```markdown
### 📄 src/auth/middleware.js

**ファイルの役割**:
認証ミドルウェアを提供し、リクエストの認証トークンを検証する。全てのAPIエンドポイントの前に実行される。

**変更の概要**:
- 変更タイプ: modified (45行追加, 12行削除)
- 主な変更: 入力検証の強化とレート制限の追加

---

#### 🔍 詳細な変更解析

**セクション 1: トークン検証の強化 (L23-L45)**

変更前のコード:
```javascript
function validateToken(token) {
  return jwt.verify(token, SECRET_KEY);
}
```

変更後のコード:
```javascript
function validateToken(token) {
  // L23: トークンの存在チェック - 空文字列やnullを防ぐ
  if (!token || typeof token !== 'string') {
    throw new Error('Invalid token format');
  }

  // L27-28: トークンの長さチェック - 異常に短い/長いトークンを拒否
  // JWTの標準的な長さは200-300文字程度
  if (token.length < 50 || token.length > 500) {
    throw new Error('Token length out of acceptable range');
  }

  // L32-36: トークンのフォーマット検証
  // JWTは "header.payload.signature" の3部構成
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Malformed JWT token');
  }

  // L40-45: Base64エンコーディングの検証
  // 各パートがBase64エンコードされているか確認
  try {
    parts.forEach(part => {
      Buffer.from(part, 'base64');
    });
  } catch (e) {
    throw new Error('Invalid Base64 encoding in token');
  }

  // L45: 最終的な署名検証（元のコードと同じ）
  return jwt.verify(token, SECRET_KEY);
}
```

**なぜこの変更が必要だったか**:
CVE-2024-1234で報告された脆弱性に対処。攻撃者が不正な形式のトークンを送信してサーバーをクラッシュさせる問題を修正。

**コードの動作詳細**:
1. **L23-25**: まず最初にトークンの存在と型をチェック。これにより、`undefined`や数値などの無効な入力を早期にリジェクト。
2. **L27-30**: 長さチェックで、極端に短い（総当たり攻撃）や長い（DoS攻撃）トークンを防ぐ。
3. **L32-36**: JWTの基本構造（3パート構成）を検証。不正なフォーマットを早期検出。
4. **L40-44**: 各パートのBase64エンコーディングを検証。デコードエラーでクラッシュする前に捕捉。
5. **L45**: 全ての検証を通過した後、元の`jwt.verify()`を実行。

**使用されているパターン**:
- **Defense in Depth**: 複数層の検証で攻撃を防ぐ
- **Fail Fast**: 問題を早期に検出してエラーを返す
- **Input Validation**: 全ての外部入力を信頼せず検証

---

**セクション 2: レート制限の追加 (L67-L89)**

[... 同様の詳細な解析 ...]
```

#### 3.4 変更内容の全体サマリ (What)

After detailed file analysis, create overall summary:

```markdown
変更されたファイル:
1. **src/auth/middleware.js** (45行追加, 12行削除)
   - トークン検証の多層防御を実装
   - レート制限機能の追加

2. **src/auth/validator.js** (23行追加, 5行削除)
   - カスタムバリデータのサポート追加

3. **test/auth.test.js** (67行追加, 0行削除)
   - 包括的なテストケースの追加
   - エッジケースのカバレッジ向上

主な技術的変更:
- 入力検証の強化（長さ、型、フォーマット）
- レート制限アルゴリズム（Token Bucket方式）の導入
- テストカバレッジ 45% → 92%に向上
```

#### 3.5 影響範囲 (Impact)

Assess **impact** on the codebase with detailed dependency analysis:

```python
# Use Serena MCP to analyze symbol dependencies
impact_analysis = {
    "affected_modules": [],
    "breaking_changes": [],
    "api_compatibility": {},
    "performance_impact": {},
    "security_impact": {}
}

# For each changed file, find what depends on it
for file_info in files_analysis:
    # Use Serena's find_referencing_symbols to find dependencies
    if file is code file:
        symbols = serena_mcp.find_symbol(
            name_path="",  # Find all symbols in file
            relative_path=file_info["path"]
        )

        for symbol in symbols:
            references = serena_mcp.find_referencing_symbols(
                name_path=symbol["name_path"],
                relative_path=file_info["path"]
            )

            impact_analysis["affected_modules"].extend(references)

# Analyze breaking changes
for change in changed_sections:
    if is_api_change(change) and not_backward_compatible(change):
        impact_analysis["breaking_changes"].append({
            "file": change["file"],
            "change": change["description"],
            "migration": generate_migration_guide(change)
        })
```

**Example output**:

```markdown
### 🏗️ 影響範囲

#### 影響を受けるモジュール

**直接的な影響** (このコードを直接使用):
1. **api/routes/auth.js** (12箇所で使用)
   - L45: `validateToken(req.headers.authorization)`
   - L67: `validateToken(sessionToken)`
   - 影響: 新しい検証ロジックが自動適用、修正不要

2. **api/routes/user.js** (8箇所で使用)
   - L23: `middleware.validateToken(token)`
   - 影響: エラーハンドリングの改善が必要（新しいエラータイプ対応）

**間接的な影響** (依存関係を通じて影響):
1. **middleware/session.js**
   - auth/middlewareを経由して影響
   - セッション検証フローに変更なし

2. **config/security.js**
   - レート制限の設定値を参照
   - 新しい設定項目の追加が必要

#### 破壊的変更 (Breaking Changes)

❌ **なし** - すべての変更は後方互換性を保持

#### API互換性

✅ **完全互換** - 既存のAPIシグネチャに変更なし

追加されたエラータイプ:
- `TokenFormatError` - 不正なフォーマット
- `TokenLengthError` - 長さが範囲外
- `RateLimitError` - レート制限超過

移行ガイド:
```javascript
// Before (既存のコード - 引き続き動作)
try {
  const user = validateToken(token);
} catch (err) {
  // 一般的なエラー処理
}

// After (推奨 - 新しいエラータイプに対応)
try {
  const user = validateToken(token);
} catch (err) {
  if (err instanceof TokenFormatError) {
    // 不正なフォーマット専用の処理
  } else if (err instanceof RateLimitError) {
    // レート制限専用の処理
  }
  // その他のエラー処理
}
```

#### パフォーマンス影響

**検証処理**:
- 追加の検証ステップ: +0.5ms (L23-L44の処理)
- 全体的なレイテンシ: 2.3ms → 2.8ms (+21%)
- トレードオフ: わずかな遅延 vs セキュリティ大幅向上

**メモリ使用量**:
- レート制限データ構造: +2MB (1万ユーザーあたり)
- Token Bucketマップ: O(active_users) のメモリ

**スケーラビリティ**:
- ✅ 問題なし: レート制限はRedisへ移行可能（コメントに記載）
- ⚠️  注意: 10万+ 同時ユーザーではRedis化を推奨

#### セキュリティ影響

**修正された脆弱性**:
- **CVE-2024-1234** (Critical): Server crash via malformed tokens
- **CVSS Score**: 9.8 → 0.0 (完全修正)

**追加されたセキュリティ機能**:
1. 入力検証の多層防御
2. DoS攻撃対策（レート制限）
3. 異常検知と早期リジェクト

**セキュリティテストカバレッジ**:
- Fuzzing test追加: 10,000パターン
- エッジケース: 全てカバー
```

#### 3.6 設計意図とアーキテクチャ (Design)

Understand **design** decisions with deep architectural analysis:

```python
# Use Sequential Thinking to analyze design patterns
design_analysis = {
    "patterns": [],
    "trade_offs": [],
    "alternatives": [],
    "extensibility": [],
    "architectural_decisions": []
}

# Analyze each pattern used
for file_info in files_analysis:
    patterns = identify_design_patterns(file_info["content_after"])
    design_analysis["patterns"].extend(patterns)

# Analyze trade-offs
trade_offs = analyze_trade_offs(
    before=files_before,
    after=files_after,
    metrics=["performance", "security", "maintainability", "complexity"]
)
design_analysis["trade_offs"] = trade_offs
```

**Example output**:

```markdown
### 🎨 設計意図とアーキテクチャ

#### 使用されている設計パターン

**1. Chain of Responsibility (責任連鎖パターン)**

```
リクエスト → 存在チェック → 型チェック → 長さチェック → フォーマット検証 → Base64検証 → 署名検証 → 成功
            ↓            ↓          ↓             ↓                ↓              ↓
           エラー       エラー      エラー         エラー           エラー         エラー
```

なぜこのパターン?
- 各検証ステップが独立して失敗可能
- 新しい検証ルールの追加が容易
- テストが書きやすい（各ステップを個別にテスト）

**2. Fail Fast (早期失敗パターン)**

実装箇所: L23-L44の各検証ステップ

利点:
- リソースの無駄を防ぐ（無効なトークンを早期にリジェクト）
- ログとエラートレースの明確化
- デバッグの容易さ

**3. Defense in Depth (多層防御)**

セキュリティレイヤー:
```
Layer 1: 存在・型チェック     → 基本的な無効入力を拒否
Layer 2: 長さチェック          → DoS攻撃を防ぐ
Layer 3: フォーマット検証      → 構造的な攻撃を防ぐ
Layer 4: エンコーディング検証  → エンコード攻撃を防ぐ
Layer 5: 署名検証              → 偽造を防ぐ
Layer 6: レート制限            → 総当たり攻撃を防ぐ
```

**4. Token Bucket (レート制限アルゴリズム)**

```javascript
// L67-L89: Token Bucket実装
class TokenBucket {
  constructor(capacity, refillRate) {
    this.capacity = capacity;      // バケットの容量（最大トークン数）
    this.tokens = capacity;        // 現在のトークン数
    this.refillRate = refillRate;  // トークンの補充レート（毎秒）
    this.lastRefill = Date.now();
  }

  tryConsume() {
    this.refill();  // まずトークンを補充
    if (this.tokens >= 1) {
      this.tokens -= 1;
      return true;  // リクエスト許可
    }
    return false;  // レート制限超過
  }

  refill() {
    const now = Date.now();
    const timePassed = (now - this.lastRefill) / 1000;
    const tokensToAdd = timePassed * this.refillRate;
    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }
}
```

なぜToken Bucket?
- **柔軟性**: バースト的なトラフィックを許容
- **公平性**: 長期的には全ユーザーが平等
- **効率性**: O(1)の時間計算量

代替案との比較:
- Fixed Window: バースト攻撃に弱い ❌
- Sliding Window: メモリ使用量が多い ❌
- Token Bucket: バランスが良い ✅

#### 設計上のトレードオフ

**1. パフォーマンス vs セキュリティ**

決定: セキュリティを優先
- 検証ステップ追加により+0.5ms のレイテンシ増加
- しかしCVE-2024-1234 (Critical)を完全修正
- **判断**: わずかな遅延は許容範囲、セキュリティは必須

**2. メモリ使用 vs スケーラビリティ**

決定: 段階的アプローチ
- 初期実装: インメモリ（+2MB/1万ユーザー）
- スケールアップ時: Redisへ移行可能（コードにコメント記載）
- **判断**: 早期最適化を避け、必要になってから移行

**3. 複雑性 vs 保守性**

追加されたコード行数: 68行
- 各ステップに詳細なコメント
- テストカバレッジ92%
- **判断**: 複雑さは増すが、コメントとテストで保守性を確保

#### 検討された代替案

**代替案 1: ライブラリ使用 (express-rate-limit)**

メリット:
- 実装が簡単
- 実績あり

デメリット:
- 依存関係の追加
- カスタマイズ制限
- **却下理由**: 学習目的のため自前実装を選択

**代替案 2: より厳格な検証 (全トークンをパース)**

メリット:
- さらに詳細なエラーメッセージ

デメリット:
- パフォーマンス低下 (+2ms)
- 複雑性増大
- **却下理由**: コスト対効果が低い

#### 将来の拡張性

**拡張ポイント 1: カスタムバリデータ**

```javascript
// L45に追加可能な拡張ポイント
const customValidators = [];  // プラグイン可能

function validateToken(token, customValidators = []) {
  // ... 既存の検証 ...

  // カスタムバリデータを実行
  for (const validator of customValidators) {
    validator(token);
  }

  return jwt.verify(token, SECRET_KEY);
}
```

**拡張ポイント 2: Redis移行**

```javascript
// L75: インメモリ → Redis への移行が容易
// 現在:
const rateLimiters = new Map();  // メモリ内

// 将来:
const rateLimiters = new RedisTokenBucket(redisClient);
// インターフェースは同じまま
```

**拡張ポイント 3: メトリクス収集**

```javascript
// 各検証ステップでメトリクスを送信可能
metrics.increment('auth.validation.format_check');
metrics.increment('auth.validation.rate_limit');
```

#### アーキテクチャ上の決定事項

**1. 同期 vs 非同期処理**

決定: 同期処理を維持
- 理由: 検証は高速（<1ms）、非同期化のオーバーヘッドが無駄
- 将来: Redis移行時は async/await に変更

**2. エラーハンドリング戦略**

決定: 例外ベース (throw Error)
- 理由: Expressのエラーミドルウェアとの統合
- 一貫性: 既存コードベースとの整合性

**3. 設定の外部化**

決定: 定数を設定ファイルへ
```javascript
// config/auth.js に移動
module.exports = {
  TOKEN_MIN_LENGTH: 50,
  TOKEN_MAX_LENGTH: 500,
  RATE_LIMIT_CAPACITY: 100,
  RATE_LIMIT_REFILL_RATE: 10
};
```

#### アーキテクチャ図

```
┌─────────────────────────────────────────────────┐
│              APIリクエスト                        │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
          ┌────────────────┐
          │  Auth Middleware │
          └────────┬─────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
    ▼                             ▼
┌─────────┐                  ┌──────────┐
│ Rate    │                  │ Token    │
│ Limiter │                  │Validator │
└────┬────┘                  └────┬─────┘
     │                            │
     │ OK                         │
     ▼                            ▼
     │        ┌───────────────────┤
     │        │ 1. 存在チェック     │
     │        ├───────────────────┤
     │        │ 2. 型チェック       │
     │        ├───────────────────┤
     │        │ 3. 長さチェック     │
     │        ├───────────────────┤
     │        │ 4. フォーマット検証 │
     │        ├───────────────────┤
     │        │ 5. Base64検証     │
     │        ├───────────────────┤
     │        │ 6. 署名検証        │
     │        └───────────────────┘
     │                            │
     └──────────┬─────────────────┘
                │ ALL OK
                ▼
         ┌─────────────┐
         │ Route Handler│
         └──────────────┘
```
```

### Phase 4: Console Output

Display analysis in console:

```markdown
📊 Commit Analysis: abc1234

## 🎯 変更の意図 (Why)
Fix security vulnerability in authentication middleware (CVE-2024-1234)

Related Issues:
- #1234: Security: Auth bypass in edge case
- #1235: Enhancement: Add rate limiting

## 📝 変更内容 (What)

Changed Files (3):
- src/auth/middleware.js (+45, -12)
- src/auth/validator.js (+23, -5)
- test/auth.test.js (+67, -0)

Key Changes:
- Add input validation for auth tokens
- Implement rate limiting (100 req/min)
- Add comprehensive test coverage

## 🏗️ 影響範囲 (Impact)

Affected Modules:
- api/routes/* (10 files) - All routes using auth
- middleware/session.js - Session handling logic
- config/security.js - Security configuration

Risk Assessment:
✅ No breaking changes
✅ Backward compatible
⚠️  Requires config update in production

## 🎨 設計意図 (Design)

Pattern: Chain of Responsibility for validation
Trade-off: +2MB memory for 10x security improvement
Extensibility: Can add custom validators via plugin

## 🔗 コンテキスト

Before this commit:
- abc0123: Refactor auth module structure
- abc0122: Add auth logging

After this commit:
- abc1235: Update documentation
- abc1236: Deploy to staging

Related PR: #5234 "Security hardening"
- 5 approving reviews
- Passed all CI checks
- Merged 2 days ago

---

💾 Exporting to Notion...
```

### Phase 5: Notion Export with Deep Analysis (use Notion MCP)

**IMPORTANT**: Export ALL detailed analysis including line-by-line code explanations.

#### 5.1 Find OSS Page

```python
# Query OSSリスト database
oss_pages = notion_mcp.query_database(
    database_id=oss_database_id,
    filter={"property": "GitHub URL", "url": {"equals": repo_url}}
)

if not oss_pages:
    print("⚠️  Repository not registered. Run: /register-oss <url>")
    return

oss_page_id = oss_pages[0]["id"]
```

#### 5.2 Get Commits Database ID from Memory

```python
# Get OSS-specific commits database ID from current_oss memory
current_oss = serena_mcp.read_memory("current_oss")
commits_database_id = current_oss["commits_database_id"]
```

**Important**: Each OSS has its own Commits & PRs database. The database ID is stored in Serena memory when the OSS is registered.

#### 5.3 Create Commit Entry with Deep Analysis Content

```python
# Build detailed content blocks with ALL analysis sections
content_blocks = []

# 1. 変更の意図 (Why) - Heading 2
content_blocks.append({
    "heading_2": {"rich_text": [{"text": {"content": "🎯 変更の意図 (Why)"}}]}
})
content_blocks.append({
    "paragraph": {"rich_text": [{"text": {"content": why_analysis_text}}]}
})

# 2. ファイルごとの詳細解析 - For EACH file
for file_analysis in files_analysis:
    # File heading
    content_blocks.append({
        "heading_2": {"rich_text": [{"text": {"content": f"📄 {file_analysis['path']}"}}]}
    })

    # File role
    content_blocks.append({
        "heading_3": {"rich_text": [{"text": {"content": "ファイルの役割"}}]}
    })
    content_blocks.append({
        "paragraph": {"rich_text": [{"text": {"content": file_analysis["file_role"]}}]}
    })

    # Change summary
    content_blocks.append({
        "heading_3": {"rich_text": [{"text": {"content": "変更の概要"}}]}
    })
    content_blocks.append({
        "paragraph": {"rich_text": [{"text": {"content": file_analysis["change_summary"]}}]}
    })

    # Detailed code walkthrough (LINE-BY-LINE)
    content_blocks.append({
        "heading_3": {"rich_text": [{"text": {"content": "🔍 詳細な変更解析"}}]}
    })

    for section in file_analysis["code_walkthrough"]:
        # Section heading
        content_blocks.append({
            "heading_4": {"rich_text": [{"text": {
                "content": f"セクション: {section['line_range']} - {section['change_type']}"
            }}]}
        })

        # Code before (if exists)
        if section["code_before"]:
            content_blocks.append({
                "paragraph": {"rich_text": [{"text": {"content": "**変更前のコード:**"}}]}
            })
            content_blocks.append({
                "code": {
                    "rich_text": [{"text": {"content": section["code_before"]}}],
                    "language": detect_language(file_analysis["path"])
                }
            })

        # Code after
        content_blocks.append({
            "paragraph": {"rich_text": [{"text": {"content": "**変更後のコード:**"}}]}
        })
        content_blocks.append({
            "code": {
                "rich_text": [{"text": {"content": section["code_after"]}}],
                "language": detect_language(file_analysis["path"])
            }
        })

        # Detailed explanation (LINE-BY-LINE)
        content_blocks.append({
            "paragraph": {"rich_text": [{"text": {"content": "**詳細な解説:**"}}]}
        })
        content_blocks.append({
            "paragraph": {"rich_text": [{"text": {"content": section["explanation"]}}]}
        })

        # Pattern used
        if section.get("patterns"):
            content_blocks.append({
                "paragraph": {"rich_text": [{"text": {"content": f"**使用パターン:** {section['patterns']}"}}]}
            })

# 3. 影響範囲 (Impact)
content_blocks.append({
    "heading_2": {"rich_text": [{"text": {"content": "🏗️ 影響範囲 (Impact)"}}]}
})
content_blocks.extend(create_impact_blocks(impact_analysis))

# 4. 設計意図とアーキテクチャ (Design)
content_blocks.append({
    "heading_2": {"rich_text": [{"text": {"content": "🎨 設計意図とアーキテクチャ"}}]}
})
content_blocks.extend(create_design_blocks(design_analysis))

# 5. コンテキスト (Context)
content_blocks.append({
    "heading_2": {"rich_text": [{"text": {"content": "🔗 コンテキスト"}}]}
})
content_blocks.extend(create_context_blocks(related_commits, related_issues, related_pr))

# 6. Full Diff (in toggle for reference)
content_blocks.append({
    "toggle": {
        "rich_text": [{"text": {"content": "📋 完全なDiff (参考)"}}],
        "children": create_diff_blocks(commit_data["files"])
    }
})

# Create page in OSS-specific Commits & PRs database
commit_page = notion_mcp.create_page(
    parent={"database_id": commits_database_id},
    properties={
        "Title": f"{commit_hash_short}: {commit_message_first_line}",
        "Type": "Commit",  # NEW: Distinguish from PRs
        "Commit ID / PR No": commit_hash,
        "Comment": commit_message,
        "GitHub URL": f"{repo_url}/commit/{commit_hash}",
        "Analyzed Date": {"start": datetime.now().isoformat()},  # NEW
        "Memo": "",  # Empty for user to fill
    },
    children=content_blocks  # ALL detailed analysis
)

print(f"✅ Exported {len(content_blocks)} content blocks to Notion")
```

**Note**:
- Each file gets its own detailed section
- Code is shown with syntax highlighting
- Line-by-line explanations are included
- Full diff is in a toggle block for reference

#### 5.4 Confirm Export

```markdown
✅ Exported to Notion!

📄 Notion Page: https://notion.so/commit-page-id
🔗 View commit: [link to OSS page] → [link to this commit]

💡 Tip: Add personal notes in the "Memo" field
```

### Phase 6: Cleanup and Restore

**IMPORTANT**: Return repository to original state after analysis.

```python
# Restore original branch
try:
    subprocess.run(
        ["git", "checkout", cleanup_info["original_branch"]],
        cwd=cleanup_info["repo_path"],
        check=True,
        capture_output=True
    )
    print(f"✅ Restored to branch: {cleanup_info['original_branch']}")

except subprocess.CalledProcessError as e:
    print(f"⚠️  Could not restore branch: {e}")
    print(f"   Please manually run: cd {cleanup_info['repo_path']} && git checkout {cleanup_info['original_branch']}")

# Deactivate Serena project
try:
    serena_mcp.think_about_whether_you_are_done()
    print(f"✅ Serena MCP analysis complete")
except:
    pass
```

### Phase 7: Next Commit Suggestions

After successful analysis, suggest next commits to analyze:

```python
# Get surrounding commits for context
timeline_commits = github_mcp.list_commits(
    owner=owner,
    repo=repo,
    per_page=5
)

# Filter out already analyzed commits
analyzed_commits = serena_mcp.read_memory("analyzed_commits") or []
unanalyzed = [c for c in timeline_commits if c["sha"] not in analyzed_commits]

# Mark current commit as analyzed
analyzed_commits.append(commit_hash)
serena_mcp.write_memory("analyzed_commits", analyzed_commits)
```

Display suggestions:

```markdown
---

🔍 Next Suggestions

Recent commits from this project:

1. 🆕 def5678 - Add rate limiting to API endpoints
   📅 2025-01-14 • 👤 janedoe • ✏️ 5 files
   /analyze-commit def5678

2. 🆕 ghi9012 - Update dependencies
   📅 2025-01-13 • 👤 maintainer • ✏️ 1 file
   /analyze-commit ghi9012

3. ✅ xyz3456 - Refactor auth module (already analyzed)

💡 Commands:
  /list-commits           # Browse all recent commits
  /list-prs              # Browse pull requests
  /current-oss           # Check current project

Continue your learning journey! 🚀
```

## Error Handling

### Repository Not Set

```
⚠️  No Repository Specified

You haven't specified a repository URL and no current project is set.

Options:
1. Register a project first:
   /register-oss https://github.com/expressjs/express
   /analyze-commit abc1234

2. Or specify URL directly:
   /analyze-commit https://github.com/expressjs/express abc1234

Check current project:
   /current-oss
```

### Commit Not Found

```
❌ Error: Commit not found

Commit: abc1234
Repository: expressjs/express

Possible reasons:
- Commit hash is incorrect
- Commit was force-pushed/deleted
- Private repository without access

Please verify the commit hash.
```

### Repository Not Registered

```
⚠️  Repository Not Registered

Before analyzing commits, register the repository:

  /register-oss https://github.com/expressjs/express

This creates a parent entry in your OSSリスト database.
```

### Large Diff

```
⚠️  Large Commit Detected

This commit changes 150+ files (12,000 lines).

Options:
1. Continue with full analysis (~5min)
2. Summary only (skip detailed analysis)
3. Cancel

> _
```

### Related Issue Not Found

```
ℹ️  Context Gathering

Found issue references: #1234, #5678

✅ #1234: Security vulnerability (loaded)
❌ #5678: Issue not found or private

Continuing with available context...
```

## Output Format

### Console (always shown)

```markdown
📊 Commit Analysis Complete

## Summary
- Changed: 3 files
- Added: 135 lines
- Removed: 17 lines
- Impact: Medium (10 dependent modules)

## Key Insights
🎯 Why: Security fix for CVE-2024-1234
📝 What: Auth middleware validation
🏗️ Impact: All API routes (backward compatible)
🎨 Design: Chain of Responsibility pattern

🔗 Full analysis: https://notion.so/commit-page-id
```

### Notion (complete analysis)

Full detailed page with:
- 🎯 変更の意図
- 📝 変更内容 (with code diff)
- 🏗️ 影響範囲
- 🎨 設計意図
- 🔗 コンテキスト (issues, commits, PR)
- 📋 Complete diff (in toggle)

## Advanced Features

### Compare Mode

```
/analyze-commit <url> <commit1>..<commit2>
```

Analyze changes between two commits.

### Focus Analysis

```
/analyze-commit <url> <commit> --focus security
```

Focus on specific aspects:
- `security`: Security implications
- `performance`: Performance impact
- `api`: API changes
- `breaking`: Breaking changes

### Skip Export

```
/analyze-commit <url> <commit> --no-export
```

Analyze only, don't export to Notion.

## Tips

1. **Start with context**: Always check related issues first
2. **Think in layers**: Why → What → Impact → Design
3. **Use your notes**: Fill the "Memo" field in Notion
4. **Compare commits**: Use before/after commits for better understanding
5. **Focus on intent**: Understand why, not just what changed
