# Agent Factory - API Reference

Complete API documentation for the Agent Factory autonomous development system.

## Table of Contents

- [Authentication](#authentication)
- [REST API Endpoints](#rest-api-endpoints)
- [WebSocket Interfaces](#websocket-interfaces)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [SDK Examples](#sdk-examples)

## Authentication

Agent Factory uses API key authentication for external access and JWT tokens for session management.

### API Key Authentication

Include your API key in the `Authorization` header:

```
Authorization: Bearer your-api-key-here
```

### Getting an API Key

```bash
curl -X POST http://localhost:8080/auth/api-keys \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Integration",
    "permissions": ["features:create", "features:read", "agents:read"]
  }'
```

## REST API Endpoints

### Base URL
```
http://localhost:8080/api/v1
```

### Health Check

#### Get System Health
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development",
  "components": {
    "database": "healthy",
    "redis": "healthy",
    "vector_store": "healthy",
    "agents": {
      "coordinator": "running",
      "planner": "running", 
      "coder": "running",
      "tester": "running",
      "reviewer": "running",
      "devops": "running"
    }
  },
  "timestamp": "2025-01-20T10:30:00Z"
}
```

---

### Features API

#### Create Feature Request
```http
POST /features
```

**Request Body:**
```json
{
  "title": "User Authentication System",
  "description": "Implement secure user login and registration with JWT tokens",
  "priority": "high",
  "requirements": [
    "Secure password hashing",
    "JWT token generation",
    "Input validation",
    "Rate limiting"
  ],
  "acceptance_criteria": [
    "All endpoints return proper HTTP status codes",
    "Response time under 200ms",
    "Test coverage > 95%"
  ],
  "context": {
    "existing_systems": ["User database already exists"],
    "constraints": ["Must be backward compatible"],
    "references": ["https://example.com/auth-spec"]
  },
  "metadata": {
    "project_id": "proj_123",
    "team": "backend",
    "deadline": "2025-02-01"
  }
}
```

**Response:**
```json
{
  "id": "feat_abc123",
  "status": "planning",
  "created_at": "2025-01-20T10:30:00Z",
  "estimated_completion": "2025-01-21T18:00:00Z",
  "assigned_agents": ["planner", "coordinator"],
  "progress_url": "/features/feat_abc123/progress",
  "websocket_url": "ws://localhost:8080/features/feat_abc123/stream"
}
```

#### Get Feature Status
```http
GET /features/{feature_id}
```

**Response:**
```json
{
  "id": "feat_abc123",
  "title": "User Authentication System",
  "status": "implementation",
  "progress": 45,
  "created_at": "2025-01-20T10:30:00Z",
  "updated_at": "2025-01-20T12:15:00Z",
  "estimated_completion": "2025-01-21T18:00:00Z",
  "current_stage": "implementation",
  "tasks": [
    {
      "id": "task_001",
      "title": "Implement password hashing",
      "status": "completed",
      "assigned_agent": "coder",
      "completion_time": "2025-01-20T11:30:00Z"
    },
    {
      "id": "task_002", 
      "title": "Create JWT token service",
      "status": "in_progress",
      "assigned_agent": "coder",
      "progress": 70
    }
  ],
  "artifacts": [
    {
      "type": "source_code",
      "path": "/src/auth/password_hash.py",
      "created_at": "2025-01-20T11:30:00Z"
    }
  ]
}
```

#### List Features
```http
GET /features?status=active&limit=10&offset=0
```

**Query Parameters:**
- `status`: Filter by status (`planning`, `implementation`, `review`, `deployment`, `completed`, `failed`)
- `priority`: Filter by priority (`low`, `medium`, `high`, `critical`)
- `project_id`: Filter by project
- `limit`: Number of results (default: 20, max: 100)
- `offset`: Pagination offset

**Response:**
```json
{
  "features": [
    {
      "id": "feat_abc123",
      "title": "User Authentication System",
      "status": "implementation",
      "progress": 45,
      "priority": "high",
      "created_at": "2025-01-20T10:30:00Z"
    }
  ],
  "pagination": {
    "total": 1,
    "limit": 10,
    "offset": 0,
    "has_more": false
  }
}
```

#### Cancel Feature
```http
DELETE /features/{feature_id}
```

**Response:**
```json
{
  "id": "feat_abc123",
  "status": "cancelled",
  "cancelled_at": "2025-01-20T14:00:00Z",
  "reason": "Requirements changed"
}
```

---

### Agents API

#### Get Agent Status
```http
GET /agents
```

**Response:**
```json
{
  "agents": [
    {
      "id": "coordinator_001",
      "name": "Task Coordinator",
      "role": "coordinator",
      "status": "idle",
      "capabilities": ["task_orchestration", "dependency_management"],
      "current_task": null,
      "last_heartbeat": "2025-01-20T10:29:00Z",
      "performance": {
        "tasks_completed": 15,
        "avg_completion_time": "2.5h",
        "success_rate": 0.95
      }
    },
    {
      "id": "planner_001",
      "name": "Feature Planner",
      "role": "planner", 
      "status": "busy",
      "current_task": "task_002",
      "estimated_completion": "2025-01-20T11:00:00Z"
    }
  ]
}
```

#### Get Specific Agent
```http
GET /agents/{agent_id}
```

**Response:**
```json
{
  "id": "coder_001",
  "name": "Implementation Coder",
  "role": "coder",
  "status": "busy",
  "capabilities": [
    "python_development",
    "api_implementation", 
    "database_integration",
    "test_writing"
  ],
  "current_task": {
    "id": "task_002",
    "title": "Create JWT token service",
    "feature_id": "feat_abc123",
    "started_at": "2025-01-20T10:45:00Z",
    "progress": 70
  },
  "performance_metrics": {
    "tasks_completed_today": 3,
    "avg_task_duration": "45m",
    "code_quality_score": 0.92,
    "test_coverage_average": 0.97
  },
  "last_heartbeat": "2025-01-20T10:29:30Z"
}
```

#### Configure Agent
```http
PUT /agents/{agent_id}/config
```

**Request Body:**
```json
{
  "settings": {
    "max_concurrent_tasks": 2,
    "preferred_frameworks": ["FastAPI", "SQLAlchemy"],
    "code_style": "PEP8",
    "test_framework": "pytest",
    "performance_mode": "balanced"
  }
}
```

---

### Projects API

#### Create Project
```http
POST /projects
```

**Request Body:**
```json
{
  "name": "E-commerce Platform",
  "description": "Full-featured online store with payment processing",
  "metadata": {
    "team": "full-stack",
    "tech_stack": ["Python", "React", "PostgreSQL"],
    "deployment_target": "AWS"
  }
}
```

**Response:**
```json
{
  "id": "proj_xyz789",
  "name": "E-commerce Platform", 
  "status": "active",
  "created_at": "2025-01-20T10:30:00Z",
  "features_count": 0,
  "completion_percentage": 0
}
```

#### List Projects
```http
GET /projects
```

---

### Tasks API

#### Get Task Details
```http
GET /tasks/{task_id}
```

**Response:**
```json
{
  "id": "task_002",
  "title": "Create JWT token service",
  "description": "Implement JWT token generation, validation, and refresh logic",
  "status": "in_progress",
  "priority": "high",
  "assigned_agent": "coder_001",
  "feature_id": "feat_abc123",
  "requirements": [
    "Token generation with expiration",
    "Token validation middleware", 
    "Refresh token mechanism"
  ],
  "acceptance_criteria": [
    "Tokens expire after 1 hour",
    "Refresh tokens valid for 7 days",
    "Proper error handling for invalid tokens"
  ],
  "progress": 70,
  "started_at": "2025-01-20T10:45:00Z",
  "estimated_completion": "2025-01-20T11:30:00Z",
  "artifacts": [
    {
      "type": "source_code",
      "path": "/src/auth/jwt_service.py",
      "status": "in_progress"
    }
  ]
}
```

---

### Knowledge Base API

#### Search Knowledge Base
```http
GET /knowledge/search?query=authentication&limit=5
```

**Response:**
```json
{
  "results": [
    {
      "id": "kb_001",
      "content": "JWT authentication best practices...",
      "source_type": "documentation",
      "relevance_score": 0.95,
      "tags": ["authentication", "jwt", "security"],
      "created_at": "2025-01-15T09:00:00Z"
    }
  ]
}
```

#### Add Knowledge Entry
```http
POST /knowledge
```

**Request Body:**
```json
{
  "content": "Implementation pattern for OAuth2 with refresh tokens...",
  "source_type": "pattern",
  "tags": ["oauth2", "authentication", "pattern"],
  "metadata": {
    "author": "system",
    "project_id": "proj_xyz789"
  }
}
```

---

## WebSocket Interfaces

### Feature Progress Stream
```
ws://localhost:8080/features/{feature_id}/stream
```

Connect to receive real-time updates about feature progress:

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8080/features/feat_abc123/stream');
```

**Messages Received:**
```json
{
  "type": "progress_update",
  "feature_id": "feat_abc123",
  "progress": 50,
  "stage": "implementation",
  "message": "JWT service implementation 70% complete",
  "timestamp": "2025-01-20T11:15:00Z"
}
```

```json
{
  "type": "task_completed",
  "feature_id": "feat_abc123", 
  "task_id": "task_001",
  "task_title": "Implement password hashing",
  "completed_by": "coder_001",
  "timestamp": "2025-01-20T11:30:00Z",
  "artifacts": ["/src/auth/password_hash.py"]
}
```

```json
{
  "type": "feature_completed",
  "feature_id": "feat_abc123",
  "status": "completed",
  "deployment_url": "https://staging.example.com",
  "completion_time": "2025-01-20T16:30:00Z",
  "summary": {
    "files_created": 8,
    "files_modified": 2,
    "tests_added": 25,
    "test_coverage": "98%"
  }
}
```

### System Events Stream
```
ws://localhost:8080/system/events
```

Receive system-wide events:

```json
{
  "type": "agent_status_change",
  "agent_id": "coder_001",
  "old_status": "idle", 
  "new_status": "busy",
  "timestamp": "2025-01-20T10:45:00Z"
}
```

---

## Data Models

### Feature
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "planning|implementation|review|deployment|completed|failed|cancelled",
  "priority": "low|medium|high|critical",
  "progress": "number (0-100)",
  "requirements": ["string"],
  "acceptance_criteria": ["string"],
  "context": {
    "existing_systems": ["string"],
    "constraints": ["string"], 
    "references": ["string"]
  },
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)",
  "estimated_completion": "string (ISO 8601)",
  "actual_completion": "string (ISO 8601)",
  "metadata": {}
}
```

### Agent
```json
{
  "id": "string",
  "name": "string", 
  "role": "coordinator|planner|coder|tester|reviewer|devops",
  "status": "idle|busy|error|offline",
  "capabilities": ["string"],
  "current_task": "string|null",
  "last_heartbeat": "string (ISO 8601)",
  "performance_metrics": {
    "tasks_completed": "number",
    "avg_completion_time": "string",
    "success_rate": "number (0-1)"
  }
}
```

### Task
```json
{
  "id": "string",
  "title": "string",
  "description": "string", 
  "status": "todo|in_progress|review|completed|failed",
  "priority": "low|medium|high|critical",
  "assigned_agent": "string",
  "feature_id": "string",
  "dependencies": ["string"],
  "requirements": ["string"],
  "acceptance_criteria": ["string"],
  "progress": "number (0-100)",
  "created_at": "string (ISO 8601)",
  "started_at": "string (ISO 8601)",
  "completed_at": "string (ISO 8601)",
  "estimated_completion": "string (ISO 8601)"
}
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": {
    "code": "FEATURE_NOT_FOUND",
    "message": "Feature with ID feat_abc123 not found", 
    "details": {
      "feature_id": "feat_abc123",
      "suggestion": "Check the feature ID and try again"
    },
    "timestamp": "2025-01-20T10:30:00Z",
    "request_id": "req_xyz789"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Invalid or missing authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `FEATURE_NOT_FOUND` | 404 | Feature does not exist |
