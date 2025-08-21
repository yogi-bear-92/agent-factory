name: "Agent-Driven Autonomous Development Framework Implementation"
description: |
  Complete implementation of a multi-agent system that autonomously develops software from 
  requirements to deployment using specialized AI agents and persistent knowledge systems.

---

## Goal

**Feature Goal**: Build a complete Agent-Driven Autonomous Development Framework where specialized AI agents (Planner, Coder, Tester, Reviewer, DevOps, Integrator) collaborate to autonomously develop software from high-level specifications to deployed applications.

**Deliverable**: Multi-agent system with persistent knowledge base, agent coordination, PRP-driven workflows, and self-improvement capabilities running on local infrastructure.

**Success Definition**: The system can take a feature specification and autonomously deliver working, tested, deployed code with proper version control and continuous learning from outcomes.

## User Persona

**Target User**: Development teams, software architects, and organizations wanting to accelerate software delivery through AI automation

**Use Case**: Submit high-level feature requirements and receive complete, tested, deployed implementations without manual coding intervention

**User Journey**: 
1. User submits feature specification via API/UI
2. System decomposes into tasks and creates PRPs
3. Agents collaborate to implement, test, and deploy
4. User receives notification of completion with deployment details
5. System learns from feedback for future improvements

**Pain Points Addressed**: 
- Manual coding bottlenecks and human resource constraints
- Inconsistent code quality and testing coverage
- Slow feature delivery cycles
- Knowledge silos and context switching overhead

## Why

- **Autonomous Development**: Enable 24/7 software development without human fatigue or availability constraints
- **Consistent Quality**: Standardized development processes with automated testing and code review
- **Rapid Iteration**: Accelerate feature delivery through parallel agent coordination
- **Knowledge Preservation**: Persistent memory system prevents loss of architectural decisions and patterns
- **Self-Improvement**: System learns from successes and failures to continuously improve outcomes
- **Cost Efficiency**: Reduce development costs through automated workflows and reduced manual intervention

## What

A comprehensive multi-agent development system that transforms feature specifications into deployed applications through:

### Core Capabilities
- **Multi-Agent Team**: Specialized agents for planning, coding, testing, reviewing, and deployment
- **Persistent Knowledge Base**: Vector database storing all project context, decisions, and learnings
- **PRP-Driven Workflows**: Structured task execution with validation gates
- **Agent Coordination**: Message-based communication and task orchestration
- **Self-Learning System**: Continuous improvement from development outcomes
- **Local-First Architecture**: Runs entirely on standard VPS infrastructure

### Success Criteria

- [ ] System autonomously delivers a complete web application from specification to deployment
- [ ] All code passes automated testing with >95% test coverage
- [ ] Proper Git version control with meaningful commit messages
- [ ] Agent coordination completes complex features without human intervention
- [ ] Knowledge base successfully provides context for decision-making
- [ ] Self-improvement measurably increases success rates over time
- [ ] System handles failure scenarios gracefully with automatic recovery

## All Needed Context

### Context Completeness Check

_This PRP provides everything needed to implement a production-ready multi-agent development system, including architecture patterns, technology choices, implementation blueprints, and validation criteria._

### Documentation & References

```yaml
# MUST READ - Include these in your context window
- url: https://github.com/NirDiamant/agents-towards-production
  why: Production-grade agent tutorials covering memory, tool integration, orchestration
  critical: Agent architecture patterns and best practices for production deployment

- url: https://python.langchain.com/docs/get_started/introduction
  why: LangChain framework for building agent workflows and tool integration
  pattern: Agent creation, memory management, and tool interfaces
  gotcha: Proper state management and token limits in agent chains

- url: https://www.trychroma.com/
  why: Local vector database for knowledge storage and RAG implementation
  pattern: Document ingestion, embedding generation, and similarity search
  gotcha: Embedding model consistency and vector dimension matching

- file: PRPs/templates/prp_base.md
  why: Existing PRP template structure for agent task specification
  pattern: Goal/Why/What/Context structure for agent instructions
  gotcha: Must adapt for programmatic agent consumption vs human reading

- file: PRPs/scripts/prp_runner.py
  why: Current PRP execution patterns for integration with agent system
  pattern: Script-based PRP processing and validation loops
  gotcha: Interactive vs headless modes for agent automation

- docfile: PRPs/ai_docs/cc_commands.md
  why: Claude Code command patterns for tool integration
  section: Tool orchestration and multi-step workflows
```

### Current Codebase Structure

