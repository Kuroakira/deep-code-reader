# OSS Learning Platform

**Automated OSS codebase analysis with intelligent insights and Notion integration, powered by Claude Code and MCP servers.**

Perfect for developers who want to:
- 🚀 Understand commits and PRs deeply
- 📚 Build a knowledge base in Notion
- 🎯 Learn WHY changes were made, not just WHAT
- 🤝 Prepare for contributions with context

## ✨ Features

### 🔍 Commit-Level Deep Analysis
- **Why (変更の意図)** - Understand the motivation behind changes
- **What (変更内容)** - See exactly what was changed
- **Impact (影響範囲)** - Know which modules are affected
- **Design (設計意図)** - Learn the design decisions and trade-offs
- **Context (コンテキスト)** - Related issues, PRs, and surrounding commits

### 🤖 Intelligent Automation
- **One-command installation** - `./install.sh` sets up everything
- **Project context memory** - Register once, analyze many commits without repeating URLs
- **Strategic analysis** - AI-powered analysis planning with Sequential Thinking
- **Symbol-level understanding** - Serena MCP for semantic code comprehension
- **Framework expertise** - Context7 MCP for official documentation patterns

### 📝 Notion Integration
- **Automatic export** - Analysis results saved to your Notion workspace
- **Structured documentation** - Consistent, searchable analysis pages
- **Team collaboration** - Share insights with your team
- **Knowledge base** - Build a library of analyzed projects

## 🚀 Quick Start

### Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/Kuroakira/deep-code-reader.git
cd deep-code-reader

# Run the installer
./install.sh
```

The installer will:
1. ✅ Check dependencies (Node.js, Python, npm)
2. 📦 Install MCP servers (GitHub, Brave Search, Notion)
3. ⚙️  Configure Claude Code
4. 🎯 Install skills and commands
5. 🔐 Set up Notion integration (optional)

### Uninstallation

To safely remove all installed components:

```bash
./uninstall.sh
```

The uninstaller will:
- 🔍 Scan for installed components
- 📋 Show what will be removed
- ⚠️  Ask for confirmation
- 🔄 Offer to restore config backups
- 💾 Preserve your Notion configuration (optional)
- 🗑️  Clean up all files

### First Analysis (30 seconds)

```bash
# Start Claude Code
claude-code

# Step 1: Register OSS repository (one time only)
/register-oss https://github.com/expressjs/express

# Step 2: Analyze commits - URL省略!
/analyze-commit abc1234567          # Just the commit hash
/analyze-commit def5678             # No URL needed!
/analyze-pr 5234                    # Just the PR number

# Check current project
/current-oss
```

**That's it!** Claude will:
- 💾 Remember your project context (no repeated URLs!)
- 🔄 Fetch commit information
- 🎯 Understand WHY the change was made
- 🏗️ Analyze impact on architecture
- 📊 Show detailed analysis in console
- 📤 Export everything to Notion automatically

## 📁 Project Structure

```
deep-code-reader/
├── install.sh                    # One-command installer
├── commands/                     # Slash commands
│   ├── register-oss.md          # Register OSS repository
│   ├── current-oss.md           # Show current project
│   ├── analyze-commit.md        # Analyze single commit
│   ├── analyze-pr.md            # Analyze pull request
│   └── setup-notion.md          # Notion configuration
├── config/                       # Configuration files
│   ├── mcp_servers.json         # MCP server setup
│   ├── notion_config.json       # Notion database IDs
│   └── notion_template.json     # Notion page template
├── skills/                       # Claude Skills
│   └── deep-code-reader/        # Code analysis skill
└── docs/                         # Documentation
```

## 🎯 Usage Examples

### Register OSS Repository

```bash
# Register once per project
/register-oss https://github.com/expressjs/express

# Creates entry in OSSリスト database
# Saves as current project in memory
```

### Check Current Project

```bash
# View currently active project
/current-oss

# Shows: Repository info, Notion page, available commands
```

### Analyze Commits

```bash
# After registration - URL not needed!
/analyze-commit abc1234
/analyze-commit def5678

# Or with explicit URL (optional)
/analyze-commit https://github.com/expressjs/express abc1234

# Shows detailed analysis in console + exports to Notion
```

### Analyze Pull Requests

```bash
# Just the PR number!
/analyze-pr 5234

# Or with full URL (optional)
/analyze-pr https://github.com/expressjs/express/pull/5234

# Asks: analyze all commits or select specific ones
```

### Switch Between Projects

```bash
# Switch to a different project
/register-oss https://github.com/facebook/react
/analyze-commit xyz9012          # Now uses react repo

