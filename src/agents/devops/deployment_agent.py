"""Deployment agent for automated deployment and monitoring."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification
from ..base import BaseAgent

logger = logging.getLogger(__name__)


class DeploymentAgent(BaseAgent):
    """Agent responsible for deployment and monitoring."""

    def __init__(
        self,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_model: str = "llama3.2:latest",
        llm_base_url: str = "http://localhost:11434",
    ):
        super().__init__(
            agent_id="devops",
            agent_type=AgentType.DEVOPS,
            knowledge_base=knowledge_base,
            message_bus=message_bus,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
        )

        logger.info("DeploymentAgent initialized")

    def _build_task_prompt(self, task: TaskSpecification, context: list[str]) -> str:
        """Build deployment prompt."""
        context_str = "\n".join(context) if context else "No relevant context found."

        return f"""You are a DevOps agent responsible for deployment and infrastructure management.

Deployment Task:
Title: {task.title}
Description: {task.description}
Requirements: {", ".join(task.requirements) if task.requirements else "None specified"}

Relevant Context:
{context_str}

Please handle deployment including:
1. Infrastructure setup and configuration
2. Deployment pipeline execution
3. Health checks and monitoring setup
4. Rollback procedures if needed
5. Performance monitoring and alerting

Provide deployment scripts, configuration, and monitoring setup.
"""
