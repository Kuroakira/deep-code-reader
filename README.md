# Deep Code Reader - Claude Skill

A comprehensive Claude Skill for understanding complex codebases through systematic analysis, visualization, and context gathering. Perfect for developers joining OSS projects or performing deep code reviews.

## 🎯 What This Skill Does

Deep Code Reader helps you understand unfamiliar codebases by:

- 🏗️ **Generating architecture diagrams** (Mermaid & draw.io formats)
- 🔄 **Tracing data flows** through the system
- 📊 **Analyzing dependencies** and identifying circular dependencies
- 🔍 **Gathering PR context** from GitHub (issues, reviews, discussions)

## 📁 Repository Structure

```
deep-code-reader/
├── SKILL.md                              # Main skill instructions for Claude
├── scripts/                              # Standalone analysis scripts
│   ├── generate_architecture_diagram.py  # Create architecture diagrams
│   ├── analyze_data_flow.py             # Trace data through the system
│   ├── analyze_dependencies.py          # Map dependencies
│   └── fetch_pr_context.py              # Get GitHub PR context
├── references/                           # Reference documentation
│   ├── code-reading-methodology.md      # Effective code reading strategies
│   └── architecture-patterns.md         # Common architecture patterns
└── assets/                               # Templates and resources
    └── architecture-template.drawio     # draw.io diagram template
```

## 🚀 Installation

### For Claude.ai Users (Recommended)

1. **Download the packaged skill** from [Releases](../../releases)
2. **Upload to Claude.ai**:
   - Go to Settings → Skills
   - Click "Upload Skill"
   - Select the downloaded `.skill` file
3. The skill will automatically activate when you work with code

### For Claude Code Users

```bash
# Clone this repository
git clone https://github.com/your-username/deep-code-reader.git

# Install to Claude skills directory
mkdir -p ~/.claude/skills
cp -r deep-code-reader ~/.claude/skills/

# The skill is now available in Claude Code
```

### For Developers (Contributing)

```bash
# Clone the repository
git clone https://github.com/your-username/deep-code-reader.git
cd deep-code-reader

# Make changes to scripts, SKILL.md, etc.
# Test your changes

# Package the skill for distribution
python /path/to/anthropic/skills/skill-creator/scripts/package_skill.py . ./dist
```

### Usage Examples

**Understand a new OSS project:**
```
Help me understand the architecture of this codebase [upload or link to repo]
```

**Trace a specific flow:**
```
Show me how authentication works in this codebase
```

**Analyze a PR:**
```
Analyze this PR and show me what changed: https://github.com/org/repo/pull/123
```

**Generate documentation:**
```
Create architecture diagrams for this project in both Mermaid and draw.io formats
```

## 📋 Features

### 1. Architecture Visualization
- Automatically detects architectural patterns (MVC, Clean Architecture, etc.)
- Generates multi-format diagrams (Mermaid for docs, draw.io for editing)
- Identifies layers and component relationships

### 2. Data Flow Analysis
- Traces function call chains
- Identifies authentication flows automatically
- Maps data processing pipelines
- Detects common patterns

### 3. Dependency Analysis
- Maps module and package dependencies
- Detects circular dependencies (code smells)
- Identifies tightly coupled components
- Analyzes external package usage

### 4. PR Context Gathering
- Fetches complete PR information from GitHub
- Links to related issues
- Includes review comments and discussions
- Shows commit history and context

## 🛠️ Included Scripts

All analysis scripts work standalone (no external dependencies):

- `generate_architecture_diagram.py` - Create architecture diagrams
- `analyze_data_flow.py` - Trace data through the system
- `analyze_dependencies.py` - Map dependencies and find issues
- `fetch_pr_context.py` - Get comprehensive PR context

## 📚 Reference Materials

- **Code Reading Methodology** - Proven strategies for understanding codebases
- **Architecture Patterns** - Recognition guide for common patterns
- **draw.io Templates** - Ready-to-use architecture diagram templates

## 💡 Use Cases

### For OSS Contributors
- Quickly understand a new project before contributing
- Identify where to add new features
- Understand the impact of potential changes

### For Code Reviewers
- Get full context on PRs before reviewing
- Understand change implications
- Verify architectural consistency

### For Documentation
- Generate up-to-date architecture diagrams
- Create visual guides for new team members
- Document data flows and dependencies

### For Refactoring
- Identify tightly coupled code
- Find circular dependencies
- Plan architectural improvements

## 🎨 Output Formats

- **Mermaid (.mmd)** - Embeddable in GitHub/GitLab markdown
- **draw.io (.drawio)** - Editable diagrams for presentations
- **JSON (.json)** - Complete analysis data for custom processing
- **Markdown (.md)** - Human-readable summaries

## 🔧 Requirements

- Python 3.7+ (for standalone script usage)
- No external dependencies (scripts use standard library only)
- GitHub token (optional, for higher API rate limits)

## 📖 Documentation

Full documentation is available in the skill's SKILL.md file, including:
- Detailed usage examples
- Best practices for each analysis type
- Integration tips (IDE, CI/CD, documentation)
- Troubleshooting guide
- Advanced usage patterns

## 🤝 Contributing

Contributions are welcome! This skill focuses on:
- Static code analysis
- Visual diagram generation
- Context gathering
- Code reading methodologies

Ideas for improvements:
- Support for additional languages (Go, Rust, Java, etc.)
- More architectural pattern detection
- Integration with additional tools
- Performance optimizations for large codebases

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Created as part of Anthropic's Claude Skills system. Inspired by the need for better tools to understand complex, unfamiliar codebases.

## 🔗 Links

- [Anthropic Skills Documentation](https://docs.anthropic.com/en/docs/build-with-claude/skills)
- [Claude Skills Repository](https://github.com/anthropics/skills)
- [Mermaid Documentation](https://mermaid.js.org/)
- [draw.io](https://www.drawio.com/)

---

**Built with ❤️ for the OSS community**
