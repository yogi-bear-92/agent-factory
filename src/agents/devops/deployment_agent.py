"""Deployment agent for automated deployment and monitoring."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification, AgentResponse, AgentPRP
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

    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process a deployment task and return a response.

        Args:
            task: Task specification to process

        Returns:
            Agent response with deployment result
        """
        try:
            logger.info(f"Processing deployment task: {task.title}")
            
            # Get relevant context for deployment
            context = await self.knowledge.get_relevant_context(
                query=f"{task.title} {task.description}", limit=5
            )
            
            # Build deployment prompt
            prompt = self._build_task_prompt(task, context)
            
            # Generate deployment plan using LLM
            deployment_result = await self.llm.agenerate([prompt])
            deployment_text = deployment_result.generations[0][0].text
            
            return AgentResponse(
                success=True,
                message="Deployment planning completed successfully",
                data={
                    "task_id": task.id,
                    "deployment_plan": deployment_text,
                    "context_used": context,
                    "deployment_status": "planned"
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to process deployment task: {e}")
            return AgentResponse(
                success=False,
                message=f"Deployment planning failed: {str(e)}",
                data={"task_id": task.id}
            )

    async def process_prp(self, prp: AgentPRP) -> AgentResponse:
        """Process a PRP and return a response.

        Args:
            prp: PRP to process

        Returns:
            Agent response with PRP result
        """
        try:
            logger.info(f"Processing PRP: {prp.goal}")
            
            # Convert PRP to deployment task
            task = TaskSpecification(
                title=prp.goal,
                description=prp.justification,
                requirements=prp.implementation_steps,
                acceptance_criteria=prp.validation_criteria
            )
            
            # Process as deployment task
            return await self.process_task(task)
            
        except Exception as e:
            logger.error(f"Failed to process PRP: {e}")
            return AgentResponse(
                success=False,
                message=f"PRP processing failed: {str(e)}",
                data={"prp_goal": prp.goal}
            )
