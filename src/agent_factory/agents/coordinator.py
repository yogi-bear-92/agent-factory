"""Task coordinator agent for orchestrating multi-agent workflows."""

import asyncio
import logging
from typing import Any

from ..models import (
    AgentInfo,
    AgentMessage,
    AgentPRP,
    AgentStatus,
    ExecutionResult,
    MessageType,
    TaskPriority,
    TaskSpecification,
)
from .base import BaseAgent

logger = logging.getLogger(__name__)


class TaskCoordinator(BaseAgent):
    """Coordinator agent that orchestrates multi-agent workflows."""

    def __init__(self, *args, **kwargs):
        """Initialize task coordinator."""
        super().__init__(*args, **kwargs)

        # Agent tracking
        self.available_agents: dict[str, AgentInfo] = {}
        self.task_assignments: dict[str, str] = {}  # task_id -> agent_id
        self.pending_tasks: list[TaskSpecification] = []

        # Role-based agent assignment
        self.role_preferences = {
            "planning": ["planner", "architect"],
            "coding": ["coder", "developer", "programmer"],
            "testing": ["tester", "qa", "validator"],
            "review": ["reviewer", "auditor", "quality_assurance"],
            "deployment": ["devops", "deployment", "infrastructure"],
            "integration": ["integrator", "merger", "coordinator"],
        }

    async def start(self) -> None:
        """Start the coordinator agent."""
        await super().start()

        # Subscribe to coordination messages
        await self.message_bus.subscribe_to_broadcast(
            "coordination", self._handle_coordination_message
        )

        logger.info("Task Coordinator started and listening for agent updates")

    async def _execute_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Execute PRP by coordinating multiple agents.

        Args:
            prp: PRP to execute

        Returns:
            Execution result
        """
        try:
            logger.info(f"Coordinating PRP execution: {prp.goal}")

            # Break down PRP into tasks
            tasks = await self._decompose_prp_to_tasks(prp)

            if not tasks:
                return ExecutionResult.failure(["No tasks generated from PRP"])

            # Execute tasks in coordination
            results = await self._execute_task_workflow(tasks, prp)

            # Aggregate results
            all_successful = all(result.is_successful for result in results)
            combined_output = {
                "prp_goal": prp.goal,
                "tasks_executed": len(tasks),
                "successful_tasks": sum(1 for r in results if r.is_successful),
                "task_results": [r.output for r in results],
                "artifacts": [],
            }

            # Collect all artifacts
            for result in results:
                combined_output["artifacts"].extend(result.artifacts)

            if all_successful:
                return ExecutionResult.success(combined_output)
            else:
                errors = []
                for result in results:
                    if not result.is_successful:
                        errors.extend(result.errors)
                return ExecutionResult.failure(errors, output=combined_output)

        except Exception as e:
            logger.error(f"Error coordinating PRP execution: {e}")
            return ExecutionResult.failure([str(e)])

    async def _execute_task_impl(self, task: TaskSpecification) -> ExecutionResult:
        """Execute task by delegating to appropriate agent.

        Args:
            task: Task to execute

        Returns:
            Execution result
        """
        try:
            # Find best agent for the task
            agent_id = await self._assign_task_to_agent(task)

            if not agent_id:
                return ExecutionResult.failure(
                    [f"No suitable agent found for task: {task.title}"]
                )

            # Send task to agent
            result = await self._delegate_task_to_agent(agent_id, task)

            return result

        except Exception as e:
            logger.error(f"Error executing task {task.title}: {e}")
            return ExecutionResult.failure([str(e)])

    async def _decompose_prp_to_tasks(self, prp: AgentPRP) -> list[TaskSpecification]:
        """Decompose PRP into specific tasks for different agents.

        Args:
            prp: PRP to decompose

        Returns:
            List of tasks
        """
        tasks = []

        # Generate tasks based on implementation steps
        for i, step in enumerate(prp.implementation_steps):
            # Determine task type and priority
            task_type = self._classify_implementation_step(step)
            priority = TaskPriority.HIGH if i < 3 else TaskPriority.MEDIUM

            task = TaskSpecification(
                title=f"Step {i + 1}: {step[:50]}...",
                description=step,
                requirements=prp.validation_criteria,
                acceptance_criteria=prp.success_metrics,
                priority=priority,
                metadata={
                    "prp_goal": prp.goal,
                    "step_index": i,
                    "task_type": task_type,
                    "original_prp": prp.to_dict(),
                },
            )
            tasks.append(task)

        # Add validation task
        validation_task = TaskSpecification(
            title="Validate PRP Implementation",
            description=f"Validate that the implementation meets all criteria for: {prp.goal}",
            requirements=prp.validation_criteria,
            acceptance_criteria=prp.success_metrics,
            priority=TaskPriority.CRITICAL,
            metadata={
                "prp_goal": prp.goal,
                "task_type": "validation",
                "depends_on": [task.id for task in tasks],
            },
        )
        tasks.append(validation_task)

        logger.info(f"Generated {len(tasks)} tasks from PRP: {prp.goal}")
        return tasks

    def _classify_implementation_step(self, step: str) -> str:
        """Classify implementation step to determine task type.

        Args:
            step: Implementation step description

        Returns:
            Task type classification
        """
        step_lower = step.lower()

        if any(
            keyword in step_lower
            for keyword in ["plan", "design", "architect", "breakdown"]
        ):
            return "planning"
        elif any(
            keyword in step_lower
            for keyword in ["implement", "code", "create", "build", "develop"]
        ):
            return "coding"
        elif any(
            keyword in step_lower for keyword in ["test", "validate", "verify", "check"]
        ):
            return "testing"
        elif any(
            keyword in step_lower
            for keyword in ["review", "audit", "quality", "inspect"]
        ):
            return "review"
        elif any(
            keyword in step_lower
            for keyword in ["deploy", "release", "install", "configure"]
        ):
            return "deployment"
        elif any(
            keyword in step_lower
            for keyword in ["integrate", "merge", "combine", "connect"]
        ):
            return "integration"
        else:
            return "general"

    async def _execute_task_workflow(
        self, tasks: list[TaskSpecification], prp: AgentPRP
    ) -> list[ExecutionResult]:
        """Execute tasks in coordinated workflow.

        Args:
            tasks: Tasks to execute
            prp: Original PRP

        Returns:
            List of execution results
        """
        results = []

        # Sort tasks by priority and dependencies
        sorted_tasks = self._sort_tasks_by_priority(tasks)

        # Execute tasks in order, with some parallelization
        for task_batch in self._create_task_batches(sorted_tasks):
            batch_results = await self._execute_task_batch(task_batch)
            results.extend(batch_results)

            # Check if any critical failures require stopping
            if any(
                not r.is_successful and task.priority == TaskPriority.CRITICAL
                for r, task in zip(batch_results, task_batch, strict=False)
            ):
                logger.warning("Critical task failed, stopping workflow")
                break

        return results

    def _sort_tasks_by_priority(
        self, tasks: list[TaskSpecification]
    ) -> list[TaskSpecification]:
        """Sort tasks by priority and dependencies.

        Args:
            tasks: Tasks to sort

        Returns:
            Sorted tasks
        """
        # Simple priority-based sorting (can be enhanced with dependency graph)
        priority_order = {
            TaskPriority.CRITICAL: 0,
            TaskPriority.HIGH: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 3,
        }

        return sorted(tasks, key=lambda t: priority_order[t.priority])

    def _create_task_batches(
        self, tasks: list[TaskSpecification]
    ) -> list[list[TaskSpecification]]:
        """Create batches of tasks that can be executed in parallel.

        Args:
            tasks: Sorted tasks

        Returns:
            List of task batches
        """
        batches = []
        current_batch = []

        for task in tasks:
            # Check if task can be parallelized (simple heuristic)
            task_type = task.metadata.get("task_type", "general")

            if (
                not current_batch
                or len(current_batch) < 3  # Max 3 parallel tasks
                and task_type != "validation"
            ):  # Validation should be sequential
                current_batch.append(task)
            else:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [task]

        if current_batch:
            batches.append(current_batch)

        return batches

    async def _execute_task_batch(
        self, batch: list[TaskSpecification]
    ) -> list[ExecutionResult]:
        """Execute a batch of tasks in parallel.

        Args:
            batch: Tasks to execute

        Returns:
            List of execution results
        """
        if len(batch) == 1:
            # Single task execution
            result = await self._execute_task_impl(batch[0])
            return [result]

        # Parallel execution
        tasks = [self._execute_task_impl(task) for task in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to failed results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ExecutionResult.failure([str(result)]))
            else:
                processed_results.append(result)

        return processed_results

    async def _assign_task_to_agent(self, task: TaskSpecification) -> str | None:
        """Assign task to the most suitable available agent.

        Args:
            task: Task to assign

        Returns:
            Agent ID if suitable agent found, None otherwise
        """
        task_type = task.metadata.get("task_type", "general")

        # Get preferred roles for this task type
        preferred_roles = self.role_preferences.get(task_type, [])

        # Find available agents with preferred roles
        suitable_agents = []
        for agent_id, agent_info in self.available_agents.items():
            if agent_info.status == AgentStatus.IDLE and (
                not preferred_roles or agent_info.role.lower() in preferred_roles
            ):
                suitable_agents.append((agent_id, agent_info))

        if not suitable_agents:
            # Fallback to any available agent
            for agent_id, agent_info in self.available_agents.items():
                if agent_info.status == AgentStatus.IDLE:
                    suitable_agents.append((agent_id, agent_info))

        if not suitable_agents:
            logger.warning(f"No available agents for task: {task.title}")
            return None

        # Choose agent (can be enhanced with load balancing)
        chosen_agent_id, _ = suitable_agents[0]

        # Mark agent as busy and track assignment
        self.available_agents[chosen_agent_id].status = AgentStatus.BUSY
        self.available_agents[chosen_agent_id].current_task = task.id
        self.task_assignments[task.id] = chosen_agent_id

        logger.info(f"Assigned task {task.title} to agent {chosen_agent_id}")
        return chosen_agent_id

    async def _delegate_task_to_agent(
        self, agent_id: str, task: TaskSpecification
    ) -> ExecutionResult:
        """Delegate task to specific agent and wait for result.

        Args:
            agent_id: Target agent ID
            task: Task to delegate

        Returns:
            Execution result
        """
        # Send task assignment message
        message = AgentMessage(
            sender_id=self.agent_id,
            recipient_id=agent_id,
            message_type=MessageType.TASK_ASSIGNMENT,
            payload={"task": task.to_dict()},
            correlation_id=task.id,
        )

        await self.message_bus.send_to_agent(agent_id, message)

        # Wait for result (with timeout)
        return await self._wait_for_task_result(task.id, timeout=300)  # 5 minutes

    async def _wait_for_task_result(
        self, task_id: str, timeout: int = 300
    ) -> ExecutionResult:
        """Wait for task result from assigned agent.

        Args:
            task_id: Task ID to wait for
            timeout: Timeout in seconds

        Returns:
            Execution result
        """
        # This is a simplified implementation
        # In a real system, you'd use proper async coordination

        start_time = asyncio.get_event_loop().time()

        while (asyncio.get_event_loop().time() - start_time) < timeout:
            await asyncio.sleep(1)

            # Check if task is completed (simplified check)
            agent_id = self.task_assignments.get(task_id)
            if agent_id and self.available_agents.get(agent_id):
                agent_info = self.available_agents[agent_id]
                if agent_info.status == AgentStatus.IDLE:
                    # Task completed, assume success for now
                    return ExecutionResult.success(
                        {
                            "task_id": task_id,
                            "agent_id": agent_id,
                            "status": "completed",
                        }
                    )

        # Timeout
        return ExecutionResult.failure([f"Task {task_id} timed out"])

    async def _handle_coordination_message(self, message: AgentMessage) -> None:
        """Handle coordination messages from other agents.

        Args:
            message: Coordination message
        """
        payload = message.payload
        msg_type = payload.get("type")

        if msg_type == "status_update":
            agent_info_data = payload.get("agent_info")
            if agent_info_data:
                agent_info = AgentInfo(**agent_info_data)
                self.available_agents[agent_info.id] = agent_info
                logger.debug(
                    f"Updated agent status: {agent_info.id} -> {agent_info.status}"
                )

        elif msg_type == "task_completed":
            task_id = payload.get("task_id")
            agent_id = payload.get("agent_id")
            if task_id and agent_id:
                # Update tracking
                if task_id in self.task_assignments:
                    del self.task_assignments[task_id]
                if agent_id in self.available_agents:
                    self.available_agents[agent_id].status = AgentStatus.IDLE
                    self.available_agents[agent_id].current_task = None

    def get_coordination_status(self) -> dict[str, Any]:
        """Get coordination status and statistics.

        Returns:
            Coordination status information
        """
        return {
            "available_agents": len(self.available_agents),
            "active_assignments": len(self.task_assignments),
            "pending_tasks": len(self.pending_tasks),
            "agent_status": {
                agent_id: info.status.value
                for agent_id, info in self.available_agents.items()
            },
            "role_distribution": {
                role: len([a for a in self.available_agents.values() if a.role == role])
                for role in set(a.role for a in self.available_agents.values())
            },
        }
