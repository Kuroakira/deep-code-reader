# Repository Structure Guide

This document explains the structure of the Deep Code Reader skill repository.

## 📁 Top-Level Structure

```
claude_skills/
├── skills/                    # All Claude Skills
│   └── deep-code-reader/     # The actual skill (this is what gets packaged)
│       ├── SKILL.md          # Main skill instructions for Claude
│       ├── scripts/          # Analysis scripts
│       ├── references/       # Reference documentation
│       └── assets/           # Templates and resources
├── skills/deep-code-reader.skill  # Packaged skill file for distribution
├── README.md                 # Main repository documentation
├── QUICKSTART.md             # Quick start guide for users
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT License
└── REPOSITORY_STRUCTURE.md  # This file
```

## 🎯 The `skills/` Directory

This directory contains all Claude Skills for the platform. Each skill is self-contained.

### `skills/deep-code-reader/`

This is the **actual skill** that gets packaged into `.skill` file. It contains:

### SKILL.md
The main instruction file that Claude reads. Contains:
- Skill metadata (name, description)
- Usage instructions
- Examples and workflows
- Best practices
- Reference to bundled resources

**When to edit:** When changing how the skill works or adding new features.

### scripts/
Standalone Python scripts that perform analysis:

- `generate_architecture_diagram.py` - Creates architecture diagrams
- `analyze_data_flow.py` - Traces data flow
- `analyze_dependencies.py` - Maps dependencies
- `fetch_pr_context.py` - Fetches GitHub PR info

**When to edit:** When improving analysis logic or adding new analysis types.

### references/
Documentation files that Claude loads when needed:

- `code-reading-methodology.md` - Code reading strategies
- `architecture-patterns.md` - Common architectural patterns

**When to edit:** When adding new patterns or methodologies.

### assets/
Resource files used in outputs:

- `architecture-template.drawio` - draw.io template

**When to edit:** When adding new templates or resources.

## 📚 Documentation Files

### README.md (Top-level)
Main documentation visible on GitHub. Contains:
- What the skill does
- Installation instructions
- Features overview
- Basic usage examples
- Links to other docs

**Audience:** Everyone visiting the GitHub repo

### QUICKSTART.md
Step-by-step guide for getting started quickly.

**Audience:** New users who want to try the skill immediately

### CONTRIBUTING.md
Guidelines for contributors.

**Audience:** Developers who want to contribute

### RELEASE_NOTES.md
Template for creating GitHub releases.

**Audience:** Maintainers creating releases

## 🔄 Workflow: From Code to Release

### 1. Development
```
Edit files in skills/deep-code-reader/
├── SKILL.md (instructions)
├── scripts/*.py (analysis logic)
├── references/*.md (documentation)
└── assets/* (templates)
```

### 2. Testing
```bash
# Test scripts individually
python skills/deep-code-reader/scripts/analyze_dependencies.py ./test-project

# Test the complete skill by uploading to Claude.ai
# or installing in Claude Code
```

### 3. Packaging
```bash
# Package the skill for distribution
cd skills
python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./

# This creates: skills/deep-code-reader.skill
```

### 4. Git Commit
```bash
git add skills/deep-code-reader/
git commit -m "Add new feature X"
git push
```

### 5. GitHub Release
1. Go to GitHub Releases
2. Create new release with tag (e.g., v1.0.0)
3. Attach `skills/deep-code-reader.skill`
4. Users download this file to use the skill

## 🎨 What Gets Published Where

### GitHub Repository (Source Code)
```
✅ skills/ directory (all skills source code)
✅ skills/deep-code-reader/ (skill source)
✅ skills/*.skill (packaged distribution files)
✅ README.md
✅ QUICKSTART.md
✅ CONTRIBUTING.md
✅ LICENSE

❌ Test outputs (*.mmd, *.json, etc.)
❌ Temporary build artifacts
```

