"""Core type definitions for the agent framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    """Types of messages between agents."""

    TASK_ASSIGNMENT = "task_assignment"
    TASK_RESULT = "task_result"
    TASK_UPDATE = "task_update"
    COORDINATION = "coordination"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class TaskPriority(str, Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(str, Enum):
    """Task execution status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SourceType(str, Enum):
    """Types of knowledge sources."""

    DOCUMENTATION = "documentation"
    CODE = "code"
    PATTERN = "pattern"
    FAILURE = "failure"
    SUCCESS = "success"
    CONTEXT = "context"


class AgentType(str, Enum):
    """Types of agents in the system."""

    COORDINATOR = "coordinator"
    PLANNER = "planner"
    CODER = "coder"
    TESTER = "tester"
    REVIEWER = "reviewer"
    DEVOPS = "devops"


@dataclass
class AgentMessage:
    """Message structure for agent communication."""

    id: str = field(default_factory=lambda: str(uuid4()))
    sender_id: str = ""
    recipient_id: str = ""
    message_type: MessageType = MessageType.COORDINATION
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    correlation_id: str | None = None


@dataclass
class TaskSpecification:
    """Specification for a task to be executed by an agent."""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    requirements: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: str | None = None
    dependencies: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class KnowledgeEntry:
    """Entry in the knowledge base."""

    id: str = field(default_factory=lambda: str(uuid4()))
    content: str = ""
    embedding: list[float] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    source_type: SourceType = SourceType.CONTEXT
    created_at: datetime = field(default_factory=datetime.utcnow)
    tags: list[str] = field(default_factory=list)


@dataclass
class AgentPRP:
    """Product Requirement Prompt optimized for agent consumption."""

    goal: str = ""
    justification: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    implementation_steps: list[str] = field(default_factory=list)
    validation_criteria: list[str] = field(default_factory=list)
    success_metrics: list[str] = field(default_factory=list)
    failure_recovery: list[str] = field(default_factory=list)


class AgentResponse(BaseModel):
    """Response from an agent after processing a task."""

    success: bool
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    execution_time: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ExecutionResult(BaseModel):
    """Result of PRP execution."""

    success: bool
    output: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    performance_metrics: dict[str, Any] = Field(default_factory=dict)
    execution_time: float = 0.0

    @classmethod
    def failure(cls, errors: list[str]) -> ExecutionResult:
        """Create a failure result."""
        return cls(success=False, errors=errors)

    @classmethod
    def success(cls, output: dict[str, Any]) -> ExecutionResult:
        """Create a success result."""
        return cls(success=True, output=output)


class FeatureRequest(BaseModel):
    """External feature request structure."""

    title: str
    description: str
    requirements: list[str]
    priority: TaskPriority = TaskPriority.MEDIUM
    acceptance_criteria: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
