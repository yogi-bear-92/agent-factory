# Agent Factory - Developer Reference

Technical reference guide for developers extending the Agent Factory system with custom agents, integrations, and advanced functionality.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Core Architecture](#core-architecture)
- [Base Classes & Interfaces](#base-classes--interfaces)
- [Custom Agent Implementation](#custom-agent-implementation)
- [Knowledge Base Integration](#knowledge-base-integration)
- [Communication Protocols](#communication-protocols)
- [Testing Framework](#testing-framework)
- [Extension Examples](#extension-examples)
- [Performance Optimization](#performance-optimization)
- [Deployment Patterns](#deployment-patterns)

## Development Environment Setup

### Prerequisites

```bash
# Required tools
python --version     # 3.12+
docker --version     # 24.0+
git --version       # 2.40+
uv --version        # 0.1.0+

# Optional but recommended
redis-cli --version  # For debugging
jq --version        # For JSON processing
```

### Development Installation

```bash
# 1. Clone and setup
git clone <repository>
cd agent-factory

# 2. Development environment
uv sync --group dev
source .venv/bin/activate

# 3. Install pre-commit hooks
pre-commit install

# 4. Run tests to verify setup
uv run pytest

# 5. Start development services
docker-compose -f docker-compose.dev.yml up -d
```

### IDE Configuration

#### VS Code Settings
```json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests/"],
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.typeChecking": "mypy"
}
```

#### PyCharm Configuration
- Interpreter: `.venv/bin/python`
- Test runner: pytest
- Code style: Black
- Type checker: mypy
- Linter: Ruff

## Core Architecture

### System Components

```python
# Core system hierarchy
agent_factory/
├── agents/          # Agent implementations
├── knowledge/       # Knowledge base and RAG
├── communication/   # Message bus and protocols
├── workflows/       # PRP engine and orchestration
├── api/            # REST and WebSocket APIs
├── config/         # Configuration management
└── tools/          # External tool integrations
```

### Key Design Patterns

#### 1. Agent Pattern
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ..models import AgentPRP, ExecutionResult, TaskSpecification

class AgentInterface(ABC):
    """Protocol for all agents in the system."""
    
    @abstractmethod
    async def process_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Process a Product Requirement Prompt."""
        pass
    
    @abstractmethod
    async def execute_task(self, task: TaskSpecification) -> AgentResponse:
        """Execute a specific task."""
        pass
    
    @abstractmethod
    async def handle_message(self, message: AgentMessage) -> None:
        """Handle incoming messages."""
        pass
```

#### 2. Observer Pattern (Message Bus)
```python
class MessageBus:
    """Event-driven communication between agents."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    async def subscribe(self, channel: str, handler: Callable):
        """Subscribe to messages on a channel."""
        if channel not in self._subscribers:
            self._subscribers[channel] = []
        self._subscribers[channel].append(handler)
    
    async def publish(self, channel: str, message: AgentMessage):
        """Publish message to all subscribers."""
        for handler in self._subscribers.get(channel, []):
            await handler(message)
```

#### 3. Strategy Pattern (LLM Providers)
```python
class LLMProvider(ABC):
    """Abstract base for LLM providers."""
    
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

class OpenAIProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs) -> str:
        # OpenAI implementation
        pass

class AzureOpenAIProvider(LLMProvider):
    async def generate(self, prompt: str, **kwargs) -> str:
        # Azure OpenAI implementation
        pass
```

## Base Classes & Interfaces

### BaseAgent Class

```python
from abc import ABC, abstractmethod
import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..communication import RedisMessageBus
from ..knowledge import ChromaVectorStore
from ..models import *

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        knowledge_base: ChromaVectorStore,
        message_bus: RedisMessageBus,
        llm_provider: LLMProvider,
        capabilities: List[str] = None,
        config: Dict[str, Any] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.knowledge_base = knowledge_base
        self.message_bus = message_bus
        self.llm_provider = llm_provider
        self.capabilities = capabilities or []
        self.config = config or {}
        
        # Agent state
        self.status = AgentStatus.IDLE
        self.current_task: Optional[TaskSpecification] = None
        self.performance_metrics = PerformanceMetrics()
        
        # Logging
        self.logger = logging.getLogger(f"agent.{self.role}")
    
    async def start(self) -> None:
        """Start the agent and begin listening for messages."""
        self.logger.info(f"Starting agent {self.name}")
        
        # Subscribe to agent-specific channel
        await self.message_bus.subscribe(
            f"agent.{self.agent_id}", 
            self.handle_message
        )
        
        # Subscribe to broadcast channels
        await self.message_bus.subscribe(
            "coordination", 
            self.handle_message
        )
        
        # Start heartbeat
        asyncio.create_task(self._heartbeat_loop())
        
        self.status = AgentStatus.IDLE
        await self._send_status_update()
    
    async def stop(self) -> None:
        """Stop the agent gracefully."""
        self.logger.info(f"Stopping agent {self.name}")
        self.status = AgentStatus.OFFLINE
        await self._send_status_update()
    
    # Abstract methods that subclasses must implement
    @abstractmethod
    async def _execute_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Execute PRP implementation logic."""
        pass
    
    @abstractmethod
    async def _execute_task_impl(
        self, 
        task: TaskSpecification
    ) -> ExecutionResult:
        """Execute task implementation logic."""
        pass
    
    # Concrete methods available to all agents
    async def process_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Process a PRP with context injection and monitoring."""
        start_time = datetime.now()
        
        try:
            self.status = AgentStatus.BUSY
            await self._send_status_update()
            
            # Inject context from knowledge base
            enhanced_prp = await self._enhance_prp_with_context(prp)
            
            # Execute the PRP
            result = await self._execute_prp(enhanced_prp)
            
            # Store outcomes in knowledge base
            await self._store_execution_outcome(enhanced_prp, result)
            
            # Update performance metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            self.performance_metrics.add_execution(
                execution_time, 
                result.is_successful
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"PRP execution failed: {e}", exc_info=True)
            return ExecutionResult.failure([str(e)])
        finally:
            self.status = AgentStatus.IDLE
            await self._send_status_update()
    
    async def _enhance_prp_with_context(
        self, 
        prp: AgentPRP
    ) -> AgentPRP:
        """Enhance PRP with relevant context from knowledge base."""
        
        # Query for relevant patterns
        relevant_context = await self.knowledge_base.query(
            query=f"{prp.goal} {' '.join(prp.context.get('keywords', []))}",
            max_results=5,
            filters={"source_type": ["PATTERN", "DOCUMENTATION"]}
        )
        
        # Add context to PRP
        enhanced_context = {
            **prp.context,
            "retrieved_patterns": relevant_context,
            "agent_capabilities": self.capabilities,
            "execution_history": await self._get_execution_history()
        }
        
        return AgentPRP(
            goal=prp.goal,
            justification=prp.justification,
            context=enhanced_context,
            implementation_steps=prp.implementation_steps,
            validation_criteria=prp.validation_criteria,
            success_metrics=prp.success_metrics,
            failure_recovery=prp.failure_recovery,
            metadata=prp.metadata
        )
    
    async def _send_status_update(self) -> None:
        """Send status update to coordination channel."""
        status_message = AgentMessage(
            sender_id=self.agent_id,
            message_type=MessageType.COORDINATION,
            payload={
                "type": "status_update",
                "agent_info": {
                    "id": self.agent_id,
                    "name": self.name,
                    "role": self.role,
                    "status": self.status.value,
                    "capabilities": self.capabilities,
                    "current_task": (
                        self.current_task.id 
                        if self.current_task else None
                    ),
                    "performance_metrics": self.performance_metrics.to_dict()
                }
            }
        )
        await self.message_bus.broadcast("coordination", status_message)
```

### Knowledge Base Integration

```python
class KnowledgeBaseIntegration:
    """Helper class for agent knowledge base operations."""
    
    def __init__(self, vector_store: ChromaVectorStore):
        self.vector_store = vector_store
    
    async def store_pattern(
        self, 
        content: str, 
        tags: List[str],
        metadata: Dict[str, Any]
    ) -> str:
        """Store a successful pattern for future use."""
        entry = KnowledgeEntry(
            content=content,
            source_type=SourceType.PATTERN,
            tags=tags,
            metadata={
                **metadata,
                "stored_by": self.__class__.__name__,
                "stored_at": datetime.now().isoformat()
            }
        )
        return await self.vector_store.store_entry(entry)
    
    async def query_patterns(
        self, 
        query: str, 
        filters: Dict[str, Any] = None
    ) -> List[KnowledgeEntry]:
        """Query for relevant patterns and context."""
        return await self.vector_store.query(
            query=query,
            max_results=10,
            filters=filters or {"source_type": ["PATTERN", "DOCUMENTATION"]}
        )
    
    async def store_failure(
        self, 
        context: str, 
        error: str, 
        recovery_steps: List[str]
    ) -> str:
        """Store failure case for learning."""
        content = f"""
        Context: {context}
        Error: {error}
        Recovery Steps:
        {chr(10).join(f"- {step}" for step in recovery_steps)}
        """
        
        entry = KnowledgeEntry(
            content=content.strip(),
            source_type=SourceType.FAILURE,
            tags=["failure", "recovery"],
            metadata={
                "error_type": type(error).__name__,
                "context_hash": hash(context)
            }
        )
        return await self.vector_store.store_entry(entry)
```

## Custom Agent Implementation

### Example: Custom DatabaseAgent

```python
from typing import Dict, List, Any
from ..agents.base import BaseAgent
from ..models import *

class DatabaseAgent(BaseAgent):
    """Agent specialized in database operations and schema management."""
    
    def __init__(self, **kwargs):
        super().__init__(
            role="database",
            capabilities=[
                "schema_design",
                "migration_generation",
                "query_optimization", 
                "data_modeling",
                "performance_analysis"
            ],
            **kwargs
        )
        
        # Database-specific configuration
        self.supported_databases = [
            "postgresql", "mysql", "sqlite", "mongodb"
        ]
        self.max_query_complexity = 10
        
    async def _execute_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Execute database-specific PRP."""
        
        try:
            # Analyze the goal to determine database operation type
            operation_type = await self._classify_database_operation(prp.goal)
            
            if operation_type == "schema_design":
                return await self._design_database_schema(prp)
            elif operation_type == "migration":
                return await self._generate_migration(prp)
            elif operation_type == "optimization":
                return await self._optimize_queries(prp)
            else:
                return ExecutionResult.failure([
                    f"Unsupported database operation: {operation_type}"
                ])
                
        except Exception as e:
            self.logger.error(f"Database PRP execution failed: {e}")
            return ExecutionResult.failure([str(e)])
    
    async def _execute_task_impl(
        self, 
        task: TaskSpecification
    ) -> ExecutionResult:
        """Execute database-specific task."""
        
        # Get relevant database patterns from knowledge base
        patterns = await self.knowledge_base.query(
            query=f"database {task.title} {' '.join(task.requirements)}",
            filters={"tags": ["database", "sql", "schema"]}
        )
        
        # Generate database solution based on task requirements
        solution = await self._generate_database_solution(task, patterns)
        
        # Validate the solution
        validation_result = await self._validate_database_solution(solution)
        
        if validation_result.is_valid:
            return ExecutionResult.success({
                "solution": solution,
                "validation": validation_result,
                "artifacts": solution.get("artifacts", [])
            })
        else:
            return ExecutionResult.failure(validation_result.errors)
    
    async def _classify_database_operation(self, goal: str) -> str:
        """Use LLM to classify the type of database operation."""
        
        classification_prompt = f"""
        Classify the following database-related goal into one of these categories:
        - schema_design: Designing database tables, relationships, constraints
        - migration: Creating database migration scripts
        - optimization: Query optimization, index creation, performance tuning
        - data_modeling: Entity relationship design, normalization
        - analysis: Performance analysis, query analysis
        
        Goal: {goal}
        
        Return only the category name.
        """
        
        response = await self.llm_provider.generate(
            classification_prompt,
            temperature=0.1,
            max_tokens=50
        )
        
        return response.strip().lower()
    
    async def _design_database_schema(self, prp: AgentPRP) -> ExecutionResult:
        """Design database schema based on PRP requirements."""
        
        schema_prompt = f"""
        Design a database schema for the following requirements:
        
        Goal: {prp.goal}
        Requirements: {prp.context.get('requirements', [])}
        
        Consider:
        - Normalization best practices
        - Proper relationships and constraints
        - Index optimization
        - Data types and constraints
        
        Provide the schema as SQL DDL statements.
        """
        
        # Get schema from LLM
        schema_sql = await self.llm_provider.generate(schema_prompt)
        
        # Validate schema
        validation_errors = await self._validate_sql_schema(schema_sql)
        
        if validation_errors:
            return ExecutionResult.failure(validation_errors)
        
        # Store successful pattern
        await self.knowledge_base.store_entry(KnowledgeEntry(
            content=f"Schema design for: {prp.goal}\n\n{schema_sql}",
            source_type=SourceType.PATTERN,
            tags=["database", "schema", "sql"],
            metadata={
                "agent": self.role,
                "goal": prp.goal,
                "database_type": "postgresql"  # Could be dynamic
            }
        ))
        
        return ExecutionResult.success({
            "schema_sql": schema_sql,
            "tables_created": self._extract_table_names(schema_sql),
            "validation": "passed"
        })
    
    async def _validate_sql_schema(self, sql: str) -> List[str]:
        """Validate SQL schema for syntax and best practices."""
        errors = []
        
        # Basic SQL syntax validation (simplified)
        if not sql.strip():
            errors.append("Empty SQL schema")
        
        if "CREATE TABLE" not in sql.upper():
            errors.append("No CREATE TABLE statements found")
        
        # Check for primary keys
        if "PRIMARY KEY" not in sql.upper():
            errors.append("No primary keys defined")
        
        # Additional validations...
        
        return errors
    
    def _extract_table_names(self, sql: str) -> List[str]:
        """Extract table names from SQL DDL."""
        import re
        pattern = r'CREATE TABLE\s+(\w+)'
        matches = re.findall(pattern, sql, re.IGNORECASE)
        return matches
```

### Agent Registration System

```python
class AgentRegistry:
    """Registry for managing agent instances and capabilities."""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._capabilities: Dict[str, List[str]] = {}
    
    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the system."""
        self._agents[agent.agent_id] = agent
        self._capabilities[agent.agent_id] = agent.capabilities
        
        self.logger.info(f"Registered agent: {agent.name} ({agent.role})")
    
    def get_agents_by_capability(self, capability: str) -> List[BaseAgent]:
        """Find agents that have a specific capability."""
        matching_agents = []
        for agent_id, capabilities in self._capabilities.items():
            if capability in capabilities:
                matching_agents.append(self._agents[agent_id])
        return matching_agents
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID."""
        return self._agents.get(agent_id)
    
    async def start_all_agents(self) -> None:
        """Start all registered agents."""
        for agent in self._agents.values():
            await agent.start()
    
    async def stop_all_agents(self) -> None:
        """Stop all registered agents."""
        for agent in self._agents.values():
            await agent.stop()

# Global registry instance
agent_registry = AgentRegistry()

# Decorator for easy agent registration
def register_agent(cls):
    """Decorator to automatically register agent classes."""
    original_init = cls.__init__
    
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        agent_registry.register_agent(self)
    
    cls.__init__ = new_init
    return cls
```

## Knowledge Base Integration

### Advanced RAG Implementation

```python
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

class AdvancedRAG:
    """Advanced Retrieval-Augmented Generation with context optimization."""
    
    def __init__(
        self, 
        vector_store: ChromaVectorStore,
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        self.vector_store = vector_store
        self.embedding_model = SentenceTransformer(embedding_model)
        self.context_cache: Dict[str, List[KnowledgeEntry]] = {}
    
    async def get_contextual_knowledge(
        self,
        query: str,
        context_type: str = "general",
        max_context_length: int = 4000,
        min_relevance_score: float = 0.7
    ) -> str:
        """Get contextually relevant knowledge for a query."""
        
        # Generate cache key
        cache_key = f"{hash(query)}_{context_type}_{max_context_length}"
        
        # Check cache first
        if cache_key in self.context_cache:
            relevant_entries = self.context_cache[cache_key]
        else:
            # Query vector store
            results = await self.vector_store.query(
                query=query,
                max_results=20,
                filters=self._get_context_filters(context_type)
            )
            
            # Filter by relevance score
            relevant_entries = [
                entry for entry in results 
                if entry.relevance_score >= min_relevance_score
            ]
            
            # Cache results
            self.context_cache[cache_key] = relevant_entries
        
        # Optimize context for token limits
        optimized_context = self._optimize_context(
            relevant_entries, 
            max_context_length
        )
        
        return self._format_context(optimized_context)
    
    def _get_context_filters(self, context_type: str) -> Dict[str, List[str]]:
        """Get filters based on context type."""
        filter_map = {
            "general": {"source_type": ["PATTERN", "DOCUMENTATION"]},
            "code": {"source_type": ["CODE", "PATTERN"], "tags": ["code"]},
            "architecture": {
                "source_type": ["PATTERN", "DOCUMENTATION"],
                "tags": ["architecture", "design"]
            },
            "debugging": {
                "source_type": ["FAILURE", "PATTERN"],
                "tags": ["error", "debug", "troubleshooting"]
            }
        }
        return filter_map.get(context_type, filter_map["general"])
    
    def _optimize_context(
        self, 
        entries: List[KnowledgeEntry], 
        max_length: int
    ) -> List[KnowledgeEntry]:
        """Optimize context selection for token limits."""
        
        # Sort by relevance score
        sorted_entries = sorted(
            entries, 
            key=lambda x: x.relevance_score, 
            reverse=True
        )
        
        # Select entries that fit within token limit
        selected_entries = []
        current_length = 0
        
        for entry in sorted_entries:
            entry_length = len(entry.content.split())
            if current_length + entry_length <= max_length:
                selected_entries.append(entry)
                current_length += entry_length
            else:
                break
        
        return selected_entries
    
    def _format_context(self, entries: List[KnowledgeEntry]) -> str:
        """Format knowledge entries into contextual prompt."""
        if not entries:
            return "No relevant context found."
        
        context_sections = []
        
        for entry in entries:
            section = f"""
            --- Context from {entry.source_type.value} ---
            {entry.content}
            
            Tags: {', '.join(entry.tags)}
            Relevance: {entry.relevance_score:.2f}
            ---
            """
            context_sections.append(section.strip())
        
        return "\n\n".join(context_sections)

    async def store_interaction_outcome(
        self,
        query: str,
        context_used: str,
        outcome: ExecutionResult,
        agent_id: str
    ) -> None:
        """Store the outcome of an interaction for learning."""
        
        outcome_content = f"""
        Query: {query}
        
        Context Used:
        {context_used}
        
        Outcome: {'Success' if outcome.is_successful else 'Failure'}
        
        {'Result: ' + str(outcome.output) if outcome.is_successful else 'Errors: ' + '; '.join(outcome.errors)}
        
        Agent: {agent_id}
        Execution Time: {outcome.execution_time}s
        """
        
        entry = KnowledgeEntry(
            content=outcome_content,
            source_type=SourceType.PATTERN if outcome.is_successful else SourceType.FAILURE,
            tags=["interaction", "outcome", agent_id],
            metadata={
                "query_hash": hash(query),
                "agent_id": agent_id,
                "success": outcome.is_successful,
                "execution_time": outcome.execution_time
            }
        )
        
        await self.vector_store.store_entry(entry)
```

## Communication Protocols

### Message Protocol Implementation

```python
from enum import Enum
from typing import Dict, Any, Callable, List
import asyncio
import json
from dataclasses import asdict

class MessagePriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class EnhancedAgentMessage:
    """Enhanced message format with routing and priority."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender_id: str = ""
    recipient_id: str = ""
    message_type: MessageType = MessageType.COORDINATION
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: Optional[str] = None
    
    # Enhanced fields
    priority: MessagePriority = MessagePriority.NORMAL
    routing_key: str = ""
    ttl: int = 3600  # Time to live in seconds
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            **asdict(self),
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "timestamp": self.timestamp.isoformat()
        }

class MessageRouter:
    """Advanced message routing with patterns and filters."""
    
    def __init__(self, message_bus: RedisMessageBus):
        self.message_bus = message_bus
        self.routes: Dict[str, List[Callable]] = {}
        self.filters: Dict[str, Callable] = {}
    
    def add_route(
        self, 
        pattern: str, 
        handler: Callable,
        filter_func: Optional[Callable] = None
    ):
        """Add a message route with optional filtering."""
        if pattern not in self.routes:
            self.routes[pattern] = []
        
        self.routes[pattern].append(handler)
        
        if filter_func:
            self.filters[f"{pattern}_{len(self.routes[pattern])}"] = filter_func
    
    async def route_message(self, message: EnhancedAgentMessage) -> bool:
        """Route message to appropriate handlers."""
        routed = False
        
        for pattern, handlers in self.routes.items():
            if self._pattern_matches(pattern, message):
                for i, handler in enumerate(handlers):
                    filter_key = f"{pattern}_{i+1}"
                    
                    # Apply filter if exists
                    if filter_key in self.filters:
                        if not await self.filters[filter_key](message):
                            continue
                    
                    # Route to handler
                    try:
                        await handler(message)
                        routed = True
                    except Exception as e:
                        logging.error(f"Handler error: {e}")
        
        return routed
    
    def _pattern_matches(
        self, 
        pattern: str, 
        message: EnhancedAgentMessage
    ) -> bool:
        """Check if message matches routing pattern."""
        
        # Simple pattern matching - can be enhanced with regex
        if pattern == "*":
            return True
        elif pattern.startswith("agent."):
            return message.routing_key.startswith("agent.")
        elif pattern == message.message_type.value:
            return True
        elif pattern == message.routing_key:
            return True
        
        return False

# Example usage
async def setup_message_routing():
    """Setup message routing for the system."""
    
    message_bus = RedisMessageBus()
    router = MessageRouter(message_bus)
    
    # Route task assignments to capable agents
    router.add_route(
        "TASK_ASSIGNMENT",
        handle_task_assignment,
        filter_func=lambda msg: msg.priority != MessagePriority.LOW
    )
    
    # Route coordination messages to all agents
    router.add_route(
        "COORDINATION", 
        broadcast_to_all_agents
    )
    
    # Route high priority messages immediately
    router.add_route(
        "*",
        handle_priority_message,
        filter_func=lambda msg: msg.priority == MessagePriority.CRITICAL
    )
```

## Testing Framework

### Agent Testing Utilities

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
from typing import Dict, Any, List

class AgentTestHarness:
    """Test harness for agent development and testing."""
    
    def __init__(self):
        self.mock_knowledge_base = AsyncMock()
        self.mock_message_bus = AsyncMock() 
        self.mock_llm_provider = AsyncMock()
        self.test_messages: List[AgentMessage] = []
        
    def create_test_agent(self, agent_class, **kwargs) -> BaseAgent:
        """Create agent instance with mocked dependencies."""
        
        config = {
            "agent_id": "test-agent-001",
            "name": "Test Agent", 
            "role": "test",
            "knowledge_base": self.mock_knowledge_base,
            "message_bus": self.mock_message_bus,
            "llm_provider": self.mock_llm_provider,
            **kwargs
        }
        
        return agent_class(**config)
    
    def setup_knowledge_base_responses(
        self, 
        responses: Dict[str, List[KnowledgeEntry]]
    ):
        """Setup mock responses for knowledge base queries."""
        
        async def mock_query(query, **kwargs):
            return responses.get(query, [])
        
        self.mock_knowledge_base.query.side_effect = mock_query
    
    def setup_llm_responses(self, responses: Dict[str, str]):
        """Setup mock responses for LLM provider."""
        
        async def mock_generate(prompt, **kwargs):
            # Match prompt to closest key
            for key, response in responses.items():
                if key.lower() in prompt.lower():
                    return response
            return "Default response"
        
        self.mock_llm_provider.generate.side_effect = mock_generate
    
    def capture_messages(self):
        """Capture messages sent through message bus."""
        
        async def mock_publish(channel, message):
            self.test_messages.append(message)
        
        async def mock_send(recipient, message):
            self.test_messages.append(message)
        
        self.mock_message_bus.publish.side_effect = mock_publish
        self.mock_message_bus.send_to_agent.side_effect = mock_send
    
    def get_messages_by_type(self, message_type: MessageType) -> List[AgentMessage]:
        """Get captured messages by type."""
        return [
            msg for msg in self.test_messages 
            if msg.message_type == message_type
        ]

# Example agent test
@pytest.mark.asyncio
class TestDatabaseAgent:
    
    async def test_schema_design_success(self):
        """Test successful schema design."""
        
        # Setup test harness
        harness = AgentTestHarness()
        
        # Setup mock responses
        harness.setup_llm_responses({
            "design a database schema": """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
        })
        
        harness.setup_knowledge_base_responses({
            "database schema design": [
                KnowledgeEntry(
                    content="Best practices for database schema design",
                    source_type=SourceType.DOCUMENTATION,
                    tags=["database", "schema"]
                )
            ]
        })
        
        # Create test agent
        agent = harness.create_test_agent(DatabaseAgent)
        
        # Create test PRP
        prp = AgentPRP(
            goal="Design a user database schema",
            justification="Need to store user data",
            context={"requirements": ["email", "timestamps"]},
            implementation_steps=["analyze requirements", "design schema"],
            validation_criteria=["valid SQL", "proper constraints"]
        )
        
        # Execute PRP
        result = await agent.process_prp(prp)
        
        # Assertions
        assert result.is_successful
        assert "CREATE TABLE users" in result.output["schema_sql"]
        assert "PRIMARY KEY" in result.output["schema_sql"]
        
        # Verify knowledge base was queried
        harness.mock_knowledge_base.query.assert_called()
        
        # Verify LLM was called
        harness.mock_llm_provider.generate.assert_called()
    
    async def test_invalid_schema_handling(self):
        """Test handling of invalid schema generation."""
        
        harness = AgentTestHarness()
        
        # Setup LLM to return invalid SQL
        harness.setup_llm_responses({
            "design a database schema": "INVALID SQL HERE"
        })
        
        agent = harness.create_test_agent(DatabaseAgent)
        
        prp = AgentPRP(
            goal="Design invalid schema",
            context={"requirements": ["test"]}
        )
        
        result = await agent.process_prp(prp)
        
        # Should fail gracefully
        assert not result.is_successful
        assert len(result.errors) > 0

# Performance testing utilities
class PerformanceTestSuite:
    """Performance testing utilities for agents."""
    
    @staticmethod
    async def benchmark_agent_response_time(
        agent: BaseAgent, 
        prps: List[AgentPRP],
        max_acceptable_time: float = 30.0
    ) -> Dict[str, Any]:
        """Benchmark agent response times."""
        
        results = []
        
        for prp in prps:
            start_time = time.time()
            result = await agent.process_prp(prp)
            execution_time = time.time() - start_time
            
            results.append({
                "prp_goal": prp.goal,
                "execution_time": execution_time,
                "success": result.is_successful,
                "within_limit": execution_time <= max_acceptable_time
            })
        
        return {
            "total_tests": len(results),
            "avg_time": sum(r["execution_time"] for r in results) / len(results),
            "max_time": max(r["execution_time"] for r in results),
            "success_rate": sum(1 for r in results if r["success"]) / len(results),
            "performance_pass_rate": sum(1 for r in results if r["within_limit"]) / len(results),
            "details": results
        }
    
    @staticmethod
    async def stress_test_agent(
        agent: BaseAgent,
        concurrent_requests: int = 10,
        test_duration: int = 60
    ) -> Dict[str, Any]:
        """Stress test agent with concurrent requests."""
        
        # Create test PRPs
        test_prp = AgentPRP(
            goal="Stress test task",
            justification="Performance testing"
        )
        
        results = []
        start_time = time.time()
        
        while time.time() - start_time < test_duration:
            # Run concurrent requests
            tasks = [
                agent.process_prp(test_prp) 
                for _ in range(concurrent_requests)
            ]
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    results.append({"success": False, "error": str(result)})
                else:
                    results.append({
                        "success": result.is_successful,
                        "execution_time": result.execution_time
                    })
        
        return {
            "total_requests": len(results),
            "success_rate": sum(1 for r in results if r["success"]) / len(results),
            "error_rate": sum(1 for r in results if not r["success"]) / len(results),
            "avg_response_time": sum(
                r.get("execution_time", 0) for r in results if r["success"]
            ) / max(sum(1 for r in results if r["success"]), 1)
        }
```

## Extension Examples

### Custom Tool Integration

```python
class GitHubIntegration:
    """Integration with GitHub API for code management."""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.github.com"
    
    async def create_pull_request(
        self,
        repo: str,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main"
    ) -> Dict[str, Any]:
        """Create a pull request."""
        
        headers = {
            "Authorization": f"token {self.api_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "title": title,
            "body": body,
            "head": head_branch,
            "base": base_branch
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/repos/{repo}/pulls",
                headers=headers,
                json=data
            ) as response:
                return await response.json()

class GitHubAgent(BaseAgent):
    """Agent that integrates with GitHub for code management."""
    
    def __init__(self, github_token: str, **kwargs):
        super().__init__(
            role="github",
            capabilities=[
                "pull_request_creation",
                "code_review",
                "issue_management",
                "repository_analysis"
            ],
            **kwargs
        )
        self.github = GitHubIntegration(github_token)
    
    async def _execute_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Execute GitHub-related PRP."""
        
        if "pull request" in prp.goal.lower():
            return await self._create_pull_request_from_prp(prp)
        elif "code review" in prp.goal.lower():
            return await self._perform_code_review(prp)
        else:
            return ExecutionResult.failure([
                f"Unsupported GitHub operation in goal: {prp.goal}"
            ])
    
    async def _create_pull_request_from_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Create pull request based on PRP."""
        
        # Extract PR details from PRP context
        repo = prp.context.get("repository")
        branch = prp.context.get("branch")
        
        if not repo or not branch:
            return ExecutionResult.failure([
                "Missing repository or branch information"
            ])
        
        # Generate PR description using LLM
        pr_description = await self._generate_pr_description(prp)
        
        # Create PR
        try:
            pr_result = await self.github.create_pull_request(
                repo=repo,
                title=prp.goal,
                body=pr_description,
                head_branch=branch
            )
            
            return ExecutionResult.success({
                "pull_request": pr_result,
                "url": pr_result.get("html_url"),
                "number": pr_result.get("number")
            })
            
        except Exception as e:
            return ExecutionResult.failure([f"PR creation failed: {e}"])
```

### Monitoring and Metrics

```python
from prometheus_client import Counter, Histogram, Gauge
import structlog

class AgentMetrics:
    """Metrics collection for agent performance."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        
        # Prometheus metrics
        self.task_counter = Counter(
            'agent_tasks_total',
            'Total tasks processed by agent',
            ['agent_id', 'task_type', 'status']
        )
        
        self.task_duration = Histogram(
            'agent_task_duration_seconds',
            'Task execution duration',
            ['agent_id', 'task_type']
        )
        
        self.active_tasks = Gauge(
            'agent_active_tasks',
            'Current active tasks',
            ['agent_id']
        )
        
        # Structured logging
        self.logger = structlog.get_logger("agent.metrics").bind(
            agent_id=agent_id
        )
    
    def record_task_start(self, task_type: str):
        """Record task start."""
        self.active_tasks.labels(agent_id=self.agent_id).inc()
        self.logger.info("Task started", task_type=task_type)
    
    def record_task_completion(
        self,
        task_type: str,
        duration: float,
        success: bool
    ):
        """Record task completion."""
        status = "success" if success else "failure"
        
        self.task_counter.labels(
            agent_id=self.agent_id,
            task_type=task_type,
            status=status
        ).inc()
        
        self.task_duration.labels(
            agent_id=self.agent_id,
            task_type=task_type
        ).observe(duration)
        
        self.active_tasks.labels(agent_id=self.agent_id).dec()
        
        self.logger.info(
            "Task completed",
            task_type=task_type,
            duration=duration,
            success=success
        )

class MonitoringMixin:
    """Mixin to add monitoring capabilities to agents."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.metrics = AgentMetrics(self.agent_id)
    
    async def process_prp(self, prp: AgentPRP) -> ExecutionResult:
        """Process PRP with monitoring."""
        task_type = f"prp_{prp.metadata.get('type', 'general')}"
        
        self.metrics.record_task_start(task_type)
        start_time = time.time()
        
        try:
            result = await super().process_prp(prp)
            duration = time.time() - start_time
            
            self.metrics.record_task_completion(
                task_type, duration, result.is_successful
            )
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_task_completion(task_type, duration, False)
            raise

# Enhanced agent with monitoring
class MonitoredDatabaseAgent(MonitoringMixin, DatabaseAgent):
    """Database agent with built-in monitoring."""
    pass
```

## Performance Optimization

### Caching Strategies

```python
from functools import wraps
import hashlib
import pickle
from typing import Any, Callable

class AgentCache:
    """Caching layer for agent operations."""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    def cache_key(self, func_name: str, *args, **kwargs) -> str:
        """Generate cache key from function and arguments."""
        key_data = f"{func_name}:{pickle.dumps((args, kwargs))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def get(self, key: str) -> Any:
        """Get cached value."""
        data = await self.redis.get(key)
        return pickle.loads(data) if data else None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Set cached value."""
        ttl = ttl or self.default_ttl
        await self.redis.setex(key, ttl, pickle.dumps(value))
    
    def cached(self, ttl: int = None):
        """Decorator for caching function results."""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = self.cache_key(func.__name__, *args, **kwargs)
                
                # Try cache first
                cached_result = await self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Cache result
                await self.set(cache_key, result, ttl)
                
                return result
            
            return wrapper
        return decorator

class CachedKnowledgeBase(ChromaVectorStore):
    """Knowledge base with caching layer."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = AgentCache(redis_client)
    
    @cache.cached(ttl=1800)  # 30 minutes
    async def query(self, query: str, **kwargs) -> List[KnowledgeEntry]:
        """Query with caching."""
        return await super().query(query, **kwargs)
```

### Connection Pooling

```python
class ConnectionPool:
    """Connection pool for external services."""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: List[Any] = []
        self.available_connections = asyncio.Queue(maxsize=max_connections)
        self.lock = asyncio.Lock()
    
    async def get_connection(self):
        """Get connection from pool."""
        try:
            return await asyncio.wait_for(
                self.available_connections.get(), 
                timeout=30.0
            )
        except asyncio.TimeoutError:
            raise Exception("Connection pool exhausted")
    
    async def return_connection(self, connection):
        """Return connection to pool."""
        await self.available_connections.put(connection)
    
    async def create_connection(self):
        """Create new connection (implement in subclass)."""
        raise NotImplementedError

class PooledLLMProvider(LLMProvider):
    """LLM provider with connection pooling."""
    
    def __init__(self, max_connections: int = 5):
        self.pool = ConnectionPool(max_connections)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using pooled connection."""
        connection = await self.pool.get_connection()
        
        try:
            # Use connection for LLM request
            response = await self._make_llm_request(connection, prompt, **kwargs)
            return response
        finally:
            await self.pool.return_connection(connection)
```

## Deployment Patterns

### Agent Factory Pattern

```python
class AgentFactory:
    """Factory for creating and managing agent instances."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.shared_resources = self._create_shared_resources()
    
    def _create_shared_resources(self) -> Dict[str, Any]:
        """Create shared resources for all agents."""
        return {
            "knowledge_base": ChromaVectorStore(
                **self.config["chroma"]
            ),
            "message_bus": RedisMessageBus(
                **self.config["redis"]
            ),
            "llm_provider": self._create_llm_provider(),
            "metrics": PrometheusMetrics()
        }
    
    def create_agent(
        self, 
        agent_type: str, 
        agent_config: Dict[str, Any]
    ) -> BaseAgent:
        """Create agent instance of specified type."""
        
        agent_classes = {
            "coordinator": TaskCoordinator,
            "planner": FeaturePlanner,
            "coder": ImplementationCoder,
            "tester": AutomatedTester,
            "reviewer": CodeReviewer,
            "devops": DevOpsAgent,
            "database": DatabaseAgent,
            "github": GitHubAgent
        }
        
        if agent_type not in agent_classes:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = agent_classes[agent_type]
        
        # Merge shared resources with agent-specific config
        full_config = {
            **self.shared_resources,
            **agent_config,
            "agent_id": f"{agent_type}-{uuid.uuid4().hex[:8]}",
            "role": agent_type
        }
        
        return agent_class(**full_config)
    
    async def create_agent_fleet(
        self, 
        fleet_config: Dict[str, Any]
    ) -> List[BaseAgent]:
        """Create a fleet of agents based on configuration."""
        
        agents = []
        
        for agent_type, instances_config in fleet_config.items():
            instance_count = instances_config.get("count", 1)
            agent_config = instances_config.get("config", {})
            
            for i in range(instance_count):
                agent = self.create_agent(agent_type, {
                    **agent_config,
                    "instance_id": i
                })
                agents.append(agent)
        
        return agents

# Usage example
async def deploy_agent_system():
    """Deploy complete agent system."""
    
    # Load configuration
    config = {
        "chroma": {"host": "localhost", "port": 8000},
        "redis": {"host": "localhost", "port": 6379},
        "llm": {"provider": "openai", "model": "gpt-4"}
    }
    
    # Create factory
    factory = AgentFactory(config)
    
    # Define fleet composition
    fleet_config = {
        "coordinator": {"count": 1},
        "planner": {"count": 1},
        "coder": {"count": 3, "config": {"max_concurrent_tasks": 2}},
        "tester": {"count": 2},
        "reviewer": {"count": 1},
        "devops": {"count": 1}
    }
    
    # Create agent fleet
    agents = await factory.create_agent_fleet(fleet_config)
    
    # Start all agents
    for agent in agents:
        await agent.start()
    
    return agents
```

### Health Monitoring

```python
class AgentHealthMonitor:
    """Health monitoring for agent fleet."""
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.health_checks = {}
    
    async def check_agent_health(self, agent: BaseAgent) -> Dict[str, Any]:
        """Check health of individual agent."""
        
        health_status = {
            "agent_id": agent.agent_id,
            "status": agent.status.value,
            "last_heartbeat": agent.info.last_heartbeat,
            "current_task": agent.current_task.id if agent.current_task else None,
            "performance_metrics": agent.performance_metrics.to_dict(),
            "memory_usage": self._get_memory_usage(),
            "healthy": True,
            "issues": []
        }
        
        # Check if agent is responsive
        if agent.status == AgentStatus.OFFLINE:
            health_status["healthy"] = False
            health_status["issues"].append("Agent is offline")
        
        # Check heartbeat freshness
        if agent.info.last_heartbeat:
            time_since_heartbeat = (
                datetime.now() - agent.info.last_heartbeat
            ).total_seconds()
            
            if time_since_heartbeat > 120:  # 2 minutes
                health_status["healthy"] = False
                health_status["issues"].append("Heartbeat is stale")
        
        return health_status
    
    async def check_fleet_health(self) -> Dict[str, Any]:
        """Check health of entire agent fleet."""
        
        agent_healths = []
        
        for agent in self.agents:
            health = await self.check_agent_health(agent)
            agent_healths.append(health)
        
        # Calculate fleet metrics
        total_agents = len(self.agents)
        healthy_agents = sum(1 for h in agent_healths if h["healthy"])
        
        return {
            "fleet_status": "healthy" if healthy_agents == total_agents else "degraded",
            "total_agents": total_agents,
            "healthy_agents": healthy_agents,
            "unhealthy_agents": total_agents - healthy_agents,
            "agent_health": agent_healths,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage."""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss_mb": memory_info.rss / 1024 / 1024,
            "vms_mb": memory_info.vms / 1024 / 1024,
            "percent": process.memory_percent()
        }
```

---

## API Documentation Generation

### Automatic API Documentation

```python
def generate_agent_api_docs(agent_class: type) -> str:
    """Generate API documentation for agent class."""
    
    capabilities = getattr(agent_class, 'capabilities', [])
    methods = [
        method for method in dir(agent_class)
        if not method.startswith('_') and callable(getattr(agent_class, method))
    ]
    
    doc = f"""
    # {agent_class.__name__} API Documentation
    
    ## Capabilities
    {chr(10).join(f"- {cap}" for cap in capabilities)}
    
    ## Public Methods
    """
    
    for method_name in methods:
        method = getattr(agent_class, method_name)
        if hasattr(method, '__doc__') and method.__doc__:
            doc += f"""
            ### {method_name}
            ```python
            {method.__doc__}
            ```
            """
    
    return doc

# Generate docs for all agent classes
def generate_all_agent_docs():
    """Generate documentation for all agent classes."""
    
    agent_classes = [
        TaskCoordinator, FeaturePlanner, ImplementationCoder,
        AutomatedTester, CodeReviewer, DevOpsAgent
    ]
    
    docs = []
    for agent_class in agent_classes:
        doc = generate_agent_api_docs(agent_class)
        docs.append(doc)
    
    return "\n\n".join(docs)
```

---

For more information, see:
- [Architecture Documentation](ARCHITECTURE.md) for system design details
- [Configuration Guide](CONFIGURATION.md) for setup and tuning
- [API Reference](API_REFERENCE.md) for external interfaces
- [Troubleshooting Guide](TROUBLESHOOTING.md) for debugging help
