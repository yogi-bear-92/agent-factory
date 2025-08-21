# Shared Documentation Components

This file contains common documentation sections shared across both agent-factory and data-for-seo projects to eliminate duplication.

## Prerequisites

### Required Tools
- **Python**: Version 3.12 or higher
- **uv**: Modern Python package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Claude Code**: AI development CLI (`npm install -g @anthropics/claude-code`)
- **Git**: For version control
- **Docker**: For running Redis, Chroma, and other services

### Verification Commands
```bash
python3 --version  # Should be 3.12+
uv --version        # Should be installed
claude --version    # Should be installed
docker --version    # Should be installed
```

## Installation Steps

### 1. Clone and Setup
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Start Development Services
```bash
./scripts/dev-start.sh
```

### 5. Initialize Claude Context
```bash
claude /prime-core
```

### 6. Verify Setup
```bash
# Check if uv is working
uv --version

# Check if Claude commands are available
ls .claude/commands/

# Check if services are running
curl -f http://localhost:8000/health
```

## Agent Descriptions

### Core Agent Roles

#### 🎯 Task Coordinator
- **Role**: Orchestrates the entire development process
- **Responsibilities**: Task distribution, dependency management, progress tracking
- **When Active**: Throughout the entire feature lifecycle
- **Capabilities**: Agent supervision, workflow coordination, resource allocation

#### 📋 Feature Planner
- **Role**: Breaks down high-level specifications into actionable tasks
- **Responsibilities**: Requirements analysis, task decomposition, PRP generation
- **When Active**: At the start of each feature and when requirements change
- **Capabilities**: Technical analysis, dependency identification, timeline estimation

#### 💻 Implementation Coder
- **Role**: Writes production-ready code following best practices
- **Responsibilities**: Code implementation, refactoring, integration
- **When Active**: During development phases
- **Capabilities**: Multiple language support, pattern recognition, context-aware coding

#### 🧪 Automated Tester
- **Role**: Ensures code quality through comprehensive testing
- **Responsibilities**: Test generation, execution, coverage analysis
- **When Active**: Continuously throughout development
- **Capabilities**: Unit tests, integration tests, performance testing, security testing

#### 👀 Code Reviewer
- **Role**: Maintains code quality and standards compliance
- **Responsibilities**: Code review, standards enforcement, security analysis
- **When Active**: After code implementation, before deployment
- **Capabilities**: Static analysis, security scanning, performance review

#### 🚀 DevOps Agent
- **Role**: Handles deployment and infrastructure management
- **Responsibilities**: CI/CD pipeline management, deployment automation, monitoring
- **When Active**: During deployment and maintenance phases
- **Capabilities**: Multi-environment deployment, rollback management, scaling

## Development Workflow

### Git Branch Naming Conventions
- `feature/feature-name` - New features
- `fix/issue-description` - Bug fixes  
- `docs/documentation-update` - Documentation changes
- `refactor/component-name` - Code refactoring

### Testing Requirements
- **Unit Tests**: All new code must have corresponding tests
- **Integration Tests**: Test component interactions
- **Template Validation**: PRPs must follow structured format
- **Execution Testing**: Validation gates must pass
- **Documentation**: Changes must be documented

### Code Style/Linting Rules
- **Python**: Follow PEP 8 with 88 character line length
- **Formatting**: Use `ruff format` for consistent formatting
- **Linting**: Use `ruff check --fix` for style enforcement
- **Type Checking**: Use `mypy src --strict` for type safety
- **Markdown**: Consistent formatting for templates and documentation
- **YAML**: Structured format for context sections in PRPs

### PR Process and Review Guidelines
1. **Create comprehensive PRP** for the feature
2. **Execute PRP** and ensure validation gates pass
3. **Write tests** for new functionality
4. **Run quality checks**: `ruff check --fix src tests && mypy src`
5. **Review changes** using `/review-staged-unstaged` command
6. **Create PR** using `/create-pr` command
7. **Ensure documentation** is updated

## Essential Commands

### Core Workflow Commands
```bash
claude /prime-core                    # Initialize project context
claude /prp-base-create "feature"     # Create comprehensive PRP
claude /prp-base-execute "prp-file"   # Execute existing PRP
claude /review-staged-unstaged        # Review changes
```

