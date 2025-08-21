# Project Structure Reference

This document provides detailed information about the repository structure for both Agent Factory projects.

## Agent Factory Structure

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
├── .cursor/                    # Cursor IDE rules and configuration
│   └── rules/                 # Comprehensive coding standards and patterns
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
├── src/                       # Source code
│   ├── agent_factory/         # Main package with core framework
│   ├── agents/               # Specialized agents (coder, planner, tester, etc.)
│   │   ├── base/             # Base agent interface and common functionality
│   │   ├── coder/            # Code generation and implementation agent
│   │   ├── planner/          # Task planning and decomposition agent
│   │   ├── tester/           # Testing and quality assurance agent
│   │   ├── reviewer/         # Code review and validation agent
│   │   ├── devops/           # Deployment and infrastructure agent
│   │   └── coordinator/      # Agent orchestration and coordination
│   ├── api/                  # REST and streaming interfaces
│   │   ├── rest/             # REST API endpoints
│   │   ├── streaming/        # WebSocket and streaming interfaces
│   │   └── ui/               # User interface components
│   ├── communication/        # Inter-agent messaging and protocols
│   │   ├── message_bus/      # Redis-based pub/sub messaging
│   │   ├── protocols/        # Message formats and protocols
│   │   └── coordination/     # Agent coordination mechanisms
│   ├── knowledge/            # Memory, RAG, and vector storage
│   │   ├── memory/           # Agent memory management
│   │   ├── rag/              # Retrieval-augmented generation
│   │   └── vector_store/     # Chroma vector database integration
│   ├── workflows/            # Process orchestration and monitoring
│   │   ├── monitoring/       # System health and performance monitoring
│   │   ├── prp_engine/       # PRP execution and validation workflows
│   │   └── validation/       # Quality assurance and validation
│   ├── tools/                # Utility functions and integrations
│   │   ├── deployment/       # Deployment automation tools
│   │   ├── git/              # Git workflow tools
│   │   └── testing/          # Testing and validation tools
│   ├── config/               # Settings and configuration
│   │   ├── settings.py       # Application configuration and environment variables
│   │   └── logging.py        # Structured logging configuration
│   └── models.py             # Core data structures and enums
├── tests/                    # Test suite
│   ├── test_models.py        # Core model tests
│   ├── test_base_agent.py    # Base agent tests
│   ├── test_chroma_store.py  # Vector store tests
│   └── test_redis_messenger.py # Message bus tests
├── docker/                   # Docker configuration
│   ├── docker-compose.yml    # Production services
│   ├── docker-compose.dev.yml # Development overrides
│   └── grafana/              # Monitoring dashboards
├── scripts/                  # Development and deployment utilities
│   ├── dev-start.sh          # Development environment startup
│   └── init_project.py       # Project initialization
├── docs/                     # Documentation
│   ├── SHARED_COMPONENTS.md  # Common documentation components
│   ├── API_REFERENCE.md      # API documentation
│   ├── ARCHITECTURE.md       # System architecture
│   ├── USER_GUIDE.md         # User guide
│   ├── DEVELOPER_REFERENCE.md # Developer reference
│   ├── CONFIGURATION.md      # Configuration guide
│   └── TROUBLESHOOTING.md    # Troubleshooting guide
├── claude_md_files/          # Framework-specific CLAUDE.md examples
│   ├── CLAUDE-REACT.md       # React project template
│   ├── CLAUDE-PYTHON-BASIC.md # Python project template
│   ├── CLAUDE-NEXTJS-15.md   # Next.js project template
│   └── ...                   # Additional framework templates
├── CLAUDE.md                  # Project-specific Claude Code instructions
├── README.md                  # Project overview and quick start
├── ONBOARDING.md             # Developer onboarding guide
├── QUICKSTART.md             # 5-minute setup guide
├── pyproject.toml            # Python project configuration and dependencies
└── requirements/              # Dependency specifications
    ├── base.txt              # Core dependencies
    └── dev.txt               # Development dependencies