```bash
agent-factory/
├── .claude/
│   ├── commands/           # 35+ pre-configured Claude commands
│   └── settings.local.json # Tool permissions
├── PRPs/
│   ├── templates/         # PRP templates with validation
│   ├── scripts/          # PRP runner and utilities
│   ├── ai_docs/          # Curated documentation
│   └── README.md         # PRP methodology
├── claude_md_files/      # Framework-specific examples
├── CLAUDE.md             # Project instructions
└── pyproject.toml        # Python package config
```

### Desired Codebase Structure with Agent Framework

```bash
agent-factory/
├── src/
│   ├── agents/           # Agent implementations
│   │   ├── base/         # Base agent classes and interfaces
│   │   ├── coordinator/  # Task coordination and orchestration
│   │   ├── planner/      # Task breakdown and PRP generation
│   │   ├── coder/        # Code implementation agents
│   │   ├── tester/       # Test execution and validation
│   │   ├── reviewer/     # Code review and quality assurance
│   │   └── devops/       # Deployment and infrastructure
│   ├── knowledge/        # Knowledge base and memory system
│   │   ├── vector_store/ # Chroma vector database integration
│   │   ├── memory/       # Agent memory management
│   │   └── rag/          # Retrieval-augmented generation
│   ├── communication/    # Agent communication layer
│   │   ├── message_bus/  # Redis pub/sub implementation
│   │   ├── protocols/    # Agent communication protocols
│   │   └── coordination/ # Task coordination logic
│   ├── workflows/        # PRP-driven workflow execution
│   │   ├── prp_engine/   # PRP processing and execution
│   │   ├── validation/   # Validation gate implementations
│   │   └── monitoring/   # Workflow monitoring and metrics
│   ├── api/              # External interfaces
│   │   ├── rest/         # FastAPI REST endpoints
│   │   ├── streaming/    # WebSocket streaming interfaces
│   │   └── ui/           # Streamlit dashboard
│   ├── tools/            # External tool integrations
│   │   ├── git/          # Git operations and version control
│   │   ├── testing/      # Test framework integrations
│   │   └── deployment/   # Deployment tool integrations
│   └── config/           # Configuration and settings
├── tests/                # Comprehensive test suite
├── docker/               # Docker configurations
├── docs/                 # Technical documentation
└── requirements/         # Dependency specifications
```

### Known Gotchas & Library Quirks

```python
# CRITICAL: LangChain agent state management
# LangChain agents maintain state across conversations but can lose context
# Must implement proper checkpointing and state persistence

# CRITICAL: Chroma vector database consistency
# Embedding models must remain consistent across sessions
# Vector dimensions must match between ingestion and querying

# CRITICAL: Redis pub/sub message ordering
# Redis doesn't guarantee message ordering in pub/sub
# Must implement sequence numbers or acknowledgment patterns

# CRITICAL: Agent token limits and context windows
# Local LLMs have strict context limits (4K-8K tokens typically)
# Must implement intelligent context truncation and summarization

# CRITICAL: Docker container coordination
# Each agent service must be independently scalable
# Network communication between containers requires proper configuration

# CRITICAL: PRP programmatic consumption
# Current PRPs are human-readable; agents need structured JSON format
# Must create agent-optimized PRP templates with clear field definitions
```

## Implementation Blueprint

### Data Models and Structure

Create the core data models ensuring type safety and consistency across the multi-agent system.

```python
# Agent Communication Models
@dataclass
class AgentMessage:
    id: str
    sender_id: str
    recipient_id: str
    message_type: MessageType
    payload: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None

@dataclass
class TaskSpecification:
    id: str
    title: str
    description: str
    requirements: List[str]
    acceptance_criteria: List[str]
    priority: TaskPriority
    assigned_agent: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)

# Knowledge Base Models
@dataclass
class KnowledgeEntry:
    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]
    source_type: SourceType
    created_at: datetime
    tags: List[str] = field(default_factory=list)

# PRP Models for Agents
@dataclass
class AgentPRP:
    goal: str
    justification: str
    context: Dict[str, Any]
    implementation_steps: List[str]
    validation_criteria: List[str]
    success_metrics: List[str]
    failure_recovery: List[str]
```

### Implementation Tasks (ordered by dependencies)

