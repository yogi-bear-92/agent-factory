"""PRP processing engine for agent execution."""

import logging
import time
from typing import Any

from ..agents.base import BaseAgent
from ..knowledge.chroma_store import ChromaVectorStore
from ..models import (
    AgentPRP,
    ExecutionResult,
    KnowledgeEntry,
    SourceType,
)

logger = logging.getLogger(__name__)


class AgentPRPProcessor:
    """Processor for executing PRPs with agents."""

    def __init__(self, knowledge_base: ChromaVectorStore):
        """Initialize PRP processor.

        Args:
            knowledge_base: Knowledge base for context injection
        """
        self.knowledge_base = knowledge_base

    async def validate_prp(self, prp: AgentPRP) -> dict[str, Any]:
        """Validate PRP structure and content.

        Args:
            prp: PRP to validate

        Returns:
            Validation result with is_valid flag and any errors
        """
        errors = []

        # Check required fields
        if not prp.goal:
            errors.append("PRP must have a goal")

        if not prp.justification:
            errors.append("PRP must have justification")

        if not prp.implementation_steps:
            errors.append("PRP must have implementation steps")

        if not prp.validation_criteria:
            errors.append("PRP must have validation criteria")

        # Check implementation steps quality
        if len(prp.implementation_steps) < 2:
            errors.append("PRP should have at least 2 implementation steps")

        # Check for vague steps
        vague_keywords = ["somehow", "maybe", "possibly", "perhaps"]
        for i, step in enumerate(prp.implementation_steps):
            if any(keyword in step.lower() for keyword in vague_keywords):
                errors.append(f"Implementation step {i + 1} is too vague: {step}")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "quality_score": self._calculate_quality_score(prp),
            "completeness": self._calculate_completeness(prp),
        }

    def _calculate_quality_score(self, prp: AgentPRP) -> float:
        """Calculate PRP quality score (0-1).

        Args:
            prp: PRP to score

        Returns:
            Quality score
        """
        score = 0.0

        # Goal clarity (0-0.2)
        if prp.goal and len(prp.goal) > 10:
            score += 0.2

        # Justification depth (0-0.2)
        if prp.justification and len(prp.justification) > 50:
            score += 0.2

        # Implementation detail (0-0.3)
        if len(prp.implementation_steps) >= 3:
            score += 0.1
        if any(len(step) > 50 for step in prp.implementation_steps):
            score += 0.1
        if len(prp.implementation_steps) >= 5:
            score += 0.1

        # Validation criteria (0-0.2)
        if len(prp.validation_criteria) >= 2:
            score += 0.1
        if len(prp.validation_criteria) >= 4:
            score += 0.1

        # Context richness (0-0.1)
        if prp.context and len(prp.context) > 0:
            score += 0.1

        return min(score, 1.0)

    def _calculate_completeness(self, prp: AgentPRP) -> float:
        """Calculate PRP completeness (0-1).

        Args:
            prp: PRP to assess

        Returns:
            Completeness score
        """
        required_fields = [
            prp.goal,
            prp.justification,
            prp.implementation_steps,
            prp.validation_criteria,
        ]

        optional_fields = [prp.success_metrics, prp.failure_recovery, prp.context]

        required_score = sum(1 for field in required_fields if field) / len(
            required_fields
        )
        optional_score = sum(1 for field in optional_fields if field) / len(
            optional_fields
        )

        return (required_score * 0.7) + (optional_score * 0.3)

    async def enhance_prp_with_context(self, prp: AgentPRP) -> AgentPRP:
        """Enhance PRP with relevant context from knowledge base.

        Args:
            prp: Original PRP

        Returns:
            Enhanced PRP with context
        """
        # Get relevant context
        context_sources = [
            SourceType.CODE,
            SourceType.DOCUMENTATION,
            SourceType.PATTERN,
        ]
        context = await self.knowledge_base.get_context_for_query(
            prp.goal, max_context_length=1500, source_types=context_sources
        )

        # Get similar successful patterns
        similar_patterns = await self.knowledge_base.query_similar(
            prp.goal, n_results=3, source_type=SourceType.PATTERN
        )

        # Get known failure patterns to avoid
        failure_patterns = await self.knowledge_base.query_similar(
            prp.goal, n_results=2, source_type=SourceType.FAILURE
        )

        # Build enhanced context
        enhanced_context = {
            **prp.context,
            "retrieved_context": context,
            "similar_patterns": [p.content for p in similar_patterns],
            "failure_patterns_to_avoid": [f.content for f in failure_patterns],
            "context_sources": len(similar_patterns) + len(failure_patterns),
        }

        return AgentPRP(
            goal=prp.goal,
            justification=prp.justification,
            context=enhanced_context,
            implementation_steps=prp.implementation_steps,
            validation_criteria=prp.validation_criteria,
            success_metrics=prp.success_metrics,
            failure_recovery=prp.failure_recovery,
            metadata={
                **prp.metadata,
                "context_enhanced": True,
                "enhancement_timestamp": time.time(),
            },
        )

    async def execute_prp_with_agent(
        self, prp: AgentPRP, agent: BaseAgent
    ) -> ExecutionResult:
        """Execute PRP with a specific agent.

        Args:
            prp: PRP to execute
            agent: Agent to execute with

        Returns:
            Execution result
        """
        logger.info(f"Executing PRP '{prp.goal}' with agent {agent.name}")

        try:
            # Validate PRP
            validation = await self.validate_prp(prp)
            if not validation["is_valid"]:
                return ExecutionResult.failure(
                    [f"PRP validation failed: {'; '.join(validation['errors'])}"]
                )

            # Enhance with context
            enhanced_prp = await self.enhance_prp_with_context(prp)

            # Execute with agent
            result = await agent.process_prp(enhanced_prp)

            # Store execution outcome
            await self._store_prp_execution_outcome(enhanced_prp, result, agent)

            return result

        except Exception as e:
            logger.error(f"Error executing PRP: {e}")
            return ExecutionResult.failure([str(e)])

    async def _store_prp_execution_outcome(
        self, prp: AgentPRP, result: ExecutionResult, agent: BaseAgent
    ) -> None:
        """Store PRP execution outcome in knowledge base.

        Args:
            prp: PRP that was executed
            result: Execution result
            agent: Agent that executed the PRP
        """
        try:
            # Create comprehensive outcome record
            outcome_content = f"""
            PRP EXECUTION OUTCOME
            
            Goal: {prp.goal}
            Agent: {agent.name} ({agent.role})
            Success: {result.is_successful}
            Execution Time: {result.execution_time:.2f}s
            
            Justification:
            {prp.justification}
            
            Implementation Approach:
            {chr(10).join(f"{i + 1}. {step}" for i, step in enumerate(prp.implementation_steps))}
            
            Validation Criteria:
            {chr(10).join(f"- {criteria}" for criteria in prp.validation_criteria)}
            
            Execution Result:
            {result.output if result.is_successful else "; ".join(result.errors)}
            
            Performance Metrics:
            {result.performance_metrics}
            
            Artifacts Generated:
            {chr(10).join(f"- {artifact}" for artifact in result.artifacts)}
            
            Context Used:
            - Enhanced with {prp.context.get("context_sources", 0)} similar patterns
            - Retrieved context length: {len(prp.context.get("retrieved_context", ""))} chars
            """

            # Determine source type based on success
            source_type = (
                SourceType.PATTERN if result.is_successful else SourceType.FAILURE
            )

            # Create knowledge entry
            entry = KnowledgeEntry(
                content=outcome_content.strip(),
                source_type=source_type,
                tags=[
                    agent.role,
                    "prp_execution",
                    "outcome",
                    "success" if result.is_successful else "failure",
                ],
                metadata={
                    "agent_id": agent.agent_id,
                    "agent_role": agent.role,
                    "prp_goal": prp.goal,
                    "success": result.is_successful,
                    "execution_time": result.execution_time,
                    "artifacts_count": len(result.artifacts),
                    "performance_score": sum(result.performance_metrics.values())
                    / max(len(result.performance_metrics), 1),
                },
            )

            await self.knowledge_base.store_entry(entry)

            logger.info(f"Stored PRP execution outcome for: {prp.goal}")

        except Exception as e:
            logger.error(f"Failed to store PRP execution outcome: {e}")

    async def get_prp_execution_history(
        self, goal_query: str, limit: int = 10
    ) -> list[KnowledgeEntry]:
        """Get execution history for similar PRPs.

        Args:
            goal_query: Query to find similar PRP goals
            limit: Maximum number of results

        Returns:
            List of execution history entries
        """
        # Search for PRP execution outcomes
        patterns = await self.knowledge_base.query_similar(
            goal_query, n_results=limit // 2, source_type=SourceType.PATTERN
        )

        failures = await self.knowledge_base.query_similar(
            goal_query, n_results=limit // 2, source_type=SourceType.FAILURE
        )

        # Filter for PRP executions
        history = []
        for entry in patterns + failures:
            if "prp_execution" in entry.tags:
                history.append(entry)

        # Sort by creation date (most recent first)
        history.sort(key=lambda e: e.created_at, reverse=True)

        return history[:limit]

    async def suggest_prp_improvements(self, prp: AgentPRP) -> dict[str, Any]:
        """Suggest improvements for a PRP based on historical data.

        Args:
            prp: PRP to analyze

        Returns:
            Dictionary with improvement suggestions
        """
        suggestions = {
            "validation_score": await self.validate_prp(prp),
            "improvements": [],
            "similar_successes": [],
            "common_failures": [],
        }

        # Get similar successful patterns
        successes = await self.knowledge_base.query_similar(
            prp.goal, n_results=3, source_type=SourceType.PATTERN
        )

        suggestions["similar_successes"] = [
            {"content": entry.content[:200] + "...", "metadata": entry.metadata}
            for entry in successes
        ]

        # Get common failure patterns
        failures = await self.knowledge_base.query_similar(
            prp.goal, n_results=3, source_type=SourceType.FAILURE
        )

        suggestions["common_failures"] = [
            {"content": entry.content[:200] + "...", "metadata": entry.metadata}
            for entry in failures
        ]

        # Generate specific improvement suggestions
        validation = suggestions["validation_score"]

        if validation["quality_score"] < 0.7:
            suggestions["improvements"].append(
                "Consider adding more detailed implementation steps"
            )

        if validation["completeness"] < 0.8:
            suggestions["improvements"].append(
                "Add success metrics and failure recovery procedures"
            )

        if len(prp.validation_criteria) < 3:
            suggestions["improvements"].append(
                "Add more specific validation criteria for better verification"
            )

        if not prp.context or len(prp.context) == 0:
            suggestions["improvements"].append(
                "Include relevant context, examples, and documentation references"
            )

        return suggestions
