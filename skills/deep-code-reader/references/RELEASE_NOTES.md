# Code Reading Methodology

## Overview

This guide provides proven strategies for understanding large, unfamiliar codebases. Use these approaches when analyzing OSS projects or joining new teams.

## Reading Strategies

### 1. Top-Down Approach (Architecture First)

Start with the big picture before diving into details.

**Steps:**
1. Read project README and documentation
2. Identify entry points (main.py, index.js, etc.)
3. Map out major components and their relationships
4. Understand data flow between components
5. Dive into specific modules

**Best for:** New projects, understanding overall design

### 2. Bottom-Up Approach (Code First)

Start with concrete code and build understanding incrementally.

**Steps:**
1. Pick an interesting function or class
2. Understand its implementation
3. Trace its callers and dependencies
4. Expand to related components
5. Build mental model of the system

**Best for:** Bug fixes, specific feature understanding

### 3. Use Case Driven (Feature Tracing)

Follow a specific user action through the codebase.

**Steps:**
1. Identify a user action (e.g., "user logs in")
2. Find the entry point (API endpoint, UI handler)
3. Trace execution flow step by step
4. Document the path taken
5. Identify key decision points

**Best for:** Understanding business logic, authentication flows

### 4. Data Flow Analysis

Follow data as it moves through the system.

**Steps:**
1. Identify data sources (DB, API, user input)
2. Track transformations and validations
3. Map storage and retrieval patterns
4. Identify data consumers
5. Document the pipeline

**Best for:** ETL systems, data processing pipelines

## Reading Techniques

### Progressive Disclosure

Read code in layers of increasing detail:
1. **Skim**: File/folder structure, naming patterns
2. **Scan**: Function signatures, class interfaces
3. **Read**: Implementation details, algorithms
4. **Analyze**: Edge cases, performance, security

### Pattern Recognition

Look for common patterns:
- **Design patterns**: Singleton, Factory, Observer, etc.
- **Architectural patterns**: MVC, Clean Architecture, Hexagonal
- **Code patterns**: Error handling, logging, validation
- **Domain patterns**: Business logic specific to the domain

### Annotation Strategy

Mark up code as you read:
- ✅ Understood
- ❓ Questions/unclear
- ⚠️ Potential issues
- 🔗 Dependencies
- 💡 Insights

## Understanding Complex Code

### Dealing with Large Functions

1. Extract the function signature
2. Identify input/output
3. Break into logical sections
4. Understand each section separately
5. Combine understanding

### Untangling Dependencies

1. List all imports
2. Categorize: external vs internal
3. Identify core dependencies
4. Map dependency graph
5. Look for circular dependencies

### Reverse Engineering Tests

1. Read test cases first
2. Understand expected behavior
3. Map tests to implementation
4. Identify uncovered cases

## OSS-Specific Strategies

### Quick Project Assessment

Before deep diving, assess:
- **Activity**: Recent commits, open issues
- **Community**: Contributors, maintainers
- **Quality**: Test coverage, CI/CD, documentation
- **Architecture**: Tech stack, design docs

### Using Project Resources

1. **Documentation**: Read docs/, wiki, comments
2. **Issues**: Search for related discussions
3. **PRs**: Read recent changes and reviews
4. **Discussions**: Community forums, Discord, Slack
5. **History**: Use git blame, git log

### Contributing Context

When planning contributions:
1. Understand contribution guidelines
2. Read CONTRIBUTING.md
3. Check issue labels (good-first-issue, help-wanted)
4. Review recent PR patterns
5. Engage with maintainers

## PR Understanding Framework

### Context Gathering

**Before reading code:**
1. Read PR description and linked issues
2. Review discussion threads
3. Check review comments
4. Understand the problem being solved

**While reading changes:**
1. Compare with base branch
2. Identify affected modules
3. Check test changes
4. Look for breaking changes

### Change Analysis

**Types of changes to identify:**
- Feature additions
- Bug fixes
- Refactoring
- Performance improvements
- Security patches
- Breaking changes

**Questions to ask:**
- Why was this change needed?
- What alternatives were considered?
- What are the trade-offs?
- How does this affect existing code?
- Are there edge cases?

## Tools and Techniques

### Code Navigation

- **IDE features**: Go to definition, find usages
- **grep/ripgrep**: Search across files
- **ctags**: Generate symbol index
- **LSP**: Language Server Protocol tools

### Visualization

- **Call graphs**: Function call relationships
- **Dependency graphs**: Module dependencies
- **Sequence diagrams**: Execution flow
- **ER diagrams**: Data relationships

### Documentation

- **Personal notes**: Wiki, markdown files
- **Diagrams**: Architecture, flow, sequence
- **Code annotations**: Comments, TODOs
- **Knowledge base**: Confluence, Notion

## Common Pitfalls

### What to Avoid

1. **Reading linearly**: Don't read every line sequentially
2. **Perfectionism**: Don't try to understand everything at once
3. **Isolation**: Don't read code without context
4. **Assumptions**: Don't assume patterns without verification
5. **Overwhelm**: Don't try to grasp the entire codebase immediately

### When Stuck

1. Take a break
2. Switch reading strategies
3. Ask questions (issues, discussions)
4. Read related documentation
5. Look for similar patterns elsewhere
6. Simplify and focus on one aspect

## Effective Note-Taking

### What to Document

- **Architecture**: High-level components
- **Patterns**: Recurring designs
- **Conventions**: Naming, structure
- **Dependencies**: Key relationships
- **Gotchas**: Tricky parts, edge cases
- **Questions**: Unclear aspects

### Documentation Format

```markdown
# [Project Name] Code Reading Notes

## Architecture Overview
- Component A: Handles X
- Component B: Handles Y

## Key Flows
### Authentication Flow
1. User submits credentials
2. System validates...

## Patterns Observed
- Repository pattern for data access
- Factory pattern for object creation

## Questions
- [ ] Why is X implemented this way?
- [ ] How does Y handle error cases?

## Insights
- System uses event-driven architecture
- Heavy use of caching for performance
```

## Progressive Understanding Checklist

Use this checklist to track understanding:

**High-Level (30 minutes):**
- [ ] Project purpose and domain
- [ ] Main technologies used
- [ ] Major components identified
- [ ] Entry points located

**Medium-Level (2-3 hours):**
- [ ] Component responsibilities clear
- [ ] Data flow understood
- [ ] Key abstractions identified
- [ ] Common patterns recognized

**Deep-Level (full day):**
- [ ] Module dependencies mapped
- [ ] Critical paths traced
- [ ] Edge cases identified
- [ ] Architecture documented

## Continuous Learning

As you read:
1. Update your mental model
2. Revise initial assumptions
3. Document new discoveries
4. Ask questions early
5. Share knowledge with team
