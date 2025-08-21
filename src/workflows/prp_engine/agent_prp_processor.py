"""Agent-optimized PRP processor for structured execution."""

import json
import logging
import re
from pathlib import Path
from typing import Any

from ...agents.base import BaseAgent
from ...knowledge.vector_store import ChromaVectorStore
from ...models import AgentPRP, ExecutionResult

logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of PRP validation."""

    def __init__(self, is_valid: bool, errors: list[str]):
        self.is_valid = is_valid
        self.errors = errors


class AgentPRPProcessor:
    """Processor for agent-optimized PRPs with structured execution."""

    def __init__(self, knowledge_base: ChromaVectorStore):
        """Initialize the PRP processor.

        Args:
            knowledge_base: Vector store for context retrieval
        """
        self.knowledge = knowledge_base
        logger.info("Initialized AgentPRPProcessor")

    def parse_markdown_prp(self, prp_path: Path) -> AgentPRP:
        """Parse a markdown PRP file into AgentPRP structure.

        Args:
            prp_path: Path to the markdown PRP file

        Returns:
            Parsed AgentPRP object

        Raises:
            FileNotFoundError: If PRP file doesn't exist
            ValueError: If PRP format is invalid
        """
        try:
            if not prp_path.exists():
                raise FileNotFoundError(f"PRP file not found: {prp_path}")

            content = prp_path.read_text(encoding="utf-8")

            # Extract sections using regex patterns
            goal = self._extract_section(content, r"## Goal", r"##")
            why = self._extract_section(content, r"## Why", r"##")
            what = self._extract_section(content, r"## What", r"##")
            context = self._extract_section(content, r"## All Needed Context", r"##")
            implementation = self._extract_section(
                content, r"## Implementation Blueprint", r"##"
            )
            validation = self._extract_section(content, r"## Validation Loop", r"##")

            # Parse implementation steps
            implementation_steps = self._parse_implementation_steps(implementation)

            # Parse validation criteria
            validation_criteria = self._parse_validation_criteria(validation)

            # Parse context information
            context_dict = self._parse_context_section(context)

            # Build AgentPRP
            agent_prp = AgentPRP(
                goal=goal.strip(),
                justification=why.strip(),
                context=context_dict,
                implementation_steps=implementation_steps,
                validation_criteria=validation_criteria,
                success_metrics=self._extract_success_metrics(what),
                failure_recovery=self._extract_failure_recovery(content),
            )

            logger.info(f"Parsed PRP from {prp_path}")
            return agent_prp

        except Exception as e:
            logger.error(f"Failed to parse PRP {prp_path}: {e}")
            raise ValueError(f"Invalid PRP format: {e}")

    def parse_json_prp(self, prp_data: dict[str, Any]) -> AgentPRP:
        """Parse a JSON PRP structure into AgentPRP.

        Args:
            prp_data: Dictionary containing PRP data

        Returns:
            Parsed AgentPRP object
        """
        try:
            return AgentPRP(
                goal=prp_data.get("goal", ""),
                justification=prp_data.get("justification", ""),
                context=prp_data.get("context", {}),
                implementation_steps=prp_data.get("implementation_steps", []),
                validation_criteria=prp_data.get("validation_criteria", []),
                success_metrics=prp_data.get("success_metrics", []),
                failure_recovery=prp_data.get("failure_recovery", []),
            )

        except Exception as e:
            logger.error(f"Failed to parse JSON PRP: {e}")
            raise ValueError(f"Invalid JSON PRP format: {e}")

    async def validate_prp(self, prp: AgentPRP) -> ValidationResult:
        """Validate a PRP for completeness and structure.

        Args:
            prp: PRP to validate

        Returns:
            ValidationResult indicating if PRP is valid
        """
        errors = []

        # Check required fields
        if not prp.goal:
            errors.append("Goal is required")

        if not prp.justification:
            errors.append("Justification is required")

        if not prp.implementation_steps:
            errors.append("Implementation steps are required")

        if not prp.validation_criteria:
            errors.append("Validation criteria are required")

        # Check goal clarity
        if len(prp.goal.split()) < 5:
            errors.append("Goal should be more descriptive (at least 5 words)")

        # Check implementation steps format
        for i, step in enumerate(prp.implementation_steps):
            if not step.strip():
                errors.append(f"Implementation step {i + 1} is empty")

        # Check validation criteria format
        for i, criterion in enumerate(prp.validation_criteria):
            if not criterion.strip():
                errors.append(f"Validation criterion {i + 1} is empty")

        return ValidationResult(len(errors) == 0, errors)

    async def execute_prp(self, prp: AgentPRP, agent: BaseAgent) -> ExecutionResult:
        """Execute a PRP with the given agent.

        Args:
            prp: PRP to execute
            agent: Agent to execute the PRP

        Returns:
            ExecutionResult with outcome
        """
        try:
            # Validate PRP before execution
            validation_result = await self.validate_prp(prp)
            if not validation_result.is_valid:
                return ExecutionResult.failure(validation_result.errors)

            # Get context from knowledge base
            context = await self.knowledge.get_context_for_prp(prp)
            enhanced_prp = self._inject_context(prp, context)

            # Execute with agent
            response = await agent.process_prp(enhanced_prp)

            # Store execution outcome
            await self._store_execution_outcome(prp, response)

            if response.success:
                return ExecutionResult.success(response.result)
            else:
                return ExecutionResult.failure(
                    [response.error_message or "Unknown error"]
                )

        except Exception as e:
            logger.error(f"PRP execution failed: {e}")
            return ExecutionResult.failure([str(e)])

    async def get_context_for_prp(self, prp: AgentPRP) -> list[str]:
        """Get relevant context for a PRP from knowledge base.

        Args:
            prp: PRP to get context for

        Returns:
            List of relevant context strings
        """
        try:
            # Build query from PRP components
            query_parts = [prp.goal]
            if prp.justification:
                query_parts.append(prp.justification)

            query = " ".join(query_parts)

            # Get context from knowledge base
            context = await self.knowledge.get_relevant_context(query, limit=10)

            return context

        except Exception as e:
            logger.error(f"Failed to get context for PRP: {e}")
            return []

    def _extract_section(
        self, content: str, start_pattern: str, end_pattern: str
    ) -> str:
        """Extract a section from markdown content.

        Args:
            content: Full markdown content
            start_pattern: Regex pattern for section start
            end_pattern: Regex pattern for section end

        Returns:
            Extracted section content
        """
        # Find section start
        start_match = re.search(start_pattern, content, re.IGNORECASE | re.MULTILINE)
        if not start_match:
            return ""

        start_pos = start_match.end()

        # Find next section start or end of content
        remaining_content = content[start_pos:]
        end_match = re.search(
            end_pattern, remaining_content, re.IGNORECASE | re.MULTILINE
        )

        if end_match:
            end_pos = end_match.start()
            section_content = remaining_content[:end_pos]
        else:
            section_content = remaining_content

        return section_content.strip()

    def _parse_implementation_steps(self, implementation_text: str) -> list[str]:
        """Parse implementation steps from text.

        Args:
            implementation_text: Raw implementation section text

        Returns:
            List of implementation steps
        """
        steps = []

        # Look for numbered or bulleted lists
        lines = implementation_text.split("\n")
        current_step = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line starts a new step
            if (
                re.match(r"^\d+\.", line)
                or re.match(r"^[-*+]\s", line)
                or line.lower().startswith("task ")
                or line.lower().startswith("step ")
            ):
                if current_step:
                    steps.append(current_step.strip())

                # Clean up step text
                current_step = re.sub(r"^\d+\.\s*", "", line)
                current_step = re.sub(r"^[-*+]\s*", "", current_step)
                current_step = re.sub(
                    r"^(task|step)\s*\d*:?\s*", "", current_step, flags=re.IGNORECASE
                )
            else:
                # Continue current step
                if current_step:
                    current_step += " " + line

        # Add final step
        if current_step:
            steps.append(current_step.strip())

        return [step for step in steps if step]

    def _parse_validation_criteria(self, validation_text: str) -> list[str]:
        """Parse validation criteria from text.

        Args:
            validation_text: Raw validation section text

        Returns:
            List of validation criteria
        """
        criteria = []

        # Extract bash commands and test descriptions
        lines = validation_text.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Skip markdown code blocks markers
            if line.startswith("```"):
                continue

            # Extract bash commands
            if (
                line.startswith("uv run")
                or line.startswith("pytest")
                or line.startswith("ruff")
                or line.startswith("mypy")
                or line.startswith("curl")
                or line.startswith("docker")
            ):
                criteria.append(line)

            # Extract test descriptions
            elif (
                line.startswith("# ")
                or line.startswith("- ")
                or "test" in line.lower()
                or "validation" in line.lower()
            ):
                criteria.append(line.lstrip("# -").strip())

        return criteria

    def _parse_context_section(self, context_text: str) -> dict[str, Any]:
        """Parse context section into structured data.

        Args:
            context_text: Raw context section text

        Returns:
            Dictionary of context information
        """
        context_dict = {}

        # Extract documentation URLs
        doc_urls = re.findall(r"https?://[^\s]+", context_text)
        if doc_urls:
            context_dict["documentation_urls"] = doc_urls

        # Extract file references
        file_refs = re.findall(r"file:\s*([^\s]+)", context_text)
        if file_refs:
            context_dict["file_references"] = file_refs

        # Extract gotchas
        gotcha_matches = re.findall(
            r"gotcha[s]?:\s*([^\n]+)", context_text, re.IGNORECASE
        )
        if gotcha_matches:
            context_dict["gotchas"] = gotcha_matches

        # Extract patterns
        pattern_matches = re.findall(
            r"pattern[s]?:\s*([^\n]+)", context_text, re.IGNORECASE
        )
        if pattern_matches:
            context_dict["patterns"] = pattern_matches

        # Store full text for reference
        context_dict["full_context"] = context_text

        return context_dict

    def _extract_success_metrics(self, what_text: str) -> list[str]:
        """Extract success metrics from the What section.

        Args:
            what_text: Raw What section text

        Returns:
            List of success metrics
        """
        metrics = []

        # Look for success criteria patterns
        lines = what_text.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for success indicators
            if any(
                keyword in line.lower()
                for keyword in ["success", "complete", "pass", "achieve", "deliver"]
            ) and any(indicator in line for indicator in ["✓", "✅", "[ ]", "-", "*"]):
                # Clean up the line
                clean_line = re.sub(r"^[-*+✓✅]\s*", "", line)
                clean_line = re.sub(r"^\[ ?\]\s*", "", clean_line)

                if clean_line:
                    metrics.append(clean_line)

        return metrics

    def _extract_failure_recovery(self, content: str) -> list[str]:
        """Extract failure recovery strategies from content.

        Args:
            content: Full PRP content

        Returns:
            List of failure recovery strategies
        """
        recovery_strategies = []

        # Look for anti-patterns section
        anti_patterns = self._extract_section(content, r"## Anti-Patterns", r"##")

        if anti_patterns:
            lines = anti_patterns.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("- ❌") or line.startswith("❌"):
                    # Convert anti-pattern to recovery strategy
                    clean_line = re.sub(r"^[-❌]\s*", "", line)
                    recovery_strategies.append(f"Avoid: {clean_line}")

        # Default recovery strategies
        if not recovery_strategies:
            recovery_strategies = [
                "Check logs for specific error messages",
                "Verify all dependencies are available",
                "Ensure validation criteria are achievable",
                "Break down complex steps into smaller parts",
            ]

        return recovery_strategies

    def _inject_context(self, prp: AgentPRP, context: list[str]) -> AgentPRP:
        """Inject retrieved context into PRP.

        Args:
            prp: Original PRP
            context: Context to inject

        Returns:
            Enhanced PRP with injected context
        """
        enhanced_prp = AgentPRP(
            goal=prp.goal,
            justification=prp.justification,
            context=prp.context.copy(),
            implementation_steps=prp.implementation_steps.copy(),
            validation_criteria=prp.validation_criteria.copy(),
            success_metrics=prp.success_metrics.copy(),
            failure_recovery=prp.failure_recovery.copy(),
        )

        # Add retrieved context
        enhanced_prp.context["retrieved_context"] = context

        return enhanced_prp

    async def _store_execution_outcome(self, prp: AgentPRP, response: Any) -> None:
        """Store PRP execution outcome in knowledge base.

        Args:
            prp: Executed PRP
            response: Agent response
        """
        try:
            await self.knowledge.store_outcome(prp, response)
            logger.debug("Stored PRP execution outcome")

        except Exception as e:
            logger.error(f"Failed to store PRP execution outcome: {e}")

    def convert_to_agent_prp(self, markdown_path: Path) -> dict[str, Any]:
        """Convert markdown PRP to agent-optimized JSON format.

        Args:
            markdown_path: Path to markdown PRP file

        Returns:
            Dictionary representation of AgentPRP
        """
        try:
            agent_prp = self.parse_markdown_prp(markdown_path)

            return {
                "goal": agent_prp.goal,
                "justification": agent_prp.justification,
                "context": agent_prp.context,
                "implementation_steps": agent_prp.implementation_steps,
                "validation_criteria": agent_prp.validation_criteria,
                "success_metrics": agent_prp.success_metrics,
                "failure_recovery": agent_prp.failure_recovery,
            }

        except Exception as e:
            logger.error(f"Failed to convert PRP: {e}")
            raise

    def save_agent_prp(self, prp: AgentPRP, output_path: Path) -> None:
        """Save AgentPRP to JSON file.

        Args:
            prp: AgentPRP to save
            output_path: Path to save JSON file
        """
        try:
            prp_dict = {
                "goal": prp.goal,
                "justification": prp.justification,
                "context": prp.context,
                "implementation_steps": prp.implementation_steps,
                "validation_criteria": prp.validation_criteria,
                "success_metrics": prp.success_metrics,
                "failure_recovery": prp.failure_recovery,
            }

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(prp_dict, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved AgentPRP to {output_path}")

        except Exception as e:
            logger.error(f"Failed to save AgentPRP: {e}")
            raise
