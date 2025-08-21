"""Feature planner agent for task breakdown and PRP generation."""

import logging
from typing import Any

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentPRP, AgentType, TaskSpecification, AgentResponse
from ..base import BaseAgent

logger = logging.getLogger(__name__)


class FeaturePlanner(BaseAgent):
    """Agent responsible for breaking down features into implementable tasks."""

    def __init__(
        self,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_model: str = "llama3.2:latest",
        llm_base_url: str = "http://localhost:11434",
    ):
        """Initialize the FeaturePlanner.

        Args:
            knowledge_base: Vector store for knowledge retrieval
            message_bus: Message bus for agent communication
            llm_model: LLM model name
            llm_base_url: LLM service base URL
        """
        super().__init__(
            agent_id="planner",
            agent_type=AgentType.PLANNER,
            knowledge_base=knowledge_base,
            message_bus=message_bus,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
        )

        logger.info("FeaturePlanner initialized")

    async def _parse_task_result(
        self, result: str, task: TaskSpecification
    ) -> dict[str, Any]:
        """Parse planning result into structured task breakdown.

        Args:
            result: Raw LLM planning result
            task: Original planning task

        Returns:
            Structured task breakdown
        """
        try:
            # Extract feature planning from result
            feature_id = task.description.get("feature_id", "unknown")

            # Generate implementation tasks
            tasks = await self._generate_implementation_tasks(result, task)

            # Generate PRP if needed
            prp = await self._generate_prp(result, task)

            return {
                "feature_id": feature_id,
                "tasks": tasks,
                "prp": prp,
                "planning_notes": result,
                "planner_id": self.agent_id,
            }

        except Exception as e:
            logger.error(f"Failed to parse planning result: {e}")
            return {"error": str(e), "raw_result": result}

    async def _generate_implementation_tasks(
        self, planning_result: str, task: TaskSpecification
    ) -> list[dict[str, Any]]:
        """Generate implementation tasks from planning result.

        Args:
            planning_result: LLM planning output
            task: Original planning task

        Returns:
            List of implementation tasks
        """
        try:
            # Parse requirements from task
            requirements = task.requirements

            # Generate tasks based on typical development workflow
            tasks = []

            # Core implementation task
            tasks.append(
                {
                    "id": f"impl_{task.id}",
                    "title": f"Implement {task.title}",
                    "description": f"Core implementation for {task.description}",
                    "assigned_agent": "coder",
                    "dependencies": [],
                    "priority": "high",
                }
            )

            # Testing task
            tasks.append(
                {
                    "id": f"test_{task.id}",
                    "title": f"Test {task.title}",
                    "description": f"Write and run tests for {task.title}",
                    "assigned_agent": "tester",
                    "dependencies": [f"impl_{task.id}"],
                    "priority": "high",
                }
            )

            # Review task
            tasks.append(
                {
                    "id": f"review_{task.id}",
                    "title": f"Review {task.title}",
                    "description": f"Code review and quality check for {task.title}",
                    "assigned_agent": "reviewer",
                    "dependencies": [f"impl_{task.id}"],
                    "priority": "medium",
                }
            )

            # Deployment task
            tasks.append(
                {
                    "id": f"deploy_{task.id}",
                    "title": f"Deploy {task.title}",
                    "description": f"Deploy and monitor {task.title}",
                    "assigned_agent": "devops",
                    "dependencies": [f"test_{task.id}", f"review_{task.id}"],
                    "priority": "medium",
                }
            )

            return tasks

        except Exception as e:
            logger.error(f"Failed to generate tasks: {e}")
            return []

    async def _generate_prp(
        self, planning_result: str, task: TaskSpecification
    ) -> dict[str, Any]:
        """Generate PRP for the feature.

        Args:
            planning_result: LLM planning output
            task: Original planning task

        Returns:
            Generated PRP
        """
        try:
            # Get relevant context for PRP generation
            context = await self.knowledge.get_relevant_context(
                query=f"{task.title} {task.description}", limit=5
            )

            prp = AgentPRP(
                goal=f"Implement {task.title}",
                justification=f"Required to deliver {task.description}",
                context={
                    "requirements": task.requirements,
                    "planning_context": context,
                    "original_task": task.id,
                },
                implementation_steps=[
                    "Analyze requirements and design approach",
                    "Implement core functionality",
                    "Write comprehensive tests",
                    "Perform code review",
                    "Deploy and validate",
                ],
                validation_criteria=[
                    "All tests pass",
                    "Code review approved",
                    "Deployment successful",
                    "Requirements met",
                ],
                success_metrics=[
                    "Feature works as specified",
                    "Performance meets requirements",
                    "No critical issues found",
                ],
                failure_recovery=[
                    "Check logs for errors",
                    "Verify dependencies",
                    "Review implementation approach",
                ],
            )

            return {
                "goal": prp.goal,
                "justification": prp.justification,
                "context": prp.context,
                "implementation_steps": prp.implementation_steps,
                "validation_criteria": prp.validation_criteria,
                "success_metrics": prp.success_metrics,
                "failure_recovery": prp.failure_recovery,
            }

        except Exception as e:
            logger.error(f"Failed to generate PRP: {e}")
            return {}

    def _build_task_prompt(self, task: TaskSpecification, context: list[str]) -> str:
        """Build planning-specific prompt.

        Args:
            task: Planning task
            context: Relevant context

        Returns:
            Planning prompt
        """
        context_str = "\n".join(context) if context else "No relevant context found."

        return f"""You are a feature planner responsible for breaking down features into implementable tasks.

Feature to Plan:
Title: {task.title}
Description: {task.description}
Requirements: {", ".join(task.requirements) if task.requirements else "None specified"}

Relevant Context:
{context_str}

Please analyze this feature and provide:
1. Technical approach and architecture considerations
2. Implementation phases and dependencies
3. Risk assessment and mitigation strategies
4. Testing and validation approach
5. Deployment considerations

Focus on creating a clear, actionable plan that other agents can execute.
"""

    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process a planning task and return a response.

        Args:
            task: Task specification to process

        Returns:
            Agent response with planning result
        """
        try:
            logger.info(f"Processing planning task: {task.title}")
            
            # Get relevant context for planning
            context = await self.knowledge.get_relevant_context(
                query=f"{task.title} {task.description}", limit=5
            )
            
            # Build planning prompt
            prompt = self._build_task_prompt(task, context)
            
            # Generate planning using LLM
            planning_result = await self.llm.agenerate([prompt])
            result_text = planning_result.generations[0][0].text
            
            # Parse and structure the result
            structured_result = await self._parse_task_result(result_text, task)
            
            return AgentResponse(
                success=True,
                message="Planning completed successfully",
                data=structured_result
            )
            
        except Exception as e:
            logger.error(f"Failed to process planning task: {e}")
            return AgentResponse(
                success=False,
                message=f"Planning failed: {str(e)}",
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
            
            # Convert PRP to planning task
            task = TaskSpecification(
                title=prp.goal,
                description=prp.justification,
                requirements=prp.implementation_steps,
                acceptance_criteria=prp.validation_criteria
            )
            
            # Process as planning task
            return await self.process_task(task)
            
        except Exception as e:
            logger.error(f"Failed to process PRP: {e}")
            return AgentResponse(
                success=False,
                message=f"PRP processing failed: {str(e)}",
                data={"prp_goal": prp.goal}
            )
