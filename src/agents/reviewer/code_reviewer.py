"""Code reviewer agent for quality assurance."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification, AgentResponse, AgentPRP
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

    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process a code review task and return a response.

        Args:
            task: Task specification to process

        Returns:
            Agent response with review result
        """
        try:
            logger.info(f"Processing code review task: {task.title}")
            
            # Get relevant context for review
            context = await self.knowledge.get_relevant_context(
                query=f"{task.title} {task.description}", limit=5
            )
            
            # Build review prompt
            prompt = self._build_task_prompt(task, context)
            
            # Generate review using LLM
            review_result = await self.llm.agenerate([prompt])
            review_text = review_result.generations[0][0].text
            
            return AgentResponse(
                success=True,
                message="Code review completed successfully",
                data={
                    "task_id": task.id,
                    "review": review_text,
                    "context_used": context,
                    "approval_status": "pending"
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to process code review task: {e}")
            return AgentResponse(
                success=False,
                message=f"Code review failed: {str(e)}",
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
            
            # Convert PRP to review task
            task = TaskSpecification(
                title=prp.goal,
                description=prp.justification,
                requirements=prp.implementation_steps,
                acceptance_criteria=prp.validation_criteria
            )
            
            # Process as review task
            return await self.process_task(task)
            
        except Exception as e:
            logger.error(f"Failed to process PRP: {e}")
            return AgentResponse(
                success=False,
                message=f"PRP processing failed: {str(e)}",
                data={"prp_goal": prp.goal}
            )
