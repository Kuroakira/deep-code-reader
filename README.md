# OSS Learning Platform

**Automated OSS codebase analysis with Notion integration, powered by Claude Code and MCP servers.**

Perfect for developers who want to:
- 🚀 Track and understand commits systematically
- 📚 Build a knowledge base in Notion
- 🎯 Learn from open source projects chronologically
- 🤝 Prepare for contributions with context

## ✨ Features

### 🔍 Batch Commit Tracking
- **Range-based addition** - Add commits 1-100, 101-200, etc.
- **Duplicate detection** - Automatically skips existing entries
- **Schema auto-detection** - Adapts to your Notion database structure
- **Simple info** - Commit ID, message, author, date, files changed

### 🤖 Intelligent Automation
- **One-command installation** - `./install.sh` sets up everything
- **Project context memory** - Register once, add commits without repeating URLs
- **Local clone support** - Fast access via local git repository
- **Symbol-level understanding** - Serena MCP for semantic code comprehension

### 📝 Notion Integration
- **Your own database** - You create and control the database structure
- **Batch export** - Add hundreds of commits efficiently
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
2. 📦 Install MCP servers (GitHub, Notion)
3. ⚙️  Configure Claude Code
4. 🎯 Install skills and commands

### Setup Notion Database (Manual)

**Before using the platform, create your Notion database:**

1. **Create a Notion Integration**
   - Visit https://www.notion.so/my-integrations
   - Create integration named "Deep Code Reader"
   - Copy the Internal Integration Secret

2. **Create a Database** with these properties:
   - `Title` (title) - Commit title
   - `Commit ID / PR No` (text) - Full commit hash
   - `Type` (select) - "Commit" option
   - `GitHub URL` (url) - Link to commit
   - `Comment` (text) - Commit message
   - `Memo` (text) - Your notes

3. **Share Database with Integration**
   - Open database in Notion
   - Click "..." → "Connections" → Add your integration

4. **Copy Database ID** from URL:
   - URL: `https://notion.so/abc123def456?v=...`
   - Database ID: `abc123def456`

### First Use (1 minute)

```bash
# Step 1: Register OSS repository with your database
/register-oss https://github.com/expressjs/express --database abc123def456

# Step 2: Add commits in batches
/add-commits 1 100      # First 100 commits (oldest)
/add-commits 101 200    # Next 100 commits
/add-commits 201 300    # Continue...

# Check progress
/current-oss
/list-commits
```

**That's it!** Claude will:
- 💾 Clone the repository locally
- 🔄 Fetch commit information
- 📊 Add commits to your Notion database
- ⏭️ Skip duplicates automatically

## 📁 Project Structure

```
deep-code-reader/
├── install.sh                    # One-command installer
├── uninstall.sh                  # Clean uninstaller
├── commands/                     # Slash commands
│   ├── register-oss.md          # Register OSS repository
│   ├── add-commits.md           # Batch add commits
│   ├── current-oss.md           # Show current project
│   └── list-commits.md          # List commits
├── config/                       # Configuration files
│   └── mcp_servers.json         # MCP server setup
├── scripts/                      # Utility scripts
│   └── utils/                   # Helper utilities
└── skills/                       # Claude Skills
    └── deep-code-reader/        # Code analysis skill
```

## 📦 Installed Files

After running `./install.sh`:

```
~/.claude/
├── deep-code-reader/            # Project-specific files
│   ├── repos/                   # Cloned repositories
│   │   └── {owner}/{repo}/      # Local git clones
│   └── current_oss.json         # Current project config
│
├── commands/                    # Slash commands
│   ├── register-oss.md
│   ├── add-commits.md
│   ├── current-oss.md
│   └── list-commits.md
│
└── skills/                      # Claude Skills
    └── deep-code-reader/

~/.claude.json                   # Claude Code CLI configuration
```

## 🎯 Usage Examples

### Register OSS Repository

```bash
# Register with your Notion database
/register-oss https://github.com/nestjs/nest --database abc123def456

# Output:
# ✅ OSS Repository Registered
# Project: nest
# Database: abc123def456
# Total Commits: 5432
```

### Add Commits in Batches

```bash
# Add oldest 100 commits
/add-commits 1 100

# Add next batch
/add-commits 101 200

# Add specific range
/add-commits 301 400
```

### Check Current Project

```bash
/current-oss

# Shows: Repository info, database, commit count
```

### List Available Commits

```bash
# List oldest commits (default)
/list-commits

# List with limit
/list-commits --limit 50

# List newest first
/list-commits --order newest
```

### Switch Between Projects

```bash
# Switch to a different project
/register-oss https://github.com/facebook/react --database def456abc789

# Add commits to new project
/add-commits 1 100
```

## 💡 What You Get

After adding commits, your Notion database will have:

| Title | Type | Commit ID | GitHub URL | Comment |
|-------|------|-----------|------------|---------|
| f7c8d10: Initial commit | Commit | f7c8d10... | https://... | Initial commit message |
| a3b4c5d: Add routing | Commit | a3b4c5d... | https://... | Add basic routing... |
| ... | ... | ... | ... | ... |

Each page contains:
- Commit metadata (author, date, files changed)
- Full commit message
- Link to GitHub
- Memo field for your notes

## 🛠️ MCP Servers Used

### Built-in (Claude Code)
- **Serena** - Semantic code understanding & project memory

### External (Auto-installed)
- **GitHub MCP** - Repository metadata and access
- **Notion MCP** - Database operations

## 🔧 Requirements

- **Node.js** v18+ (for MCP servers)
- **Claude Code** (CLI or Desktop)
- **Notion account** (for database)
- **GitHub account** (for API access)

## 🎓 Use Cases

### For Open Source Contributors
```
1. Register interesting projects
2. Add commits chronologically
3. Study how the project evolved
4. Build understanding for contributions
```

### For Development Teams
```
1. Track commits from team projects
2. Build searchable commit history
3. Add notes and context
4. Share knowledge base
```

### For Learners
```
1. Study project evolution from first commit
2. Understand how features were built
3. Learn patterns from experienced developers
4. Build personal knowledge base
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `/register-oss` | Register OSS repository with database |
| `/add-commits` | Batch add commits to Notion |
| `/current-oss` | Show current project info |
| `/list-commits` | List available commits |

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🔗 Links

- **GitHub Repository**: https://github.com/Kuroakira/deep-code-reader
- **Issues & Feedback**: https://github.com/Kuroakira/deep-code-reader/issues

---

**Built with ❤️ for the OSS community**

*Making open source more accessible, one commit at a time.*
