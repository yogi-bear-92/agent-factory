"""Core data models for the Agent Factory framework."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class MessageType(Enum):
    """Types of messages that can be sent between agents."""

    TASK_ASSIGNMENT = "task_assignment"
    TASK_RESULT = "task_result"
    TASK_UPDATE = "task_update"
    COORDINATION = "coordination"
    ERROR = "error"
    HEARTBEAT = "heartbeat"


class TaskPriority(Enum):
    """Priority levels for tasks."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SourceType(Enum):
    """Types of knowledge sources."""

    CODE = "code"
    DOCUMENTATION = "documentation"
    PRP = "prp"
    CONVERSATION = "conversation"
    PATTERN = "pattern"
    FAILURE = "failure"


class AgentStatus(Enum):
    """Status of an agent."""

    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class AgentMessage:
    """Message format for inter-agent communication."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    recipient_id: str = ""
    message_type: MessageType = MessageType.COORDINATION
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "message_type": self.message_type.value,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentMessage:
        """Create from dictionary."""
        return cls(
            id=data["id"],
            sender_id=data["sender_id"],
            recipient_id=data["recipient_id"],
            message_type=MessageType(data["message_type"]),
            payload=data["payload"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            correlation_id=data.get("correlation_id"),
        )


@dataclass
class TaskSpecification:
    """Specification for a task to be executed by an agent."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    requirements: list[str] = field(default_factory=list)
    acceptance_criteria: list[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_agent: str | None = None
    dependencies: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "requirements": self.requirements,
            "acceptance_criteria": self.acceptance_criteria,
            "priority": self.priority.value,
            "assigned_agent": self.assigned_agent,
            "dependencies": self.dependencies,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class KnowledgeEntry:
    """Entry in the knowledge base."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""
    embedding: list[float] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    source_type: SourceType = SourceType.DOCUMENTATION
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "source_type": self.source_type.value,
            "created_at": self.created_at.isoformat(),
            "tags": self.tags,
        }


@dataclass
class AgentPRP:
    """Product Requirement Prompt for agents."""

    goal: str = ""
    justification: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    implementation_steps: list[str] = field(default_factory=list)
    validation_criteria: list[str] = field(default_factory=list)
    success_metrics: list[str] = field(default_factory=list)
    failure_recovery: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "goal": self.goal,
            "justification": self.justification,
            "context": self.context,
            "implementation_steps": self.implementation_steps,
            "validation_criteria": self.validation_criteria,
            "success_metrics": self.success_metrics,
            "failure_recovery": self.failure_recovery,
            "metadata": self.metadata,
        }


@dataclass
class AgentResponse:
    """Response from an agent after processing a task or PRP."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str = ""
    task_id: str | None = None
    success: bool = False
    result: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "success": self.success,
            "result": self.result,
            "error_message": self.error_message,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class AgentInfo:
    """Information about an agent."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    role: str = ""
    status: AgentStatus = AgentStatus.IDLE
    capabilities: list[str] = field(default_factory=list)
    current_task: str | None = None
    last_heartbeat: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "status": self.status.value,
            "capabilities": self.capabilities,
            "current_task": self.current_task,
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class ExecutionResult:
    """Result of PRP or task execution."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_successful: bool = False
    output: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    performance_metrics: dict[str, float] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def success(cls, output: dict[str, Any], **kwargs) -> ExecutionResult:
        """Create a successful result."""
        return cls(is_successful=True, output=output, **kwargs)

    @classmethod
    def failure(cls, errors: list[str], **kwargs) -> ExecutionResult:
        """Create a failed result."""
        return cls(is_successful=False, errors=errors, **kwargs)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "is_successful": self.is_successful,
            "output": self.output,
            "errors": self.errors,
            "performance_metrics": self.performance_metrics,
            "artifacts": self.artifacts,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp.isoformat(),
        }
