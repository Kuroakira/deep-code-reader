# Quick Start Guide - OSS Learning Platform

This guide will help you start analyzing OSS commits in 5 minutes.

## Installation (2 minutes)

### Step 1: Clone Repository

```bash
git clone https://github.com/Kuroakira/deep-code-reader.git
cd deep-code-reader
```

### Step 2: Run Installer

```bash
./install.sh
```

The installer will:
1. ✅ Check dependencies (Node.js, Python, npm)
2. 📦 Install MCP servers (GitHub, Brave Search, Notion)
3. ⚙️  Configure Claude Code
4. 🎯 Install skills and commands
5. 🔐 Set up Notion integration

### Step 3: Configure Notion

During installation, you'll be prompted:

```
Setup Notion now? (y/n)
```

**Say yes** and provide:
1. **Notion API Key** - Get from https://www.notion.so/my-integrations
2. **OSSリスト Database ID** - Create a database with:
   - Name (title)
   - GitHub URL (url)
3. **Commit & PRリスト Database ID** - Create a database with:
   - Title (title)
   - Commit ID / PR No (text)
   - Comment (text)
   - Created Date (date)
   - GitHub URL (url)
   - Memo (text)
   - OSS (relation to OSSリスト)

**Don't forget**: Share both databases with your integration!

---

## First Analysis (3 minutes)

### Step 1: Start Claude Code

```bash
claude-code
```

### Step 2: Register OSS Repository

```
/register-oss https://github.com/expressjs/express
```

**What happens:**
- ✅ Creates entry in your OSSリスト database
- ✅ Fetches repository metadata
- ✅ Returns Notion page URL

**Output:**
```
✅ OSS Repository Registered!

📦 Project: Express.js
🔗 GitHub: https://github.com/expressjs/express
📄 Notion: https://notion.so/Express-js-abc123

💡 Next: /analyze-commit <url> <commit-hash>
```

### Step 3: Analyze a Commit

```
/analyze-commit https://github.com/expressjs/express abc1234567
```

**What happens:**
- 📥 Fetches commit data from GitHub
- 🔍 Extracts related issues
- 🧠 Analyzes with AI (Sequential Thinking + Serena MCP)
- 📊 Shows detailed analysis in console
- 💾 Exports to Notion automatically

**Console Output:**
```
📊 Commit Analysis: abc1234

## 🎯 変更の意図 (Why)
Fix security vulnerability in authentication middleware

## 📝 変更内容 (What)
Changed Files: 3
- src/auth/middleware.js (+45, -12)
- src/auth/validator.js (+23, -5)
- test/auth.test.js (+67, -0)

## 🏗️ 影響範囲 (Impact)
Affected Modules: 10 files
✅ No breaking changes

## 🎨 設計意図 (Design)
Chain of Responsibility pattern
Trade-off: +2MB memory for 10x security

## 🔗 コンテキスト
Related Issues: #1234, #1235
PR: #5234 (5 reviews)

✅ Exported to Notion: https://notion.so/commit-abc123
```

### Step 4: Check Notion

Open the Notion page to see:
- ✅ Full structured analysis
- ✅ Code diff with syntax highlighting
- ✅ All context (issues, commits, PR)
- ✅ Memo field for your notes

---

## Advanced Usage

### Analyze Pull Requests

```
/analyze-pr https://github.com/expressjs/express/pull/5234
```

Analyzes all commits in the PR:
- Lists all commits
- You choose: all, specific, or summary only
- Creates individual pages for each commit
- Links them in Notion

### Compare Multiple Commits

```
/analyze-commit <url> <commit1>
/analyze-commit <url> <commit2>
/analyze-commit <url> <commit3>
```

Build a timeline of changes in your Notion database.

### Focus on Specific Aspects

```
/analyze-commit <url> <commit> --focus security
/analyze-commit <url> <commit> --focus performance
```

Get targeted analysis.

---

## Tips for Learning

### 1. Start Small
- Pick a small, focused commit (< 5 files changed)
- Understand it completely before moving to bigger ones

### 2. Follow a Feature
- Find a feature you're interested in
- Analyze all commits related to it
- See how it evolved over time

### 3. Study Patterns
- Look for recurring design patterns
- Notice how experienced developers structure changes
- Learn from commit messages

### 4. Use the Memo Field
- Add your own insights in Notion
- Note questions to explore later
- Link related commits

### 5. Build Your Database
- Consistently analyze commits
- Create a personal knowledge base
- Review your notes periodically

---

## Troubleshooting

### "Repository not registered"

```
⚠️  Repository Not Registered

Run: /register-oss <url>
```

**Solution**: Register the repository first with `/register-oss`.

### "Notion not configured"

```
❌ Notion not configured

Run: /setup-notion
```

**Solution**:
1. Run `/setup-notion` command
2. Or manually edit `config/notion_config.json`

### "Commit not found"

```
❌ Commit not found: abc1234
```

**Solution**:
- Verify commit hash is correct
- Use full hash or at least 7 characters
- Check if commit exists in repository

### "Rate limit exceeded"

```
⚠️  GitHub API rate limit

Try again in: 5 minutes
```

**Solution**:
- Wait for rate limit reset
- Set `GITHUB_TOKEN` environment variable for higher limits

---

## What's Next?

### Explore More Commits
- Analyze commits from different contributors
- Compare different approaches to similar problems
- Build your understanding incrementally

### Analyze PRs
- Study complete features through PR analysis
- Understand the review process
- Learn from discussions

### Build Your Knowledge Base
- Organize commits by topic in Notion
- Add tags and relations
- Create summary pages

### Contribute Back
- Use insights to make your first contribution
- Write better commit messages
- Share your learning with others

---

## Need Help?

- **Documentation**: See README.md for full details
- **Commands**: All commands have detailed .md files in `commands/`
- **Issues**: Report problems at https://github.com/Kuroakira/deep-code-reader/issues

---

**Happy Learning! 🚀**

*Remember: Understanding WHY is more important than knowing WHAT.*
