# OSS Learning Platform

**Automated OSS codebase analysis with intelligent insights and Notion integration, powered by Claude Code and MCP servers.**

Perfect for developers who want to:
- 🚀 Quickly understand unfamiliar OSS projects
- 📚 Build a knowledge base of analyzed codebases
- 🤝 Identify contribution opportunities
- 📊 Generate comprehensive architecture documentation

## ✨ Features

### 🔍 Deep Code Analysis
- **Architecture visualization** - Mermaid & draw.io diagrams
- **Data flow tracing** - Understand how data moves through the system
- **Dependency mapping** - Identify module relationships and circular dependencies
- **Pattern recognition** - Detect MVC, Clean Architecture, and other patterns

### 🤖 Intelligent Automation
- **One-command installation** - `./install.sh` sets up everything
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
git clone https://github.com/Kuroakira/claude_skills.git
cd claude_skills

# Run the installer
./install.sh
```

The installer will:
1. ✅ Check dependencies (Node.js, Python, npm)
2. 📦 Install MCP servers (GitHub, Brave Search, Notion)
3. ⚙️  Configure Claude Code
4. 🎯 Install skills and commands
5. 🔐 Set up Notion integration (optional)

### First Analysis (30 seconds)

```bash
# Start Claude Code
claude-code

# Analyze any GitHub repository
/analyze-oss https://github.com/expressjs/express main
```

**That's it!** Claude will:
- 🔄 Clone the repository
- 🏗️ Analyze architecture
- 📊 Generate diagrams
- 💡 Provide contribution recommendations
- 📤 Export everything to Notion

## 📁 Project Structure

```
claude_skills/
├── install.sh                    # One-command installer
├── commands/                     # Slash commands
│   ├── analyze-oss.md           # Main analysis command
│   ├── setup-notion.md          # Notion configuration
│   └── export-analysis.md       # Manual export
├── config/                       # Configuration files
│   ├── mcp_servers.json         # MCP server setup
│   ├── notion_template.json     # Notion page template
│   └── default_settings.json    # Platform settings
├── scripts/                      # Utilities
│   ├── setup/                   # Installation scripts
│   └── utils/                   # Helper functions
├── skills/                       # Claude Skills
│   └── deep-code-reader/        # Code analysis skill
└── docs/                         # Documentation
```

## 🎯 Usage Examples

### Basic Analysis

```bash
# Analyze a repository at HEAD
/analyze-oss https://github.com/vuejs/core

# Analyze a specific commit
/analyze-oss https://github.com/react/react v18.0.0

# Quick architecture-only analysis
/analyze-oss https://github.com/django/django --quick
```

### Notion Integration

```bash
# Set up Notion (first time only)
/setup-notion

# Analysis automatically exports to Notion
/analyze-oss https://github.com/sveltejs/svelte

# Manually export previous analysis
/export-analysis
```

### Advanced Options

```bash
# Focus on specific directory
/analyze-oss <url> --focus src/core

# Export with custom template
/export-analysis --template detailed

# Batch export multiple analyses
/export-analysis --batch
```

## 💡 What You Get

After analyzing a repository, you'll receive:

### 📊 In Claude Code

```markdown
## Analysis Complete: Express.js

### Architecture
- Pattern: Layered Architecture
- Layers: Router → Middleware → Application → Response
- Tech Stack: JavaScript, Node.js

### Key Data Flows
- HTTP Request → Middleware Chain → Route Handler → Response
- Error Handling → Error Middleware → Client

### Dependencies
- External: 30 packages
- Circular deps: 0
- Key libraries: body-parser, cookie-parser, debug

### Contribution Opportunities
1. Add TypeScript definitions for middleware
2. Improve error handling in router module
3. Add tests for edge cases in request parsing

Notion: https://notion.so/your-analysis-page
```

### 📝 In Notion

A beautifully formatted page with:
- 🏗️ Architecture overview with diagrams
- 🔄 Data flow visualizations
- 📦 Dependency graphs
- 💡 Actionable contribution recommendations
- 📋 Raw analysis data (JSON)

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
- **Python** 3.8+ (for analysis scripts)
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

- **GitHub Repository**: https://github.com/Kuroakira/claude_skills
- **Issues & Feedback**: https://github.com/Kuroakira/claude_skills/issues
- **Discussions**: https://github.com/Kuroakira/claude_skills/discussions
- **Anthropic Skills**: https://docs.anthropic.com/en/docs/build-with-claude/skills
- **MCP Documentation**: https://modelcontextprotocol.io/

---

**Built with ❤️ for the OSS community**

*Making open source more accessible, one analysis at a time.*