# Switch back
/register-oss https://github.com/expressjs/express
/analyze-commit abc1234          # Back to express
```

### Notion Setup

```bash
# Configure Notion integration (first time only)
/setup-notion

# Or manually edit: config/notion_config.json
```

## 💡 What You Get

After analyzing a commit, you'll receive:

### 📊 In Claude Code

```markdown
📊 Commit Analysis: abc1234

## 🎯 変更の意図 (Why)
Fix security vulnerability in authentication middleware (CVE-2024-1234)

Related Issues: #1234, #1235

## 📝 変更内容 (What)
Changed Files (3):
- src/auth/middleware.js (+45, -12)
- src/auth/validator.js (+23, -5)
- test/auth.test.js (+67, -0)

## 🏗️ 影響範囲 (Impact)
Affected Modules:
- api/routes/* (10 files)
- middleware/session.js
✅ No breaking changes

## 🎨 設計意図 (Design)
Pattern: Chain of Responsibility
Trade-off: +2MB memory for 10x security

## 🔗 コンテキスト
Before: abc0123 - Refactor auth module
After: abc1235 - Update documentation
PR: #5234 (5 approving reviews)

💾 Exported to Notion: https://notion.so/commit-page
```

### 📝 In Notion

A structured analysis page with:
- 🎯 変更の意図 - Why this change was made
- 📝 変更内容 - What was changed (with code diff)
- 🏗️ 影響範囲 - Impact on the codebase
- 🎨 設計意図 - Design decisions and trade-offs
- 🔗 コンテキスト - Related issues, commits, PRs
- 📋 Complete diff (in toggle)
- 📝 Memo field (for your notes)

## 🛠️ MCP Servers Used

This platform leverages powerful MCP servers:

### Built-in (Claude Code)
- **Serena** - Semantic code understanding & project memory
- **Context7** - Official framework documentation
- **Sequential Thinking** - Strategic analysis planning

### External (Auto-installed)
- **GitHub MCP** - Repository metadata and access
- **Brave Search MCP** - Web search for documentation
- **Notion MCP** - Automated export to Notion

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[REPOSITORY_STRUCTURE.md](REPOSITORY_STRUCTURE.md)** - Project organization
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[docs/MCP_SETUP.md](docs/MCP_SETUP.md)** - MCP server configuration
- **[docs/NOTION_INTEGRATION.md](docs/NOTION_INTEGRATION.md)** - Notion setup guide

## 🧪 Supported Languages & Frameworks

### Current Support
- **Python** - Full support (Django, Flask, FastAPI)
- **JavaScript/TypeScript** - Full support (React, Vue, Express, Next.js)

### Planned Support
- **Go** - Coming soon
- **Rust** - Coming soon
- **Java** - Coming soon
- **Ruby** - Coming soon

## 🔧 Requirements

- **Node.js** v18+ (for MCP servers)
- **Claude Code** (CLI or Desktop)
- **Notion account** (optional, for exports)
- **GitHub account** (for analyzing private repos)

## 🎓 Use Cases

### For Open Source Contributors
```
1. Discover new projects to contribute to
2. Understand codebase before first PR
3. Identify "good first issues"
4. Learn architectural patterns
```

### For Development Teams
```
1. Onboard new team members faster
2. Document legacy codebases
3. Plan refactoring initiatives
4. Share architecture knowledge
```

### For Technical Leads
```
1. Evaluate potential dependencies
2. Assess code quality and architecture
3. Make informed technology decisions
4. Build technical documentation
```

### For Learners
```
1. Study real-world code architecture
2. Learn from established projects
3. Build a personal knowledge base
4. Understand best practices
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Testing requirements
- Pull request process

Ideas for contributions:
- Support for additional languages
- New analysis capabilities
- Alternative export formats
- Performance optimizations

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

Built with:
- [Claude Code](https://claude.com/claude-code) by Anthropic
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Notion API](https://developers.notion.com/)
- [GitHub API](https://docs.github.com/en/rest)

Inspired by the need for better tools to understand and contribute to open source projects.

## 🔗 Links

- **GitHub Repository**: https://github.com/Kuroakira/deep-code-reader
- **Issues & Feedback**: https://github.com/Kuroakira/deep-code-reader/issues
- **Discussions**: https://github.com/Kuroakira/deep-code-reader/discussions
- **Anthropic Skills**: https://docs.anthropic.com/en/docs/build-with-claude/skills
- **MCP Documentation**: https://modelcontextprotocol.io/

---

**Built with ❤️ for the OSS community**

*Making open source more accessible, one analysis at a time.*
