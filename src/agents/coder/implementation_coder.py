"""Implementation coder agent for code generation."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification, AgentResponse, AgentPRP
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

    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process an implementation task and return a response.

        Args:
            task: Task specification to process

        Returns:
            Agent response with implementation result
        """
        try:
            logger.info(f"Processing implementation task: {task.title}")
            
            # Get relevant context for implementation
            context = await self.knowledge.get_relevant_context(
                query=f"{task.title} {task.description}", limit=5
            )
            
            # Build implementation prompt
            prompt = self._build_task_prompt(task, context)
            
            # Generate code using LLM
            code_result = await self.llm.agenerate([prompt])
            code_text = code_result.generations[0][0].text
            
            return AgentResponse(
                success=True,
                message="Code implementation completed successfully",
                data={
                    "task_id": task.id,
                    "code": code_text,
                    "context_used": context
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to process implementation task: {e}")
            return AgentResponse(
                success=False,
                message=f"Implementation failed: {str(e)}",
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
            
            # Convert PRP to implementation task
            task = TaskSpecification(
                title=prp.goal,
                description=prp.justification,
                requirements=prp.implementation_steps,
                acceptance_criteria=prp.validation_criteria
            )
            
            # Process as implementation task
            return await self.process_task(task)
            
        except Exception as e:
            logger.error(f"Failed to process PRP: {e}")
            return AgentResponse(
                success=False,
                message=f"PRP processing failed: {str(e)}",
                data={"prp_goal": prp.goal}
            )
