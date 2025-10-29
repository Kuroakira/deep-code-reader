---
name: deep-code-reader
description: Comprehensive codebase analysis and understanding tool for OSS projects. This skill should be used when users need to understand existing code architecture, trace data flows, analyze dependencies, or comprehend pull request contexts. Ideal for onboarding to new projects, deep code reading, and systematic codebase exploration.
---

# Deep Code Reader

A comprehensive skill for understanding complex codebases through systematic analysis, visualization, and context gathering. Designed specifically for developers joining OSS projects or performing deep code reviews.

## Core Capabilities

This skill provides four main analysis capabilities:

1. **Architecture Visualization** - Generate architecture diagrams in Mermaid and draw.io formats
2. **Data Flow Tracing** - Trace how data moves through the system
3. **Dependency Analysis** - Map module dependencies and identify circular dependencies
4. **PR Context Gathering** - Fetch comprehensive pull request context from GitHub

## When to Use This Skill

Use this skill when the user needs to:

- Understand the overall architecture of an unfamiliar codebase
- Trace authentication flows or data processing pipelines
- Analyze dependencies between modules or packages
- Understand the context and changes in a GitHub pull request
- Generate documentation diagrams for a project
- Identify architectural patterns in existing code
- Prepare for code contributions to OSS projects

## Quick Start

### 1. Generate Architecture Diagram

To create an overview of the codebase architecture:

```bash
python scripts/generate_architecture_diagram.py /path/to/codebase --format both --output arch
```

This generates:
- `arch_architecture.mmd` - Mermaid architecture diagram
- `arch_dependencies.mmd` - Mermaid dependency graph
- `arch_architecture.drawio` - draw.io editable diagram
- `arch_analysis.json` - Full analysis data

**Options:**
- `--format` - Output format: `mermaid`, `drawio`, or `both` (default: both)
- `--type` - Diagram type: `architecture`, `dependencies`, or `both` (default: architecture)
- `--output` - Output file prefix (default: architecture)

### 2. Analyze Data Flow

To understand how data flows through the system:

```bash
python scripts/analyze_data_flow.py /path/to/codebase --pattern all --output dataflow
```

For tracing a specific function:

```bash
python scripts/analyze_data_flow.py /path/to/codebase --trace function_name --depth 5
```

This generates:
- `dataflow_analysis.json` - Complete flow analysis
- `dataflow_auth_flow.mmd` - Authentication flow diagram (if detected)
- `dataflow_data_flow.mmd` - Data processing flow diagram (if detected)
- `dataflow_trace_[function].mmd` - Specific function trace diagram

**Options:**
- `--trace` - Function name to trace from
- `--depth` - Maximum trace depth (default: 5)
- `--pattern` - Pattern to identify: `auth`, `data`, or `all` (default: all)

### 3. Analyze Dependencies

To map module dependencies and find issues:

```bash
python scripts/analyze_dependencies.py /path/to/codebase --diagrams all --output deps
```

This generates:
- `deps_analysis.json` - Complete dependency data
- `deps_packages.mmd` - Package-level dependency diagram
- `deps_modules.mmd` - Module-level dependency diagram
- `deps_circular.mmd` - Circular dependency diagram (if found)

**Options:**
- `--diagrams` - Which diagrams to generate: `all`, `package`, `module`, `circular` (default: all)

### 4. Fetch PR Context

To understand a GitHub pull request comprehensively:

```bash
python scripts/fetch_pr_context.py https://github.com/owner/repo/pull/123 --format both --output pr_context
```

This generates:
- `pr_context.json` - Complete PR data including commits, reviews, comments
- `pr_context.md` - Human-readable markdown summary

**Options:**
- `--format` - Output format: `json`, `markdown`, or `both` (default: both)
- `--token` - GitHub personal access token (or set GITHUB_TOKEN env var)

**Note:** For higher API rate limits, provide a GitHub token via `--token` or set the `GITHUB_TOKEN` environment variable.

## Workflow Examples

### Example 1: OSS Project Onboarding

**Scenario:** User wants to understand a new OSS project they're contributing to.

**Steps:**

