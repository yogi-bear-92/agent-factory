# Agent Factory - Developer Onboarding Guide

Welcome to the **agent-factory** project! This comprehensive guide will help you understand and contribute to this AI-driven development framework that combines the Product Requirement Prompt (PRP) methodology with Claude Code integration.

## 1. Project Overview

### Project Name and Purpose
**agent-factory** is an AI Agent Factory enhanced with the **PRP (Product Requirement Prompt) Framework**. The core concept: **"PRP = PRD + curated codebase intelligence + agent/runbook"** - designed to enable AI agents to ship production-ready code on the first pass.

### Main Functionality
- **PRP Creation and Execution**: Systematic approach to creating comprehensive prompts for AI coding agents
- **Command-Driven Development**: Pre-configured Claude Code commands for various development workflows
- **Template-Based Methodology**: Structured PRP templates with validation loops
- **AI Documentation Curation**: Curated documentation for context injection into AI workflows

### Tech Stack
- **Language**: Python 3.12+ 
- **Package Manager**: uv (modern Python package manager)
- **AI Framework**: Claude Code CLI integration
- **MCP Servers**: serena (desktop), archon (remote HTTP), browsermcp (browser automation)
- **Documentation**: Markdown-based templates and structured YAML configurations

### Architecture Pattern
**Template-Driven Framework Architecture**:
- Command layer (`.claude/commands/`)
- Template layer (`PRPs/templates/`)
- Documentation layer (`PRPs/ai_docs/`)
- Execution layer (`PRPs/scripts/`)
- Framework examples (`claude_md_files/`)

### Key Dependencies
- **uv**: Modern Python package manager and script runner
- **Claude Code**: AI-powered development CLI tool
- **MCP Protocol**: For server integrations (serena, archon, browsermcp)

## 2. Repository Structure

```
agent-factory/
├── .claude/                    # Claude Code configuration
│   ├── commands/              # 35+ pre-configured commands
│   │   ├── prp-commands/      # PRP creation and execution workflows
│   │   ├── development/       # Core development utilities
│   │   ├── code-quality/      # Review and refactoring commands  
│   │   ├── rapid-development/ # Parallel PRP creation tools
│   │   ├── git-operations/    # Conflict resolution and git operations
│   │   └── typescript/        # TypeScript-specific commands
│   └── settings.local.json    # Tool permissions and configuration
├── PRPs/                      # Product Requirement Prompt framework
│   ├── templates/             # Structured PRP templates
│   │   ├── prp_base.md        # Main implementation template
│   │   ├── prp_planning.md    # Planning document template
│   │   ├── prp_spec.md        # Specification template
│   │   └── ...                # Additional specialized templates
│   ├── scripts/               # PRP execution scripts
│   │   └── prp_runner.py      # Main PRP execution script
│   ├── ai_docs/               # Curated Claude Code documentation
│   │   ├── getting_started.md # Claude Code basics
│   │   ├── cc_commands.md     # Command system documentation
│   │   ├── subagents.md       # Multi-agent orchestration
│   │   └── ...                # Additional AI workflow docs
│   └── README.md              # PRP methodology explanation
├── claude_md_files/           # Framework-specific CLAUDE.md examples
│   ├── CLAUDE-REACT.md        # React project template
│   ├── CLAUDE-PYTHON-BASIC.md # Python project template
│   ├── CLAUDE-NEXTJS-15.md    # Next.js project template
│   └── ...                    # Additional framework templates
├── CLAUDE.md                  # Project-specific Claude Code instructions
└── pyproject.toml             # Python project configuration
```

### Directory Purposes

- **`.claude/commands/`**: Command-driven development workflows organized by function
- **`PRPs/templates/`**: Structured templates for creating comprehensive implementation prompts
- **`PRPs/ai_docs/`**: Curated documentation for AI context injection
- **`claude_md_files/`**: Framework-specific CLAUDE.md examples for different tech stacks
- **`PRPs/scripts/`**: Automation scripts for PRP execution and management

### Unique Organizational Patterns

1. **Command-Driven Architecture**: All development workflows are pre-configured as Claude Code commands
2. **Template-First Approach**: Every implementation starts with a structured template
3. **Context Injection System**: Systematic curation of documentation for AI agents
4. **Validation-First Design**: Every template includes executable validation gates

## 3. Getting Started

### Prerequisites
- **Python**: Version 3.12 or higher
- **uv**: Modern Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Claude Code**: AI development CLI (`npm install -g @anthropics/claude-code`)
- **Git**: For version control

### Environment Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd agent-factory
   ```

2. **Verify prerequisites**:
   ```bash
   python3 --version  # Should be 3.12+
   uv --version        # Should be installed
   claude --version    # Should be installed
   ```

3. **Initialize project context**:
   ```bash
   claude /prime-core
   ```

### How to Install Dependencies
This project uses minimal dependencies managed by `uv`:
```bash
# Dependencies are managed in pyproject.toml
# No installation required for basic usage
```

### Configuration Files
- **`.claude/settings.local.json`**: Claude Code tool permissions
- **`CLAUDE.md`**: Project-specific instructions for Claude Code
- **`pyproject.toml`**: Python project metadata and dependencies

### How to Run the Project Locally

1. **Prime Claude with project context**:
   ```bash
   claude /prime-core
   ```

2. **Create a PRP**:
   ```bash
   claude /prp-base-create "your feature description"
   ```

3. **Execute a PRP**:
   ```bash
   # Interactive mode (recommended)
   uv run PRPs/scripts/prp_runner.py --prp your-feature --interactive
   
   # Headless mode
   uv run PRPs/scripts/prp_runner.py --prp your-feature --output-format json
   ```

### How to Run Tests
Currently, the project is template-based and doesn't have traditional tests. Validation happens through:
- **Template validation**: Ensuring PRPs follow structured format
- **Execution validation**: Running PRP validation gates
- **Command testing**: Testing Claude Code commands work as expected

### How to Build for Production
This is a development framework, not a deployable application. "Production" means:
- Well-structured PRPs that enable successful AI implementations
- Properly configured Claude Code commands
- Curated documentation for AI context injection

## 4. Key Components

### Entry Points
- **`PRPs/scripts/prp_runner.py`**: Main script for executing PRPs with AI agents
- **`.claude/commands/`**: All development workflows accessible via `/command-name`
- **`CLAUDE.md`**: Project instructions loaded by Claude Code

### Core Business Logic
- **PRP Template System** (`PRPs/templates/`): Structured approach to AI prompt creation
- **Command Orchestration** (`.claude/commands/`): Pre-configured development workflows
- **Context Curation** (`PRPs/ai_docs/`): Documentation system for AI agents

### Configuration Management
- **`.claude/settings.local.json`**: Tool permissions and Claude Code configuration
- **`CLAUDE.md`**: Project-specific instructions and conventions
- **`pyproject.toml`**: Python project metadata

### Key Files Explained

1. **`PRPs/scripts/prp_runner.py`**: 
   - Executes PRPs with Claude Code
   - Supports interactive and headless modes
   - Handles streaming JSON output for monitoring

2. **`PRPs/templates/prp_base.md`**: 
   - Comprehensive template for implementation PRPs
   - Includes validation gates and implementation blueprints
   - Designed for "one-pass implementation success"

3. **`.claude/commands/prp-commands/prp-base-create.md`**: 
   - Command for creating comprehensive PRPs
   - Includes research process and quality gates
   - Uses multi-agent approach for thorough context gathering

## 5. Development Workflow

### Git Branch Naming Conventions
This project follows standard conventions:
- `feature/feature-name` - New features
- `fix/issue-description` - Bug fixes  
- `docs/documentation-update` - Documentation changes
- `refactor/component-name` - Code refactoring

### How to Create a New Feature

1. **Use PRP methodology**:
   ```bash
   claude /prp-base-create "feature description"
   ```

2. **Execute the PRP**:
   ```bash
   uv run PRPs/scripts/prp_runner.py --prp feature-name --interactive
   ```

3. **Review and commit changes**:
   ```bash
   claude /review-staged-unstaged
   claude /smart-commit "feature description"
   ```

### Testing Requirements
- **Template Validation**: PRPs must follow structured format
- **Execution Testing**: Validation gates must pass
- **Documentation**: Changes must be documented

### Code Style/Linting Rules
- **Python**: Standard Python conventions (would use ruff/black if this were a Python codebase)
- **Markdown**: Consistent formatting for templates and documentation
- **YAML**: Structured format for context sections in PRPs

### PR Process and Review Guidelines
1. **Create comprehensive PRP** for the feature
2. **Execute PRP** and ensure validation gates pass
3. **Review changes** using `/review-staged-unstaged` command
4. **Create PR** using `/create-pr` command
5. **Ensure documentation** is updated

### Claude Code Command System
Access commands via `/` prefix:
- `/prp-base-create` - Create comprehensive PRPs
- `/prp-base-execute` - Execute PRPs against codebase  
- `/prime-core` - Initialize project context
- `/review-staged-unstaged` - Review changes using PRP methodology
- `/debug` - Debugging workflow
- `/smart-commit` - Intelligent git commits

## 6. Architecture Decisions

### Design Patterns
1. **Template Method Pattern**: Structured PRP templates with defined sections
2. **Command Pattern**: All workflows are encapsulated as executable commands
3. **Strategy Pattern**: Different PRP templates for different implementation types
4. **Observer Pattern**: Validation gates provide feedback loops

### State Management Approach
- **Stateless Templates**: PRPs are stateless, reusable templates
- **Context Injection**: State comes from curated documentation and codebase analysis
- **Execution Tracking**: PRP runner provides execution state and progress

### Error Handling Strategy
- **Validation Gates**: Multiple levels of validation (syntax, tests, integration)
- **Progressive Success**: Start simple, validate, then enhance
- **Failure Recovery**: Clear error messages and recovery paths

### Performance Optimizations
- **Multi-Agent Orchestration**: Parallel research and implementation
- **Context Caching**: Reusable documentation and patterns
- **Template Reuse**: Structured templates prevent reinventing patterns

### Security Measures
- **Sandboxed Execution**: Claude Code provides safe execution environment
- **Permission System**: Explicit tool permissions in settings
- **Code Review**: Built-in review commands for security validation

## 7. Common Tasks

### How to Add a New PRP Template
1. **Study existing templates** in `PRPs/templates/`
2. **Follow the template structure** from `prp_base.md`
3. **Include validation gates** appropriate for the use case
4. **Test with real implementation** to ensure effectiveness

### How to Add a New Claude Command
1. **Create command file** in appropriate `.claude/commands/` subdirectory
2. **Follow existing command format** with YAML frontmatter
3. **Include clear instructions** and argument placeholders
4. **Test command execution** before committing

### How to Update Documentation
1. **For AI documentation**: Add/update files in `PRPs/ai_docs/`
2. **For templates**: Update relevant template in `PRPs/templates/`
3. **For project instructions**: Update `CLAUDE.md`
4. **For framework examples**: Update relevant file in `claude_md_files/`

### How to Debug PRP Issues
1. **Use debug command**: `claude /debug`
2. **Check validation gates**: Ensure all validation commands work
3. **Verify context completeness**: Apply "No Prior Knowledge" test
4. **Test incremental execution**: Break down into smaller steps

### How to Update the Framework
1. **Update templates** based on learnings from implementations
2. **Add new commands** for discovered workflows
3. **Curate new documentation** for AI context injection
4. **Test with real projects** to validate improvements

## 8. Potential Gotchas

### Non-Obvious Configurations
- **MCP Server Configuration**: Multiple MCP servers (serena, archon, browsermcp) need proper setup
- **Tool Permissions**: `.claude/settings.local.json` controls which tools are available
- **Template Dependencies**: Some templates reference specific documentation that must exist

### Required Environment Variables
- **Claude Code API**: May require authentication setup
- **MCP Servers**: Remote servers may need configuration
- **Project Context**: CLAUDE.md instructions are critical for proper operation

### External Service Dependencies
- **Claude Code Service**: Requires internet connection and valid API access
- **MCP Servers**: archon runs on localhost:8051, requires server availability
- **Documentation URLs**: Template references to external documentation must be accessible

### Known Issues or Workarounds
- **Context Window Limits**: Large PRPs may hit context limits; use focused templates
- **Command Execution**: Some commands require specific project structure
- **Template Evolution**: Older PRPs may not follow current template standards

### Performance Bottlenecks
- **Research Phase**: Comprehensive PRP creation can be time-intensive
- **Multi-Agent Coordination**: Parallel agent execution requires coordination
- **Context Loading**: Large documentation sets may slow initial loading

### Areas of Technical Debt
- **Template Versioning**: No formal versioning system for template evolution
- **Command Discovery**: Command system could benefit from better discovery mechanism
- **Validation Standardization**: Validation gates vary across templates

## 9. Documentation and Resources

### Existing Documentation Structure
- **`PRPs/README.md`**: Core PRP methodology explanation
- **`PRPs/ai_docs/`**: Curated Claude Code documentation for AI agents
- **`.claude/commands/`**: Self-documenting command system
- **`CLAUDE.md`**: Project-specific instructions for Claude Code

### Key Documentation Files
- **`PRPs/ai_docs/getting_started.md`**: Claude Code basics
- **`PRPs/ai_docs/cc_commands.md`**: Command system documentation  
- **`PRPs/ai_docs/subagents.md`**: Multi-agent orchestration patterns
- **`PRPs/templates/prp_base.md`**: Comprehensive implementation template

### Framework Examples
The `claude_md_files/` directory contains CLAUDE.md examples for various frameworks:
- React (`CLAUDE-REACT.md`)
- Python (`CLAUDE-PYTHON-BASIC.md`)
- Next.js (`CLAUDE-NEXTJS-15.md`)
- Node.js (`CLAUDE-NODE.md`)
- And more...

### API Documentation
This is a framework project, not an API. "Documentation" refers to:
- **Template Documentation**: Structured PRP formats
- **Command Documentation**: Claude Code command specifications
- **Context Documentation**: AI-consumable documentation patterns

## 10. Next Steps - Onboarding Checklist

### Set Up Development Environment
- [ ] Install Python 3.12+
- [ ] Install uv package manager
- [ ] Install Claude Code CLI
- [ ] Clone the repository
- [ ] Verify all prerequisites work

### Run the Project Successfully  
- [ ] Execute `claude /prime-core` to initialize context
- [ ] Browse available commands: `ls .claude/commands/`
- [ ] Read `PRPs/README.md` to understand PRP methodology
- [ ] Examine template structure in `PRPs/templates/prp_base.md`

### Make a Small Test Change
- [ ] Create a simple PRP: `claude /prp-base-create "simple test feature"`
- [ ] Review the generated PRP structure
- [ ] Make a small modification to a template
- [ ] Test command execution: `claude /prime-core`

### Run the Test Suite
- [ ] Validate templates are properly formatted
- [ ] Test PRP runner: `uv run PRPs/scripts/prp_runner.py --help`
- [ ] Verify Claude Code commands work: `claude /review-staged-unstaged`
- [ ] Check MCP server connectivity (if configured)

### Understand the Main User Flow
- [ ] **PRP Creation**: Use `/prp-base-create` to create comprehensive implementation prompts
- [ ] **PRP Execution**: Use `prp_runner.py` to execute PRPs with AI agents
- [ ] **Review and Refinement**: Use `/review-staged-unstaged` to validate implementations
- [ ] **Template Evolution**: Update templates based on implementation learnings

### Identify Area to Start Contributing
Choose based on your interests and expertise:

- **Template Development**: Improve existing templates or create new ones
- **Command Enhancement**: Add new Claude Code commands for discovered workflows
- **Documentation Curation**: Add AI-consumable documentation to `PRPs/ai_docs/`
- **Framework Examples**: Create CLAUDE.md examples for new frameworks
- **Validation Systems**: Improve validation gates and quality assurance
- **Multi-Agent Orchestration**: Enhance parallel execution and coordination

### Recommended First Contributions
1. **Study the PRP methodology** by reading `PRPs/README.md`
2. **Create a test PRP** for a simple feature you understand
3. **Execute the PRP** and observe the validation process
4. **Identify improvement opportunities** in templates or commands
5. **Propose enhancements** based on your experience

## Getting Help

- **Project Documentation**: Start with `PRPs/README.md` and `CLAUDE.md`
- **Command Reference**: Browse `.claude/commands/` for available workflows
- **Template Guide**: Study `PRPs/templates/prp_base.md` for implementation patterns
- **Claude Code Help**: Use `claude /help` for CLI assistance

Welcome to the agent-factory! This framework is designed to enable AI agents to ship production-ready code through comprehensive context and validation. Your contributions will help make AI-driven development more reliable and effective.