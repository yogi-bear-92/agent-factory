# Agent Factory - User Guide

Welcome to **Agent Factory**, an AI-driven autonomous development framework that transforms feature specifications into deployed applications using specialized AI agents.

## Table of Contents

- [Getting Started](#getting-started)
- [Core Concepts](#core-concepts)
- [Agent Team Overview](#agent-team-overview)
- [Creating Feature Specifications](#creating-feature-specifications)
- [Monitoring Development Progress](#monitoring-development-progress)
- [Understanding Results](#understanding-results)
- [Common Use Cases](#common-use-cases)
- [Advanced Workflows](#advanced-workflows)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Prerequisites

> **📖 Detailed Prerequisites**: See [Shared Components - Prerequisites](SHARED_COMPONENTS.md#prerequisites) for complete installation requirements.

### Quick Start

> **📖 Complete Quick Start**: See [../QUICKSTART.md](../QUICKSTART.md) for the complete 5-minute setup guide.

**Summary:**
1. Install dependencies and start services
2. Initialize Claude context
3. Create your first PRP
4. Execute with multi-agent system

## Core Concepts

### Product Requirement Prompts (PRPs)

PRPs are comprehensive, structured documents that provide everything an AI agent needs to successfully implement a feature:

**PRP Structure**:
- **Goal**: Clear, specific objective
- **Why**: Business justification and user value
- **What**: Detailed requirements and success criteria
- **Context**: All necessary documentation, examples, and gotchas
- **Implementation Blueprint**: Step-by-step technical plan
- **Validation Gates**: Executable tests and quality checks

### Core Concepts Overview

> **📖 Detailed Core Concepts**: See [Shared Components - Core Concepts](SHARED_COMPONENTS.md#core-concepts) for comprehensive explanations of:
> - Product Requirement Prompts (PRPs)
> - Autonomous Development Workflow
> - Knowledge Base architecture

## Agent Team Overview

> **📖 Complete Agent Descriptions**: See [Shared Components - Agent Descriptions](SHARED_COMPONENTS.md#agent-descriptions) for detailed information about each agent's role, responsibilities, and capabilities.

## Creating Feature Specifications

### Basic Feature Request

The simplest way to request a feature is through a JSON specification:

```json
{
  "title": "Shopping Cart API",
  "description": "REST API for e-commerce shopping cart functionality",
  "priority": "high",
  "requirements": [
    "Add/remove items from cart",
    "Calculate totals with tax",
    "Apply discount codes",
    "Session persistence",
    "RESTful endpoints"
  ],
  "acceptance_criteria": [
    "All endpoints return proper HTTP status codes",
    "Response time under 200ms",
    "Handles concurrent users",
    "Input validation on all endpoints",
    "Comprehensive test coverage >95%"
  ]
}
```

### Advanced PRP Creation

For complex features, you can provide additional context:

```json
{
  "title": "Real-time Chat System",
  "description": "WebSocket-based chat with rooms and message history",
  "priority": "medium",
  "requirements": [
    "WebSocket connections",
    "Room-based messaging",
    "Message persistence",
    "User authentication",
    "Typing indicators"
  ],
  "context": {
    "existing_systems": [
      "User authentication system already exists",
      "Redis available for session storage"
    ],
    "constraints": [
      "Must support 1000+ concurrent connections",
      "Message history limited to 30 days"
    ],
    "references": [
      "Similar implementation in project X",
      "Follow WebSocket best practices guide"
    ]
  },
  "success_metrics": [
    "Supports 1000+ concurrent connections",
    "Message delivery latency <100ms",
    "99.9% uptime",
    "Zero data loss"
  ]
}
```

### Using Claude Code for PRP Creation

For the most comprehensive PRPs, use the built-in Claude Code commands:

```bash
# Generate a comprehensive PRP with research and context
claude /prp-base-create "Real-time notification system with push notifications"

# Create planning documents with architecture diagrams
claude /prp-planning-create "Microservices architecture for notification service"
```

## Monitoring Development Progress

### Real-time Progress Tracking

Connect to the WebSocket endpoint for live updates:

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/progress');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log(`Agent ${update.agent_id}: ${update.status}`);
  console.log(`Progress: ${update.progress}%`);
};
```

### REST API Status Checks

Query specific feature status:

```bash
# Get feature status
curl http://localhost:8080/features/{feature_id}/status

# Get agent status
curl http://localhost:8080/agents/status

# Get detailed progress
curl http://localhost:8080/features/{feature_id}/progress
```

### Progress Indicators

**Feature Lifecycle Stages**:
1. **Planning** (0-20%): Feature analysis and task breakdown
2. **Implementation** (20-70%): Code development and testing
3. **Review** (70-85%): Code review and quality assurance
4. **Deployment** (85-95%): Build, deploy, and verify
5. **Complete** (100%): Feature deployed and verified

**Agent Status Types**:
- `idle`: Agent available for new tasks
- `busy`: Agent actively working on a task
- `error`: Agent encountered an issue
- `offline`: Agent not responding

## Understanding Results

### Success Notifications

When a feature is successfully completed, you'll receive:

```json
{
  "feature_id": "feat_123",
  "status": "completed",
  "deployment_url": "https://your-app.com",
  "completion_time": "2025-01-20T10:30:00Z",
  "summary": {
    "files_created": 15,
    "files_modified": 3,
    "tests_added": 45,
    "test_coverage": "97%",
    "performance_score": "A+"
  },
  "artifacts": [
    "Generated API documentation",
    "Deployment logs",
    "Test results",
    "Performance metrics"
  ]
}
```

### Delivery Package

Each completed feature includes:

- **Source Code**: All implementation files with proper documentation
- **Tests**: Comprehensive test suite with high coverage
- **Documentation**: API docs, README updates, architectural decisions
- **Deployment Config**: Docker files, CI/CD pipeline, environment configs
- **Monitoring**: Health checks, metrics, logging configuration

### Quality Metrics

Features are validated against multiple quality gates:

**Code Quality**:
- Linting compliance: 100%
- Security scan: No critical issues
- Performance: Response times within SLA
- Test coverage: >95%

**Architecture Quality**:
- Design patterns followed
- SOLID principles applied
- Scalability considerations addressed
- Security best practices implemented

## Common Use Cases

### 1. Web Application Features

**User Authentication System**:
```json
{
  "title": "OAuth2 Social Login",
  "description": "Add Google and GitHub OAuth2 authentication",
  "requirements": [
    "OAuth2 flow implementation",
    "User profile synchronization", 
    "Session management",
    "Security best practices"
  ]
}
```

**Result**: Complete authentication system with login pages, API endpoints, database schema, tests, and security measures.

### 2. API Development

**RESTful Microservice**:
```json
{
  "title": "Product Catalog API",
  "description": "CRUD API for product management with search",
  "requirements": [
    "RESTful endpoints",
    "Database integration",
    "Search functionality",
    "Pagination and filtering",
    "API documentation"
  ]
}
```

**Result**: Fully functional API with OpenAPI documentation, database migrations, comprehensive tests, and deployment configuration.

### 3. Data Processing

**ETL Pipeline**:
```json
{
  "title": "Customer Data Pipeline", 
  "description": "Extract, transform, load customer data from multiple sources",
  "requirements": [
    "Multiple data source connectors",
    "Data transformation logic",
    "Error handling and retry",
    "Monitoring and alerting",
    "Scheduling"
  ]
}
```

**Result**: Complete data pipeline with source connectors, transformation logic, scheduling system, monitoring, and documentation.

### 4. Infrastructure Automation

**Deployment Pipeline**:
```json
{
  "title": "Multi-Environment CI/CD",
  "description": "Automated deployment pipeline for staging and production",
  "requirements": [
    "GitHub Actions workflows",
    "Environment-specific configs", 
    "Blue-green deployment",
    "Rollback capabilities",
    "Health checks"
  ]
}
```

**Result**: Complete CI/CD pipeline with automated testing, deployment strategies, monitoring, and rollback procedures.

## Advanced Workflows

### Multi-Feature Projects

For complex projects spanning multiple features:

1. **Create Project Structure**:
   ```bash
   curl -X POST http://localhost:8080/projects/create \
     -d '{"name": "E-commerce Platform", "description": "Full-featured online store"}'
   ```

2. **Submit Related Features**:
   ```bash
   # Each feature references the project
   curl -X POST http://localhost:8080/features/create \
     -d '{"project_id": "proj_123", "title": "Product Catalog", ...}'
   ```

3. **Coordinate Dependencies**:
   Features can specify dependencies on other features, and the system will ensure proper ordering.

### Custom Agent Configuration

Customize agent behavior for specific domains:

```json
{
  "agent_config": {
    "coder": {
      "preferred_patterns": ["Repository Pattern", "Factory Pattern"],
      "code_style": "PEP8",
      "frameworks": ["FastAPI", "SQLAlchemy"]
    },
    "tester": {
      "test_frameworks": ["pytest", "unittest"],
      "coverage_threshold": 95,
      "performance_testing": true
    }
  }
}
```

### Continuous Learning Mode

Enable the system to learn from your feedback:

```bash
# Provide feedback on completed features
curl -X POST http://localhost:8080/features/{feature_id}/feedback \
  -d '{
    "rating": 4,
    "improvements": ["Better error handling", "More comprehensive tests"],
    "successes": ["Excellent API design", "Good performance"]
  }'
```

## Troubleshooting

### Common Issues

**Feature Stuck in Planning**:
- Check if requirements are clear and specific
- Ensure all referenced documentation is accessible
- Verify no circular dependencies exist

**Agent Communication Errors**:
- Confirm Redis is running and accessible
- Check network connectivity between components
- Verify message bus configuration

**Knowledge Base Issues**:
- Ensure Chroma vector database is running
- Check if initial knowledge indexing completed
- Verify embedding model consistency

**Deployment Failures**:
- Check deployment target accessibility
- Verify credentials and permissions
- Review deployment logs for specific errors

### Getting Help

1. **Check System Status**: `curl http://localhost:8080/health`
2. **Review Logs**: Check agent logs for detailed error messages
3. **Agent Status**: Verify all agents are running and responsive
4. **Knowledge Base**: Ensure vector database is accessible and populated

For additional support, refer to:
- [Configuration Guide](CONFIGURATION.md) for setup issues
- [Architecture Documentation](ARCHITECTURE.md) for system understanding
- [API Reference](API_REFERENCE.md) for integration details
- [Troubleshooting Guide](TROUBLESHOOTING.md) for specific problems

---

## Next Steps

Once you're comfortable with basic usage:

1. **Explore Advanced Configuration**: Customize agents for your specific needs
2. **Set Up Monitoring**: Implement comprehensive system monitoring
3. **Create Custom Workflows**: Develop domain-specific development patterns
4. **Scale Your Deployment**: Configure multi-instance, high-availability setup

Happy autonomous developing! 🚀