1. Generate overall architecture:
   ```bash
   python scripts/generate_architecture_diagram.py ./project --format both
   ```

2. Identify patterns and analyze dependencies:
   ```bash
   python scripts/analyze_dependencies.py ./project
   ```

3. Understand authentication flow:
   ```bash
   python scripts/analyze_data_flow.py ./project --pattern auth
   ```

4. Read the methodology guide:
   ```
   Review references/code-reading-methodology.md for effective reading strategies
   ```

### Example 2: Understanding a Specific PR

**Scenario:** User needs to review a complex PR with multiple commits and discussions.

**Steps:**

1. Fetch PR context:
   ```bash
   python scripts/fetch_pr_context.py https://github.com/org/repo/pull/456
   ```

2. Analyze changed files' dependencies:
   ```bash
   # Extract changed files from pr_context.json
   python scripts/analyze_dependencies.py ./project
   ```

3. Trace data flow for affected functions:
   ```bash
   python scripts/analyze_data_flow.py ./project --trace affected_function
   ```

### Example 3: Architecture Documentation

**Scenario:** User needs to create architecture documentation for their project.

**Steps:**

1. Generate all diagrams:
   ```bash
   python scripts/generate_architecture_diagram.py ./project --type both --format both
   python scripts/analyze_dependencies.py ./project --diagrams all
   python scripts/analyze_data_flow.py ./project --pattern all
   ```

2. Edit draw.io diagram for presentation:
   - Open `*_architecture.drawio` in draw.io
   - Customize colors, layout, and annotations
   - Export to PNG/SVG for documentation

3. Include Mermaid diagrams in markdown documentation:
   ```markdown
   ## Architecture Overview
   
   \`\`\`mermaid
   [paste contents of *_architecture.mmd]
   \`\`\`
   ```

## Understanding the Outputs

### Mermaid Diagrams (.mmd)