```

## Data for SEO Structure

```
data-for-seo/
├── .claude/                    # Claude Code configuration
│   ├── commands/              # Pre-configured commands for SEO automation
│   │   ├── prp-commands/      # PRP creation and execution workflows
│   │   ├── development/       # Core development utilities
│   │   ├── code-quality/      # Review and refactoring commands  
│   │   ├── rapid-development/ # Parallel PRP creation tools
│   │   ├── git-operations/    # Conflict resolution and git operations
│   │   └── seo-specific/      # SEO automation specific commands
│   └── settings.local.json    # Tool permissions and configuration
├── .cursor/                    # Cursor IDE rules and configuration
│   └── rules/                 # Comprehensive coding standards and patterns
├── PRPs/                      # Product Requirement Prompt framework
│   ├── templates/             # Structured PRP templates
│   │   ├── prp_base.md        # Main implementation template
│   │   ├── prp_seo.md         # SEO-specific implementation template
│   │   ├── prp_planning.md    # Planning document template
│   │   └── ...                # Additional specialized templates
│   ├── scripts/               # PRP execution scripts
│   │   └── prp_runner.py      # Main PRP execution script
│   ├── ai_docs/               # Curated Claude Code documentation
│   │   ├── getting_started.md # Claude Code basics
│   │   ├── cc_commands.md     # Command system documentation
│   │   ├── subagents.md       # Multi-agent orchestration
│   │   ├── seo_patterns.md    # SEO-specific patterns and best practices
│   │   └── ...                # Additional AI workflow docs
│   └── README.md              # PRP methodology explanation
├── src/                       # Source code
│   ├── agent_factory/         # Main package with core framework
│   ├── agents/               # Specialized agents for SEO
│   │   ├── base/             # Base agent interface and common functionality
│   │   ├── seo_analyst/      # SEO analysis and keyword research agent
│   │   ├── content_optimizer/ # Content optimization agent
│   │   ├── technical_auditor/ # Technical SEO analysis agent
│   │   ├── performance_monitor/ # SEO performance tracking agent
│   │   ├── automation_engineer/ # Workflow automation agent
│   │   └── coordinator/      # Agent orchestration and coordination
│   ├── api/                  # REST and streaming interfaces
│   │   ├── rest/             # REST API endpoints
│   │   ├── streaming/        # WebSocket and streaming interfaces
│   │   └── ui/               # User interface components
│   ├── communication/        # Inter-agent messaging and protocols
│   │   ├── message_bus/      # Redis-based pub/sub messaging
│   │   ├── protocols/        # Message formats and protocols
│   │   └── coordination/     # Agent coordination mechanisms
│   ├── knowledge/            # Memory, RAG, and vector storage
│   │   ├── memory/           # Agent memory management
│   │   ├── rag/              # Retrieval-augmented generation
│   │   └── vector_store/     # Chroma vector database integration
│   ├── workflows/            # Process orchestration and monitoring
│   │   ├── monitoring/       # System health and performance monitoring
│   │   ├── prp_engine/       # PRP execution and validation workflows
│   │   └── validation/       # Quality assurance and validation
│   ├── tools/                # Utility functions and integrations
│   │   ├── deployment/       # Deployment automation tools
│   │   ├── git/              # Git workflow tools
│   │   ├── testing/          # Testing and validation tools
│   │   └── seo/              # SEO-specific tools and utilities
│   ├── config/               # Settings and configuration
│   │   ├── settings.py       # Application configuration and environment variables
│   │   └── logging.py        # Structured logging configuration
│   └── models.py             # Core data structures and enums
├── tests/                    # Test suite
│   ├── test_models.py        # Core model tests
│   ├── test_seo_agents.py    # SEO agent tests
│   ├── test_seo_services.py  # SEO service tests
│   └── test_integrations.py  # Integration tests
├── docker/                   # Docker configuration
│   ├── docker-compose.yml    # Production services
│   ├── docker-compose.dev.yml # Development overrides
│   └── grafana/              # Monitoring dashboards
├── scripts/                  # Development and deployment utilities
│   ├── dev-start.sh          # Development environment startup
│   ├── init-project.sh       # Project initialization
│   └── seo-setup.sh          # SEO-specific setup
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md       # SEO-focused system architecture
│   ├── ONBOARDING.md         # SEO developer onboarding guide
│   └── QUICKSTART.md         # SEO quick start guide
├── claude_md_files/          # Framework-specific CLAUDE.md examples
│   ├── CLAUDE-SEO.md         # SEO project template
│   ├── CLAUDE-PYTHON-BASIC.md # Python project template
│   └── ...                   # Additional framework templates
├── CLAUDE.md                  # Project-specific Claude Code instructions
├── README.md                  # Project overview and quick start
├── pyproject.toml            # Python project configuration and dependencies
└── requirements/              # Dependency specifications
    ├── base.txt              # Core dependencies
    └── dev.txt               # Development dependencies
```

## Directory Purposes

### Common Directories

- **`.claude/commands/`**: Command-driven development workflows organized by function
- **`.cursor/rules/`**: Comprehensive coding standards and project patterns for Cursor IDE
- **`PRPs/templates/`**: Structured templates for creating comprehensive implementation prompts
- **`PRPs/ai_docs/`**: Curated documentation for AI context injection
- **`claude_md_files/`**: Framework-specific CLAUDE.md examples for different tech stacks
- **`PRPs/scripts/`**: Automation scripts for PRP execution and management
- **`src/agents/`**: Specialized AI agents for different development/SEO functions
- **`src/communication/`**: Inter-agent messaging and coordination systems
- **`src/knowledge/`**: Knowledge management and vector storage
- **`src/workflows/`**: Process orchestration and monitoring

### SEO-Specific Directories (data-for-seo)

- **`src/tools/seo/`**: SEO-specific tools and utilities
- **`src/agents/seo_*/`**: Specialized SEO agents
- **`scripts/seo-setup.sh`**: SEO-specific setup scripts
- **`PRPs/ai_docs/seo_patterns.md`**: SEO-specific patterns and best practices

## Organizational Patterns

1. **Command-Driven Architecture**: All development workflows are pre-configured as Claude Code commands
2. **Template-First Approach**: Every implementation starts with a structured template
3. **Context Injection System**: Systematic curation of documentation for AI agents
4. **Validation-First Design**: Every template includes executable validation gates
5. **Multi-Agent System**: Specialized agents working together through coordinated workflows
6. **Knowledge-Centric**: Vector database and RAG for context-aware decision making
7. **SEO-Focused** (data-for-seo): Domain-specific patterns and workflows for SEO automation
