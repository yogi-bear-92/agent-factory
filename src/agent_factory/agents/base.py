"""Base agent interface and implementation."""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Protocol

from langchain_core.language_models import BaseLanguageModel

from ..communication.redis_messenger import RedisMessageBus
from ..knowledge.chroma_store import ChromaVectorStore
from ..models import (
    AgentInfo,
    AgentMessage,
    AgentPRP,
    AgentResponse,
    AgentStatus,
    ExecutionResult,
    MessageType,
    TaskSpecification,
)

logger = logging.getLogger(__name__)


class AgentInterface(Protocol):
    """Protocol defining the agent interface."""

    async def process_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Process a Product Requirement Prompt."""
        ...

    async def execute_task(self, task: TaskSpecification) -> AgentResponse:
        """Execute a specific task."""
        ...

    async def handle_message(self, message: AgentMessage) -> None:
        """Handle incoming messages."""
        ...


class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm: BaseLanguageModel | None = None,
        capabilities: list[str] | None = None,
    ):
        """Initialize base agent.

        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name
            role: Role of the agent (e.g., "coder", "tester")
            knowledge_base: Vector store for knowledge
            message_bus: Communication layer
            llm: Language model for the agent
            capabilities: List of agent capabilities
        """
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.knowledge_base = knowledge_base
        self.message_bus = message_bus
        self.llm = llm
        self.capabilities = capabilities or []

        # Agent state
        self.info = AgentInfo(
            id=agent_id,
            name=name,
            role=role,
            status=AgentStatus.IDLE,
            capabilities=self.capabilities,
        )

        # Task tracking
        self.current_task: TaskSpecification | None = None
        self.task_history: list[AgentResponse] = []

        # Heartbeat
        self._heartbeat_task: asyncio.Task | None = None
        self._heartbeat_interval = 30  # seconds

        # Message handlers
        self._message_handlers = {
            MessageType.TASK_ASSIGNMENT: self._handle_task_assignment,
            MessageType.TASK_RESULT: self._handle_task_result,
            MessageType.COORDINATION: self._handle_coordination,
            MessageType.HEARTBEAT: self._handle_heartbeat,
        }

    async def start(self) -> None:
        """Start the agent."""
        logger.info(f"Starting agent {self.name} ({self.agent_id})")

        # Subscribe to agent-specific messages
        await self.message_bus.subscribe_to_agent_messages(
            self.agent_id, self.handle_message
        )

        # Subscribe to coordination broadcasts
        await self.message_bus.subscribe_to_broadcast(
            "coordination", self.handle_message
        )

        # Start heartbeat
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        # Update status
        self.info.status = AgentStatus.IDLE
        await self._send_status_update()

        logger.info(f"Agent {self.name} started successfully")

    async def stop(self) -> None:
        """Stop the agent."""
        logger.info(f"Stopping agent {self.name}")

        # Cancel heartbeat
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                pass

        # Update status
        self.info.status = AgentStatus.OFFLINE
        await self._send_status_update()

        logger.info(f"Agent {self.name} stopped")

    async def handle_message(self, message: AgentMessage) -> None:
        """Handle incoming messages.

        Args:
            message: Incoming message
        """
        logger.debug(f"Agent {self.name} received message: {message.message_type}")

        try:
            handler = self._message_handlers.get(message.message_type)
            if handler:
                await handler(message)
            else:
                logger.warning(f"No handler for message type: {message.message_type}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self._send_error_response(message, str(e))

    async def process_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Process a Product Requirement Prompt.

        Args:
            prp: PRP to process

        Returns:
            Execution result
        """
        start_time = time.time()

        try:
            # Update status
            self.info.status = AgentStatus.BUSY
            await self._send_status_update()

            # Get relevant context from knowledge base
            context = await self.knowledge_base.get_context_for_query(
                prp.goal, max_context_length=2000
            )

            # Add context to PRP
            enhanced_prp = AgentPRP(
                goal=prp.goal,
                justification=prp.justification,
                context={**prp.context, "retrieved_context": context},
                implementation_steps=prp.implementation_steps,
                validation_criteria=prp.validation_criteria,
                success_metrics=prp.success_metrics,
                failure_recovery=prp.failure_recovery,
                metadata=prp.metadata,
            )

            # Execute PRP
            result = await self._execute_prp(enhanced_prp)

            # Store outcome in knowledge base
            await self._store_execution_outcome(enhanced_prp, result)

            execution_time = time.time() - start_time
            result.execution_time = execution_time

            return result

        except Exception as e:
            logger.error(f"Error processing PRP: {e}")
            execution_time = time.time() - start_time
            return ExecutionResult.failure([str(e)], execution_time=execution_time)
        finally:
            # Reset status
            self.info.status = AgentStatus.IDLE
            await self._send_status_update()

    @abstractmethod
    async def _execute_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Execute PRP implementation (to be implemented by subclasses).

        Args:
            prp: Enhanced PRP with context

        Returns:
            Execution result
        """
        pass

    async def execute_task(self, task: TaskSpecification) -> AgentResponse:
        """Execute a specific task.

        Args:
            task: Task to execute

        Returns:
            Agent response
        """
        start_time = time.time()

        try:
            # Update current task
            self.current_task = task
            self.info.current_task = task.id
            self.info.status = AgentStatus.BUSY
            await self._send_status_update()

            # Execute task implementation
            result = await self._execute_task_impl(task)

            # Create response
            execution_time = time.time() - start_time
            response = AgentResponse(
                agent_id=self.agent_id,
                task_id=task.id,
                success=result.is_successful,
                result=result.output,
                error_message=None
                if result.is_successful
                else "; ".join(result.errors),
                execution_time=execution_time,
            )

            # Store in history
            self.task_history.append(response)

            return response

        except Exception as e:
            logger.error(f"Error executing task: {e}")
            execution_time = time.time() - start_time
            return AgentResponse(
                agent_id=self.agent_id,
                task_id=task.id,
                success=False,
                error_message=str(e),
                execution_time=execution_time,
            )
        finally:
            # Reset task state
            self.current_task = None
            self.info.current_task = None
            self.info.status = AgentStatus.IDLE
            await self._send_status_update()

    @abstractmethod
    async def _execute_task_impl(self, task: TaskSpecification) -> ExecutionResult:
        """Execute task implementation (to be implemented by subclasses).

        Args:
            task: Task to execute

        Returns:
            Execution result
        """
        pass

    async def _handle_task_assignment(self, message: AgentMessage) -> None:
        """Handle task assignment message.

        Args:
            message: Task assignment message
        """
        try:
            task_data = message.payload.get("task")
            if not task_data:
                raise ValueError("No task data in message")

            # Create task object
            task = TaskSpecification(**task_data)

            # Execute task
            response = await self.execute_task(task)

            # Send response
            response_message = AgentMessage(
                sender_id=self.agent_id,
                recipient_id=message.sender_id,
                message_type=MessageType.TASK_RESULT,
                payload={"response": response.to_dict()},
                correlation_id=message.correlation_id,
            )

            await self.message_bus.send_to_agent(message.sender_id, response_message)

        except Exception as e:
            logger.error(f"Error handling task assignment: {e}")
            await self._send_error_response(message, str(e))

    async def _handle_task_result(self, message: AgentMessage) -> None:
        """Handle task result message.

        Args:
            message: Task result message
        """
        # Default implementation - can be overridden
        logger.info(f"Received task result from {message.sender_id}")

    async def _handle_coordination(self, message: AgentMessage) -> None:
        """Handle coordination message.

        Args:
            message: Coordination message
        """
        # Default implementation - can be overridden
        logger.info(f"Received coordination message: {message.payload}")

    async def _handle_heartbeat(self, message: AgentMessage) -> None:
        """Handle heartbeat message.

        Args:
            message: Heartbeat message
        """
        # Update last heartbeat time
        self.info.last_heartbeat = datetime.now()

    async def _send_status_update(self) -> None:
        """Send status update to coordination channel."""
        status_message = AgentMessage(
            sender_id=self.agent_id,
            message_type=MessageType.COORDINATION,
            payload={"type": "status_update", "agent_info": self.info.to_dict()},
        )

        await self.message_bus.broadcast_message("coordination", status_message)

    async def _send_error_response(
        self, original_message: AgentMessage, error: str
    ) -> None:
        """Send error response.

        Args:
            original_message: Original message that caused error
            error: Error description
        """
        error_message = AgentMessage(
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            message_type=MessageType.ERROR,
            payload={"error": error, "original_message_id": original_message.id},
            correlation_id=original_message.correlation_id,
        )

        await self.message_bus.send_to_agent(original_message.sender_id, error_message)

    async def _heartbeat_loop(self) -> None:
        """Send periodic heartbeat messages."""
        try:
            while True:
                heartbeat_message = AgentMessage(
                    sender_id=self.agent_id,
                    message_type=MessageType.HEARTBEAT,
                    payload={"status": self.info.status.value},
                )

                await self.message_bus.broadcast_message("heartbeat", heartbeat_message)
                await asyncio.sleep(self._heartbeat_interval)

        except asyncio.CancelledError:
            logger.debug(f"Heartbeat cancelled for agent {self.name}")
        except Exception as e:
            logger.error(f"Error in heartbeat loop: {e}")

    async def _store_execution_outcome(
        self, prp: AgentPRP, result: ExecutionResult
    ) -> None:
        """Store execution outcome in knowledge base.

        Args:
            prp: PRP that was executed
            result: Execution result
        """
        try:
            from ..models import KnowledgeEntry, SourceType

            # Create knowledge entry for the outcome
            outcome_content = f"""
            PRP Goal: {prp.goal}
            Agent: {self.name} ({self.role})
            Success: {result.is_successful}
            Execution Time: {result.execution_time:.2f}s
            
            Implementation Steps:
            {chr(10).join(f"- {step}" for step in prp.implementation_steps)}
            
            Result:
            {result.output if result.is_successful else "; ".join(result.errors)}
            
            Performance Metrics:
            {result.performance_metrics}
            """

            entry = KnowledgeEntry(
                content=outcome_content.strip(),
                source_type=SourceType.PATTERN
                if result.is_successful
                else SourceType.FAILURE,
                tags=[self.role, "execution_outcome"],
                metadata={
                    "agent_id": self.agent_id,
                    "agent_role": self.role,
                    "prp_goal": prp.goal,
                    "success": result.is_successful,
                    "execution_time": result.execution_time,
                },
            )

            await self.knowledge_base.store_entry(entry)

        except Exception as e:
            logger.error(f"Failed to store execution outcome: {e}")

    def get_status(self) -> dict[str, Any]:
        """Get current agent status.

        Returns:
            Status information
        """
        return {
            "agent_info": self.info.to_dict(),
            "current_task": self.current_task.to_dict() if self.current_task else None,
            "task_history_count": len(self.task_history),
            "capabilities": self.capabilities,
        }
