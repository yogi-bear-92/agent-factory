# Agent Factory Documentation

Welcome to the comprehensive documentation for **Agent Factory** - an AI-driven autonomous development framework that transforms feature specifications into deployed applications using specialized AI agents.

## 🚀 Quick Start

- **New to Agent Factory?** Start with the [User Guide](USER_GUIDE.md)
- **Setting up the system?** Check the [Configuration Guide](CONFIGURATION.md)
- **Having issues?** Visit our [Troubleshooting Guide](TROUBLESHOOTING.md)

## 📚 Documentation Categories

### For Users

#### [User Guide](USER_GUIDE.md) - Getting Started & Usage
Complete guide for end users working with the autonomous development system:
- Getting started with the agent system
- Creating and submitting feature specifications
- Understanding agent roles and capabilities  
- Monitoring development progress
- Interpreting results and deployment notifications
- Common use cases and examples

### For Developers & Integrators

#### [API Reference](API_REFERENCE.md) - Complete API Documentation
Comprehensive reference for REST and WebSocket interfaces:
- REST API endpoints with examples
- WebSocket streaming interfaces
- Authentication and authorization
- Request/response schemas
- Error handling and rate limiting
- SDK examples in multiple languages

#### [Architecture Documentation](ARCHITECTURE.md) - System Design
In-depth technical documentation covering system architecture:
- High-level system design and components
- Agent roles and communication patterns
- Redis pub/sub messaging architecture
- Chroma vector database design
- LangChain/LangGraph workflow orchestration
- Deployment and scaling considerations

#### [Developer Reference](DEVELOPER_REFERENCE.md) - Extension Guide
Technical reference for developers extending the system:
- Base classes and interfaces
- Custom agent implementation guide
- Knowledge base integration patterns
- Communication protocol specifications
- Testing frameworks and utilities

### For Operations & DevOps

#### [Configuration Guide](CONFIGURATION.md) - Setup & Configuration
Complete configuration reference for system deployment:
- Environment variables and .env setup
- Agent configuration and tuning
- LLM provider configuration (OpenAI, Azure, local)
- Redis and Chroma database configuration
- Docker deployment configurations
- Security settings and best practices

#### [Integration Guide](INTEGRATION_GUIDE.md) - External Integrations
Guide for integrating with external tools and systems:
- Git integration for version control
- CI/CD pipeline integration
- External API integrations
- MCP server integrations (serena, archon, browsermcp)
- Custom tool development
- Webhook configurations

### For Project Management & Best Practices

#### [Best Practices Guide](BEST_PRACTICES.md) - Optimization & Standards
Guidelines for optimal usage and system management:
- PRP template selection and customization
- Context curation strategies
- Agent task decomposition patterns
- Validation gate design principles
- Performance optimization techniques
- Security considerations
- Scaling strategies for large projects

### For Support & Maintenance

#### [Troubleshooting Guide](TROUBLESHOOTING.md) - Problem Resolution
Comprehensive troubleshooting reference:
- Common setup and installation issues
- Agent communication problems
- Knowledge base indexing issues
- PRP execution failures and recovery
- Performance bottlenecks and solutions
- Log analysis and debugging techniques
- FAQ section with solutions

## 📖 Documentation by Use Case

### I Want To...

