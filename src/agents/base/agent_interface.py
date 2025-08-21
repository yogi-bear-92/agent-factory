"""Base agent interface and abstract classes."""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Any

from langchain.llms.base import LLM
from langchain_community.llms import Ollama

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import (
    AgentMessage,
    AgentPRP,
    AgentResponse,
    AgentType,
    MessageType,
    TaskSpecification,
)

logger = logging.getLogger(__name__)


class AgentInterface(ABC):
    """Protocol defining the interface for all agents."""

    @abstractmethod
    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process a task and return a response."""
        pass

    @abstractmethod
    async def process_prp(self, prp: AgentPRP) -> AgentResponse:
        """Process a PRP and return a response."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the agent is healthy and operational."""
        pass


class BaseAgent(AgentInterface):
    """Base implementation for all agents in the system."""

    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_model: str = "llama3.2:latest",
        llm_base_url: str = "http://localhost:11434",
    ):
        """Initialize the base agent.

        Args:
            agent_id: Unique identifier for this agent
            agent_type: Type of agent (coordinator, planner, etc.)
            knowledge_base: Vector store for knowledge retrieval
            message_bus: Message bus for communication
            llm_model: LLM model name to use
            llm_base_url: Base URL for the LLM service
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.knowledge = knowledge_base
        self.messenger = message_bus

        # Initialize LLM
        self.llm = self._initialize_llm(llm_model, llm_base_url)

        # Agent state
        self.is_running = False
        self.current_task: TaskSpecification | None = None
        self.performance_metrics: dict[str, Any] = {}

        logger.info(f"Initialized {agent_type.value} agent: {agent_id}")

    def _initialize_llm(self, model: str, base_url: str) -> LLM:
        """Initialize the LLM for this agent.

        Args:
            model: Model name
            base_url: Base URL for the LLM service

        Returns:
            Initialized LLM instance
        """
        try:
            return Ollama(
                model=model,
                base_url=base_url,
                temperature=0.1,
                num_ctx=8192,
                repeat_penalty=1.1,
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

    async def start(self) -> None:
        """Start the agent and begin listening for messages."""
        try:
            self.is_running = True

            # Subscribe to agent-specific channel
            await self.messenger.subscribe(
                f"agent.{self.agent_id}", self.handle_message
            )

            # Subscribe to broadcast channels
            await self.messenger.subscribe(
                "broadcast.coordination", self.handle_broadcast
            )

            logger.info(f"Agent {self.agent_id} started and listening")

            # Send heartbeat to announce availability
            await self.messenger.send_heartbeat(self.agent_id)

        except Exception as e:
            logger.error(f"Failed to start agent {self.agent_id}: {e}")
            raise

    async def stop(self) -> None:
        """Stop the agent and cleanup resources."""
        try:
            self.is_running = False
            self.current_task = None

            logger.info(f"Agent {self.agent_id} stopped")

        except Exception as e:
            logger.error(f"Error stopping agent {self.agent_id}: {e}")

    async def handle_message(self, message: AgentMessage) -> None:
        """Handle incoming messages.

        Args:
            message: Received message
        """
        try:
            logger.debug(
                f"Agent {self.agent_id} received message: {message.message_type}"
            )

            if message.message_type == MessageType.TASK_ASSIGNMENT:
                await self._handle_task_assignment(message)
            elif message.message_type == MessageType.TASK_UPDATE:
                await self._handle_task_update(message)
            elif message.message_type == MessageType.COORDINATION:
                await self._handle_coordination(message)
            else:
                logger.warning(f"Unknown message type: {message.message_type}")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_error_response(message, e)

    async def handle_broadcast(self, message: AgentMessage) -> None:
        """Handle broadcast messages.

        Args:
            message: Broadcast message
        """
        try:
            logger.debug(f"Agent {self.agent_id} received broadcast: {message.payload}")

            # Override in subclasses for specific broadcast handling

        except Exception as e:
            logger.error(f"Error handling broadcast: {e}")

    async def _handle_task_assignment(self, message: AgentMessage) -> None:
        """Handle task assignment messages.

        Args:
            message: Task assignment message
        """
        try:
            # Parse task from message payload
            task_data = message.payload
            task = TaskSpecification(
                id=task_data.get("id", ""),
                title=task_data.get("title", ""),
                description=task_data.get("description", ""),
                requirements=task_data.get("requirements", []),
                acceptance_criteria=task_data.get("acceptance_criteria", []),
                priority=task_data.get("priority", "medium"),
                assigned_agent=self.agent_id,
            )

            # Process the task
            response = await self.process_task(task)

            # Send response back
            await self.messenger.send_result(
                recipient_id=message.sender_id,
                result_data={"task_id": task.id, "response": response.model_dump()},
                sender_id=self.agent_id,
                correlation_id=message.correlation_id,
            )

        except Exception as e:
            logger.error(f"Error handling task assignment: {e}")
            await self.send_error_response(message, e)

    async def _handle_task_update(self, message: AgentMessage) -> None:
        """Handle task update messages.

        Args:
            message: Task update message
        """
        # Override in subclasses if needed
        pass

    async def _handle_coordination(self, message: AgentMessage) -> None:
        """Handle coordination messages.

        Args:
            message: Coordination message
        """
        # Override in subclasses for specific coordination logic
        pass

    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process a task specification.

        Args:
            task: Task to process

        Returns:
            Agent response with results
        """
        start_time = time.time()

        try:
            self.current_task = task

            # Get relevant context from knowledge base
            context = await self.knowledge.get_relevant_context(
                query=f"{task.title} {task.description}", limit=5
            )

            # Build prompt for LLM
            prompt = self._build_task_prompt(task, context)

            # Process with LLM
            result = await self._process_with_llm(prompt)

            # Parse and validate result
            parsed_result = await self._parse_task_result(result, task)

            execution_time = time.time() - start_time

            response = AgentResponse(
                agent_id=self.agent_id,
                task_id=task.id,
                success=True,
                result=parsed_result,
                execution_time=execution_time,
            )

            # Store outcome in knowledge base
            await self._store_task_outcome(task, response)

            return response

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Error processing task {task.id}: {e}")

            return AgentResponse(
                agent_id=self.agent_id,
                task_id=task.id,
                success=False,
                error_message=str(e),
                execution_time=execution_time,
            )
        finally:
            self.current_task = None

    async def process_prp(self, prp: AgentPRP) -> AgentResponse:
        """Process a Product Requirement Prompt.

        Args:
            prp: PRP to process

        Returns:
            Agent response with results
        """
        start_time = time.time()

        try:
            # Get relevant context from knowledge base
            context = await self.knowledge.get_relevant_context(
                query=prp.goal, limit=10
            )

            # Inject context into PRP
            enhanced_prp = self._inject_context(prp, context)

            # Build prompt for LLM
            prompt = self._build_prp_prompt(enhanced_prp)

            # Process with LLM
            result = await self._process_with_llm(prompt)

            # Parse and validate result
            parsed_result = await self._parse_prp_result(result, prp)

            execution_time = time.time() - start_time

            response = AgentResponse(
                agent_id=self.agent_id,
                task_id="prp",
                success=True,
                result=parsed_result,
                execution_time=execution_time,
            )

            # Store outcome for learning
            await self.knowledge.store_outcome(prp, response)

            return response

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Error processing PRP: {e}")

            return AgentResponse(
                agent_id=self.agent_id,
                task_id="prp",
                success=False,
                error_message=str(e),
                execution_time=execution_time,
            )

    def _build_task_prompt(self, task: TaskSpecification, context: list[str]) -> str:
        """Build prompt for task processing.

        Args:
            task: Task specification
            context: Relevant context from knowledge base

        Returns:
            Formatted prompt string
        """
        context_str = "\n".join(context) if context else "No relevant context found."

        return f"""You are a {self.agent_type.value} agent processing a task.

Task Details:
Title: {task.title}
Description: {task.description}
Requirements: {", ".join(task.requirements)}
Acceptance Criteria: {", ".join(task.acceptance_criteria)}

Relevant Context:
{context_str}

Please process this task according to your role as a {self.agent_type.value} agent.
Provide a structured response with clear actions and outcomes.
"""

    def _build_prp_prompt(self, prp: AgentPRP) -> str:
        """Build prompt for PRP processing.

        Args:
            prp: Enhanced PRP with context

        Returns:
            Formatted prompt string
        """
        return f"""You are a {self.agent_type.value} agent processing a Product Requirement Prompt.

Goal: {prp.goal}
Justification: {prp.justification}

Implementation Steps:
{chr(10).join(f"- {step}" for step in prp.implementation_steps)}

Validation Criteria:
{chr(10).join(f"- {criterion}" for criterion in prp.validation_criteria)}

Context Information:
{chr(10).join(f"- {key}: {value}" for key, value in prp.context.items())}

Please execute this PRP according to your role as a {self.agent_type.value} agent.
Follow the implementation steps and ensure all validation criteria are met.
"""

    def _inject_context(self, prp: AgentPRP, context: list[str]) -> AgentPRP:
        """Inject retrieved context into PRP.

        Args:
            prp: Original PRP
            context: Context to inject

        Returns:
            Enhanced PRP with injected context
        """
        enhanced_prp = AgentPRP(
            goal=prp.goal,
            justification=prp.justification,
            context=prp.context.copy(),
            implementation_steps=prp.implementation_steps.copy(),
            validation_criteria=prp.validation_criteria.copy(),
            success_metrics=prp.success_metrics.copy(),
            failure_recovery=prp.failure_recovery.copy(),
        )

        # Add retrieved context
        enhanced_prp.context["retrieved_context"] = context

        return enhanced_prp

    async def _process_with_llm(self, prompt: str) -> str:
        """Process prompt with LLM.

        Args:
            prompt: Prompt to process

        Returns:
            LLM response
        """
        try:
            # Use asyncio to run the LLM in a thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self.llm.invoke, prompt)
            return result

        except Exception as e:
            logger.error(f"LLM processing failed: {e}")
            raise

    async def _parse_task_result(
        self, result: str, task: TaskSpecification
    ) -> dict[str, Any]:
        """Parse and validate task result.

        Args:
            result: Raw LLM result
            task: Original task

        Returns:
            Parsed result dictionary
        """
        # Basic parsing - override in subclasses for specific formats
        return {
            "raw_output": result,
            "task_id": task.id,
            "processed_by": self.agent_type.value,
        }

    async def _parse_prp_result(self, result: str, prp: AgentPRP) -> dict[str, Any]:
        """Parse and validate PRP result.

        Args:
            result: Raw LLM result
            prp: Original PRP

        Returns:
            Parsed result dictionary
        """
        # Basic parsing - override in subclasses for specific formats
        return {
            "raw_output": result,
            "goal": prp.goal,
            "processed_by": self.agent_type.value,
        }

    async def _store_task_outcome(
        self, task: TaskSpecification, response: AgentResponse
    ) -> None:
        """Store task outcome in knowledge base.

        Args:
            task: Processed task
            response: Agent response
        """
        try:
            from ...models import KnowledgeEntry, SourceType

            outcome_type = (
                SourceType.SUCCESS if response.success else SourceType.FAILURE
            )

            entry = KnowledgeEntry(
                content=f"Task Outcome: {task.title}",
                metadata={
                    "task_id": task.id,
                    "agent_type": self.agent_type.value,
                    "success": response.success,
                    "execution_time": response.execution_time,
                },
                source_type=outcome_type,
                tags=["task", "outcome", self.agent_type.value],
            )

            await self.knowledge.store_knowledge(entry)

        except Exception as e:
            logger.error(f"Failed to store task outcome: {e}")

    async def send_error_response(
        self, original_message: AgentMessage, error: Exception
    ) -> None:
        """Send error response for a failed message.

        Args:
            original_message: Message that caused the error
            error: Error that occurred
        """
        try:
            error_message = AgentMessage(
                sender_id=self.agent_id,
                recipient_id=original_message.sender_id,
                message_type=MessageType.ERROR,
                payload={
                    "error": str(error),
                    "original_message_id": original_message.id,
                },
                correlation_id=original_message.correlation_id,
            )

            await self.messenger.publish(
                f"agent.{original_message.sender_id}", error_message
            )

        except Exception as e:
            logger.error(f"Failed to send error response: {e}")

    async def health_check(self) -> bool:
        """Check if the agent is healthy and operational.

        Returns:
            True if agent is healthy
        """
        try:
            # Check if agent is running
            if not self.is_running:
                return False

            # Check knowledge base connection
            knowledge_healthy = await self.knowledge.get_stats() is not None

            # Check message bus connection
            messenger_healthy = await self.messenger.health_check()

            # Test LLM connection
            try:
                await self._process_with_llm("Test prompt")
                llm_healthy = True
            except:
                llm_healthy = False

            return knowledge_healthy and messenger_healthy and llm_healthy

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    async def get_metrics(self) -> dict[str, Any]:
        """Get performance metrics for this agent.

        Returns:
            Dictionary of performance metrics
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "is_running": self.is_running,
            "current_task": self.current_task.id if self.current_task else None,
            "performance_metrics": self.performance_metrics,
        }
