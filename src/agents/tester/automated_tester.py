"""Automated tester agent for test execution."""

import logging

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentType, TaskSpecification, AgentResponse, AgentPRP
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

    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process a testing task and return a response.

        Args:
            task: Task specification to process

        Returns:
            Agent response with testing result
        """
        try:
            logger.info(f"Processing testing task: {task.title}")
            
            # Get relevant context for testing
            context = await self.knowledge.get_relevant_context(
                query=f"{task.title} {task.description}", limit=5
            )
            
            # Build testing prompt
            prompt = self._build_task_prompt(task, context)
            
            # Generate tests using LLM
            test_result = await self.llm.agenerate([prompt])
            test_text = test_result.generations[0][0].text
            
            return AgentResponse(
                success=True,
                message="Test generation completed successfully",
                data={
                    "task_id": task.id,
                    "tests": test_text,
                    "context_used": context
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to process testing task: {e}")
            return AgentResponse(
                success=False,
                message=f"Testing failed: {str(e)}",
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
            
            # Convert PRP to testing task
            task = TaskSpecification(
                title=prp.goal,
                description=prp.justification,
                requirements=prp.implementation_steps,
                acceptance_criteria=prp.validation_criteria
            )
            
            # Process as testing task
            return await self.process_task(task)
            
        except Exception as e:
            logger.error(f"Failed to process PRP: {e}")
            return AgentResponse(
                success=False,
                message=f"PRP processing failed: {str(e)}",
                data={"prp_goal": prp.goal}
            )
