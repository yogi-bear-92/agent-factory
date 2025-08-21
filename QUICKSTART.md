# Agent Factory - Quick Start Guide

Get up and running with the PRP (Product Requirement Prompt) Framework in 5 minutes.

> **📖 Common Setup Steps**: For detailed prerequisites and installation steps, see [Shared Components](docs/SHARED_COMPONENTS.md#prerequisites)

## Quick Setup (1 minute)

Follow the [standard installation steps](docs/SHARED_COMPONENTS.md#installation-steps), then:

## Your First PRP (2 minutes)

1. **Create a PRP for a simple feature**:
   ```bash
   claude /prp-base-create "add a hello world function"
   ```

2. **Execute the PRP** (interactive mode):
   ```bash
   uv run PRPs/scripts/prp_runner.py --prp hello-world --interactive
   ```

3. **Review what was created**:
   ```bash
   # Check the generated PRP
   cat PRPs/hello-world.md
   
   # Review any changes made
   claude /review-staged-unstaged
   ```

## Essential Commands

> **📖 Complete Command Reference**: See [Shared Components - Essential Commands](docs/SHARED_COMPONENTS.md#essential-commands) for full command documentation.

## Project Structure Overview

```
agent-factory/
├── .claude/commands/     # 35+ pre-configured Claude commands
├── .cursor/rules/        # Comprehensive coding standards and patterns
├── PRPs/
│   ├── templates/        # PRP templates (start here)
│   ├── scripts/          # PRP execution scripts  
│   ├── ai_docs/          # Curated AI documentation
│   └── README.md         # PRP methodology (read this!)
├── src/                  # Source code
│   ├── agents/           # Multi-agent system (coder, planner, tester, etc.)
│   ├── communication/    # Redis pub/sub messaging
│   ├── knowledge/        # Vector database and RAG
│   ├── workflows/        # Process orchestration
│   └── config/           # Settings and configuration
├── tests/                # Test suite
├── docker-compose.dev.yml # Development services
├── claude_md_files/      # Framework-specific examples
└── CLAUDE.md             # Project instructions
```

## Multi-Agent System

> **📖 Agent Details**: See [Shared Components - Agent Descriptions](docs/SHARED_COMPONENTS.md#agent-descriptions) for detailed information about each agent's role and capabilities.

## Knowledge Management

- **Vector Database**: Chroma for storing and retrieving knowledge
- **RAG System**: Retrieval-augmented generation for context-aware decisions
- **Redis Message Bus**: Inter-agent communication and coordination

## Azure Setup

- For Azure AI Foundry + Container Apps deployment, see docs/AZURE.md

## Next Steps

1. **Read the methodology**: `cat PRPs/README.md`
2. **Study templates**: `cat PRPs/templates/prp_base.md`
3. **Browse commands**: `ls .claude/commands/*/`
4. **Understand agents**: Explore `src/agents/` directory
5. **Read full onboarding**: `cat ONBOARDING.md`

## Key Concepts

> **📖 Core Concepts**: See [Shared Components - Core Concepts](docs/SHARED_COMPONENTS.md#core-concepts) for detailed explanations of PRPs, workflows, and architecture.

## Getting Help

- **Commands**: Browse `.claude/commands/` directory
- **Templates**: Check `PRPs/templates/` for examples  
- **Methodology**: Read `PRPs/README.md`
- **Coding Standards**: Check `.cursor/rules/` for guidelines
- **Agent Patterns**: Study `src/agents/` for multi-agent system
- **Full guide**: See `ONBOARDING.md`

You're ready to start using the PRP framework with the multi-agent system! Begin with a simple feature and work your way up to more complex implementations.