### GitHub Releases (Distribution)
```
✅ skills/deep-code-reader.skill (packaged skill file)
✅ Release notes
✅ Source code (automatic GitHub archive)
```

### Claude.ai (User Installation)
```
Users download: skills/deep-code-reader.skill (from GitHub Release)
Users upload to: Claude.ai Settings → Skills
```

## 🔧 For Contributors

### Making Changes

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kuroakira/claude_skills.git
   cd claude_skills
   ```

2. **Make changes** in the `skills/deep-code-reader/` directory

3. **Test your changes**
   ```bash
   # Test scripts
   python skills/deep-code-reader/scripts/your_script.py

   # Package and test in Claude
   cd skills
   python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./
   # Upload skills/deep-code-reader.skill to Claude.ai
   ```

4. **Update documentation** if needed
   - Update SKILL.md for skill behavior changes
   - Update README.md for user-facing changes
   - Update references/ for new patterns or methodologies

5. **Commit and PR**
   ```bash
   git add skills/deep-code-reader/
   git commit -m "Your descriptive commit message"
   git push origin your-branch
   # Create PR on GitHub
   ```

### File Organization Principles

**Scripts (`scripts/`):**
- Self-contained, no external dependencies
- Can be run standalone
- Include argparse for CLI usage
- Well-documented with docstrings

**References (`references/`):**
- Markdown format
- Loaded by Claude as needed
- Comprehensive but not verbose
- Include examples

**Assets (`assets/`):**
- Binary or template files
- Not loaded into context
- Used in output generation

**SKILL.md:**
- Clear, concise instructions
- Concrete examples
- References to scripts/references/assets
- Keep under 500 lines

## 📦 Packaging Details

The `.skill` file is a ZIP archive containing the skill directory:

```
skills/deep-code-reader.skill (ZIP file)
└── deep-code-reader/
    ├── SKILL.md
    ├── scripts/
    ├── references/
    └── assets/
```

Users can:
- Upload to Claude.ai directly
- Extract and modify if needed
- Install in Claude Code

## 🔍 Finding Your Way Around

**Want to understand how the skill works?**
→ Read `skills/deep-code-reader/SKILL.md`

**Want to modify analysis logic?**
→ Edit `skills/deep-code-reader/scripts/*.py`

**Want to add architectural patterns?**
→ Edit `skills/deep-code-reader/references/architecture-patterns.md`

**Want to improve user docs?**
→ Edit `README.md` or `QUICKSTART.md`

**Want to contribute?**
→ Read `CONTRIBUTING.md`

## 🚀 Quick Commands

```bash
# Test a script
python skills/deep-code-reader/scripts/analyze_dependencies.py ./your-project

# Package the skill
cd skills
python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./

# Install locally for testing
cp -r skills/deep-code-reader ~/.claude/skills/

# Create a release
# 1. Tag the version
git tag v1.0.0
git push origin v1.0.0

# 2. Package the skill
cd skills
python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./

# 3. Create GitHub release and attach skills/deep-code-reader.skill
```

## ❓ FAQ

**Q: Why is there both a `skills/deep-code-reader/` directory and a `skills/deep-code-reader.skill` file?**
A: The directory is the source code (on GitHub). The `.skill` file is the packaged distribution (in Releases and repository). Think of it like source code vs compiled binary.

**Q: Do I commit the `.skill` file to Git?**
A: Yes, the `.skill` file is committed in the `skills/` directory for easy distribution. It's also attached to GitHub Releases.

**Q: Where do test outputs go?**
A: Test outputs (*.mmd, *.json, etc.) should be gitignored and not committed.

**Q: How do I update the skill description?**
A: Edit the `description` field in `skills/deep-code-reader/SKILL.md` frontmatter.

**Q: Can users modify the skill?**
A: Yes, they can extract the `.skill` file (it's a ZIP), modify contents, and repackage.

---

**Remember:** The `skills/` directory contains all your skills source code. The `.skill` files are packaged distributions. Everything else is documentation and tooling to help users and contributors.
