"""Code reviewer agent for quality assurance."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification
from ..base import BaseAgent

logger = logging.getLogger(__name__)


class CodeReviewer(BaseAgent):
    """Agent responsible for code review and quality assurance."""

    def __init__(
        self,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_model: str = "llama3.2:latest",
        llm_base_url: str = "http://localhost:11434",
    ):
        super().__init__(
            agent_id="reviewer",
            agent_type=AgentType.REVIEWER,
            knowledge_base=knowledge_base,
            message_bus=message_bus,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
        )

        logger.info("CodeReviewer initialized")

    def _build_task_prompt(self, task: TaskSpecification, context: list[str]) -> str:
        """Build code review prompt."""
        context_str = "\n".join(context) if context else "No relevant context found."

        return f"""You are a code reviewer responsible for ensuring high-quality, maintainable code.

Review Task:
Title: {task.title}
Description: {task.description}
Requirements: {", ".join(task.requirements) if task.requirements else "None specified"}

Relevant Context:
{context_str}

Please conduct a thorough code review focusing on:
1. Code quality and maintainability
2. Security vulnerabilities
3. Performance considerations
4. Adherence to coding standards
5. Documentation completeness
6. Test coverage adequacy

Provide detailed feedback and approval/rejection recommendation.
"""
