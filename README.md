# Agent Factory - AI Agent-Driven Autonomous Development Framework

A comprehensive framework for building autonomous software development teams using specialized AI agents that collaborate to develop software from requirements to deployment.

## Overview

The **agent-factory** implements the **PRP (Product Requirement Prompt) Framework** combined with a multi-agent system where specialized AI agents (Planner, Coder, Tester, Reviewer, DevOps, Integrator) work together to autonomously develop software.

## Core Concept

**PRP = PRD + curated codebase intelligence + agent/runbook** - designed to enable AI agents to ship production-ready code on the first pass.

## Features

- **Multi-Agent Development Team**: Specialized agents for different development roles
- **Persistent Knowledge Base**: Vector database with RAG for context-aware decisions
- **PRP-Driven Workflows**: Structured task execution with validation gates
- **Agent Coordination**: Redis pub/sub messaging for seamless communication
- **Self-Learning System**: Continuous improvement from development outcomes
- **Local-First Architecture**: Runs entirely on standard VPS infrastructure

## Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Initialize project context**:
   ```bash
   claude /prime-core
   ```

3. **Create a PRP**:
   ```bash
   claude /prp-base-create "your feature description"
   ```

4. **Execute PRP with agents**:
   ```bash
   uv run PRPs/scripts/prp_runner.py --prp your-feature --interactive
   ```

## Architecture

- **Agent Framework**: LangChain + LangGraph for stateful workflows
- **Vector Database**: Chroma for knowledge storage and retrieval
- **Communication**: Redis pub/sub for agent coordination
- **API Layer**: FastAPI for external interfaces
- **Deployment**: Docker containers for scalable deployment

## CLI alias: rovodev

Use rovodev as a friendly alias to the Claude Code CLI.
Examples:
- rovodev /prime-core
- rovodev /prp-base-create "add a hello world function"

Note: It forwards to the `claude` CLI. Install via: npm install -g @anthropics/claude-code

## Development

See [ONBOARDING.md](ONBOARDING.md) for detailed development guide and [CLAUDE.md](CLAUDE.md) for AI-specific instructions.

## Azure Setup

See docs/AZURE.md for step-by-step instructions for:
- Using Azure AI Foundry (Azure OpenAI) with this project
- Deploying to Azure Container Apps via GitHub Actions

## MCP Integration

The framework integrates with multiple MCP servers:
- **serena**: Desktop app context and project management
- **archon**: Remote HTTP server for advanced AI workflows
- **browsermcp**: Browser automation capabilities

## License

MIT License - see LICENSE file for details.