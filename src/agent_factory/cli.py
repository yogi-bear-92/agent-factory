"""Rovo Dev CLI alias.

This CLI acts as a project-local alias for the Claude Code CLI so you can
use `rovodev` instead of `claude` for all project commands.

Examples:
  rovodev /prime-core
  rovodev /prp-base-create "add a hello world function"

If the Claude CLI is not installed, a clear message will be shown with
installation instructions.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from typing import List


def _print_help() -> None:
    help_text = (
        "Rovo Dev - project helper CLI (alias for Claude Code)\n\n"
        "Usage:\n"
        "  rovodev /<claude-command> [args...]\n\n"
        "Examples:\n"
        "  rovodev /prime-core\n"
        "  rovodev /prp-base-create \"add a hello world function\"\n\n"
        "Notes:\n"
        "  - This command forwards directly to the 'claude' CLI.\n"
        "  - Ensure the Claude Code CLI is installed: npm install -g @anthropics/claude-code\n"
    )
    print(help_text)


def _forward_to_claude(argv: List[str]) -> int:
    """Forward the provided arguments to the `claude` CLI."""
    claude_path = shutil.which("claude")
    if not claude_path:
        print(
            "Error: Claude Code CLI not found.\n\n"
            "Install it with:\n"
            "  npm install -g @anthropics/claude-code\n\n"
            "Then re-run your command, e.g.:\n"
            "  rovodev /prime-core\n"
        )
        return 127

    try:
        completed = subprocess.run([claude_path, *argv], check=False)
        return completed.returncode
    except KeyboardInterrupt:
        return 130


def main() -> None:
    argv = sys.argv[1:]

    if not argv or argv[0] in {"-h", "--help", "help"}:
        _print_help()
        sys.exit(0)

    sys.exit(_forward_to_claude(argv))


if __name__ == "__main__":
    main()
