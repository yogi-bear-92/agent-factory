# PRP: Create and Execute a Feature

Overview
This guide walks you through creating a Product Requirement Prompt (PRP) and executing it with the agent team, both interactively and headlessly. It uses the built-in PRP templates and scripts included in this repo.

Prerequisites
- Python 3.12+
- uv (Python package manager)
- Claude Code CLI (for /commands)

Install tools
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Claude Code
npm install -g @anthropics/claude-code
```

Initialize project context
```bash
claude /prime-core
uv --version
ls .claude/commands/
```

Create a PRP
- Write a concise description of your feature.
```bash
claude /prp-base-create "add a hello world function"
```
- The PRP will be saved under PRPs/ using the generated name (e.g., PRPs/hello-world.md).

Execute the PRP
Interactive mode:
```bash
uv run PRPs/scripts/prp_runner.py --prp hello-world --interactive
```
Headless mode (JSON output):
```bash
uv run PRPs/scripts/prp_runner.py --prp hello-world --output-format json
```

Review outputs
```bash
# Inspect PRP
cat PRPs/hello-world.md

# Review changes
claude /review-staged-unstaged
```

Validation gates
- Run tests (if present) and ensure code quality gates pass.
```bash
pytest -q || true
```
- Use the review command to catch issues early:
```bash
claude /review-general
```

Troubleshooting
- If packages are missing or environment is off, run:
```bash
uv sync
```
- To validate project health:
```bash
python scripts/test_init.py
```
- For configuration checks (e.g., directories, logging):
```bash
python scripts/init_project.py
```

Next steps
- Explore PRP templates in PRPs/templates/
- Add curated docs to PRPs/ai_docs/ if your feature needs library context
- Iterate: refine PRP → execute → validate → review
