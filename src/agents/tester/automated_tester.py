"""Automated tester agent for test execution."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification
from ..base import BaseAgent

logger = logging.getLogger(__name__)


class AutomatedTester(BaseAgent):
    """Agent responsible for automated testing."""

    def __init__(
        self,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_model: str = "llama3.2:latest",
        llm_base_url: str = "http://localhost:11434",
    ):
        super().__init__(
            agent_id="tester",
            agent_type=AgentType.TESTER,
            knowledge_base=knowledge_base,
            message_bus=message_bus,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
        )

        logger.info("AutomatedTester initialized")

    def _build_task_prompt(self, task: TaskSpecification, context: list[str]) -> str:
        """Build testing prompt."""
        context_str = "\n".join(context) if context else "No relevant context found."

        return f"""You are an automated testing agent responsible for comprehensive test coverage.

Testing Task:
Title: {task.title}
Description: {task.description}
Requirements: {", ".join(task.requirements) if task.requirements else "None specified"}

Relevant Context:
{context_str}

Please create comprehensive tests including:
1. Unit tests for individual functions
2. Integration tests for component interaction
3. End-to-end tests for user workflows
4. Performance and load tests
5. Security and edge case tests

Provide test code, test data, and execution instructions.
"""
