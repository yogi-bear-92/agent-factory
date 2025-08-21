"""Implementation coder agent for code generation."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification
from ..base import BaseAgent

logger = logging.getLogger(__name__)


class ImplementationCoder(BaseAgent):
    """Agent responsible for code implementation."""

    def __init__(
        self,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_model: str = "llama3.2:latest",
        llm_base_url: str = "http://localhost:11434",
    ):
        super().__init__(
            agent_id="coder",
            agent_type=AgentType.CODER,
            knowledge_base=knowledge_base,
            message_bus=message_bus,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
        )

        logger.info("ImplementationCoder initialized")

    def _build_task_prompt(self, task: TaskSpecification, context: list[str]) -> str:
        """Build code implementation prompt."""
        context_str = "\n".join(context) if context else "No relevant context found."

        return f"""You are a code implementation agent responsible for writing production-ready code.

Implementation Task:
Title: {task.title}
Description: {task.description}
Requirements: {", ".join(task.requirements) if task.requirements else "None specified"}

Relevant Context:
{context_str}

Please implement this feature following best practices:
1. Write clean, maintainable code
2. Include proper error handling
3. Add type hints and documentation
4. Follow existing code patterns
5. Ensure security and performance

Provide the complete implementation with file structure and code.
"""