Mermaid diagrams can be:
- Rendered directly in GitHub/GitLab markdown
- Visualized in the Mermaid Live Editor (https://mermaid.live)
- Converted to images using mermaid-cli
- Embedded in documentation

### draw.io Diagrams (.drawio)

draw.io files can be:
- Opened and edited in https://app.diagrams.net
- Integrated with VS Code via draw.io extension
- Exported to PNG, SVG, PDF for presentations
- Version controlled alongside code

### JSON Analysis Files

JSON files contain complete analysis data and can be:
- Processed programmatically for custom analysis
- Used to generate custom visualizations
- Compared across versions to track changes
- Integrated into CI/CD pipelines

## Best Practices

### For Architecture Analysis

1. **Start broad, then narrow**: Generate overall architecture first, then focus on specific areas
2. **Compare formats**: Use Mermaid for quick viewing, draw.io for detailed editing
3. **Update regularly**: Regenerate diagrams as the codebase evolves
4. **Validate findings**: Cross-reference generated diagrams with actual code

### For Data Flow Analysis

1. **Identify entry points**: Start tracing from API endpoints or main functions
2. **Follow the data**: Track how data transforms through the system
3. **Note patterns**: Look for consistent patterns in how data flows
4. **Document findings**: Add notes about discovered flows to project documentation

### For Dependency Analysis

1. **Check for cycles**: Circular dependencies indicate design issues
2. **Identify coupling**: High fan-out suggests tight coupling
3. **Review externals**: Ensure external dependencies are necessary and up-to-date
4. **Plan refactoring**: Use insights to guide architectural improvements

### For PR Analysis

1. **Read context first**: Understand the problem before diving into code
2. **Check linked issues**: Issues provide valuable context about why changes were made
3. **Review discussions**: Comments often reveal important considerations
4. **Trace impact**: Use dependency analysis to understand change ripple effects

## Reference Materials

### Code Reading Methodology

See `references/code-reading-methodology.md` for:
- Different reading strategies (top-down, bottom-up, use case driven)
- Techniques for understanding complex code
- OSS-specific strategies
- PR understanding framework
- Note-taking templates

**When to read:** When planning your approach to understanding a new codebase.

### Architecture Patterns

See `references/architecture-patterns.md` for:
- Common architectural patterns (MVC, Clean Architecture, Microservices)
- Pattern recognition guide
- Quick reference table
- Anti-patterns to watch for

**When to read:** When trying to identify what architectural pattern a codebase uses.

## Templates

### draw.io Architecture Template

Use `assets/architecture-template.drawio` as a starting point for custom architecture diagrams. The template includes:
- Standard layer structure
- Color-coded layers (presentation, API, business logic, data access)
- Database representation
- Proper connections and styling

**To use:**
1. Open in draw.io
2. Customize layers based on actual architecture
3. Add components within each layer
4. Save and export as needed

## Integration Tips

### IDE Integration

- **VS Code**: Install draw.io extension to edit diagrams in IDE
- **IntelliJ**: Use Mermaid plugin for live preview
- **Git hooks**: Run analysis on pre-commit to track changes

### Documentation Integration

Include generated diagrams in project documentation:

\`\`\`markdown
# Architecture

Our system follows a layered architecture:

![Architecture](./docs/diagrams/architecture.png)

## Data Flow

Authentication flow:

\`\`\`mermaid
[paste auth flow mermaid]
\`\`\`
\`\`\`

### CI/CD Integration

Add architecture validation to CI:

\`\`\`yaml
- name: Analyze Architecture
  run: |
    python scripts/analyze_dependencies.py . --output deps
    # Fail if circular dependencies found
    [ $(jq '.metrics.circular_dependencies' deps_analysis.json) -eq 0 ]
\`\`\`

## Troubleshooting

### Script Errors

**Import errors:**
- Ensure you're using Python 3.7+
- All scripts use only standard library (no external dependencies needed)

**Permission errors:**
- Make scripts executable: `chmod +x scripts/*.py`
- Or run with python: `python3 scripts/script_name.py`

### GitHub API Rate Limits

**Problem:** API requests failing with rate limit errors

**Solution:**
1. Set `GITHUB_TOKEN` environment variable
2. Or pass token with `--token` flag
3. Personal access token only needs public repo read access

### Large Codebases

**Problem:** Analysis takes too long or produces too much output

**Solution:**
1. Focus analysis on specific directories
2. Use `--max-nodes` parameter to limit diagram complexity
3. Exclude unnecessary directories in the analyzer

## Advanced Usage

### Custom Analysis Scripts

All analysis results are in JSON format, making it easy to write custom analysis:

\`\`\`python
import json

# Load dependency analysis
with open('deps_analysis.json') as f:
    deps = json.load(f)

# Find modules with most dependencies
modules = deps['module_dependencies']
sorted_modules = sorted(modules.items(), 
                       key=lambda x: len(x[1]), 
                       reverse=True)

print("Top 10 most dependent modules:")
for module, module_deps in sorted_modules[:10]:
    print(f"  {module}: {len(module_deps)} dependencies")
\`\`\`

### Combining Multiple Analyses

Correlate different analyses for deeper insights:

\`\`\`python
# Example: Find which highly-coupled modules are involved in auth flow
import json

# Load both analyses
with open('deps_analysis.json') as f:
    deps = json.load(f)
with open('dataflow_analysis.json') as f:
    flow = json.load(f)

# Find intersection
auth_funcs = set(flow['patterns']['authentication_functions'])
high_deps = set(m for m, d in deps['metrics']['high_fan_out'][:10])

overlap = auth_funcs & high_deps
print(f"Auth functions with high coupling: {overlap}")
\`\`\`

## Limitations

- **Language support**: Python and JavaScript/TypeScript analysis. Other languages need manual diagram creation.
- **Dynamic behavior**: Static analysis can't capture runtime behavior or dynamic imports
- **Accuracy**: Generated diagrams are best-effort and may need manual refinement
- **Scale**: Very large codebases (>100k LOC) may need focused analysis on subdirectories

## Summary

The Deep Code Reader skill provides a systematic approach to understanding complex codebases through:

1. **Automated analysis** - Scripts that analyze code structure
2. **Visual diagrams** - Multiple format support for different use cases
3. **Contextual understanding** - PR context and code reading methodologies
4. **Best practices** - Guides for effective code reading and analysis

Use this skill whenever facing an unfamiliar codebase or needing to deeply understand existing code.
