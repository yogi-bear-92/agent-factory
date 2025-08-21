"""Test core data models."""

import pytest
from datetime import datetime
from agent_factory.models import (
    AgentMessage,
    TaskSpecification,
    KnowledgeEntry,
    AgentPRP,
    MessageType,
    TaskPriority,
    SourceType
)


def test_agent_message_creation():
    """Test AgentMessage creation and serialization."""
    message = AgentMessage(
        sender_id="agent_1",
        recipient_id="agent_2",
        message_type=MessageType.TASK_ASSIGNMENT,
        payload={"test": "data"}
    )
    
    assert message.sender_id == "agent_1"
    assert message.recipient_id == "agent_2"
    assert message.message_type == MessageType.TASK_ASSIGNMENT
    assert message.payload == {"test": "data"}
    assert message.id is not None
    assert isinstance(message.timestamp, datetime)


def test_agent_message_serialization():
    """Test AgentMessage to_dict and from_dict."""
    original = AgentMessage(
        sender_id="agent_1",
        recipient_id="agent_2",
        message_type=MessageType.COORDINATION,
        payload={"key": "value"}
    )
    
    # Test serialization
    data = original.to_dict()
    assert isinstance(data, dict)
    assert data["sender_id"] == "agent_1"
    assert data["message_type"] == "coordination"
    
    # Test deserialization
    restored = AgentMessage.from_dict(data)
    assert restored.sender_id == original.sender_id
    assert restored.recipient_id == original.recipient_id
    assert restored.message_type == original.message_type
    assert restored.payload == original.payload


def test_task_specification():
    """Test TaskSpecification creation."""
    task = TaskSpecification(
        title="Test Task",
        description="A test task",
        requirements=["req1", "req2"],
        priority=TaskPriority.HIGH
    )
    
    assert task.title == "Test Task"
    assert task.priority == TaskPriority.HIGH
    assert len(task.requirements) == 2
    assert task.id is not None


def test_knowledge_entry():
    """Test KnowledgeEntry creation."""
    entry = KnowledgeEntry(
        content="Test knowledge content",
        source_type=SourceType.CODE,
        tags=["test", "example"]
    )
    
    assert entry.content == "Test knowledge content"
    assert entry.source_type == SourceType.CODE
    assert entry.tags == ["test", "example"]
    assert entry.id is not None


def test_agent_prp():
    """Test AgentPRP creation."""
    prp = AgentPRP(
        goal="Test goal",
        justification="Test justification",
        implementation_steps=["step1", "step2"]
    )
    
    assert prp.goal == "Test goal"
    assert prp.justification == "Test justification"
    assert len(prp.implementation_steps) == 2