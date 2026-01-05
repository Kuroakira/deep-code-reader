---
name: add-commits
description: Batch add commits to Notion database with intelligent column name detection
---

# Add Commits in Batch

Add multiple commits to the Notion database. The command intelligently analyzes your database column names and maps commit data accordingly.

## Usage

```
/add-commits <start> <end>
/add-commits <start> <end> --database <database_id>
```

**Parameters**:
- `start`: Starting commit number (1-indexed, oldest first)
- `end`: Ending commit number (inclusive)
- `--database`: (Optional) Notion database ID. Uses current project's database if not specified.

**Examples**:
```
# Add commits 1-100 (oldest 100 commits)
/add-commits 1 100

# Add commits 301-400
/add-commits 301 400

# Add with specific database ID
/add-commits 1 50 --database abc123def456
```

## Workflow

### Phase 1: Setup and Validation

#### Step 1.1: Get Current Project Configuration

```python
import json
import os
from pathlib import Path

# Read current OSS configuration
config_path = Path.home() / ".claude" / "deep-code-reader" / "current_oss.json"

if not config_path.exists():
    print("Error: No project configured.")
    print("Run: /register-oss <github-url> --database <database-id>")
    exit(1)

with open(config_path) as f:
    current_oss = json.load(f)

owner = current_oss["owner"]
repo = current_oss["repo"]
local_repo_path = current_oss.get("local_repo_path")
database_id = current_oss.get("database_id")

# Check for --database override
if args.get("database"):
    database_id = args["database"]

if not database_id:
    print("Error: No database ID found.")
    print("Run: /register-oss <github-url> --database <database-id>")
    exit(1)

if not local_repo_path or not Path(local_repo_path).exists():
    print("Error: Local repository not found.")
    print("Run: /register-oss to clone the repository")
    exit(1)

print(f"Project: {owner}/{repo}")
print(f"Database: {database_id}")
print(f"Local repo: {local_repo_path}")
```

#### Step 1.2: Get Notion API Key

```python
# Get Notion API key from MCP server configuration
mcp_config_path = Path.home() / ".claude.json"

with open(mcp_config_path) as f:
    mcp_config = json.load(f)

notion_config = mcp_config.get("mcpServers", {}).get("notion", {})
notion_api_key = notion_config.get("env", {}).get("NOTION_API_KEY")

if not notion_api_key:
    print("Error: Notion API key not configured.")
    print("Check your MCP server configuration.")
    exit(1)
```

### Phase 2: Run the Python Script

The core logic is in `scripts/utils/add_commits.py` which:

1. **Analyzes column names** - Reads your database schema and intelligently maps columns
2. **Detects duplicates** - Checks existing entries and skips already-added commits
3. **Adds commits** - Creates Notion pages with properly mapped data

```bash
# Set environment variable for API key
export NOTION_API_KEY="your-api-key"

# Run the script
python scripts/utils/add_commits.py \
    $START \
    $END \
    --repo "$LOCAL_REPO_PATH" \
    --owner "$OWNER" \
    --name "$REPO" \
    --database "$DATABASE_ID"
```

### Phase 3: Execution via Claude

Claude should execute the command by:

1. Reading current project configuration
2. Setting up environment variables
3. Running the Python script with proper arguments
4. Displaying the results

```python
import subprocess
import os

# Set up environment
env = os.environ.copy()
env["NOTION_API_KEY"] = notion_api_key

# Build command
script_path = Path(__file__).parent.parent / "scripts" / "utils" / "add_commits.py"

cmd = [
    "python3", str(script_path),
    str(args["start"]),
    str(args["end"]),
    "--repo", local_repo_path,
    "--owner", owner,
    "--name", repo,
    "--database", database_id
]

# Execute
result = subprocess.run(cmd, env=env, capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
```

## Intelligent Column Mapping

The script analyzes your column names and automatically maps commit data. It supports:

### Supported Languages

- **English**: hash, message, author, date, url, type, files, memo
- **Japanese**: ハッシュ, メッセージ, 作成者, 日付, リンク, タイプ, ファイル, メモ
- **Common patterns**: commit_id, github_url, created_at, file_count

### Mapping Examples

| Your Column Name | Detected As | Data Filled |
|-----------------|-------------|-------------|
| `Commit Hash` | commit_hash | Full SHA |
| `ハッシュ` | commit_hash | Full SHA |
| `SHA` | commit_hash | Full SHA |
| `Message` | message | Commit message |
| `説明` | message | Commit message |
| `Description` | message | Commit message |
| `Author` | author_name | Author name |
| `作成者` | author_name | Author name |
| `Committed By` | author_name | Author name |
| `Date` | date | Commit date |
| `日付` | date | Commit date |
| `Created At` | date | Commit date |
| `GitHub URL` | github_url | Commit link |
| `リンク` | github_url | Commit link |
| `Link` | github_url | Commit link |
| `Type` | type | "Commit" |
| `種類` | type | "Commit" |
| `Category` | type | "Commit" |
| `Files` | files_changed | File count |
| `ファイル数` | files_changed | File count |
| `Changes` | files_changed | File count |
| `Memo` | memo | (empty) |
| `備考` | memo | (empty) |

### Unmapped Columns

Columns that don't match any pattern are left empty. You can fill them manually in Notion.

## Output Example

```
============================================================
Add Commits to Notion
============================================================

Repository: nestjs/nest
Local Path: ~/.claude/deep-code-reader/repos/nestjs/nest
Database: abc123def456
Range: 1 to 100

📊 Analyzing database columns...
   Found 7 properties

   Column Analysis:
   --------------------------------------------------
   ✓ 'コミットID' (rich_text) → commit_hash (score: 7.00)
   ✓ 'メッセージ' (rich_text) → message (score: 6.30)
   ✓ '作成者' (rich_text) → author_name (score: 5.60)
   ✓ 'GitHub' (url) → github_url (score: 3.50)
   ✓ '日付' (date) → date (score: 4.20)
   ✓ 'タイプ' (select) → type (score: 2.80)
   - 'メモ' (rich_text) → (unmapped)
   --------------------------------------------------

   Final mapping:
   • commit_hash → 'コミットID'
   • message → 'メッセージ'
   • author_name → '作成者'
   • github_url → 'GitHub'
   • date → '日付'
   • type → 'タイプ'
   • title → 'タイトル'

🔍 Checking for existing entries...
   Found 0 existing commit entries

📥 Fetching commits 1 to 100...
   Fetched 100 commits

📊 Summary:
   Commits to add: 100
   Duplicates skipped: 0

📤 Adding 100 commits to Notion...
   Progress: 10/100
   Progress: 20/100
   ...
   Progress: 100/100

============================================================
Complete!
============================================================

Added: 100
Errors: 0
Skipped: 0

View in Notion: https://notion.so/abc123def456
```

## Tips

1. **Name columns clearly** - Use descriptive names like "Commit Hash" or "コミットID"
2. **Any language works** - English, Japanese, or mixed naming is supported
3. **Re-run safely** - Duplicates are automatically skipped
4. **Check mapping** - The output shows how columns were mapped
5. **Unmapped is OK** - Extra columns stay empty for your notes

## Troubleshooting

### "No project configured"

Run `/register-oss <github-url> --database <id>` first.

### "Column not mapped correctly"

The script uses keyword matching. Rename your column to include clearer keywords:
- For commit hash: include "hash", "sha", "id"
- For message: include "message", "description", "comment"
- For author: include "author", "by", "committer"

### "API rate limit"

Notion has rate limits. Wait a few minutes and try again with a smaller range.
