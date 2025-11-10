# Quick Start Guide - Deep Code Reader

This guide will help you get started with the Deep Code Reader skill in 5 minutes.

## Installation

### Option 1: Claude.ai (Web/Mobile/Desktop)
1. Download `skills/deep-code-reader.skill` from releases
2. Open Claude.ai → Settings → Skills
3. Click "Upload Skill" and select the `.skill` file
4. The skill activates automatically when you work with code

### Option 2: Claude Code (Terminal)
```bash
# Clone the repository
git clone https://github.com/Kuroakira/claude_skills.git

# Copy to skills directory
mkdir -p ~/.claude/skills
cp -r claude_skills/skills/deep-code-reader ~/.claude/skills/deep-code-reader

# The skill is now available in Claude Code
```

## First Steps

### 1. Understand a Project's Architecture (2 minutes)

**Ask Claude:**
```
I want to understand the architecture of this project. 
Can you analyze it and create diagrams?
```

Then provide the path to your codebase or upload files.

**Claude will:**
- Analyze the directory structure
- Detect architectural patterns
- Generate Mermaid and draw.io diagrams
- Identify major components and layers

**You'll get:**
- `architecture.mmd` - View in GitHub or Mermaid Live Editor
- `architecture.drawio` - Edit in draw.io
- `architecture_analysis.json` - Raw data for further analysis

### 2. Trace a Specific Flow (3 minutes)

**Ask Claude:**
```
Show me how authentication works in this codebase
```

**Claude will:**
- Scan for authentication-related functions
- Trace the execution flow
- Generate a flow diagram
- Identify key decision points

**You'll get:**
- Flow diagram showing the auth process
- List of involved functions
- Entry points and exit points

### 3. Analyze a GitHub PR (2 minutes)

**Ask Claude:**
```
Help me understand this PR: https://github.com/org/repo/pull/123
```

**Claude will:**
- Fetch PR metadata and description
- Get linked issues
- Retrieve all comments and reviews
- Show commit history
- Identify changed files

**You'll get:**
- Comprehensive markdown summary
- JSON with all PR data
- Context needed for informed review

### 4. Find Dependency Issues (3 minutes)

**Ask Claude:**
```
Analyze the dependencies in this codebase and 
check for any circular dependencies
```

**Claude will:**
- Map all module dependencies
- Detect circular dependencies
- Identify highly coupled modules
- List external package usage

**You'll get:**
- Dependency diagrams
- Circular dependency warnings
- Coupling metrics

## Example Conversations

### Scenario: New OSS Contributor

**You:** I want to contribute to this project but I'm not familiar with it yet. 
Can you help me understand the codebase?

**Claude:** I'll use the Deep Code Reader skill to analyze this project. Let me:
1. Generate an architecture overview
2. Identify the main architectural patterns
3. Show you where key features are implemented

[Claude runs analysis and creates diagrams]

**Claude:** Here's what I found:
- The project uses Clean Architecture with clear layer separation
- Main components: API layer, Domain layer, Infrastructure
- Authentication is handled in the Infrastructure/Auth module
- Here's a diagram showing the architecture...

### Scenario: PR Review

**You:** Can you help me review this PR? 
https://github.com/fastapi/fastapi/pull/12345

**Claude:** I'll fetch the complete context for this PR...

[Claude gathers PR information]

**Claude:** This PR addresses issue #12340 about WebSocket support. Here's the context:
- 5 commits over 2 days
- Changes 8 files (mostly in the WebSocket module)
- 2 reviewers have approved
- One concern about backward compatibility (see comment thread)
- Here's what changed...

## Tips for Best Results

1. **Be specific about what you want to understand**
   - "Show me the authentication flow" ✅
   - "Explain this code" ❌ (too vague)

2. **Provide context**
   - Upload files or share repository links
   - Mention specific areas of interest
   - Ask follow-up questions

3. **Use the right analysis for your need**
   - Architecture diagrams → Overall understanding
   - Data flow → Specific feature understanding
   - Dependencies → Code quality/refactoring
   - PR context → Code review preparation

4. **Iterate on the analysis**
   - Start with broad analysis
   - Then drill down into specific areas
   - Ask for clarification on unclear parts

## Common Use Cases

### Use Case 1: Project Onboarding
```
I'm new to this project. Help me understand:
1. The overall architecture
2. Where the main business logic lives
3. How to add a new feature
```

### Use Case 2: Bug Investigation
```
There's a bug in the payment processing. Can you:
1. Show me the payment flow
2. Identify all functions involved
3. Help me trace where the issue might be
```

### Use Case 3: Refactoring Planning
```
I want to refactor the authentication module. Help me:
1. Understand current dependencies
2. Identify what would be affected
3. Suggest a refactoring approach
```

### Use Case 4: Documentation
```
Generate architecture documentation for this project including:
1. High-level architecture diagram
2. Component relationship diagrams
3. Data flow diagrams
```

## Next Steps

1. **Try the skill** with your own projects
2. **Read the full documentation** in SKILL.md
3. **Check the reference materials** for code reading strategies
4. **Customize the templates** for your needs

## Troubleshooting

**Problem:** Skill doesn't activate

**Solution:** Make sure you've mentioned code analysis, architecture, or uploaded code files

---

**Problem:** GitHub API rate limit exceeded

**Solution:** Set a GitHub token:
```bash
export GITHUB_TOKEN=your_token_here
```

---

**Problem:** Analysis takes too long

**Solution:** Focus on specific directories instead of the entire codebase

## Getting Help

- Check the main README.md for full documentation
- Review SKILL.md for detailed usage instructions
- See references/ for code reading methodologies
- Open an issue on GitHub for bugs or questions

## What's Next?

Once you're comfortable with the basics:
- Explore advanced usage in SKILL.md
- Customize scripts for your workflow
- Integrate with your development tools
- Share your insights with the team

**Happy Code Reading! 🚀**
