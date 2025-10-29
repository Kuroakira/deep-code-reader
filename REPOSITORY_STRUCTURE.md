# Repository Structure Guide

This document explains the structure of the Deep Code Reader skill repository.

## 📁 Top-Level Structure

```
deep-code-reader-repo/
├── deep-code-reader/          # The actual skill (this is what gets packaged)
│   ├── SKILL.md              # Main skill instructions for Claude
│   ├── scripts/              # Analysis scripts
│   ├── references/           # Reference documentation
│   ├── assets/               # Templates and resources
│   └── .gitignore           # Git ignore patterns
├── README.md                 # Main repository documentation
├── QUICKSTART.md             # Quick start guide for users
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT License
└── RELEASE_NOTES.md         # Template for GitHub releases
```

## 🎯 The `deep-code-reader/` Directory

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
Edit files in deep-code-reader/
├── SKILL.md (instructions)
├── scripts/*.py (analysis logic)
├── references/*.md (documentation)
└── assets/* (templates)
```

### 2. Testing
```bash
# Test scripts individually
python deep-code-reader/scripts/analyze_dependencies.py ./test-project

# Test the complete skill by uploading to Claude.ai
# or installing in Claude Code
```

### 3. Packaging
```bash
# Package the skill for distribution
python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./dist

# This creates: dist/deep-code-reader.skill
```

### 4. Git Commit
```bash
git add deep-code-reader/
git commit -m "Add new feature X"
git push
```

### 5. GitHub Release
1. Go to GitHub Releases
2. Create new release with tag (e.g., v1.0.0)
3. Attach `dist/deep-code-reader.skill`
4. Users download this file to use the skill

## 🎨 What Gets Published Where

### GitHub Repository (Source Code)
```
✅ deep-code-reader/ directory (full source)
✅ README.md
✅ QUICKSTART.md
✅ CONTRIBUTING.md
✅ LICENSE
✅ RELEASE_NOTES.md (template)

❌ dist/ (build artifacts - ignored)
❌ *.skill files (distribution files - not source)
❌ Test outputs (*.mmd, *.json, etc.)
```

### GitHub Releases (Distribution)
```
✅ deep-code-reader.skill (packaged skill file)
✅ Release notes (from RELEASE_NOTES.md template)
✅ Source code (automatic GitHub archive)
```

### Claude.ai (User Installation)
```
Users download: deep-code-reader.skill (from GitHub Release)
Users upload to: Claude.ai Settings → Skills
```

## 🔧 For Contributors

### Making Changes

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/deep-code-reader.git
   cd deep-code-reader
   ```

2. **Make changes** in the `deep-code-reader/` directory

3. **Test your changes**
   ```bash
   # Test scripts
   python deep-code-reader/scripts/your_script.py
   
   # Package and test in Claude
   python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./dist
   # Upload dist/deep-code-reader.skill to Claude.ai
   ```

4. **Update documentation** if needed
   - Update SKILL.md for skill behavior changes
   - Update README.md for user-facing changes
   - Update references/ for new patterns or methodologies

5. **Commit and PR**
   ```bash
   git add deep-code-reader/
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
deep-code-reader.skill (ZIP file)
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
→ Read `deep-code-reader/SKILL.md`

**Want to modify analysis logic?**
→ Edit `deep-code-reader/scripts/*.py`

**Want to add architectural patterns?**
→ Edit `deep-code-reader/references/architecture-patterns.md`

**Want to improve user docs?**
→ Edit `README.md` or `QUICKSTART.md`

**Want to contribute?**
→ Read `CONTRIBUTING.md`

**Want to create a release?**
→ Follow `RELEASE_NOTES.md`

## 🚀 Quick Commands

```bash
# Test a script
python deep-code-reader/scripts/analyze_dependencies.py ./your-project

# Package the skill
python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./dist

# Install locally for testing
cp -r deep-code-reader ~/.claude/skills/

# Create a release
# 1. Tag the version
git tag v1.0.0
git push origin v1.0.0

# 2. Package the skill
python /path/to/skill-creator/scripts/package_skill.py deep-code-reader ./dist

# 3. Create GitHub release and attach dist/deep-code-reader.skill
```

## ❓ FAQ

**Q: Why is there both a `deep-code-reader/` directory and a `deep-code-reader.skill` file?**
A: The directory is the source code (on GitHub). The `.skill` file is the packaged distribution (in Releases). Think of it like source code vs compiled binary.

**Q: Do I commit the `.skill` file to Git?**
A: No, add `*.skill` to `.gitignore`. Only attach it to GitHub Releases.

**Q: Where do test outputs go?**
A: Test outputs (*.mmd, *.json, etc.) should be gitignored and not committed.

**Q: How do I update the skill description?**
A: Edit the `description` field in `deep-code-reader/SKILL.md` frontmatter.

**Q: Can users modify the skill?**
A: Yes, they can extract the `.skill` file (it's a ZIP), modify contents, and repackage.

---

**Remember:** The `deep-code-reader/` directory is your source code. Everything else is documentation and tooling to help users and contributors.