```yaml
Task 1: CREATE src/knowledge/vector_store/chroma_client.py
  - IMPLEMENT: ChromaVectorStore class with async operations
  - FOLLOW pattern: Chroma documentation patterns for local deployment
  - NAMING: ChromaVectorStore class, async def store_*, query_*, delete_* methods
  - DEPENDENCIES: Install chromadb, sentence-transformers for embeddings
  - PLACEMENT: Knowledge layer foundational component

Task 2: CREATE src/communication/message_bus/redis_messenger.py
  - IMPLEMENT: RedisMessageBus class for agent communication
  - FOLLOW pattern: Redis pub/sub with async/await support
  - NAMING: RedisMessageBus class, async def publish_*, subscribe_*, handle_* methods
  - DEPENDENCIES: Install redis-py with async support
  - PLACEMENT: Communication layer foundation

Task 3: CREATE src/agents/base/agent_interface.py
  - IMPLEMENT: BaseAgent abstract class and AgentInterface protocol
  - FOLLOW pattern: LangChain agent base classes and interfaces
  - NAMING: BaseAgent, AgentInterface, async def process_*, execute_*, respond_* methods
  - DEPENDENCIES: Import from Task 1 and 2 for knowledge and communication
  - PLACEMENT: Agent system foundation

Task 4: CREATE src/workflows/prp_engine/agent_prp_processor.py
  - IMPLEMENT: AgentPRPProcessor for structured PRP execution
  - FOLLOW pattern: PRPs/scripts/prp_runner.py but for programmatic agent use
  - NAMING: AgentPRPProcessor class, async def parse_*, execute_*, validate_* methods
  - DEPENDENCIES: Import agent interfaces and knowledge base
  - PLACEMENT: Workflow execution core

Task 5: CREATE src/agents/coordinator/task_coordinator.py
  - IMPLEMENT: TaskCoordinator agent for high-level orchestration
  - FOLLOW pattern: Multi-agent coordination patterns from LangChain
  - NAMING: TaskCoordinator class inheriting from BaseAgent
  - DEPENDENCIES: Use message bus and PRP processor from previous tasks
  - PLACEMENT: Central coordination agent

Task 6: CREATE src/agents/planner/feature_planner.py
  - IMPLEMENT: FeaturePlanner agent for task breakdown and PRP generation
  - FOLLOW pattern: Planning agent patterns with structured output
  - NAMING: FeaturePlanner class, async def analyze_*, breakdown_*, generate_prp_* methods
  - DEPENDENCIES: Knowledge base for context retrieval, coordinator for task assignment
  - PLACEMENT: Planning layer agent

Task 7: CREATE src/agents/coder/implementation_coder.py
  - IMPLEMENT: ImplementationCoder agent for code generation
  - FOLLOW pattern: Code generation with existing codebase context awareness
  - NAMING: ImplementationCoder class, async def implement_*, refactor_*, integrate_* methods
  - DEPENDENCIES: Knowledge base for pattern retrieval, file system tools
  - PLACEMENT: Implementation layer agent

Task 8: CREATE src/agents/tester/automated_tester.py
  - IMPLEMENT: AutomatedTester agent for test execution and validation
  - FOLLOW pattern: Test automation with multiple framework support
  - NAMING: AutomatedTester class, async def run_tests_*, generate_reports_*, validate_* methods
  - DEPENDENCIES: Testing tool integrations, result reporting to knowledge base
  - PLACEMENT: Quality assurance layer

Task 9: CREATE src/agents/reviewer/code_reviewer.py
  - IMPLEMENT: CodeReviewer agent for quality and standards checking
  - FOLLOW pattern: Automated code review with configurable rules
  - NAMING: CodeReviewer class, async def review_*, check_standards_*, suggest_improvements_* methods
  - DEPENDENCIES: Static analysis tools, knowledge base for standards
  - PLACEMENT: Quality assurance layer

Task 10: CREATE src/agents/devops/deployment_agent.py
  - IMPLEMENT: DeploymentAgent for automated deployment and monitoring
  - FOLLOW pattern: CI/CD automation with deployment pipelines
  - NAMING: DeploymentAgent class, async def deploy_*, monitor_*, rollback_* methods
  - DEPENDENCIES: Deployment tools, infrastructure monitoring
  - PLACEMENT: Operations layer agent

Task 11: CREATE src/api/rest/agent_api.py
  - IMPLEMENT: FastAPI application with agent coordination endpoints
  - FOLLOW pattern: RESTful API design with async request handling
  - NAMING: FastAPI app, /features/create, /tasks/status, /agents/health endpoints
  - DEPENDENCIES: All agent implementations, message bus for communication
  - PLACEMENT: External interface layer

Task 12: CREATE src/workflows/monitoring/agent_monitor.py
  - IMPLEMENT: AgentMonitor for system observability and metrics
  - FOLLOW pattern: Observability best practices with structured logging
  - NAMING: AgentMonitor class, async def track_*, analyze_*, alert_* methods
  - DEPENDENCIES: All agent implementations for metrics collection
  - PLACEMENT: Monitoring and observability layer

Task 13: CREATE docker/docker-compose.yml
  - IMPLEMENT: Multi-container deployment configuration
  - FOLLOW pattern: Microservices with Redis, Chroma, and agent services
  - NAMING: Standard Docker Compose service definitions
  - DEPENDENCIES: All implemented services and their configurations
  - PLACEMENT: Deployment configuration
```

