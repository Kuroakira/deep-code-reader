# Contributing to Deep Code Reader

Thank you for your interest in contributing to Deep Code Reader! This document provides guidelines for contributing to this Claude Skill.

## 🎯 What We're Looking For

We welcome contributions that:

- Add support for additional programming languages
- Improve analysis accuracy and performance
- Enhance diagram generation capabilities
- Add new architectural pattern detection
- Improve documentation and examples
- Fix bugs and issues

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Familiarity with Claude Skills (see [Anthropic's documentation](https://docs.anthropic.com/en/docs/build-with-claude/skills))

### Setting Up Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/Kuroakira/deep-code-reader.git
   cd deep-code-reader
   ```

2. **Create a branch for your changes**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Edit files in `scripts/`, `references/`, `assets/`, or `SKILL.md`
   - Follow the code style guidelines below

4. **Test your changes**
   ```bash
   # Test individual scripts
   python scripts/generate_architecture_diagram.py ./test-project
   python scripts/analyze_dependencies.py ./test-project

   # Test the complete skill
   # Upload to Claude.ai or install in Claude Code and test
   ```

5. **Clean up after testing** (optional)
   ```bash
   # Uninstall test installation
   ./uninstall.sh
   ```

6. **Package and verify**
   ```bash
   # Requires the skill-creator tool from anthropics/skills
   python /path/to/skill-creator/scripts/package_skill.py . ./dist
   ```

## 📝 Code Style Guidelines

### Python Scripts

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add docstrings for classes and functions
- Keep functions focused and single-purpose
- Use descriptive variable names

**Example:**
```python
def analyze_file(self, file_path: Path) -> Dict[str, Any]:
    """
    Analyze a single Python file for imports and structure.
    
    Args:
        file_path: Path to the Python file to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    # Implementation
```

### SKILL.md

- Use clear, concise language
- Include concrete examples
- Follow the established structure
- Update the description if adding major features

### Documentation

- Keep documentation up-to-date with code changes
- Use markdown formatting consistently
- Include code examples for new features
- Add screenshots or diagrams where helpful

## 🔍 Types of Contributions

### 1. Adding Language Support

Currently supported: Python, JavaScript/TypeScript

To add a new language:

1. Add parsing logic in the relevant script (e.g., `analyze_dependencies.py`)
2. Update the language detection logic
3. Add examples to the documentation
4. Test with real-world projects in that language

**Example structure:**
```python
def analyze_rust_file(self, file_path: Path):
    """Analyze Rust file for module dependencies"""
    # Implementation
```

### 2. Improving Analysis

Enhance existing analysis capabilities:

- Better pattern detection
- More accurate dependency mapping
- Improved circular dependency detection
- Performance optimizations

### 3. Adding Features

New features should:

- Align with the skill's core purpose (code understanding)
- Be well-documented in SKILL.md
- Include usage examples
- Not add external dependencies (if possible)

### 4. Documentation

- Fix typos or unclear explanations
- Add usage examples
- Create tutorials or guides
- Improve code comments

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, test:

- [ ] Scripts run without errors on sample projects
- [ ] Generated diagrams are accurate and readable
- [ ] All output formats work (Mermaid, draw.io, JSON)
- [ ] Error handling works correctly
- [ ] Documentation is accurate and complete

### Test Projects

Test your changes against various project types:

- Small projects (< 10 files)
- Medium projects (10-100 files)
- Large projects (100+ files)
- Different architectural patterns (MVC, Clean Architecture, etc.)
- Different languages (if applicable)

## 📋 Pull Request Process

1. **Update documentation**
   - Update SKILL.md if behavior changes
   - Update README.md if installation or usage changes
   - Add/update code comments

2. **Test thoroughly**
   - Run all scripts manually
   - Test with different types of projects
   - Verify package creation works

3. **Create a clear PR description**
   ```markdown
   ## Description
   Brief description of what this PR does
   
   ## Changes
   - Added X feature
   - Fixed Y bug
   - Improved Z performance
   
   ## Testing
   - Tested on projects: A, B, C
   - Verified output formats: Mermaid, draw.io, JSON
   
   ## Screenshots (if applicable)
   [Add screenshots of new diagrams or features]
   ```

4. **Keep PRs focused**
   - One feature/fix per PR
   - Split large changes into multiple PRs
   - Avoid mixing refactoring with new features

## 🐛 Reporting Bugs

Use GitHub Issues to report bugs. Include:

1. **Description** - Clear description of the issue
2. **Steps to reproduce** - How to trigger the bug
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment** - Python version, OS, Claude version
6. **Code sample** - Minimal code to reproduce (if applicable)

**Example:**
```markdown
### Description
`analyze_dependencies.py` fails on projects with circular imports

### Steps to Reproduce
1. Run: `python scripts/analyze_dependencies.py ./test-project`
2. Project contains circular import: module_a.py imports module_b.py which imports module_a.py

### Expected Behavior
Script should detect and report circular dependency

### Actual Behavior
Script crashes with RecursionError

### Environment
- Python 3.9
- macOS 14.0
- Claude.ai (web version)
```

## 💡 Feature Requests

For new features, open a GitHub Issue with:

1. **Use case** - Why is this needed?
2. **Proposed solution** - How should it work?
3. **Examples** - What would the usage look like?
4. **Alternatives** - What other approaches were considered?

## 🔧 Development Tips

### Understanding the Skill Structure

The skill follows Claude's progressive disclosure pattern:

1. **Metadata** (name + description) - Always in context
2. **SKILL.md body** - Loaded when skill triggers
3. **Bundled resources** - Loaded as needed by Claude

### Working with Scripts

Scripts should be:
- **Self-contained** - Use only standard library
- **Well-documented** - Clear docstrings and comments
- **Robust** - Handle errors gracefully
- **Testable** - Easy to run standalone

### Packaging for Testing

```bash
# Package the skill
python /path/to/skill-creator/scripts/package_skill.py . ./dist

# Upload dist/deep-code-reader.skill to Claude.ai for testing
```

## 📚 Resources

- [Anthropic Skills Documentation](https://docs.anthropic.com/en/docs/build-with-claude/skills)
- [anthropics/skills Repository](https://github.com/anthropics/skills)
- [Skill Creator Guide](https://github.com/anthropics/skills/tree/main/skill-creator)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

- Open a GitHub Issue for questions about contributing
- Check existing issues and documentation first
- Join the Anthropic Discord for real-time discussion

---

Thank you for contributing to Deep Code Reader! 🎉