| `AGENT_NOT_AVAILABLE` | 409 | Requested agent is busy or offline |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `SYSTEM_OVERLOAD` | 503 | System temporarily unavailable |
| `AGENT_ERROR` | 500 | Internal agent processing error |

### Error Examples

#### Validation Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "fields": {
        "priority": "must be one of: low, medium, high, critical",
        "requirements": "must contain at least one requirement"
      }
    }
  }
}
```

#### Rate Limit Error
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED", 
    "message": "Rate limit exceeded",
    "details": {
      "limit": 100,
      "window": "1h",
      "reset_at": "2025-01-20T11:00:00Z"
    }
  }
}
```

---

## Rate Limiting

### Limits by Endpoint

| Endpoint | Rate Limit | Window |
|----------|------------|---------|
| `POST /features` | 10 requests | 1 hour |
| `GET /features` | 100 requests | 1 minute |
| `GET /agents` | 200 requests | 1 minute |
| `WebSocket connections` | 5 connections | Per client |

### Rate Limit Headers

Response headers include current rate limit status:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642680000
X-RateLimit-Window: 60
```

---

## SDK Examples

### Python SDK

```python
import asyncio
from agent_factory_client import AgentFactoryClient

client = AgentFactoryClient(
    base_url="http://localhost:8080",
    api_key="your-api-key"
)

