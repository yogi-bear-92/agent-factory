# Technology Stack

## Core Technologies
- **Python**: Version 3.12+ (specified in pyproject.toml)
- **uv**: Modern Python package manager and script runner
- **Claude Code**: AI-powered development CLI tool for agent interactions

## Package Management
- **uv**: Used for dependency management and script execution
- **pyproject.toml**: Python project configuration with minimal dependencies
- Current dependencies: None (framework is template/command-based)

## MCP Servers
- **serena**: Desktop app context with project management capabilities
- **archon**: Remote HTTP server (localhost:8051) for advanced AI workflows
- **browsermcp**: Browser automation and interaction capabilities

## Framework Components
- **LangChain**: For multi-agent systems and LLM integration
- **FastAPI**: For REST API endpoints and streaming interfaces
- **Redis**: For agent communication via pub/sub messaging
- **Chroma**: Local vector database for knowledge storage and RAG
- **Docker**: For containerized deployment and service orchestration

## Operating System
- **Darwin** (macOS): Primary development environment
- **Linux VPS**: Target deployment environment

## Development Tools
- **Git**: Version control system
- **Docker**: Containerization for multi-agent deployments
- **Testing**: pytest for automated testing
- **Linting**: ruff for code formatting and style checking
- **Type Checking**: mypy for static type analysis