#### 🎯 **Submit a feature for autonomous development**
1. Read [User Guide - Creating Feature Specifications](USER_GUIDE.md#creating-feature-specifications)
2. Review [Best Practices - PRP Creation](BEST_PRACTICES.md#prp-creation-patterns)
3. Use [API Reference - Features API](API_REFERENCE.md#features-api) for integration

#### 🔧 **Set up Agent Factory for my team**
1. Follow [Configuration Guide - Environment Setup](CONFIGURATION.md#environment-setup)
2. Configure [Integration Guide - Git Integration](INTEGRATION_GUIDE.md#git-integration)
3. Set up monitoring using [Architecture Guide - Observability](ARCHITECTURE.md#monitoring-and-observability)

#### ⚡ **Integrate Agent Factory with our existing systems**
1. Review [API Reference - Authentication](API_REFERENCE.md#authentication)
2. Set up [Integration Guide - CI/CD Integration](INTEGRATION_GUIDE.md#cicd-pipeline-integration)
3. Configure [Integration Guide - Webhooks](INTEGRATION_GUIDE.md#webhook-configurations)

#### 🏗️ **Extend Agent Factory with custom agents**
1. Study [Developer Reference - Custom Agents](DEVELOPER_REFERENCE.md#custom-agent-implementation)
2. Understand [Architecture - Agent Communication](ARCHITECTURE.md#communication-patterns)
3. Follow [Best Practices - Agent Development](BEST_PRACTICES.md#agent-development-patterns)

#### 🐛 **Debug issues with the system**
1. Check [Troubleshooting Guide - Common Issues](TROUBLESHOOTING.md#common-issues)
2. Review [Architecture - System Health](ARCHITECTURE.md#monitoring-and-observability)
3. Use [API Reference - System Health](API_REFERENCE.md#health-check) endpoints

#### 📊 **Scale Agent Factory for high-volume usage**
1. Review [Architecture - Scalability](ARCHITECTURE.md#scalability-considerations)
2. Configure [Configuration Guide - Performance Tuning](CONFIGURATION.md#performance-tuning)
3. Implement [Best Practices - Scaling Strategies](BEST_PRACTICES.md#scaling-strategies)

## 🏗️ System Components Overview

### Core Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   REST API      │    │  WebSocket      │    │   Web UI        │
│   (FastAPI)     │    │  Streaming      │    │  (Streamlit)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────────────────────────────────────────────────────┐
│                  Agent Orchestration Layer                      │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ Task Coordinator│ Feature Planner │ Implementation Coder        │
├─────────────────┼─────────────────┼─────────────────────────────┤
│ Code Reviewer   │ Automated Tester│ DevOps Agent                │
└─────────────────┴─────────────────┴─────────────────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Redis Message   │    │ Chroma Vector   │    │ PostgreSQL      │
│ Bus (Pub/Sub)   │    │ Database        │    │ (Metadata)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Agent Roles

| Agent | Purpose | Key Capabilities |
|-------|---------|------------------|
| **Task Coordinator** | Orchestrates entire development lifecycle | Task distribution, dependency management, progress tracking |
| **Feature Planner** | Breaks down specifications into tasks | Requirements analysis, task decomposition, PRP generation |
| **Implementation Coder** | Writes production-ready code | Multi-language development, integration, refactoring |
| **Automated Tester** | Ensures code quality through testing | Unit/integration/performance testing, coverage analysis |
| **Code Reviewer** | Maintains quality and standards | Code review, security analysis, standards enforcement |
| **DevOps Agent** | Handles deployment and infrastructure | Containerization, deployment automation, monitoring |

## 🔗 External Resources

### Related Projects & Integration
- **MCP Servers**: [serena](https://github.com/modelcontextprotocol/servers), [archon](https://github.com/pchesnea/archon), browsermcp
- **LangChain**: [Framework Documentation](https://python.langchain.com/docs/get_started/introduction)
- **Chroma**: [Vector Database Documentation](https://www.trychroma.com/)
- **Redis**: [Pub/Sub Documentation](https://redis.io/docs/manual/pubsub/)
- **FastAPI**: [Web Framework Documentation](https://fastapi.tiangolo.com/)

### Community & Support
- **GitHub Repository**: [agent-factory](https://github.com/user/agent-factory)
- **Issues & Bug Reports**: Use GitHub Issues
- **Feature Requests**: Use GitHub Discussions
- **Community Discord**: [Join our Discord](https://discord.gg/agent-factory)

## 📋 Documentation Maintenance

This documentation is actively maintained and updated. Last updated: **August 2025**

### Documentation Status
See our [Documentation Status](DOCUMENTATION_STATUS.md) page for current progress and upcoming work.

### Contributing to Documentation
1. Follow the [Contributing Guide](../CONTRIBUTING.md)
2. Use the documentation templates in `/docs/templates/`
3. Ensure all examples are tested and working
4. Update cross-references when adding new content

### Documentation Standards
- **Clarity**: Write for your target audience
- **Completeness**: Include working examples
- **Consistency**: Follow established patterns
- **Currency**: Keep information up-to-date

---

## 🚀 Ready to Get Started?

Choose your path:

- **New User**: Start with the [User Guide](USER_GUIDE.md)
- **Developer**: Begin with [Architecture Documentation](ARCHITECTURE.md)
- **Ops Engineer**: Check out the [Configuration Guide](CONFIGURATION.md)
- **Integrator**: Review the [API Reference](API_REFERENCE.md)

**Happy autonomous developing!** 🤖✨
