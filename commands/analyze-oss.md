---
name: analyze-oss
description: Deep analysis of OSS repository with automatic Notion export
---

# OSS Repository Deep Analysis

You are an expert code analyst helping developers understand and contribute to open source projects. Your task is to perform comprehensive codebase analysis and document findings in Notion.

## Input Parameters

Required:
- **Repository URL**: GitHub repository URL (e.g., https://github.com/user/repo)

Optional:
- **Commit ID**: Specific commit hash or branch name (default: HEAD/main)

## Analysis Workflow

Follow this systematic workflow to ensure thorough analysis:

### Phase 1: Repository Acquisition (use GitHub MCP)

1. **Validate URL**: Ensure it's a valid GitHub repository
2. **Check access**: Verify repository is accessible (handle private repos)
3. **Clone repository**: Use `scripts/utils/clone_repository.py`
   ```bash
   python3 scripts/utils/clone_repository.py <repo_url> --commit <commit_id> --info
   ```
4. **Extract metadata**: Get project name, commit info, language stats

### Phase 2: Strategic Analysis Planning (use Sequential Thinking MCP)

Before diving into code, analyze the project strategically:

1. **Project type identification**:
   - Web application, library, CLI tool, framework, etc.
   - Primary language(s) and frameworks
   - Project maturity and size

2. **Analysis priorities**:
   - Key components to understand first
   - Critical data flows to trace
   - Important architectural patterns
   - Potential contribution areas

3. **Resource allocation**:
   - Estimate analysis complexity
   - Identify areas needing deep vs shallow analysis
   - Plan tool usage (Serena vs native)

### Phase 3: Architecture Analysis (use Serena MCP + deep-code-reader)

1. **High-level structure** (use Serena):
   - Use `mcp__serena__list_dir` to explore project structure
   - Use `mcp__serena__get_symbols_overview` for key files
   - Use `mcp__serena__find_symbol` for important classes/functions

2. **Generate architecture diagram**:
   ```bash
   python3 skills/deep-code-reader/scripts/generate_architecture_diagram.py \
     <repo_path> --format both --output architecture
   ```

3. **Identify patterns** (use Context7 MCP):
   - Detect architectural pattern (MVC, Clean Architecture, etc.)
   - Identify design patterns in use
   - Note framework-specific patterns

4. **Document findings**:
   - Architecture summary (2-3 paragraphs)
   - Layer descriptions
   - Key components and their roles
   - Technology stack

### Phase 4: Data Flow Analysis

1. **Identify entry points**:
   - API endpoints, CLI commands, UI entry points
   - Event handlers and callbacks

2. **Trace critical flows**:
   ```bash
   python3 skills/deep-code-reader/scripts/analyze_data_flow.py \
     <repo_path> --pattern all --output dataflow
   ```

3. **Authentication/Authorization** (if applicable):
   - How users are authenticated
   - Permission/authorization mechanisms
   - Session management

4. **Data processing pipelines**:
   - Input validation
   - Business logic flow
   - Data persistence

### Phase 5: Dependency Analysis

1. **Analyze dependencies**:
   ```bash
   python3 skills/deep-code-reader/scripts/analyze_dependencies.py \
     <repo_path> --diagrams all --output deps
   ```

2. **External dependencies**:
   - Third-party libraries
   - Version requirements
   - Potential security concerns

3. **Internal coupling**:
   - Module interdependencies
   - Circular dependencies (code smells)
   - Tight vs loose coupling

### Phase 6: Contribution Recommendations

Based on analysis, identify:

1. **Good first issues**:
   - Areas suitable for newcomers
   - Well-isolated components
   - Clear improvement opportunities

2. **Architecture improvements**:
   - Refactoring opportunities
   - Performance bottlenecks
   - Code quality issues

3. **Missing functionality**:
   - Common features not implemented
   - Integration opportunities
   - Documentation gaps

### Phase 7: Notion Export (use Notion MCP)

1. **Prepare export data**:
   - Consolidate all analysis results
   - Format diagrams (Mermaid, JSON)
   - Compile recommendations

2. **Build Notion page**:
   - Use `scripts/utils/notion_helpers.py`
   - Load Notion template
   - Populate with analysis data

3. **Export to Notion** (use Notion MCP tools):
   - Create page in configured database
   - Upload all content blocks
   - Set properties (repo URL, commit, date, etc.)
   - Return Notion page URL

## Output Format

Provide the user with:

### 1. Analysis Summary (in chat)

```markdown
## 📊 Analysis Complete: [Project Name]

### 🏗️ Architecture
[2-3 sentence summary of architecture]
- Pattern: [e.g., MVC, Clean Architecture]
- Layers: [key layers]
- Tech Stack: [main technologies]

### 🔄 Key Data Flows
- [Flow 1: e.g., Authentication via JWT]
- [Flow 2: e.g., API request processing]
- [Flow 3: e.g., Database transactions]

### 📦 Dependencies
- External: [count] packages
- Circular deps: [count] (⚠️ if > 0)
- Key libraries: [top 3]

### 💡 Contribution Opportunities
1. [Specific recommendation]
2. [Specific recommendation]
3. [Specific recommendation]

### 🔗 Full Analysis
Notion: [Notion page URL]

### 📂 Generated Artifacts
- Architecture diagram: [path]
- Data flow diagram: [path]
- Dependency graph: [path]
- Raw analysis data: [path]
```

### 2. Embedded Diagrams

Include key Mermaid diagrams inline (architecture and main data flow).

### 3. Notion Link

Prominently display the Notion page URL for detailed exploration.

## Error Handling

### Invalid Repository URL
```
❌ Error: Invalid repository URL

Please provide a valid GitHub URL:
  ✓ https://github.com/user/repo
  ✓ https://github.com/user/repo/tree/branch
  ✗ gitlab.com/user/repo (only GitHub supported)
```

### Private Repository
```
⚠️  Private Repository Detected

This repository requires authentication.
Please set GITHUB_TOKEN:
  export GITHUB_TOKEN=your_token

Or provide token via:
  /analyze-oss <url> --token <token>
```

### Repository Too Large
```
⚠️  Large Repository (>100k LOC)

This may take 5-10 minutes. Options:
1. Continue with full analysis
2. Focus on specific directory: /analyze-oss <url> --focus src/core
3. Quick analysis (architecture only): /analyze-oss <url> --quick
```

### Notion Configuration Missing
```
⚠️  Notion Not Configured

Analysis complete, but cannot export to Notion.
Please configure Notion:
  1. Edit: config/notion_config.json
  2. Add your API key and database ID
  3. Run: /setup-notion

Analysis results saved locally:
  - JSON: /tmp/oss_analysis/results.json
  - Diagrams: /tmp/oss_analysis/*.mmd
```

### Analysis Timeout
```
⚠️  Analysis Timeout

Full analysis exceeded 5 minutes. Partial results:
  ✓ Architecture: Complete
  ✓ Dependencies: Complete
  ⏳ Data flow: Incomplete

Options:
1. Use partial results
2. Retry with --timeout 600
3. Focus analysis: --focus src/
```

## Best Practices

1. **Start broad, go deep**: Architecture → Dependencies → Data flows → Details
2. **Use right tools**: Serena for symbols, native grep for patterns, Context7 for frameworks
3. **Progressive disclosure**: Present summary first, detailed analysis in Notion
4. **Actionable insights**: Always provide specific contribution recommendations
5. **Save artifacts**: Keep generated files for user reference

## Example Usage

```
User: /analyze-oss https://github.com/expressjs/express main