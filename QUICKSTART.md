# Quick Start Guide - OSS Learning Platform

This guide will help you start tracking OSS commits in 5 minutes.

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
2. 📦 Install MCP servers (GitHub, Notion)
3. ⚙️  Configure Claude Code
4. 🎯 Install skills and commands

---

## Setup Notion Database (2 minutes)

### Step 1: Create Notion Integration

1. Visit https://www.notion.so/my-integrations
2. Click "New integration"
3. Name it "Deep Code Reader"
4. Copy the **Internal Integration Secret**

### Step 2: Create Database

Create a new database in Notion with these properties:

| Property Name | Type | Description |
|--------------|------|-------------|
| Title | Title | Commit title (auto) |
| Commit ID / PR No | Text | Full commit hash |
| Type | Select | Options: "Commit" |
| GitHub URL | URL | Link to commit |
| Comment | Text | Commit message |
| Memo | Text | Your notes |

### Step 3: Share Database

1. Open your database in Notion
2. Click "..." menu → "Connections"
3. Add your "Deep Code Reader" integration

### Step 4: Copy Database ID

From your database URL:
```
https://notion.so/abc123def456?v=...
              ↑↑↑↑↑↑↑↑↑↑↑↑
              This is your database ID
```

---

## First Use (1 minute)

### Step 1: Start Claude Code

```bash
claude
```

### Step 2: Register OSS Repository

```
/register-oss https://github.com/expressjs/express --database abc123def456
```

**What happens:**
- ✅ Clones repository locally
- ✅ Saves project configuration
- ✅ Shows total commit count

**Output:**
```
==================================================
OSS Repository Registered
==================================================

Project: express
GitHub: https://github.com/expressjs/express
Database: abc123def456
Local Clone: ~/.claude/deep-code-reader/repos/expressjs/express

Total Commits: 5847
Initial Commit: f7c8d10

==================================================
```

### Step 3: Add Commits

```
/add-commits 1 100
```

**What happens:**
- 📥 Fetches commits 1-100 (oldest first)
- 🔍 Checks for duplicates
- 💾 Adds to Notion database

**Output:**
```
Commit range: 1 to 100 (100 commits)
Found 0 existing commit entries
Commits to add: 100
Duplicates skipped: 0

Adding 100 commits to Notion...
  Progress: 10/100
  Progress: 20/100
  ...
  Progress: 100/100

Completed!
  Added: 100
  Errors: 0
```

### Step 4: Check Notion

Open Notion to see your commits!

---

## Daily Workflow

```bash
# Check current project
/current-oss

# Add next batch of commits
/add-commits 101 200

# List what's available
/list-commits --limit 20

# Switch projects
/register-oss https://github.com/facebook/react --database xyz789
/add-commits 1 100
```

---

## Tips

### 1. Start from the Beginning
- Use `/add-commits 1 100` to start from the first commit
- Understand how the project evolved

### 2. Work in Batches
- Add 100 commits at a time
- `/add-commits 1 100`, then `/add-commits 101 200`

### 3. Track Multiple Projects
- Each project needs its own Notion database
- Use `--database` to specify which one

### 4. Use the Memo Field
- Add your own notes in Notion
- Link related commits
- Document insights

---

## Troubleshooting

### "No project set"

```
No project set. Run: /register-oss <url> --database <id>
```

**Solution**: Register a project first.

### "Cannot access database"

```
Error: Cannot access database
```

**Solution**:
1. Verify database ID is correct
2. Check integration is connected to database
3. Open database → "..." → "Connections" → Add integration

### "Range exceeds total"

```
Warning: Requested range exceeds total commits
Adjusting range to 1 to 432
```

**Not an error**: The command auto-adjusts to available commits.

### "Duplicates skipped"

```
Duplicates skipped: 50
```

**Not an error**: Already-added commits are skipped automatically.

---

## Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/register-oss` | Register project | `/register-oss <url> --database <id>` |
| `/add-commits` | Add commits | `/add-commits 1 100` |
| `/current-oss` | Show current project | `/current-oss` |
| `/list-commits` | List commits | `/list-commits --limit 50` |

---

## Uninstallation

```bash
./uninstall.sh
```

- ✅ Removes installed components
- ✅ Preserves your Notion data
- ✅ Offers config backup restore

---

## Need Help?

- **Documentation**: See README.md
- **Commands**: Check `commands/` folder
- **Issues**: https://github.com/Kuroakira/deep-code-reader/issues

---

**Happy Learning! 🚀**

*Track commits systematically, build your knowledge base.*