async def create_feature():
    feature = await client.features.create({
        "title": "User Authentication System",
        "description": "Implement secure user login",
        "priority": "high",
        "requirements": [
            "Secure password hashing",
            "JWT token generation"
        ]
    })
    
    print(f"Feature created: {feature.id}")
    
    # Stream progress updates
    async for update in client.features.stream_progress(feature.id):
        print(f"Progress: {update.progress}% - {update.message}")
        
        if update.type == "feature_completed":
            print(f"Deployment URL: {update.deployment_url}")
            break

asyncio.run(create_feature())
```

### JavaScript SDK

```javascript
import { AgentFactoryClient } from '@agent-factory/client';

const client = new AgentFactoryClient({
  baseURL: 'http://localhost:8080',
  apiKey: 'your-api-key'
});

async function createFeature() {
  const feature = await client.features.create({
    title: 'User Authentication System',
    description: 'Implement secure user login',
    priority: 'high',
    requirements: [
      'Secure password hashing',
      'JWT token generation'
    ]
  });

  console.log(`Feature created: ${feature.id}`);

  // Stream progress updates
  const stream = client.features.streamProgress(feature.id);
  
  stream.onMessage((update) => {
    console.log(`Progress: ${update.progress}% - ${update.message}`);
    
    if (update.type === 'feature_completed') {
      console.log(`Deployment URL: ${update.deployment_url}`);
      stream.close();
    }
  });
}

createFeature();
```

### cURL Examples

#### Create Feature
```bash
curl -X POST http://localhost:8080/features \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "User Authentication System",
    "description": "Implement secure user login and registration",
    "priority": "high",
    "requirements": [
      "Secure password hashing",
      "JWT token generation",
      "Input validation"
    ]
  }'
```

#### Get Feature Status
```bash
curl -X GET http://localhost:8080/features/feat_abc123 \
  -H "Authorization: Bearer your-api-key"
```

#### Stream Progress (using websocat)
```bash
websocat ws://localhost:8080/features/feat_abc123/stream \
  --header "Authorization: Bearer your-api-key"
```

---

## Postman Collection

A complete Postman collection is available at: `/docs/postman/Agent Factory API.json`

Import this collection to test all API endpoints with pre-configured examples and environment variables.

---

For additional information, see:
- [User Guide](USER_GUIDE.md) for usage examples
- [Configuration Guide](CONFIGURATION.md) for setup details
- [Architecture Documentation](ARCHITECTURE.md) for system design
- [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues
