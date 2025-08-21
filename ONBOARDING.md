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
- **Multi-Agent System**: Specialized agents (Planner, Coder, Tester, Reviewer, DevOps, Coordinator) working together
- **Knowledge Management**: Vector database with RAG for context-aware decisions
- **Agent Coordination**: Redis pub/sub messaging for seamless communication

### Tech Stack
- **Language**: Python 3.12+ 
- **Package Manager**: uv (modern Python package manager)
- **AI Framework**: Claude Code CLI integration + LangChain + LangGraph
- **MCP Servers**: serena (desktop), archon (remote HTTP), browsermcp (browser automation)
- **Vector Database**: Chroma for knowledge storage and retrieval
- **Message Bus**: Redis for agent communication
- **API Framework**: FastAPI for REST and streaming interfaces
- **Documentation**: Markdown-based templates and structured YAML configurations

### Architecture Pattern
**Multi-Agent System with Template-Driven Framework Architecture**:
- **Agent Layer**: Specialized agents for different development roles
- **Command Layer** (`.claude/commands/`): Pre-configured development workflows
- **Template Layer** (`PRPs/templates/`): Structured PRP templates with validation
- **Documentation Layer** (`PRPs/ai_docs/`): Curated documentation for AI context injection
- **Execution Layer** (`PRPs/scripts/`): PRP execution and agent coordination
- **Framework Examples** (`claude_md_files/`): Framework-specific CLAUDE.md examples

### Key Dependencies
- **uv**: Modern Python package manager and script runner
- **Claude Code**: AI-powered development CLI tool
- **MCP Protocol**: For server integrations (serena, archon, browsermcp)
- **LangChain**: Multi-agent orchestration and LLM integration
- **Chroma**: Vector database for knowledge storage
- **Redis**: Message bus for agent communication
- **FastAPI**: Web framework for API endpoints

## 2. Repository Structure

> **📖 Complete Project Structure**: See [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) for detailed repository structure and directory explanations.

## 3. Getting Started

### Prerequisites

> **📖 Detailed Prerequisites**: See [Shared Components - Prerequisites](docs/SHARED_COMPONENTS.md#prerequisites) for complete installation requirements and verification steps.

### Environment Setup

> **📖 Standard Setup Process**: Follow the [standard installation steps](docs/SHARED_COMPONENTS.md#installation-steps) for the complete setup process.

### How to Install Dependencies
This project uses `uv` for dependency management:
```bash
# Install all dependencies
uv sync

# Install development dependencies
uv sync --extra dev

# Update dependencies
uv sync --upgrade
```

### Configuration Files
- **`.env`**: Environment variables (copy from `.env.example`)
- **`.claude/settings.local.json`**: Claude Code tool permissions
- **`CLAUDE.md`**: Project-specific instructions for Claude Code
- **`pyproject.toml`**: Python project metadata and dependencies
- **`docker-compose.dev.yml`**: Development service configuration

### How to Run the Project Locally

1. **Start development services**:
   ```bash
   ./scripts/dev-start.sh
   ```

2. **Verify services are running**:
   ```bash
   curl -f http://localhost:8000/health
   ```

3. **Prime Claude with project context**:
   ```bash
   claude /prime-core
   ```

4. **Create a PRP**:
   ```bash
   claude /prp-base-create "your feature description"
   ```

5. **Execute a PRP**:
   ```bash
   # Interactive mode (recommended)
   uv run PRPs/scripts/prp_runner.py --prp your-feature --interactive
   
   # Headless mode
   uv run PRPs/scripts/prp_runner.py --prp your-feature --output-format json
   ```

### How to Run Tests
```bash
# Run all tests
uv run pytest -v

# Run specific test file
uv run pytest tests/test_models.py -v

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run tests with pattern matching
uv run pytest -k "test_name" --maxfail=1
```

### How to Build for Production
```bash
# Build Docker images
docker-compose build

# Start production services
docker-compose up -d

# Check service health
docker-compose ps
```

## 4. Key Components

### Entry Points
- **`PRPs/scripts/prp_runner.py`**: Main script for executing PRPs with AI agents
- **`.claude/commands/`**: All development workflows accessible via `/command-name`
- **`CLAUDE.md`**: Project instructions loaded by Claude Code
- **`src/agent_factory/cli.py`**: Command-line interface for the framework

### Core Business Logic
- **PRP Template System** (`PRPs/templates/`): Structured approach to AI prompt creation
- **Command Orchestration** (`.claude/commands/`): Pre-configured development workflows
- **Context Curation** (`PRPs/ai_docs/`): Documentation system for AI agents
- **Multi-Agent System** (`src/agents/`): Specialized agents for different development roles
- **Knowledge Management** (`src/knowledge/`): Vector database and RAG implementation

### Configuration Management
- **`src/config/settings.py`**: Centralized configuration with Pydantic models
- **`.claude/settings.local.json`**: Tool permissions and Claude Code configuration
- **`CLAUDE.md`**: Project-specific instructions and conventions
- **`pyproject.toml`**: Python project metadata and dependencies

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

4. **`src/models.py`**: 
   - Core data structures for the agent framework
   - Defines message types, task specifications, and execution results
   - Uses Pydantic for validation and serialization

5. **`src/agents/base/agent_interface.py`**: 
   - Base class for all agents in the system
   - Defines common interface and behavior patterns
   - Ensures consistency across different agent types

## 5. Development Workflow

### Development Workflow

> **📖 Complete Development Workflow**: See [Shared Components - Development Workflow](docs/SHARED_COMPONENTS.md#development-workflow) for detailed information about:
> - Git branch naming conventions
> - Testing requirements  
> - Code style and linting rules
> - PR process and review guidelines
> - Claude Code command system

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

## 6. Architecture Decisions

### Design Patterns
1. **Template Method Pattern**: Structured PRP templates with defined sections
2. **Command Pattern**: All workflows are encapsulated as executable commands
3. **Strategy Pattern**: Different PRP templates for different implementation types
4. **Observer Pattern**: Validation gates provide feedback loops
5. **Factory Pattern**: Agent creation and management
6. **Repository Pattern**: Knowledge and data access abstraction

### State Management Approach
- **Stateless Templates**: PRPs are stateless, reusable templates
- **Context Injection**: State comes from curated documentation and codebase analysis
- **Execution Tracking**: PRP runner provides execution state and progress
- **Agent State**: Individual agents maintain their own state and memory

### Error Handling Strategy
- **Validation Gates**: Multiple levels of validation (syntax, tests, integration)
- **Progressive Success**: Start simple, validate, then enhance
- **Failure Recovery**: Clear error messages and recovery paths
- **Structured Results**: Use `ExecutionResult` for consistent error handling

### Performance Optimizations
- **Multi-Agent Orchestration**: Parallel research and implementation
- **Context Caching**: Reusable documentation and patterns
- **Template Reuse**: Structured templates prevent reinventing patterns
- **Async Operations**: Non-blocking I/O for better performance
- **Connection Pooling**: Efficient resource management

### Security Measures
- **Sandboxed Execution**: Claude Code provides safe execution environment
- **Permission System**: Explicit tool permissions in settings
- **Code Review**: Built-in review commands for security validation
- **Environment Variables**: Secure configuration management
- **Input Validation**: Pydantic models for data validation

## 7. Common Tasks

### How to Add a New Agent
1. **Create agent class** in `src/agents/` directory
2. **Inherit from BaseAgent** in `src/agents/base/agent_interface.py`
3. **Implement required methods**: `process_message()`, `execute_task()`
4. **Add tests** in corresponding test directory
5. **Update agent registry** if needed

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
- **Environment Variables**: Required for Redis, Chroma, and other services

### Required Environment Variables
- **Claude Code API**: May require authentication setup
- **MCP Servers**: Remote servers may need configuration
- **Project Context**: CLAUDE.md instructions are critical for proper operation
- **Service Configuration**: Redis, Chroma, and API settings

### External Service Dependencies
- **Claude Code Service**: Requires internet connection and valid API access
- **MCP Servers**: archon runs on localhost:8051, requires server availability
- **Documentation URLs**: Template references to external documentation must be accessible
- **Docker Services**: Redis, Chroma, and other services must be running

### Known Issues or Workarounds
- **Context Window Limits**: Large PRPs may hit context limits; use focused templates
- **Command Execution**: Some commands require specific project structure
- **Template Evolution**: Older PRPs may not follow current template standards
- **Service Dependencies**: Ensure all required services are running before testing

### Performance Bottlenecks
- **Research Phase**: Comprehensive PRP creation can be time-intensive
- **Multi-Agent Coordination**: Parallel agent execution requires coordination
- **Context Loading**: Large documentation sets may slow initial loading
- **Vector Database**: Chroma operations can be slow with large datasets

### Areas of Technical Debt
- **Template Versioning**: No formal versioning system for template evolution
- **Command Discovery**: Command system could benefit from better discovery mechanism
- **Validation Standardization**: Validation gates vary across templates
- **Test Coverage**: Some components lack comprehensive test coverage

## 9. Documentation and Resources

### Existing Documentation Structure
- **`PRPs/README.md`**: Core PRP methodology explanation
- **`PRPs/ai_docs/`**: Curated Claude Code documentation for AI agents
- **`.claude/commands/`**: Self-documenting command system
- **`CLAUDE.md`**: Project-specific instructions for Claude Code
- **`.cursor/rules/`**: Comprehensive coding standards and patterns

### Key Documentation Files
- **`PRPs/ai_docs/getting_started.md`**: Claude Code basics
- **`PRPs/ai_docs/cc_commands.md`**: Command system documentation  
- **`PRPs/ai_docs/subagents.md`**: Multi-agent orchestration patterns
- **`PRPs/templates/prp_base.md`**: Comprehensive implementation template
- **`.cursor/rules/python-coding-standards.mdc`**: Python coding standards
- **`.cursor/rules/agent-development-patterns.mdc`**: Agent development patterns

### Framework Examples
The `claude_md_files/` directory contains CLAUDE.md examples for various frameworks:
- React (`CLAUDE-REACT.md`)
- Python (`CLAUDE-PYTHON-BASIC.md`)
- Next.js (`CLAUDE-NEXTJS-15.md`)
- Node.js (`CLAUDE-NODE.md`)
- And more...

### API Documentation
This is a framework project with multiple components:
- **Agent API**: Agent interface and communication protocols
- **Knowledge API**: Vector database and RAG operations
- **Workflow API**: PRP execution and validation
- **Communication API**: Message bus and coordination

## 10. Next Steps - Onboarding Checklist

### Set Up Development Environment
- [ ] Install Python 3.12+
- [ ] Install uv package manager
- [ ] Install Claude Code CLI
- [ ] Install Docker
- [ ] Clone the repository
- [ ] Verify all prerequisites work

### Run the Project Successfully  
- [ ] Execute `uv sync` to install dependencies
- [ ] Copy and configure `.env` file
- [ ] Run `./scripts/dev-start.sh` to start services
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
- [ ] Run tests: `uv run pytest -v`

### Understand the Main User Flow
- [ ] **PRP Creation**: Use `/prp-base-create` to create comprehensive implementation prompts
- [ ] **PRP Execution**: Use `prp_runner.py` to execute PRPs with AI agents
- [ ] **Review and Refinement**: Use `/review-staged-unstaged` to validate implementations
- [ ] **Template Evolution**: Update templates based on implementation learnings
- [ ] **Multi-Agent Coordination**: Understand how agents work together

### Identify Area to Start Contributing
Choose based on your interests and expertise:

- **Template Development**: Improve existing templates or create new ones
- **Command Enhancement**: Add new Claude Code commands for discovered workflows
- **Documentation Curation**: Add AI-consumable documentation to `PRPs/ai_docs/`
- **Framework Examples**: Create CLAUDE.md examples for new frameworks
- **Validation Systems**: Improve validation gates and quality assurance
- **Multi-Agent Orchestration**: Enhance parallel execution and coordination
- **Agent Development**: Extend or improve existing agents
- **Knowledge Management**: Enhance vector database and RAG capabilities

### Recommended First Contributions
1. **Study the PRP methodology** by reading `PRPs/README.md`
2. **Create a test PRP** for a simple feature you understand
3. **Execute the PRP** and observe the validation process
4. **Identify improvement opportunities** in templates or commands
5. **Propose enhancements** based on your experience
6. **Contribute to agent development** by understanding the multi-agent system

## Getting Help

- **Project Documentation**: Start with `PRPs/README.md` and `CLAUDE.md`
- **Command Reference**: Browse `.claude/commands/` for available workflows
- **Template Guide**: Study `PRPs/templates/prp_base.md` for implementation patterns
- **Claude Code Help**: Use `claude /help` for CLI assistance
- **Coding Standards**: Check `.cursor/rules/` for comprehensive guidelines
- **Agent Patterns**: Study `src/agents/` for multi-agent system understanding

Welcome to the agent-factory! This framework is designed to enable AI agents to ship production-ready code through comprehensive context and validation. Your contributions will help make AI-driven development more reliable and effective.