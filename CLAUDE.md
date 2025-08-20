# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Nature

This is the **agent-factory** project, now enhanced with the **PRP (Product Requirement Prompt) Framework**. The core concept: **"PRP = PRD + curated codebase intelligence + agent/runbook"** - designed to enable AI agents to ship production-ready code on the first pass.

## Core Architecture

### Command-Driven System

- **pre-configured Claude Code commands** in `.claude/commands/`
- Commands organized by function:
  - `prp-commands/` - PRP creation and execution workflows
  - `development/` - Core development utilities (prime-core, onboarding, debug)
  - `code-quality/` - Review and refactoring commands
  - `rapid-development/` - Parallel PRP creation and experimental tools
  - `git-operations/` - Conflict resolution and smart git operations
  - `typescript/` - TypeScript-specific commands

### Template-Based Methodology

- **PRP Templates** in `PRPs/templates/` follow structured format with validation loops
- **Context-Rich Approach**: Every PRP must include comprehensive documentation, examples, and gotchas
- **Validation-First Design**: Each PRP contains executable validation gates (syntax, tests, integration)

### AI Documentation Curation

- `PRPs/ai_docs/` contains curated Claude Code documentation for context injection
- `claude_md_files/` provides framework-specific CLAUDE.md examples

### MCP Integration

The project includes configured MCP servers:
- **serena** - Desktop app context and project management
- **archon** - Remote HTTP server for advanced AI workflows
- **browsermcp** - Browser automation capabilities

## Development Commands

### PRP Execution

```bash
# Interactive mode (recommended for development)
uv run PRPs/scripts/prp_runner.py --prp [prp-name] --interactive

# Headless mode (for CI/CD)
uv run PRPs/scripts/prp_runner.py --prp [prp-name] --output-format json

# Streaming JSON (for real-time monitoring)
uv run PRPs/scripts/prp_runner.py --prp [prp-name] --output-format stream-json
```

### Key Claude Commands

- `/prp-base-create` - Generate comprehensive PRPs with research
- `/prp-base-execute` - Execute PRPs against codebase
- `/prp-planning-create` - Create planning documents with diagrams
- `/prime-core` - Prime Claude with project context
- `/review-staged-unstaged` - Review git changes using PRP methodology
- `/debug` - Debugging workflow
- `/onboarding` - Onboarding process for new team members

## Critical Success Patterns

### The PRP Methodology

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Progressive Success**: Start simple, validate, then enhance

### PRP Structure Requirements

- **Goal**: Specific end state and desires
- **Why**: Business value and user impact
- **What**: User-visible behavior and technical requirements
- **All Needed Context**: Documentation URLs, code examples, gotchas, patterns
- **Implementation Blueprint**: Pseudocode with critical details and task lists
- **Validation Loop**: Executable commands for syntax, tests, integration

### Validation Gates (Must be Executable)

```bash
# Level 1: Syntax & Style
# Add your linting/formatting commands here
# Example: ruff check --fix && mypy .

# Level 2: Unit Tests  
# Add your test commands here
# Example: uv run pytest tests/ -v

# Level 3: Integration
# Add your integration test commands here

# Level 4: Deployment
# Add deployment validation commands here
```

## Anti-Patterns to Avoid

- ⚠️ Don't create minimal context prompts - context is everything - the PRP must be comprehensive and self-contained, reference relevant documentation and examples.
- ⚠️ Don't skip validation steps - they're critical for one-pass success - The better The AI is at running the validation loop, the more likely it is to succeed.
- ⚠️ Don't ignore the structured PRP format - it's battle-tested
- ⚠️ Don't create new patterns when existing templates work
- ⚠️ Don't hardcode values that should be config
- ⚠️ Don't catch all exceptions - be specific

## Working with This Framework

### When Creating new PRPs

1. **Context Process**: New PRPs must consist of context sections, Context is King!
2. **Use Templates**: Start with appropriate template from `PRPs/templates/`
3. **Research Phase**: Include all relevant documentation and examples
4. **Validation Planning**: Define executable validation steps

### When Executing PRPs

1. **Load PRP**: Read and understand all context and requirements
2. **ULTRATHINK**: Create comprehensive plan, break down into todos, use subagents, batch tools etc check `PRPs/ai_docs/`
3. **Execute**: Implement following the blueprint
4. **Validate**: Run each validation command, fix failures
5. **Complete**: Ensure all checklist items done

### Command Usage

- Read the `.claude/commands` directory
- Access via `/` prefix in Claude Code
- Commands are self-documenting with argument placeholders
- Use parallel creation commands for rapid development
- Leverage existing review and refactoring commands

## Project Structure Understanding

```
agent-factory/
├── .claude/
│   ├── commands/           # 28+ Claude Code commands
│   └── settings.json      # Tool permissions
├── PRPs/
│   ├── templates/         # PRP templates with validation
│   ├── scripts/          # PRP runner and utilities
│   ├── ai_docs/          # Curated Claude Code documentation
│   ├── README.md         # PRP methodology guide
│   └── *.md              # Active and example PRPs
├── claude_md_files/      # Framework-specific CLAUDE.md examples
├── CLAUDE.md             # This file - project-specific guidelines
└── pyproject.toml        # Python package configuration
```

## MCP Servers Available

- **serena**: Desktop app context with project management
- **archon**: Remote HTTP server (localhost:8051) for advanced AI workflows  
- **browsermcp**: Browser automation and interaction capabilities

## Getting Started

1. Use `/prime-core` to initialize project context
2. Create PRPs with `/prp-base-create [feature description]`
3. Execute PRPs with `/prp-base-execute PRPs/[prp-file].md`
4. Review changes with `/review-staged-unstaged`

Remember: This framework is about **one-pass implementation success through comprehensive context and validation**. Every PRP should contain the exact context for an AI agent to successfully implement working code in a single pass.