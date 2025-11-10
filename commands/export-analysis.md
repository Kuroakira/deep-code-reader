---
name: export-analysis
description: Manually export existing analysis results to Notion
---

# Export Analysis to Notion

Manually export code analysis results to Notion. Use this when:
- You've run analysis without auto-export
- You want to re-export with different formatting
- You're updating an existing analysis

## Usage

```
/export-analysis [analysis-file]
```

**Parameters**:
- `analysis-file` (optional): Path to JSON analysis file
  - Default: Most recent analysis in `/tmp/oss_analysis/`

## Workflow

### Step 1: Locate Analysis Results

If no file specified, find the most recent analysis:

```bash
# Find recent analyses
ls -lt /tmp/oss_analysis/*.json | head -5
```

Show user the available analyses:

```markdown
📂 Available Analyses:

1. express_analysis_20250111_120530.json
   - Repository: expressjs/express
   - Analyzed: 2025-01-11 12:05:30
   - Size: 245 KB

2. react_analysis_20250111_103042.json
   - Repository: facebook/react
   - Analyzed: 2025-01-11 10:30:42
   - Size: 1.2 MB

Which analysis would you like to export? (1-2)
```

### Step 2: Verify Notion Configuration

Check if Notion is configured:

```python
import json
from pathlib import Path

config_file = Path("config/notion_config.json")

if not config_file.exists():
    print("❌ Notion not configured. Run: /setup-notion")
    exit(1)

with open(config_file) as f:
    config = json.load(f)

if config.get("api_key") == "YOUR_NOTION_API_KEY":
    print("⚠️  Notion API key not set. Run: /setup-notion")
    exit(1)
```

### Step 3: Load Analysis Data

Parse the analysis JSON:

```python
with open(analysis_file) as f:
    analysis_data = json.load(f)

# Verify required fields
required = ["project_name", "repo_url", "commit_id", "architecture"]
missing = [f for f in required if f not in analysis_data]

if missing:
    print(f"❌ Invalid analysis file. Missing: {', '.join(missing)}")
    exit(1)
```

### Step 4: Build Notion Page

Use the Notion helpers:

```python
from scripts.utils.notion_helpers import NotionExporter

exporter = NotionExporter()
page_content = exporter.build_page_content(analysis_data)
```

### Step 5: Export to Notion (use Notion MCP)

Export using Notion MCP tools:

1. **Create page in database**:
   - Use `mcp__notion__create_page` or equivalent
   - Pass database_id from config
   - Include all properties and content blocks

2. **Upload diagrams** (if available):
   - Embed Mermaid as code blocks
   - Link to external diagrams if needed

3. **Get page URL**:
   - Extract URL from response
   - Return to user

### Step 6: Confirm Success

Display result to user:

```markdown
✅ Analysis Exported to Notion!

📊 Project: [project_name]
📅 Analysis Date: [date]
🔗 Notion Page: [notion_url]

📋 Exported Content:
- Architecture overview ✓
- Architecture diagrams ✓
- Data flow analysis ✓
- Dependency mapping ✓
- Recommendations ✓

💡 View in Notion: [clickable link]
```

## Options

Support additional export options:

### Update Existing Page

```
/export-analysis --update [page-id]
```

Updates an existing Notion page instead of creating new one.

### Custom Template

```
/export-analysis --template custom
```

Uses custom template from `config/notion_template_custom.json`.

### Export Format

```
/export-analysis --format [compact|detailed|summary]
```

- `compact`: Summary only, no raw data
- `detailed`: Full analysis with all diagrams (default)
- `summary`: Architecture and recommendations only

## Error Handling

### Analysis File Not Found

```
❌ Error: Analysis file not found

Path: /tmp/oss_analysis/foo_analysis.json

Available analyses:
- /tmp/oss_analysis/express_analysis.json
- /tmp/oss_analysis/react_analysis.json

Use: /export-analysis [file-path]
```

### Notion API Error

```
❌ Error: Failed to create Notion page

Error: "Invalid database_id"

Possible fixes:
1. Verify database ID in config/notion_config.json
2. Ensure database is shared with integration
3. Run: /setup-notion to reconfigure

Details: [error message from Notion API]
```

### Rate Limit

```
⚠️  Notion API Rate Limit

You've hit Notion's rate limit (3 requests/second).

Retrying in: 5 seconds...
[Progress bar]

✅ Export resumed
```

### Incomplete Analysis

```
⚠️  Incomplete Analysis Data

The analysis file is missing some sections:
✓ Architecture
✗ Data flow
✗ Dependencies

Export anyway? (yes/no)

> _
```

## Batch Export

Support exporting multiple analyses:

```
/export-analysis --batch
```

Export all analyses in `/tmp/oss_analysis/`:

```markdown
📦 Batch Export Mode

Found 3 analyses:
1. express_analysis.json → ⏳ Exporting...
2. react_analysis.json → ⏳ Queued
3. vue_analysis.json → ⏳ Queued

Progress: [▓▓▓░░░░░░░] 1/3

✅ Exported: express_analysis
   URL: https://notion.so/page-1

✅ Exported: react_analysis
   URL: https://notion.so/page-2

✅ Exported: vue_analysis
   URL: https://notion.so/page-3

🎉 Batch export complete! (3/3 successful)
```

## Output Format

Standard success output:

```markdown
✅ Export Complete

📊 Analysis: [project_name]
🔗 Notion: [notion_url]

📋 Details:
- Repository: [repo_url]
- Commit: [commit_id]
- Analyzed: [date]
- Exported: [export_date]

💡 Next steps:
- View in Notion: [URL]
- Share with team
- Add personal notes in Notion
```
