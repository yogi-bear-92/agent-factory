"""Redis-based message bus for agent communication."""

import asyncio
import json
import logging
from collections.abc import Callable
from typing import Any

import redis.asyncio as redis
from redis.asyncio import Redis

from ...models import AgentMessage, MessageType

logger = logging.getLogger(__name__)


class RedisMessageBus:
    """Redis-based message bus for asynchronous agent communication."""

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        db: int = 0,
        max_connections: int = 10,
    ):
        """Initialize Redis message bus.

        Args:
            redis_url: Redis connection URL
            db: Redis database number
            max_connections: Maximum connection pool size
        """
        self.redis_url = redis_url
        self.db = db
        self.max_connections = max_connections

        # Connection pools
        self.pool = redis.ConnectionPool.from_url(
            redis_url, db=db, max_connections=max_connections, retry_on_timeout=True
        )

        self.redis_client: Redis | None = None
        self.pubsub_client: Redis | None = None
        self.subscribers: dict[str, list[Callable]] = {}
        self.running = False

        logger.info(f"Initialized Redis message bus: {redis_url}")

    async def connect(self) -> None:
        """Establish Redis connections."""
        try:
            self.redis_client = redis.Redis(connection_pool=self.pool)
            self.pubsub_client = redis.Redis(connection_pool=self.pool)

            # Test connection
            await self.redis_client.ping()
            logger.info("Connected to Redis successfully")

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self) -> None:
        """Close Redis connections."""
        try:
            self.running = False

            if self.redis_client:
                await self.redis_client.aclose()

            if self.pubsub_client:
                await self.pubsub_client.aclose()

            logger.info("Disconnected from Redis")

        except Exception as e:
            logger.error(f"Error disconnecting from Redis: {e}")

    async def publish(self, channel: str, message: AgentMessage) -> bool:
        """Publish a message to a channel.

        Args:
            channel: Channel name to publish to
            message: Message to publish

        Returns:
            True if message was published successfully
        """
        try:
            if not self.redis_client:
                await self.connect()

            # Serialize message
            message_data = {
                "id": message.id,
                "sender_id": message.sender_id,
                "recipient_id": message.recipient_id,
                "message_type": message.message_type.value,
                "payload": message.payload,
                "timestamp": message.timestamp.isoformat(),
                "correlation_id": message.correlation_id,
            }

            message_json = json.dumps(message_data)

            # Publish to Redis
            result = await self.redis_client.publish(channel, message_json)

            logger.debug(f"Published message {message.id} to channel {channel}")
            return result > 0

        except Exception as e:
            logger.error(f"Failed to publish message to {channel}: {e}")
            return False

    async def subscribe(
        self, channel: str, handler: Callable[[AgentMessage], None]
    ) -> None:
        """Subscribe to a channel with a message handler.

        Args:
            channel: Channel name to subscribe to
            handler: Async function to handle received messages
        """
        try:
            if channel not in self.subscribers:
                self.subscribers[channel] = []

            self.subscribers[channel].append(handler)
            logger.info(f"Subscribed to channel: {channel}")

        except Exception as e:
            logger.error(f"Failed to subscribe to {channel}: {e}")

    async def start_listening(self) -> None:
        """Start listening for messages on subscribed channels."""
        try:
            if not self.pubsub_client:
                await self.connect()

            if not self.subscribers:
                logger.warning("No channels subscribed, nothing to listen to")
                return

            pubsub = self.pubsub_client.pubsub()

            # Subscribe to all channels
            for channel in self.subscribers.keys():
                await pubsub.subscribe(channel)
                logger.info(f"Listening on channel: {channel}")

            self.running = True

            # Listen for messages
            async for message in pubsub.listen():
                if not self.running:
                    break

                if message["type"] == "message":
                    await self._handle_message(
                        message["channel"].decode(), message["data"]
                    )

            await pubsub.unsubscribe()
            await pubsub.aclose()

        except Exception as e:
            logger.error(f"Error in message listening loop: {e}")
            raise

    async def _handle_message(self, channel: str, data: bytes) -> None:
        """Handle incoming message from Redis.

        Args:
            channel: Channel the message came from
            data: Raw message data
        """
        try:
            # Deserialize message
            message_data = json.loads(data.decode())

            # Reconstruct AgentMessage
            from datetime import datetime

            message = AgentMessage(
                id=message_data["id"],
                sender_id=message_data["sender_id"],
                recipient_id=message_data["recipient_id"],
                message_type=MessageType(message_data["message_type"]),
                payload=message_data["payload"],
                timestamp=datetime.fromisoformat(message_data["timestamp"]),
                correlation_id=message_data.get("correlation_id"),
            )

            # Call all handlers for this channel
            if channel in self.subscribers:
                for handler in self.subscribers[channel]:
                    try:
                        if asyncio.iscoroutinefunction(handler):
                            await handler(message)
                        else:
                            handler(message)
                    except Exception as e:
                        logger.error(f"Error in message handler: {e}")

            logger.debug(f"Handled message {message.id} from channel {channel}")

        except Exception as e:
            logger.error(f"Failed to handle message from {channel}: {e}")

    async def send_task(
        self, recipient_id: str, task_data: dict[str, Any], sender_id: str
    ) -> bool:
        """Send a task to a specific agent.

        Args:
            recipient_id: ID of the agent to receive the task
            task_data: Task data to send
            sender_id: ID of the sending agent

        Returns:
            True if task was sent successfully
        """
        try:
            message = AgentMessage(
                sender_id=sender_id,
                recipient_id=recipient_id,
                message_type=MessageType.TASK_ASSIGNMENT,
                payload=task_data,
            )

            return await self.publish(f"agent.{recipient_id}", message)

        except Exception as e:
            logger.error(f"Failed to send task: {e}")
            return False

    async def send_message(self, message: AgentMessage) -> bool:
        """Send a message to a specific agent.

        Args:
            message: Message to send

        Returns:
            True if message was sent successfully
        """
        try:
            if not message.recipient_id:
                logger.error("Message must have a recipient_id")
                return False

            return await self.publish(f"agent.{message.recipient_id}", message)

        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False

    async def send_result(
        self,
        recipient_id: str,
        result_data: dict[str, Any],
        sender_id: str,
        correlation_id: str | None = None,
    ) -> bool:
        """Send a task result to a specific agent.

        Args:
            recipient_id: ID of the agent to receive the result
            result_data: Result data
            sender_id: ID of the sending agent
            correlation_id: Optional correlation ID for tracking

        Returns:
            True if result was sent successfully
        """
        message = AgentMessage(
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=MessageType.TASK_RESULT,
            payload=result_data,
            correlation_id=correlation_id,
        )

        channel = f"agent.{recipient_id}"
        return await self.publish(channel, message)

    async def broadcast(self, topic: str, data: dict[str, Any], sender_id: str) -> bool:
        """Broadcast a message to all agents listening on a topic.

        Args:
            topic: Topic to broadcast to
            data: Data to broadcast
            sender_id: ID of the sending agent

        Returns:
            True if broadcast was successful
        """
        message = AgentMessage(
            sender_id=sender_id,
            recipient_id="broadcast",
            message_type=MessageType.COORDINATION,
            payload=data,
        )

        channel = f"broadcast.{topic}"
        return await self.publish(channel, message)

    async def send_heartbeat(self, agent_id: str) -> bool:
        """Send a heartbeat message from an agent.

        Args:
            agent_id: ID of the agent sending the heartbeat

        Returns:
            True if heartbeat was sent successfully
        """
        message = AgentMessage(
            sender_id=agent_id,
            recipient_id="system",
            message_type=MessageType.HEARTBEAT,
            payload={"status": "alive", "timestamp": "now"},
        )

        return await self.publish("system.heartbeat", message)

    async def get_channel_info(self, channel: str) -> dict[str, Any]:
        """Get information about a channel.

        Args:
            channel: Channel name

        Returns:
            Dictionary containing channel information
        """
        try:
            if not self.redis_client:
                await self.connect()

            # Get number of subscribers
            pubsub_channels = await self.redis_client.pubsub_channels(pattern=channel)
            num_subscribers = await self.redis_client.pubsub_numsub(channel)

            return {
                "channel": channel,
                "exists": channel in pubsub_channels,
                "subscribers": dict(num_subscribers).get(channel, 0),
            }

        except Exception as e:
            logger.error(f"Failed to get channel info for {channel}: {e}")
            return {}

    async def list_active_channels(self) -> list[str]:
        """List all active channels.

        Returns:
            List of active channel names
        """
        try:
            if not self.redis_client:
                await self.connect()

            channels = await self.redis_client.pubsub_channels()
            return [ch.decode() for ch in channels]

        except Exception as e:
            logger.error(f"Failed to list active channels: {e}")
            return []

    async def stop_listening(self) -> None:
        """Stop listening for messages."""
        self.running = False
        logger.info("Stopped message bus listening")

    async def health_check(self) -> bool:
        """Check if Redis connection is healthy.

        Returns:
            True if connection is healthy
        """
        try:
            if not self.redis_client:
                await self.connect()

            await self.redis_client.ping()
            return True

        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
