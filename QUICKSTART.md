# Agent Factory - Quick Start Guide

Get up and running with the PRP (Product Requirement Prompt) Framework in 5 minutes.

## Prerequisites (2 minutes)

1. **Install required tools**:
   ```bash
   # Install uv (Python package manager)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install Claude Code (AI development CLI)
   npm install -g @anthropics/claude-code
   
   # Verify Python 3.12+
   python3 --version
   ```

2. **Clone and enter the project**:
   ```bash
   git clone <repository-url>
   cd agent-factory
   ```

## Quick Setup (1 minute)

1. **Initialize Claude with project context**:
   ```bash
   claude /prime-core
   ```

2. **Verify setup**:
   ```bash
   # Check if uv is working
   uv --version
   
   # Check if Claude commands are available
   ls .claude/commands/
   ```

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

```bash
# Core workflow commands
claude /prime-core                    # Initialize project context
claude /prp-base-create "feature"     # Create comprehensive PRP
claude /prp-base-execute "prp-file"   # Execute existing PRP
claude /review-staged-unstaged        # Review changes

# PRP execution modes
uv run PRPs/scripts/prp_runner.py --prp name --interactive    # Interactive
uv run PRPs/scripts/prp_runner.py --prp name --output-format json  # Headless
```

## Project Structure Overview

```
agent-factory/
├── .claude/commands/     # 35+ pre-configured Claude commands
├── PRPs/
│   ├── templates/        # PRP templates (start here)
│   ├── scripts/          # PRP execution scripts  
│   ├── ai_docs/          # Curated AI documentation
│   └── README.md         # PRP methodology (read this!)
├── claude_md_files/      # Framework-specific examples
└── CLAUDE.md             # Project instructions
```

## Azure Setup

- For Azure AI Foundry + Container Apps deployment, see docs/AZURE.md

## Next Steps

1. **Read the methodology**: `cat PRPs/README.md`
2. **Study templates**: `cat PRPs/templates/prp_base.md`
3. **Browse commands**: `ls .claude/commands/*/`
4. **Read full onboarding**: `cat ONBOARDING.md`

## Key Concepts

- **PRP = PRD + curated codebase intelligence + agent/runbook**
- **Goal**: Enable AI agents to ship production-ready code on the first pass
- **Method**: Comprehensive context + structured templates + validation gates
- **Workflow**: Create PRP → Execute with AI → Validate → Refine

## Getting Help

- **Commands**: Browse `.claude/commands/` directory
- **Templates**: Check `PRPs/templates/` for examples  
- **Methodology**: Read `PRPs/README.md`
- **Full guide**: See `ONBOARDING.md`

You're ready to start using the PRP framework! Begin with a simple feature and work your way up to more complex implementations.