# Code Style and Conventions

## PRP (Product Requirement Prompt) Conventions

### PRP Structure Requirements
Every PRP must follow this structured format:
- **Goal**: Specific end state and desires
- **Why**: Business value and user impact  
- **What**: User-visible behavior and technical requirements
- **All Needed Context**: Documentation URLs, code examples, gotchas, patterns
- **Implementation Blueprint**: Pseudocode with critical details and task lists
- **Validation Loop**: Executable commands for syntax, tests, integration

### Context Guidelines
1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Information Dense**: Use keywords and patterns from the codebase
3. **No Prior Knowledge**: PRPs must be self-contained and comprehensive
4. **Reference Existing Patterns**: Always include examples from the codebase

### Template Usage
- Start with appropriate template from `PRPs/templates/`
- Follow the template structure exactly
- Use existing templates rather than creating new patterns

## Python Code Conventions

### General Style
- **Python Version**: 3.12+ required
- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Follow structured docstring format
- **Naming**: Use descriptive names, follow Python naming conventions

### Import Organization
```python
# Standard library imports first
import os
import sys
from pathlib import Path

# Third-party imports
import requests
from fastapi import FastAPI

# Local imports
from .models import AgentMessage
from .utils import helper_function
```

### Error Handling
- Don't catch all exceptions - be specific
- Use appropriate exception types
- Include meaningful error messages

## Command System Conventions

### Command Structure
- Commands are organized by function in `.claude/commands/`
- Use YAML frontmatter for metadata
- Include clear argument placeholders
- Self-documenting with examples

### Command Categories
- `prp-commands/` - PRP creation and execution workflows
- `development/` - Core development utilities
- `code-quality/` - Review and refactoring commands
- `rapid-development/` - Parallel PRP creation tools
- `git-operations/` - Git workflows
- `typescript/` - TypeScript-specific commands

## File Organization

### Project Structure
```
agent-factory/
├── .claude/commands/      # Claude Code commands
├── PRPs/
│   ├── templates/        # PRP templates
│   ├── scripts/         # Execution scripts
│   ├── ai_docs/         # AI documentation
│   └── *.md             # Active PRPs
├── claude_md_files/     # Framework examples
└── pyproject.toml       # Project config
```

### Naming Conventions
- **Files**: Use kebab-case for PRPs, snake_case for Python
- **Directories**: Use kebab-case for Claude commands, snake_case for Python packages
- **Variables**: snake_case in Python
- **Classes**: PascalCase in Python
- **Constants**: UPPER_SNAKE_CASE

## Anti-Patterns to Avoid

### PRP Anti-Patterns
- ❌ Don't create minimal context prompts
- ❌ Don't skip validation steps
- ❌ Don't ignore the structured PRP format
- ❌ Don't create new patterns when existing templates work

### Code Anti-Patterns
- ❌ Don't hardcode values that should be config
- ❌ Don't catch all exceptions - be specific
- ❌ Don't skip type hints
- ❌ Don't ignore existing patterns and conventions