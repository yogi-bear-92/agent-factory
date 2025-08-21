"""Tests for BaseAgent implementation."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.agent_factory.models import (
    AgentMessage, MessageType, TaskSpecification, AgentPRP, 
    ExecutionResult, AgentStatus, AgentInfo
)
from src.agent_factory.agents.base import BaseAgent


class TestAgent(BaseAgent):
    """Test implementation of BaseAgent."""
    
    async def _execute_prp(self, prp):
        """Test PRP execution."""
        return ExecutionResult.success({"result": f"Executed: {prp.goal}"})
    
    async def _execute_task_impl(self, task):
        """Test task execution.""" 
        return ExecutionResult.success({"result": f"Completed: {task.title}"})


@pytest.fixture
def mock_knowledge_base():
    """Mock knowledge base."""
    mock = AsyncMock()
    mock.get_context_for_query = AsyncMock(return_value=["context1", "context2"])
    mock.store_entry = AsyncMock(return_value="entry_id")
    return mock


@pytest.fixture
def mock_message_bus():
    """Mock message bus."""
    mock = AsyncMock()
    mock.subscribe = AsyncMock()
    mock.publish = AsyncMock(return_value=True)
    mock.send_to_agent = AsyncMock(return_value=True)
    mock.broadcast_message = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def test_agent(mock_knowledge_base, mock_message_bus):
    """Create test agent instance."""
    return TestAgent(
        agent_id="test_agent_1",
        name="Test Agent",
        role="tester",
        knowledge_base=mock_knowledge_base,
        message_bus=mock_message_bus,
        capabilities=["testing", "validation"]
    )


@pytest.mark.asyncio
async def test_agent_initialization(test_agent):
    """Test agent initialization."""
    assert test_agent.agent_id == "test_agent_1"
    assert test_agent.name == "Test Agent"
    assert test_agent.role == "tester"
    assert test_agent.info.status == AgentStatus.IDLE
    assert "testing" in test_agent.capabilities
    assert test_agent.current_task is None


@pytest.mark.asyncio
async def test_process_prp(test_agent):
    """Test PRP processing."""
    prp = AgentPRP(
        goal="Test goal",
        justification="Testing PRP processing",
        implementation_steps=["step1", "step2"],
        validation_criteria=["criteria1"]
    )
    
    result = await test_agent.process_prp(prp)
    
    assert result.is_successful
    assert "Executed: Test goal" in str(result.output)
    assert result.execution_time > 0
    
    # Verify knowledge base was called
    test_agent.knowledge_base.get_context_for_query.assert_called_once()
    test_agent.knowledge_base.store_entry.assert_called_once()


@pytest.mark.asyncio
async def test_execute_task(test_agent):
    """Test task execution."""
    task = TaskSpecification(
        title="Test Task",
        description="Testing task execution",
        requirements=["req1", "req2"]
    )
    
    response = await test_agent.execute_task(task)
    
    assert response.success
    assert response.agent_id == "test_agent_1"
    assert response.task_id == task.id
    assert "Completed: Test Task" in str(response.result)
    assert response.execution_time > 0


if __name__ == "__main__":
    pytest.main([__file__])