### PRP Execution Modes
```bash
uv run PRPs/scripts/prp_runner.py --prp name --interactive    # Interactive
uv run PRPs/scripts/prp_runner.py --prp name --output-format json  # Headless
```

### Development Commands
```bash
./scripts/dev-start.sh                # Start development services
uv sync                              # Install/update dependencies
uv run pytest -v                     # Run tests
```

### Claude Code Command System
Access commands via `/` prefix:
- `/prp-base-create` - Create comprehensive PRPs
- `/prp-base-execute` - Execute PRPs against codebase  
- `/prime-core` - Initialize project context
- `/review-staged-unstaged` - Review changes using PRP methodology
- `/debug` - Debugging workflow
- `/smart-commit` - Intelligent git commits

## Core Concepts

### Product Requirement Prompts (PRPs)
**PRP = PRD + curated codebase intelligence + agent/runbook** - designed to enable AI agents to ship production-ready code on the first pass.

#### PRP Structure
- **Goal**: Clear, specific objective
- **Why**: Business justification and user value
- **What**: Detailed requirements and success criteria
- **Context**: All necessary documentation, examples, and gotchas
- **Implementation Blueprint**: Step-by-step technical plan
- **Validation Gates**: Executable tests and quality checks

### Autonomous Development Workflow
1. **Specification Submission**: You provide high-level feature requirements
2. **Task Decomposition**: The Planner agent breaks down the feature into manageable tasks
3. **Agent Coordination**: The Coordinator assigns tasks to specialized agents
4. **Parallel Execution**: Multiple agents work simultaneously on different aspects
5. **Quality Assurance**: Automated testing and code review
6. **Deployment**: Automated deployment and monitoring
7. **Learning**: System captures outcomes for future improvements

### Knowledge Base
Agent Factory maintains a persistent vector database that stores:
- **Project Context**: Codebase structure, architecture decisions
- **Implementation Patterns**: Successful code patterns and solutions  
- **Historical Outcomes**: Previous successes and failures
- **Domain Knowledge**: Framework documentation, best practices
- **Team Preferences**: Coding standards, deployment patterns

## Architecture Overview

### High-Level Architecture
**Multi-Agent System with Event-Driven Communication** and **Knowledge-Centric Design**

### Core Components
1. **PRP Execution Engine**: Orchestrates the execution of Product Requirement Prompts
2. **Multi-Agent System**: Specialized agents for different development functions
3. **Knowledge Management**: Stores and retrieves context-aware information
4. **Communication Layer**: Enables inter-agent communication and coordination

### Technology Stack
- **Language**: Python 3.12+ 
- **Package Manager**: uv (modern Python package manager)
- **AI Framework**: Claude Code CLI integration + LangChain + LangGraph
- **MCP Servers**: serena (desktop), archon (remote HTTP), browsermcp (browser automation)
- **Vector Database**: Chroma for knowledge storage and retrieval
- **Message Bus**: Redis for agent communication
- **API Framework**: FastAPI for REST and streaming interfaces
- **Documentation**: Markdown-based templates and structured YAML configurations

## Common Troubleshooting

### Quick Health Check
```bash
# Check system status
curl http://localhost:8000/health

# Check all services
docker-compose ps

# Check agent status
curl http://localhost:8000/agents

# Check logs for errors
docker-compose logs --tail=50
```

### Common Issues
- **Service won't start**: Check logs and verify configuration
- **Connection issues**: Test Redis and Chroma connectivity
- **Agent communication errors**: Verify message bus configuration
- **Performance issues**: Check resource usage and scaling

## Getting Help
- **Project Documentation**: Start with project-specific README and CLAUDE.md
- **Command Reference**: Browse `.claude/commands/` for available workflows
- **Template Guide**: Study PRP templates for implementation patterns
- **Claude Code Help**: Use `claude /help` for CLI assistance
- **Coding Standards**: Check `.cursor/rules/` for comprehensive guidelines
- **Agent Patterns**: Study `src/agents/` for multi-agent system understanding
