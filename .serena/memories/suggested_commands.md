# Suggested Commands for Agent Factory Development

## Core PRP Workflow Commands

### PRP Creation and Execution
```bash
# Create comprehensive PRPs with research
claude /prp-base-create "feature description"

# Execute PRPs against codebase
claude /prp-base-execute PRPs/[prp-file].md

# Create planning documents with diagrams
claude /prp-planning-create "planning topic"
```

### PRP Script Execution
```bash
# Interactive mode (recommended for development)
uv run PRPs/scripts/prp_runner.py --prp [prp-name] --interactive

# Headless mode (for CI/CD)
uv run PRPs/scripts/prp_runner.py --prp [prp-name] --output-format json

# Streaming JSON (for real-time monitoring)
uv run PRPs/scripts/prp_runner.py --prp [prp-name] --output-format stream-json
```

## Development Workflow Commands

### Project Initialization
```bash
# Prime Claude with project context
claude /prime-core

# Onboarding process for new team members
claude /onboarding
```

### Code Quality and Review
```bash
# Review git changes using PRP methodology
claude /review-staged-unstaged

# Debugging workflow
claude /debug
```

## System Commands (Darwin/macOS)

### File System Navigation
```bash
# List files and directories
ls -la

# Find files
find . -name "*.py" -type f

# Search in files
grep -r "pattern" .

# Tree view (if installed)
tree -I '__pycache__|*.pyc|node_modules|.git'
```

### Git Operations
```bash
# Initialize repository
git init

# Add and commit changes
git add .
git commit -m "commit message"

# Create and push repository
gh repo create
git remote add origin <url>
git push -u origin main
```

### Python/uv Commands
```bash
# Check Python version
python3 --version

# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run Python scripts with uv
uv run python script.py

# Install dependencies (when needed)
uv add package-name
```

## Claude Code Commands Available

### PRP Commands
- `/prp-base-create` - Generate comprehensive PRPs with research
- `/prp-base-execute` - Execute PRPs against codebase
- `/prp-planning-create` - Create planning documents
- `/prp-spec-create` - Create specification documents
- `/prp-task-create` - Create task-oriented PRPs

### Development Commands
- `/prime-core` - Initialize project context
- `/debug` - Debugging workflow
- `/onboarding` - Team onboarding process
- `/smart-commit` - Intelligent git commits
- `/create-pr` - Create pull requests

### Code Quality Commands
- `/review-staged-unstaged` - Review changes
- Various refactoring and quality commands

### Rapid Development Commands
- Parallel PRP creation tools
- Experimental development workflows

### Git Operations Commands
- Conflict resolution workflows
- Smart git operations

### TypeScript Commands
- TypeScript-specific development workflows