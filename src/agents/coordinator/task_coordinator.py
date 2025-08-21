"""Task coordinator agent for high-level orchestration."""

import asyncio
import logging
from typing import Any
from uuid import uuid4

from ...communication.message_bus import RedisMessageBus
from ...knowledge.vector_store import ChromaVectorStore
from ...models import (
    AgentMessage,
    AgentType,
    FeatureRequest,
    AgentResponse,
    AgentPRP,
    TaskSpecification,
    MessageType,
)
from ...workflows.prp_engine import AgentPRPProcessor
from ..base import BaseAgent

logger = logging.getLogger(__name__)


class TaskCoordinator(BaseAgent):
    """Central coordination agent for task orchestration and workflow management."""

    def __init__(
        self,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_model: str = "llama3.2:latest",
        llm_base_url: str = "http://localhost:11434",
    ):
        """Initialize the TaskCoordinator.

        Args:
            knowledge_base: Vector store for knowledge retrieval
            message_bus: Message bus for agent communication
            llm_model: LLM model name
            llm_base_url: LLM service base URL
        """
        super().__init__(
            agent_id="coordinator",
            agent_type=AgentType.COORDINATOR,
            knowledge_base=knowledge_base,
            message_bus=message_bus,
            llm_model=llm_model,
            llm_base_url=llm_base_url,
        )

        self.prp_processor = AgentPRPProcessor(knowledge_base)
        self.active_features: dict[str, FeatureRequest] = {}
        self.task_assignments: dict[str, str] = {}  # task_id -> agent_id
        self.agent_status: dict[str, str] = {}  # agent_id -> status

        logger.info("TaskCoordinator initialized")

    async def handle_feature_request(self, feature_request: FeatureRequest) -> str:
        """Handle incoming feature request and orchestrate implementation.

        Args:
            feature_request: Feature to implement

        Returns:
            Feature ID for tracking
        """
        try:
            feature_id = str(uuid4())
            self.active_features[feature_id] = feature_request

            logger.info(f"Received feature request: {feature_request.title}")

            # Start feature implementation workflow
            await self._orchestrate_feature_implementation(feature_id, feature_request)

            return feature_id

        except Exception as e:
            logger.error(f"Failed to handle feature request: {e}")
            raise

    async def _orchestrate_feature_implementation(
        self, feature_id: str, feature_request: FeatureRequest
    ) -> None:
        """Orchestrate the complete feature implementation workflow.

        Args:
            feature_id: Unique feature identifier
            feature_request: Feature specification
        """
        try:
            # Step 1: Send to planner for task breakdown
            await self._assign_to_planner(feature_id, feature_request)

            # Step 2: Wait for planning completion
            planning_result = await self._wait_for_planning(feature_id)

            if not planning_result:
                logger.error(f"Planning failed for feature {feature_id}")
                return

            # Step 3: Coordinate implementation tasks
            await self._coordinate_implementation_tasks(feature_id, planning_result)

            # Step 4: Monitor progress and handle coordination
            await self._monitor_feature_progress(feature_id)

        except Exception as e:
            logger.error(f"Feature orchestration failed: {e}")

    async def _assign_to_planner(
        self, feature_id: str, feature_request: FeatureRequest
    ) -> None:
        """Assign feature to planner agent for breakdown.

        Args:
            feature_id: Feature identifier
            feature_request: Feature specification
        """
        task_data = {
            "id": f"plan_{feature_id}",
            "title": f"Plan feature: {feature_request.title}",
            "description": feature_request.description,
            "requirements": feature_request.requirements,
            "feature_id": feature_id,
            "type": "feature_planning",
        }

        await self.messenger.send_task(
            recipient_id="planner",
            task_data=task_data,
            sender_id=self.agent_id,
            correlation_id=feature_id,
        )

        logger.info(f"Assigned feature {feature_id} to planner")

    async def _wait_for_planning(
        self, feature_id: str, timeout: int = 300
    ) -> dict[str, Any] | None:
        """Wait for planning completion.

        Args:
            feature_id: Feature identifier
            timeout: Timeout in seconds

        Returns:
            Planning result or None if timeout
        """
        # This would be implemented with proper async waiting
        # For now, return a mock result
        await asyncio.sleep(1)  # Simulate planning time

        return {
            "feature_id": feature_id,
            "tasks": [
                {
                    "id": f"task_1_{feature_id}",
                    "title": "Implement core functionality",
                    "assigned_agent": "coder",
                    "dependencies": [],
                },
                {
                    "id": f"task_2_{feature_id}",
                    "title": "Write tests",
                    "assigned_agent": "tester",
                    "dependencies": [f"task_1_{feature_id}"],
                },
                {
                    "id": f"task_3_{feature_id}",
                    "title": "Code review",
                    "assigned_agent": "reviewer",
                    "dependencies": [f"task_1_{feature_id}"],
                },
                {
                    "id": f"task_4_{feature_id}",
                    "title": "Deploy",
                    "assigned_agent": "devops",
                    "dependencies": [f"task_2_{feature_id}", f"task_3_{feature_id}"],
                },
            ],
        }

    async def _coordinate_implementation_tasks(
        self, feature_id: str, planning_result: dict[str, Any]
    ) -> None:
        """Coordinate implementation tasks based on planning result.

        Args:
            feature_id: Feature identifier
            planning_result: Result from planner agent
        """
        try:
            tasks = planning_result.get("tasks", [])

            # Build dependency graph
            task_dependencies = {}
            for task in tasks:
                task_dependencies[task["id"]] = task.get("dependencies", [])

            # Execute tasks respecting dependencies
            completed_tasks = set()

            while len(completed_tasks) < len(tasks):
                # Find tasks ready to execute
                ready_tasks = []
                for task in tasks:
                    task_id = task["id"]
                    if task_id not in completed_tasks and all(
                        dep in completed_tasks for dep in task_dependencies[task_id]
                    ):
                        ready_tasks.append(task)

                # Execute ready tasks in parallel
                if ready_tasks:
                    await self._execute_tasks_parallel(ready_tasks, feature_id)

                    # Mark tasks as completed (simplified)
                    for task in ready_tasks:
                        completed_tasks.add(task["id"])
                        logger.info(f"Completed task: {task['title']}")

                # Small delay to prevent tight loop
                await asyncio.sleep(1)

            logger.info(f"All tasks completed for feature {feature_id}")

        except Exception as e:
            logger.error(f"Task coordination failed: {e}")

    async def _execute_tasks_parallel(
        self, tasks: list[dict[str, Any]], feature_id: str
    ) -> None:
        """Execute multiple tasks in parallel.

        Args:
            tasks: List of tasks to execute
            feature_id: Feature identifier
        """

        async def execute_single_task(task: dict[str, Any]) -> None:
            """Execute a single task."""
            try:
                task_data = {
                    "id": task["id"],
                    "title": task["title"],
                    "description": task.get("description", ""),
                    "feature_id": feature_id,
                    "type": "implementation",
                }

                await self.messenger.send_task(
                    recipient_id=task["assigned_agent"],
                    task_data=task_data,
                    sender_id=self.agent_id,
                    correlation_id=feature_id,
                )

                # Wait for task completion (simplified)
                await asyncio.sleep(2)  # Simulate task execution time

            except Exception as e:
                logger.error(f"Failed to execute task {task['id']}: {e}")

        # Execute all tasks concurrently
        await asyncio.gather(*[execute_single_task(task) for task in tasks])

    async def _monitor_feature_progress(self, feature_id: str) -> None:
        """Monitor progress of feature implementation.

        Args:
            feature_id: Feature identifier
        """
        try:
            # Implementation would track actual task progress
            # For now, just log completion
            logger.info(f"Feature {feature_id} implementation completed")

            # Store successful outcome
            from ...models import KnowledgeEntry, SourceType

            entry = KnowledgeEntry(
                content=f"Successfully completed feature: {self.active_features[feature_id].title}",
                metadata={
                    "feature_id": feature_id,
                    "feature_title": self.active_features[feature_id].title,
                    "coordinator": self.agent_id,
                },
                source_type=SourceType.SUCCESS,
                tags=["feature", "completion", "coordination"],
            )

            await self.knowledge.store_knowledge(entry)

        except Exception as e:
            logger.error(f"Feature monitoring failed: {e}")

    async def handle_task_result(self, message: AgentMessage) -> None:
        """Handle task completion results from other agents.

        Args:
            message: Result message from agent
        """
        try:
            result_data = message.payload
            task_id = result_data.get("task_id")
            success = result_data.get("response", {}).get("success", False)

            logger.info(
                f"Received task result for {task_id}: {'success' if success else 'failure'}"
            )

            if success:
                # Update task status and check for next steps
                await self._handle_successful_task(task_id, result_data)
            else:
                # Handle failure and potentially retry or escalate
                await self._handle_failed_task(task_id, result_data)

        except Exception as e:
            logger.error(f"Failed to handle task result: {e}")

    async def _handle_successful_task(
        self, task_id: str, result_data: dict[str, Any]
    ) -> None:
        """Handle successful task completion.

        Args:
            task_id: Completed task ID
            result_data: Task result data
        """
        # Store success pattern
        success_pattern = {
            "task_id": task_id,
            "description": f"Task {task_id} completed successfully",
            "result_data": result_data,
            "coordinator": self.agent_id,
        }

        await self.knowledge.store_pattern(success_pattern)

    async def _handle_failed_task(
        self, task_id: str, result_data: dict[str, Any]
    ) -> None:
        """Handle failed task.

        Args:
            task_id: Failed task ID
            result_data: Task result data
        """
        # Store failure pattern for learning
        failure_pattern = {
            "task_id": task_id,
            "description": f"Task {task_id} failed",
            "error": result_data.get("response", {}).get(
                "error_message", "Unknown error"
            ),
            "coordinator": self.agent_id,
        }

        await self.knowledge.store_failure_pattern(failure_pattern)

        # Could implement retry logic here

    async def _handle_coordination(self, message: AgentMessage) -> None:
        """Handle coordination messages from other agents.

        Args:
            message: Coordination message
        """
        try:
            payload = message.payload
            coordination_type = payload.get("type")

            if coordination_type == "agent_status":
                # Update agent status
                self.agent_status[message.sender_id] = payload.get("status", "unknown")
                logger.debug(
                    f"Updated status for {message.sender_id}: {payload.get('status')}"
                )

            elif coordination_type == "resource_request":
                # Handle resource allocation requests
                await self._handle_resource_request(message)

            elif coordination_type == "escalation":
                # Handle escalated issues
                await self._handle_escalation(message)

        except Exception as e:
            logger.error(f"Coordination handling failed: {e}")

    async def _handle_resource_request(self, message: AgentMessage) -> None:
        """Handle resource allocation requests.

        Args:
            message: Resource request message
        """
        # Implementation would manage resource allocation
        logger.info(f"Resource request from {message.sender_id}")

    async def _handle_escalation(self, message: AgentMessage) -> None:
        """Handle escalated issues from agents.

        Args:
            message: Escalation message
        """
        # Implementation would handle escalated issues
        logger.warning(f"Escalation from {message.sender_id}: {message.payload}")

    async def get_feature_status(self, feature_id: str) -> dict[str, Any]:
        """Get status of a feature implementation.

        Args:
            feature_id: Feature identifier

        Returns:
            Feature status information
        """
        try:
            if feature_id not in self.active_features:
                return {"error": "Feature not found"}

            feature = self.active_features[feature_id]

            return {
                "feature_id": feature_id,
                "title": feature.title,
                "description": feature.description,
                "status": "in_progress",  # Would track actual status
                "agent_status": self.agent_status,
                "active_tasks": len(self.task_assignments),
            }

        except Exception as e:
            logger.error(f"Failed to get feature status: {e}")
            return {"error": str(e)}

    async def list_active_features(self) -> list[dict[str, Any]]:
        """List all active features.

        Returns:
            List of active feature information
        """
        try:
            return [
                {
                    "feature_id": feature_id,
                    "title": feature.title,
                    "description": feature.description,
                    "priority": feature.priority.value,
                }
                for feature_id, feature in self.active_features.items()
            ]

        except Exception as e:
            logger.error(f"Failed to list active features: {e}")
            return []

    async def get_system_status(self) -> dict[str, Any]:
        """Get overall system status.

        Returns:
            System status information
        """
        try:
            return {
                "coordinator_id": self.agent_id,
                "active_features": len(self.active_features),
                "agent_count": len(self.agent_status),
                "task_assignments": len(self.task_assignments),
                "knowledge_stats": await self.knowledge.get_stats(),
            }

        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}

    async def process_task(self, task: TaskSpecification) -> AgentResponse:
        """Process a task and return a response.

        Args:
            task: Task specification to process

        Returns:
            Agent response with task result
        """
        try:
            logger.info(f"Processing task: {task.title}")
            
            # For coordinator, delegate to appropriate agent
            if task.assigned_agent and task.assigned_agent != self.agent_id:
                # Forward task to assigned agent
                await self.messenger.send_message(
                    AgentMessage(
                        sender_id=self.agent_id,
                        recipient_id=task.assigned_agent,
                        message_type=MessageType.TASK_ASSIGNMENT,
                        payload={"task": task.__dict__}
                    )
                )
                return AgentResponse(
                    success=True,
                    message="Task delegated to assigned agent",
                    data={"task_id": task.id, "assigned_agent": task.assigned_agent}
                )
            else:
                # Handle coordination tasks locally
                return await self._handle_coordination_task(task)
                
        except Exception as e:
            logger.error(f"Failed to process task: {e}")
            return AgentResponse(
                success=False,
                message=f"Task processing failed: {str(e)}",
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
            logger.info(f"Processing PRP: {prp.title}")
            
            # Convert PRP to feature request and handle
            feature_request = FeatureRequest(
                title=prp.title,
                description=prp.description,
                requirements=prp.requirements,
                priority=prp.priority,
                acceptance_criteria=prp.acceptance_criteria
            )
            
            feature_id = await self.handle_feature_request(feature_request)
            
            return AgentResponse(
                success=True,
                message="PRP processed successfully",
                data={"feature_id": feature_id, "title": prp.title}
            )
            
        except Exception as e:
            logger.error(f"Failed to process PRP: {e}")
            return AgentResponse(
                success=False,
                message=f"PRP processing failed: {str(e)}",
                data={"prp_title": prp.title}
            )

    async def _handle_coordination_task(self, task: TaskSpecification) -> AgentResponse:
        """Handle coordination-specific tasks.

        Args:
            task: Coordination task

        Returns:
            Agent response
        """
        try:
            if "status_check" in task.title.lower():
                return AgentResponse(
                    success=True,
                    message="System status retrieved",
                    data=await self.get_system_status()
                )
            elif "feature_list" in task.title.lower():
                return AgentResponse(
                    success=True,
                    message="Active features listed",
                    data=await self.list_active_features()
                )
            else:
                return AgentResponse(
                    success=False,
                    message="Unknown coordination task",
                    data={"task_title": task.title}
                )
                
        except Exception as e:
            logger.error(f"Failed to handle coordination task: {e}")
            return AgentResponse(
                success=False,
                message=f"Coordination task failed: {str(e)}",
                data={"task_id": task.id}
            )
