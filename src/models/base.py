"""Base models for the Agent Factory framework."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum, auto
from typing import Any

from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    """Result of an agent execution."""

    success: bool = Field(default=False, description="Whether execution was successful")
    errors: list[str] = Field(default_factory=list, description="Error messages")
    output: dict[str, Any] = Field(default_factory=dict, description="Output data")
    performance_metrics: dict[str, Any] = Field(
        default_factory=dict, description="Performance metrics"
    )
    execution_time: float = Field(default=0.0, description="Execution time in seconds")


class SourceType(str, Enum):
    """Types of knowledge sources."""

    CODE = "code"
    DOCS = "docs"
    PATTERN = "pattern"
    FAILURE = "failure"
    SUCCESS = "success"
    FEEDBACK = "feedback"
    SEO = "seo"


class KnowledgeEntry(BaseModel):
    """Knowledge entry in the vector store."""

    id: str = Field(default_factory=lambda: f"entry_{datetime.now(UTC).timestamp()}")
    content: str = Field(..., description="Content of the knowledge entry")
    metadata: dict[str, Any] = Field(default_factory=dict)
    source_type: SourceType = Field(..., description="Type of knowledge source")
    tags: list[str] = Field(default_factory=list)
    embedding: list[float] | None = Field(default=None, description="Vector embedding")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))