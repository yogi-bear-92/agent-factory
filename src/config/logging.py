"""Logging configuration for the Agent Factory framework."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog
from structlog.contextvars import clear_contextvars
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, TimeStamper, add_log_level
from structlog.stdlib import LoggerFactory, add_logger_name, filter_by_level

from .settings import settings


def configure_logging() -> None:
    """Configure structured logging for the application."""
    import logging

    # Clear any existing context
    clear_contextvars()

    # Create logs directory
    logs_dir = Path(settings.logs_directory)
    logs_dir.mkdir(exist_ok=True)

    # Get numeric log level
    log_level = getattr(logging, settings.monitoring.log_level.upper(), logging.INFO)

    # Configure processors
    shared_processors = [
        filter_by_level,
        add_log_level,
        add_logger_name,
        TimeStamper(fmt="iso", utc=True),
    ]

    if settings.debug:
        # Development: pretty console output
        processors = shared_processors + [
            structlog.dev.set_exc_info,
            ConsoleRenderer(colors=True),
        ]

        structlog.configure(
            processors=processors,
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            logger_factory=LoggerFactory(),
            cache_logger_on_first_use=False,
        )
    else:
        # Production: JSON output
        processors = shared_processors + [
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            JSONRenderer(),
        ]

        structlog.configure(
            processors=processors,
            wrapper_class=structlog.make_filtering_bound_logger(log_level),
            logger_factory=LoggerFactory(),
            cache_logger_on_first_use=True,
        )


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a configured logger instance.

    Args:
        name: Logger name, typically __name__ of the calling module

    Returns:
        Configured structlog logger instance
    """
    return structlog.get_logger(name)


def log_context(**kwargs: Any) -> None:
    """Add context variables that will be included in all subsequent log entries.

    Args:
        **kwargs: Key-value pairs to add to logging context
    """
    for key, value in kwargs.items():
        structlog.contextvars.bind_contextvars(**{key: value})


def clear_log_context() -> None:
    """Clear all context variables from logging context."""
    clear_contextvars()


# Configure logging on import
configure_logging()