### Implementation Patterns & Key Details

```python
# Agent Base Pattern - All agents inherit from this
class BaseAgent:
    def __init__(self, agent_id: str, knowledge_base: ChromaVectorStore, 
                 message_bus: RedisMessageBus):
        self.agent_id = agent_id
        self.knowledge = knowledge_base
        self.messenger = message_bus
        self.llm = self._initialize_llm()
        
    async def process_prp(self, prp: AgentPRP) -> AgentResponse:
        # PATTERN: Standard PRP processing flow
        context = await self.knowledge.get_relevant_context(prp.goal)
        response = await self.llm.process(prp, context)
        await self.knowledge.store_outcome(prp, response)
        return response

# Knowledge Retrieval Pattern - RAG implementation
class KnowledgeRetriever:
    async def get_relevant_context(self, query: str, limit: int = 5) -> List[str]:
        # PATTERN: Embedding-based similarity search
        embedding = await self.embed_query(query)
        results = await self.vector_store.query(embedding, limit)
        # GOTCHA: Always include metadata for context understanding
        return [self._format_context(result) for result in results]

# Agent Communication Pattern - Message passing
class AgentCommunicator:
    async def send_task(self, recipient: str, task: TaskSpecification):
        message = AgentMessage(
            sender_id=self.agent_id,
            recipient_id=recipient,
            message_type=MessageType.TASK_ASSIGNMENT,
            payload=asdict(task),
            correlation_id=task.id
        )
        await self.message_bus.publish(f"agent.{recipient}", message)
        
    # PATTERN: Async message handling with error recovery
    async def handle_message(self, message: AgentMessage):
        try:
            if message.message_type == MessageType.TASK_ASSIGNMENT:
                await self.process_task(TaskSpecification(**message.payload))
            elif message.message_type == MessageType.TASK_RESULT:
                await self.handle_task_result(message.payload)
        except Exception as e:
            await self.send_error_response(message, e)

# PRP Engine Pattern - Structured execution
class AgentPRPProcessor:
    async def execute_prp(self, prp: AgentPRP, agent: BaseAgent) -> ExecutionResult:
        # PATTERN: Validation before execution
        validation_result = await self.validate_prp(prp)
        if not validation_result.is_valid:
            return ExecutionResult.failure(validation_result.errors)
            
        # PATTERN: Context injection from knowledge base
        context = await self.knowledge.get_context_for_prp(prp)
        enhanced_prp = self.inject_context(prp, context)
        
        # PATTERN: Execution with monitoring
        result = await agent.execute(enhanced_prp)
        await self.store_execution_outcome(prp, result)
        
        return result

# Self-Learning Pattern - Outcome analysis
class LearningSystem:
    async def learn_from_outcome(self, prp: AgentPRP, result: ExecutionResult):
        # PATTERN: Success pattern extraction
        if result.is_successful:
            success_pattern = self.extract_success_pattern(prp, result)
            await self.knowledge.store_pattern(success_pattern)
        else:
            # PATTERN: Failure analysis and prevention
            failure_analysis = self.analyze_failure(prp, result)
            await self.knowledge.store_failure_pattern(failure_analysis)
            
        # PATTERN: Continuous improvement
        await self.update_agent_behaviors(result.performance_metrics)
```

### Integration Points

```yaml
VECTOR_DATABASE:
  - storage: "Chroma local vector database for embeddings"
  - index: "Create collections for docs, code, patterns, failures"
  - embedding: "Use sentence-transformers/all-MiniLM-L6-v2 for consistency"

MESSAGE_BUS:
  - redis: "Redis pub/sub for agent communication"
  - channels: "agent.{agent_id} for direct messaging, broadcast.{topic} for announcements"
  - persistence: "Redis streams for message history and replay"

API_GATEWAY:
  - fastapi: "REST API for external feature requests"
  - websockets: "Real-time progress streaming to clients"
  - authentication: "API key based access control"

EXTERNAL_TOOLS:
  - git: "GitPython for version control operations"
  - testing: "pytest, unittest integration for automated testing"
  - linting: "ruff, mypy integration for code quality"
  - deployment: "Docker compose for local deployment automation"

MONITORING:
  - logging: "Structured JSON logging with correlation IDs"
  - metrics: "Prometheus metrics for agent performance"
  - tracing: "OpenTelemetry for distributed request tracing"
```

