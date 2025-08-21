"""Tests for RedisMessageBus implementation."""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src.agent_factory.models import AgentMessage, MessageType
from src.communication.message_bus.redis_messenger import RedisMessageBus


@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    mock = AsyncMock()
    mock.ping = AsyncMock(return_value=True)
    mock.publish = AsyncMock(return_value=1)
    mock.pubsub = MagicMock()
    mock.aclose = AsyncMock()
    return mock


@pytest.fixture 
def message_bus():
    """Create RedisMessageBus instance for testing."""
    return RedisMessageBus(redis_url="redis://localhost:6379")


@pytest.mark.asyncio
async def test_basic_publish_subscribe(message_bus, mock_redis):
    """Test basic publish/subscribe functionality."""
    with patch('redis.asyncio.Redis') as mock_redis_class:
        mock_redis_class.return_value = mock_redis
        message_bus.redis_client = mock_redis
        message_bus.pubsub_client = mock_redis
        
        # Create test message
        message = AgentMessage(
            sender_id="agent1",
            recipient_id="agent2", 
            message_type=MessageType.TASK_ASSIGNMENT,
            payload={"task": "test"}
        )
        
        # Test publish
        result = await message_bus.publish("test_channel", message)
        assert result is True
        mock_redis.publish.assert_called_once()


@pytest.mark.asyncio
async def test_connection_management(message_bus, mock_redis):
    """Test connection establishment and cleanup."""
    with patch('redis.asyncio.ConnectionPool') as mock_pool, \
         patch('redis.asyncio.Redis') as mock_redis_class:
        
        mock_redis_class.return_value = mock_redis
        
        # Test connect
        await message_bus.connect()
        assert message_bus.redis_client is not None
        assert message_bus.pubsub_client is not None
        mock_redis.ping.assert_called_once()
        
        # Test disconnect
        await message_bus.disconnect()
        mock_redis.aclose.assert_called()


@pytest.mark.asyncio 
async def test_task_messaging(message_bus, mock_redis):
    """Test task assignment and result messaging."""
    with patch('redis.asyncio.Redis') as mock_redis_class:
        mock_redis_class.return_value = mock_redis
        message_bus.redis_client = mock_redis
        
        # Test send task
        result = await message_bus.send_task(
            recipient_id="agent2",
            task_data={"task": "implement feature"},
            sender_id="coordinator"
        )
        
        assert result is True
        mock_redis.publish.assert_called()
        
        # Test send result
        result = await message_bus.send_result(
            recipient_id="coordinator", 
            result_data={"status": "completed"},
            sender_id="agent2"
        )
        
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__])
