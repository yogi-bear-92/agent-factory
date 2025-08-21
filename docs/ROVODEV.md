# Rovo Dev CLI

The `rovodev` command is a friendly alias for the Claude Code CLI (`claude`). It forwards all arguments to `claude` so your existing workflows still work, but with a project-friendly name.

Usage:
- rovodev /prime-core
- rovodev /prp-base-create "your feature"

Install Claude Code CLI if you haven’t already:
```
npm install -g @anthropics/claude-code
```

The console entrypoint is defined in `pyproject.toml` under `[project.scripts]`.