## Validation Loop

### Level 1: Component Testing (Immediate Feedback)

```bash
# Test each component as implemented
uv run pytest src/knowledge/tests/ -v
uv run pytest src/communication/tests/ -v
uv run pytest src/agents/tests/ -v

# Integration testing between components
uv run pytest src/workflows/tests/ -v
uv run pytest src/api/tests/ -v

# Code quality validation
ruff check src/ --fix
mypy src/
ruff format src/

# Expected: All component tests pass, no linting errors
```

### Level 2: Agent System Testing (Multi-Agent Validation)

```bash
# Start the complete system
docker-compose up -d

# Verify all services are healthy
curl http://localhost:8000/health
curl http://localhost:8001/agents/status

# Test agent communication
uv run python -m src.tests.integration.test_agent_communication

# Test knowledge base operations
uv run python -m src.tests.integration.test_knowledge_base

# Test PRP processing
uv run python -m src.tests.integration.test_prp_execution

# Expected: All agents communicate successfully, knowledge retrieval works
```

### Level 3: End-to-End Workflow Testing (System Validation)

```bash
# Submit a simple feature request
curl -X POST http://localhost:8000/features \
  -H "Content-Type: application/json" \
  -d '{
    "title": "User Authentication API",
    "description": "Create REST API endpoints for user login/logout",
    "requirements": ["JWT tokens", "Password hashing", "Rate limiting"]
  }'

# Monitor agent coordination
curl http://localhost:8000/features/{feature_id}/status

# Verify code generation
ls -la generated_code/
git log --oneline

# Test deployment
curl http://localhost:3000/auth/health

# Expected: Complete feature delivered with tests and deployment
```

### Level 4: Self-Learning and Performance Validation

```bash
# Performance metrics validation
curl http://localhost:8000/metrics/agents
curl http://localhost:8000/metrics/features

# Learning system validation
uv run python -m src.tests.validation.test_learning_system

# Knowledge base growth validation
curl http://localhost:8000/knowledge/stats

# Multi-feature parallel processing
uv run python -m src.tests.load.test_concurrent_features

# Failure recovery testing
uv run python -m src.tests.chaos.test_agent_failures

# Expected: System learns from outcomes, improves over time, handles failures gracefully
```

## Final Validation Checklist

### Technical Validation

- [ ] All 4 validation levels completed successfully
- [ ] All tests pass: `uv run pytest src/ -v`
- [ ] No linting errors: `ruff check src/`
- [ ] No type errors: `mypy src/`
- [ ] Docker compose deployment successful
- [ ] All agent services healthy and communicating

### Functional Validation

- [ ] System autonomously completes feature from specification to deployment
- [ ] Agent coordination works without human intervention
- [ ] Knowledge base provides relevant context for decision-making
- [ ] PRP execution follows structured validation gates
- [ ] Self-learning improves success rates over iterations
- [ ] Failure scenarios handled gracefully with recovery

### Performance Validation

- [ ] Feature delivery time under 30 minutes for simple features
- [ ] Agent response time under 10 seconds for task processing
- [ ] Knowledge retrieval under 2 seconds for context queries
- [ ] System handles 5+ concurrent features without degradation
- [ ] Memory usage stable over extended operation

### Integration Validation

- [ ] Integrates with existing agent-factory PRP methodology
- [ ] Compatible with current Claude Code command system
- [ ] Knowledge base successfully stores and retrieves project context
- [ ] API endpoints respond correctly to external requests
- [ ] Monitoring and observability provide actionable insights

---

## Anti-Patterns to Avoid

- ❌ Don't implement agents as simple LLM wrappers - they need state and memory
- ❌ Don't skip the knowledge base - agents will repeat mistakes without learning
- ❌ Don't use synchronous communication - async message passing is essential
- ❌ Don't ignore failure scenarios - agents must handle and learn from failures
- ❌ Don't hardcode agent behaviors - make them configurable and learnable
- ❌ Don't skip monitoring - observability is critical for multi-agent debugging
- ❌ Don't forget security - API endpoints need authentication and input validation